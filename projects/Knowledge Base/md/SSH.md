# 1 `SSH`

Generic `ssh` command

```
ssh -i ~/.ssh/your_private_key  ssh_username@ssh_hostname
```

Hostname can be IP address or DNS-resolvable name.<br><br>

Username is username for the user using SSH.<br><br>

`-p` option can be used to explicitly specify a port.<br><br><br><br>



# 2 `SSH` Aliasing

Aliases can be used for the full `username@hostname.....` `ssh` command<br><br>

Aliases are in `~/.ssh/config` or `/root/.ssh/config` file<br><br><br><br>

## 2.1 Alias Example

Consider entire `ssh` command:

```
ssh -i ~/.ssh/your_private_key  ssh_username@ssh_hostname
```
<br>

Alias for this would be:

```
Host ALIAS
  HostName ssh_hostname
  User ssh_username
  Port 22
  IdentityFile ~/.ssh/your_private_key
```


This would be the respective `config` file.<br><br>

`ssh` command for alias would be

```
ssh ALIAS
```
<br><br><br><br>



# 3 Home dir for user

Directory `/dir1/dir2/` on remote/server can be used as the root directory for the SSH user. Do

```
ssh -i ~/.ssh/your_private_key  ssh_username@ssh_hostname:/dir1/dir2/
```
<br><br>