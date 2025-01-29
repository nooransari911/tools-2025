# initialize
sudo restic -r /run/media/.... init


# backup
sudo restic -r /run/media/.... backup /path
you can use multiple paths simultaneously;
use --exclude flag to ignore folders, --include flag to include folders;
--files-from="path of file" uses all paths in the .txt file;
--exclude-file="path of file" excludes all paths in the .txt file;
# view all snaphots
sudo restic -r /run/media/.... snapshots


# restore
all files:
sudo restic -r /run/media/.... restore snaphot_id --target /path

one file:
sudo restic -r /run/media/.... restore snaphot_id --target /path --include /path_of_file


# mount
sudo restic -r /run/media/.... mount /path
