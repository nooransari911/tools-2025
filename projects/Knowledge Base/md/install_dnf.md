# 1 list all user installed packages in dnf
dnf repoquery --userinstalled

# 2 save  all user installed packages in dnf to text file
dnf repoquery --userinstalled > dnf_packages.txt


# 3 install all packages from text file
sudo xargs dnf install -y < user_installed_packages.txt



# 4 List all enabled repos
dnf repolist --enabled > dnf_repos.txt
