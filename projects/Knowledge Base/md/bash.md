## 0.1 ##
Add user to a group:
sudo adduser <username> <group_to_join>

Change user owner:
(sudo) chown new_user:new_user_group <directory/files>
chown ansarimn:ansarimn .

Alias:
alias hx="helix"
alias btop="btop --utf-force"


Fixing wrong time:
sudo timedatectl set-local-rtc 1 --adjust-system-clock


View user installed applications
sudo dnf history userinstalled


Create symbolic soft link
ln -s file link_to_file
