import time
import pywifi
from pywifi import const

# Initialize wifi interface
wifi = pywifi.PyWiFi()
iface = wifi.interfaces()[0]

# Define the function to connect to a WiFi network
def connect_to_wifi(ssid, password):
    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password
    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)
    iface.connect(tmp_profile)
    time.sleep(3)  # Wait for connection to establish
    return iface.status() == const.IFACE_CONNECTED

# List nearby WiFi networks
scan_results = iface.scan_results()
print("Scanning nearby WiFi networks...")
password = input("Enter the password for the network: ")

for wifi_network in scan_results:
    ssid = wifi_network.ssid
    print(f"Trying to connect to {ssid}...")
    if connect_to_wifi(ssid, password):
        print(f"Connected to {ssid} successfully!")
        break
    else:
        print(f"Failed to connect to {ssid}")
