# 1 SFTP

It is FTP over SSH.

It works exactly like SSH: it uses private key, public key, username, hostname
<br><br><br><br>




# 2 Setting up a SFTP server
## 2.1 `sftp` shell
Generic `sftp` command

```
sftp -i ~/.ssh/your_private_key  ssh_username@ssh_hostname
```
<br>

## 2.2 Filezilla
Filezilla:

- Host field: `sftp://ssh_hostname`
- Username field:  `username`
- Port field: `22`
- Private key: set it from settings
<br>

## 2.3 Dolphin/any file manager

Dolphin/any file manager:

- Host field: Alias for `ssh` (see [[SSH#2.1 Alias Example]])
- Username field:  `username`
- Protocol field: SFTP
- Port field: `22`
<br><br>

## 2.4 Mount on local with `sshfs`


```
sshfs -o IdentityFile=~/.ssh/your_private_key /your-local-mount-point/ ssh_username@ssh_hostname:/root_dir_for_SSH_user/
```

`sshfs` mounts the SFTP server on a local mount point. Now the mountpoint effectively acts as local storage.

To unmount, try
```
sudo fusermount -u /your-local-mount-point/
```

If it fails, try again a few times

<br><br>