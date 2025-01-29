# Repos
## List all repos
`sudo dnf repolist all`

## List all enabled repos
`sudo dnf repolist --enabled`

## Enable a repo
`sudo dnf config-manager --enable <repo name`


## Disable a repo
`sudo dnf config-manager --disable <repo name`





# Packages
## Show dnf history
`sudo dnf history`

## Details about a particular transaction
`sudo dnf history info <transaction_id>` (id from history)

## Show logs for abcd
`grep -i abcd /var/log/dnf.log`



## Check all packages for potential corruption or unintentional changes
`sudo rpm -Va`

## Check all packages and grep one for potential corruption or unintentional changes
`sudo rpm -Va | grep abcd`

## Check if a package is needed by another installed package
`dnf repoquery --whatrequires <package> | xargs dnf list installed`


