## Complete Setup Guide

1. Install Chrony:
   First, make sure Chrony is installed on the new computer:
   ```
   sudo dnf install chrony
   ```

2. Configure `/etc/chrony.conf` using minimal/original `chrony.conf` given here.

3. Ensure that any firewalls on the new computer allow NTP traffic (UDP port 123).
    ```
    sudo firewall-cmd --add-service=ntp --permanent
    sudo firewall-cmd --reload
    ```


3. Start and Enable Chrony:
   After configuring `chrony.conf`, start the Chrony service and enable it to start on boot:
   ```
    sudo systemctl start chronyd
    sudo systemctl enable chronyd
   ```

4. Verify Configuration:
   After starting Chrony, check the synchronization status:
   ```
   chronyc tracking
   chronyc sources -v
   ```

5. Monitor Synchronization:
   For ongoing monitoring, you can use:
   ```
   watch -n 1 chronyc tracking
   watch -n 1 chronyc sources -v
   ```

6. Now run the timedatectl part given here




### Additional Considerations
- Network Stability: A stable and low-latency network connection to the NTP servers is crucial for maintaining synchronization quality.

- Backup Configuration: Once you’ve verified that the new system is synchronized well, consider backing up your `chrony.conf` for future reference.

- NTP Service: Make sure that your NTP service (like Chrony) is installed and running, as timedatectl set-ntp true relies on an NTP service for synchronization.







## Setup timedatectl
```
#!/bin/bash

# Set the time zone to Asia/Kolkata
sudo timedatectl set-timezone Asia/Kolkata

# Enable NTP synchronization
sudo timedatectl set-ntp true

# Sync the hardware clock with the system clock
sudo hwclock --systohc --utc

# Optional: Display the current settings
timedatectl
```



## Original /etc/chrony.conf
```
# Use public servers from the pool.ntp.org project.
# Please consider joining the pool (https://www.pool.ntp.org/join.html).
pool 0.pool.ntp.org minpoll 4 maxpoll 14
pool 1.pool.ntp.org minpoll 4 maxpoll 14
pool 2.pool.ntp.org minpoll 4 maxpoll 14
pool 3.pool.ntp.org minpoll 4 maxpoll 14
# Use NTP servers from DHCP.
sourcedir /run/chrony-dhcp

# Record the rate at which the system clock gains/losses time.
driftfile /var/lib/chrony/drift

# Allow the system clock to be stepped in the first three updates
# if its offset is larger than 1 second.
makestep 1.0 3

# Enable kernel synchronization of the real-time clock (RTC).
rtcsync

# Enable hardware timestamping on all interfaces that support it.
#hwtimestamp *

# Increase the minimum number of selectable sources required to adjust
# the system clock.
#minsources 2

# Allow NTP client access from local network.
allow 192.168.0.0/16

# Serve time even if not synchronized to a time source.
#local stratum 10

# Require authentication (nts or key option) for all NTP sources.
#authselectmode require

# Specify file containing keys for NTP authentication.
#keyfile /etc/chrony.keys

# Save NTS keys and cookies.
ntsdumpdir /var/lib/chrony

# Insert/delete leap seconds by slewing instead of stepping.
#leapsecmode slew

# Get TAI-UTC offset and leap seconds from the system tz database.
leapsectz right/UTC

# Specify directory for log files.
logdir /var/log/chrony

# Select which information is logged.
log measurements statistics tracking
```

## Minimal /etc/chrony.conf
```
# Use public servers from the pool.ntp.org project.
pool 0.pool.ntp.org minpoll 4 maxpoll 14
pool 1.pool.ntp.org minpoll 4 maxpoll 14
pool 2.pool.ntp.org minpoll 4 maxpoll 14
pool 3.pool.ntp.org minpoll 4 maxpoll 14

# Allow NTP client access from local network (adjust as necessary).
allow 192.168.0.0/16

# Record the rate at which the system clock gains/losses time.
driftfile /var/lib/chrony/drift

# Enable kernel synchronization of the real-time clock (RTC).
rtcsync

# Allow the system clock to be stepped in the first three updates if its offset is larger than 1 second.
makestep 1.0 3

# Specify directory for log files.
logdir /var/log/chrony

# Specify NTP servers (optional: add your specific servers here).
server time.cloudflare.com iburst
server www.time.nplindia.org iburst
```
