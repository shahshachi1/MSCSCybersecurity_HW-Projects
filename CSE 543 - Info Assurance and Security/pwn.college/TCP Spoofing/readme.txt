TCP Spoofing Challenge Write-Up

Objective:
The goal was to extract a flag from a service called FlagIt, which authenticates users based solely on their source IP address. If the source IP is the trusted IP 10.2.4.10, the service accepts a destination IP from the user and sends the flag via UDP to port 13337 at that address.
Since the attacker’s machine is 10.0.0.2, we must spoof a TCP connection as if we are 10.2.4.10 (the trusted client), and trick the server into sending the flag to 10.0.0.2.

Overview of the Attack Strategy:
	- Probe the server’s TCP Initial Sequence Number (ISN) by sending a legit SYN from our real IP.
	- Announce our real IP to the server to ensure it knows where to send the UDP flag.
	- Craft a spoofed TCP handshake using 10.2.4.10 as the source IP.
	- Blindly guess the server’s ISN (within a small ±30 window).
	- Send our real IP as the payload using various encodings (raw, newline, null-terminated).
	- Sniff for the UDP flag in the same script.
	- Repeat until the flag is received.

Script Breakdown:
	- Global Variables: Defines the attacker IP, the trusted (spoofed) IP, the target server, ports, and interface.
		iface = "eth0"
		real_ip = "10.0.0.2"
		spoofed_ip = "10.2.4.10"
		target_ip = "10.0.0.3"
		sport = 54321
		dport = 13337
		client_seq = 12345
	- get_mac(ip): Performs an ARP request to dynamically retrieve the MAC address of 10.0.0.3. This is critical since the server’s MAC changes frequently in the CTF environment.
	- announce_self(): Sends a fake ARP broadcast claiming “I am 10.0.0.2,” so the server knows where to send the UDP response. This helps prevent the server from dropping the UDP packet due to a missing or outdated ARP entry.
	- sniff_flag(): Launches a background thread to sniff UDP port 13337 and print the flag when it arrives/ 
	This is essential to avoid requiring an external listener.
	- run_attack(): 
		Performs one complete spoofing attempt:
			1. Sends a real SYN to get the server’s current ISN
			2. Sends a spoofed SYN using the trusted IP
			3. Loops over ±30 sequence numbers
			4. For each guess:
			5. Sends a forged ACK
			6. Sends multiple PSH+ACK packets with payloads:
		These cover different string-termination possibilities expected by the server. If any guess is successful, the TCP handshake completes and the payload is accepted.
	- Auto-Retry Loop: This ensures reliability even in cases of MAC flapping, packet loss, or server-side randomness.
	- Success Output: Once a guessed handshake works and the server accepts the spoofed payload, the flag is sent back via UDP.

Output Generation:
	- Run /challenge/run
	- Since I do not have root permission within the /challenge directory, I had to run the challenge from the outside directory (where I had copied the /challenge scripts) and run 'python3 run.py' (my script).
	- I wait for the script to complete and I recieve the flag!