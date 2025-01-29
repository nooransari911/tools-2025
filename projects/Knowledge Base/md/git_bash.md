## SSH Key generation template
Non-root ::
ssh-keygen -t ed25519 -C "email@address.com"
#This generates two keys: public (non-.pub) and private (*.pub);
mkdir ~/.ssh
mv public_key ~/.ssh
mv private_key.pub ~/.ssh
exec ssh-agent bash
ssh-add ~/.ssh/public_key

Root ::
su
cp -r /home/ansarimn/.ssh/ /.ssh/
exec ssh-agent bash
ssh-add /.ssh/public_key



## Git Configs
git config --global --add safe.directory dir/DSA3
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
git config pull.rebase false




## Git Push Template
exec ssh-agent bash
ssh-add ~/.ssh/...
ssh -T git@github.com
git add .
git remote set-url origin git@github.com:nooransari911/DSA3.git
echo "Enter commit message:"
read commit_message
echo ""
echo "Starting commit;"
git commit -m "$commit_message"
echo ""
echo "Starting push;"
git push -u origin main


## Git Pull Template
git pull origin main


## Recover lost files
git log
git reset --hard <hash of most recent commit>

Alternatively, git restore --s=HEAD --staged --worktree -- .
