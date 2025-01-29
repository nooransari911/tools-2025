# Install squid
sudo yum update -y
sudo yum install squid

# edit `squid.conf`
sudo nano /etc/squid/squid.conf

Add these lines (basic):
acl all src all
http_access allow all

Or (more secure):
acl allowed_networks src <your-ip-address>/32
http_access allow allowed_networks


# Open port 3128
## Install iptables
sudo yum install iptables-services -y
sudo service iptables save

## Open port 3128
sudo iptables -I INPUT -p tcp --dport 3128 -j ACCEPT

## Show iptables status
sudo iptables -L

## Alternate for firewall-cmd
sudo firewall-cmd --add-port=3128/tcp --permanent
sudo firewall-cmd --reload



# Start squid
sudo systemctl start squid
sudo systemctl enable squid
sudo systemctl status squid

# Config proxy on local
Add ip add of remote and port 3128 as proxy on local machine

