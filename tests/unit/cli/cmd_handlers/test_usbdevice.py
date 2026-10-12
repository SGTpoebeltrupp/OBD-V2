import pytest
import argparse
from unittest.mock import call

from obd_v2.cli.cli_args_parser import build_parser
from obd_v2.cli.cmd_handlers.usbdevice import cmd_usbdevice

import obd_v2.options as options
_ = options.translator('obd_v2')


def test_cmd_usbdevice_calls_obd_device_methods_in_order(mocker, capsys):
    mock_obd_device_class = mocker.patch(
        "obd_v2.cli.cmd_handlers.usbdevice.OBDDevice"
    )
    mock_obd_device = mock_obd_device_class.return_value
    mock_obd_device.start_session_can.return_value = "OK"

    cmd_usbdevice(argparse.Namespace())
    captured = capsys.readouterr()

    assert mock_obd_device.mock_calls == [
        call.init_can(),
        call.set_can_addr(26, {}),
        call.start_session_can("10C0"),
    ]
    assert captured.out.strip() == "OK"