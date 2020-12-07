# Copyright (c) Facebook, Inc. and its affiliates. All rights reserved.

# This source code is licensed under the license found in the LICENSE file in the root directory of this source tree.

from __future__ import absolute_import
import logging

import pyudev

logger = logging.getLogger(__name__)


class DigitHandler(object):
    STREAMS = {
        # VGA resolution support 30 (default) and 15 fps
        u"VGA": {
            u"resolution": {u"width": 640, u"height": 480},
            u"fps": {u"30fps": 30, u"15fps": 15},
        },
        # QVGA resolution support 60 (default) and 30 fps
        u"QVGA": {
            u"resolution": {u"width": 320, u"height": 240},
            u"fps": {u"60fps": 60, u"30fps": 30},
        },
    }

    @staticmethod
    def _parse(digit_dev):
        digit_info = {
            u"dev_name": digit_dev[u"DEVNAME"],
            u"manufacturer": digit_dev[u"ID_VENDOR"],
            u"model": digit_dev[u"ID_MODEL"],
            u"revision": digit_dev[u"ID_REVISION"],
            u"serial": digit_dev[u"ID_SERIAL_SHORT"],
        }
        return digit_info

    @staticmethod
    def list_digits():
        context = pyudev.Context()
        logger.debug(u"Finding udev devices with subsystem=video4linux, id_model=DIGIT")
        digits = context.list_devices(subsystem=u"video4linux", ID_MODEL=u"DIGIT")
        logger.debug(u"Following udev devices found: ")
        for device in digits:
            logger.debug(device)
        digits = [dict(DigitHandler._parse(_)) for _ in digits]
        if not digits:
            logger.debug(u"Could not find any udev devices matching parameters")
        return digits

    @staticmethod
    def find_digit(serial):
        digits = DigitHandler.list_digits()
        logger.debug("Searching for DIGIT with serial number {}".format(serial))
        for digit in digits:
            if digit[u"serial"] == serial:
                return digit
        logger.error("No DIGIT with serial number {} found".format(serial))
        return None
