# Copyright (c) Facebook, Inc. and its affiliates. All rights reserved.

# This source code is licensed under the license found in the LICENSE file in the root directory of this source tree.

from __future__ import absolute_import
import logging

import cv2
import numpy as np

from digit_interface.digit_handler import DigitHandler

logger = logging.getLogger(__name__)


class Digit(object):
    def __init__(self, serial = None, name = None):
        u"""
        DIGIT Device class for a single DIGIT
        :param serial: DIGIT device serial
        :param name: Human friendly identifier name for the device
        """
        self.serial = serial
        self.name = name

        self.__dev = None

        self.dev_name = u""
        self.manufacturer = u""
        self.model = u""
        self.revision = u""

        self.resolution = {}
        self.fps = 0
        self.intensity = 0

        if self.serial is not None:
            logger.debug("Digit object constructed with serial {}".format(self.serial))
            self.populate(serial)

    def connect(self):
        logger.info("{}:Connecting to DIGIT".format(self.serial))
        self.__dev = cv2.VideoCapture(self.dev_name)
        if not self.__dev.isOpened():
            logger.error(
                "Cannot open video capture device {} - {}".format(self.serial, self.dev_name)
            )
            raise Exception("Error opening video stream: {}".format(self.dev_name))
        # set stream defaults, QVGA at 60 fps
        logger.info(
            "{}:Setting stream defaults to QVGA, 60fps, maximum LED intensity.".format(self.serial)
        )
        logger.debug(
            "Default stream to QVGA {}".format(DigitHandler.STREAMS['QVGA']['resolution'])
        )
        self.set_resolution(DigitHandler.STREAMS[u"QVGA"])
        logger.debug(
            "Default stream with {} fps".format(DigitHandler.STREAMS['QVGA']['fps']['60fps'])
        )
        self.set_fps(DigitHandler.STREAMS[u"QVGA"][u"fps"][u"60fps"])
        logger.debug(u"Setting maximum LED illumination intensity")
        self.set_intensity(255)

    def set_resolution(self, resolution):
        u"""
        Sets stream resolution based on supported streams in DigitHandler.STREAMS
        :param resolution: QVGA or VGA from DigitHandler.STREAMS
        :return: None
        """
        self.resolution = resolution[u"resolution"]
        width = self.resolution[u"width"]
        height = self.resolution[u"height"]
        logger.debug("{}:Stream resolution set to {}w x {}h".format(self.serial, height, width))
        self.__dev.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.__dev.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def set_fps(self, fps):
        u"""
        Sets the stream fps, only valid values from DigitHandler.STREAMS are accepted.
        This should typically be called after the resolution is set as the stream fps defaults to the
        highest fps
        :param fps: Stream FPS
        :return: None
        """
        self.fps = fps
        logger.debug("{}:Stream FPS set to {}".format(self.serial, self.fps))
        self.__dev.set(cv2.CAP_PROP_FPS, self.fps)

    def set_intensity(self, intensity):
        intensity = 1 if intensity < 1 else 255 if intensity > 255 else intensity
        self.intensity = intensity
        logger.debug("{}:LED intensity set to {}".format(self.serial, self.intensity))
        self.__dev.set(cv2.CAP_PROP_ZOOM, self.intensity)
        return self.intensity

    def get_frame(self, transpose = False):
        u"""
        Returns a single image frame for the device
        :param transpose: Show direct output from the image sensor, WxH instead of HxW
        :return: Image frame array
        """
        ret, frame = self.__dev.read()
        if not ret:
            logger.error(
                "Cannot retrieve frame data from {}, is DIGIT device open?".format(self.serial)
            )
            raise Exception(
                "Unable to grab frame from {} - {}!".format(self.serial, self.dev_name)
            )
        if not transpose:
            frame = cv2.transpose(frame, frame)
            frame = cv2.flip(frame, 0)
        return frame

    def save_frame(self, path):
        u"""
        Saves a single image frame to host
        :param path: Path and file name where the frame shall be saved to
        :return: None
        """
        frame = self.get_frame()
        logger.debug("Saving frame to {}".format(path))
        cv2.imwrite(path, frame)
        return frame

    def get_diff(self, ref_frame):
        u"""
        Returns the difference between two frames
        :param ref_frame: Original frame
        :return: Frame difference
        """
        diff = self.get_frame() - ref_frame
        return diff

    def show_view(self, ref_frame = None):
        u"""
        Creates OpenCV named window with live view of DIGIT device, ESC to close window
        :param ref_frame: Specify reference frame to show image difference
        :return: None
        """
        while True:
            frame = self.get_frame()
            if ref_frame is not None:
                frame = self.get_diff(ref_frame)
            cv2.imshow("Digit View {}".format(self.serial), frame)
            if cv2.waitKey(1) == 27:
                break
        cv2.destroyAllWindows()

    def disconnect(self):
        logger.debug("{}:Closing DIGIT device".format(self.serial))
        self.__dev.release()

    def info(self):
        u"""
        Returns DIGIT device info
        :return: String representation of DIGIT device
        """
        has_dev = self.__dev is not None
        is_connected = False
        if has_dev:
            is_connected = self.__dev.isOpened()
        info_string = (
            "Name: {} {}"
            "\n\t- Model: {}"
            "\n\t- Revision: {}"
            "\n\t- CV Device?: {}"
            "\n\t- Connected?: {}"
            "\nStream Info:"
            "\n\t- Resolution: {} x {}"
            "\n\t- FPS: {}"
            "\n\t- LED Intensity: {}".format(self.name, self.dev_name, self.model, self.revision, has_dev, is_connected, self.resolution['width'], self.resolution['height'], self.fps, self.intensity)
        )
        return info_string

    def populate(self, serial):
        u"""
        Find the connected DIGIT based on the serial number and populate device parameters into the class
        :param serial: DIGIT serial number
        :return:
        """
        digit = DigitHandler.find_digit(serial)
        if digit is None:
            raise Exception("Cannot find DIGIT with serial {}".format(self.serial))
        self.dev_name = digit[u"dev_name"]
        self.manufacturer = digit[u"manufacturer"]
        self.model = digit[u"model"]
        self.revision = digit[u"revision"]
        self.serial = digit[u"serial"]
