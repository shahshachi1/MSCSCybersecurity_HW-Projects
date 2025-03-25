from scapy.all import Ether, IP, UDP, sendp, get_if_hwaddr

# Setup
iface = "eth0"
src_mac = get_if_hwaddr(iface)
dst_mac = "ee:ee:ee:ee:ee:ee"

# Build forged UDP packet
frame = Ether(src=src_mac, dst=dst_mac) / \
        IP(src="10.2.4.10", dst="10.0.0.3") / \
        UDP(sport=12345, dport=13337) / \
        b"SpoofedUDP"

# Send it!
sendp(frame, iface=iface, verbose=True)
