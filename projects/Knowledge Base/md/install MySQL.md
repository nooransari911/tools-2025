- Install MySQL configs from repo https://dev.mysql.com/downloads/repo/yum/

- Install mysql server by `sudo yum install mysql-community-server`

- `systemctl start mysqld`

- `systemctl status mysqld`

- `sudo grep 'temporary password' /var/log/mysqld.log`

- `mysql -uroot -p`

- Enable these repos with `config-manager --enable`:
    - sudo dnf config-manager --enable mysql80-community
    - sudo dnf config-manager --enable mysql-tools-8.4-lts-community
    - sudo dnf config-manager --enable mysql-tools-community
    -

- Install mysql workbench `sudo dnf install mysql-workbench-community`
