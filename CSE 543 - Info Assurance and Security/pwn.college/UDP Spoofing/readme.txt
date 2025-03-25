UDP Spoofing Challenge Write-Up

Objective:
Send a forged UDP packet to a remote host that authenticates based solely on source IP.
Constraints:
	- The remote host is at 10.0.0.3 and listens on UDP port 13337.
	- The only trusted IP is 10.2.4.10.
	- You must send the spoofed packet from eth0 (your interface at 10.0.0.2).
	- You cannot change your real IP, so you must spoof the packet manually at Layer 2.

Overview of the Attack Strategy:
	- Since the remote service trusts packets based only on their source IP, the solution is simple:
	- Forge a Layer 2 (Ethernet) frame manually.
	- Set the source IP to 10.2.4.10.
	- Set the destination IP to 10.0.0.3 and UDP destination port to 13337.
	- Send the spoofed frame with Scapy’s sendp() (raw Layer 2 send).

Script Breakdown:
	- Imported Scapy modules for crafting Ethernet/IP/UDP packets and sending at Layer 2.
	- Set Interface and MAC Addresses:
			iface = "eth0"
			src_mac = get_if_hwaddr(iface)
			dst_mac = "ee:ee:ee:ee:ee:ee"
		- Grabs the interface MAC address.
		- Uses a known or assumed broadcast/listener MAC. In CTF environments like this, ee:ee:ee:ee:ee:ee is often used by default.
	- Build the Packet:
		- Constructs a complete Ethernet frame with a forged IP header.
		- The IP source is the trusted address, 10.2.4.10.
		- The UDP data can be any payload (not used for auth).
		- Since we're forging at Layer 2, the OS never sees or drops the packet, even with the fake source IP.
	- Send the Frame:
		sendp(frame, iface=iface, verbose=True)
		- Sends the frame directly on the wire.
		- Bypasses the kernel stack entirely.
	- Then recieve the flag!


Output Generation:
	- Run /challenge/run
	- Since I do not have root permission within the /challenge directory, I had to run the challenge from the outside directory (where I had copied the /challenge scripts) and run 'python3 run.py' (my script).
	- I wait for the script to complete and I recieve the flag!