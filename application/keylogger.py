import usb.core
import sys

USB_IF = 0  # Interface
USB_TIMEOUT = 5  # Timeout in MS

Vendor_ID = 0x9da
Product_ID = 0x9090
# print(usb.core.show_devices())  # Show all devices()
# help(usb.core)  # For getting documentation
# idVendor=0x1a2c, idProduct=0x2124  # My keyboard id's
# idVendor=0x9da, idProduct=0x9090    # Unknown USB DEVICE
dev = usb.core.find(find_all=True)
for cfg in dev:  # Get vendor ID from devices
    sys.stdout.write('Hexadecimal VendorID=' + hex(cfg.idVendor) + ' & ProductID=' + hex(cfg.idProduct) + '\n')

dev = usb.core.find(idVendor=Vendor_ID, idProduct=Product_ID)
print(f'Devices: {dev}')
endpoint = dev[0][(0, 0)][0]
cfg = dev.get_active_configuration()
interface_number = cfg[(0, 0)].bInterfaceNumber
intf = usb.util.find_descriptor(cfg, bInterfaceNumber=interface_number)

if dev is None:
    raise ValueError('device not found')
    # sys.exit(1)
else:
    print("Device Found")
    usb.util.claim_interface(dev, 0)
    dev = usb.core.find(idVendor=Vendor_ID, idProduct=Product_ID)

try:
    dev.set_configuration()
    print("Configuration set")
except:
    print("configuration not set")


reading_address = 0x81
data = dev.read(reading_address, 4)
print(f'data: {data}')

