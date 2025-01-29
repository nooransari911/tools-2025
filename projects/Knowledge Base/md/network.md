## Cloudflare WARP
systemctl enable --now warp-svc
warp-cli register
warp-cli connect
warp-cli status
warp-cli warp-dns-stats


## DNS and WARP
Add
`nameserver 1.1.1.1` to /etc/resolv.conf;
`DNS=1.1.1.1`, `ResolveUnicastSingleLabel=yes` to /etc/systemd/resolved.conf;


## DNS over TLS
Edit `/etc/systemd/resolved.conf` file.

Make
- `DNSOverTLS=opportunistic` for fallback to plaintext
- `DNSOverTLS=yes` for strict DNS over TLS

Then
```
sudo ln -sf /run/systemd/resolve/stub-resolv.conf /etc/resolv.conf
sudo systemctl restart systemd-resolved
```

In wireshark, DNS will no longer appear DNS. It will appear as encrypted traffic over TCP port 853. The DNS query and response content will be encrypted, so you won't be able to read the domain names or IP addresses being resolved in plaintext.

Upon fallback to plaintext, DNS query-response will appear in plaintext over TCP/TCP as usual.

Wireshark filters:
- DNSOverTLS: `tcp.port == 853`
- Plaintext: `udp.port == 53 || tcp.port == 53`








## vnstat
`sudo chown vnstat:vnstat /var/lib/vnstat`
`sudo chown vnstat:vnstat /var/lib/vnstat/*`

## Wireshark filter
`not icmpv6 and not nbns and not igmp and not ssdp and not mdns and not llmnr`


## Spoofing MAC address
### Promiscuous Mode
Promiscuous mode is a network interface configuration in which the network adapter captures all traffic on the network, regardless of whether it is addressed to the adapter's MAC address or not. Normally, network interfaces only capture and process packets addressed specifically to them (or broadcast/multicast packets).

### Why promisc mode enables spoofing MAC address
In promiscuous mode, it captures all packets, including those meant for the spoofed address, allowing the connection to work.

Without promiscuous mode, the network card might be set to only accept packets intended for the original hardware MAC address, causing your internet connection to fail.

### Show interface details
`ip link show <interface>`

### Enable Promiscuous Mode
`sudo ip link set enp0s13f0u1c2 promisc on`

### Spoof mac address cli
```
sudo ip link set <interface> down
sudo ip link set <interface> address <new_mac_address>
sudo ip link set <interface> up
```
