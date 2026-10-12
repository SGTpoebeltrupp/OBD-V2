import argparse

from obd_v2.core.usbdevice.obd_device import OBDDevice

def cmd_usbdevice(args: argparse.Namespace) -> int:
    dev = OBDDevice()
    dev.init_can()
    dev.set_can_addr(26, {})
    print(dev.start_session_can("10C0"))