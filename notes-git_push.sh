# exec ssh-agent bash
# ssh-add ~/.ssh/github_key_1
cd /home/ansarimn/Downloads/notes/
echo "$(date '+%Y-%m-%d %H:%M:%S') Pushing notes dir"
ssh -T git@github.com

rsync -avz /home/ansarimn/.config/helix/ /home/ansarimn/Downloads/notes/system/helix/ > /dev/null
rsync -avz /home/ansarimn/.config/bat/ /home/ansarimn/Downloads/notes/system/bat/ > /dev/null
rsync -avz /home/ansarimn/.bashrc /home/ansarimn/Downloads/notes/system/.bashrc > /dev/null

# git add .gitignore
git add .
# git remote add origin https://github.com/nooransari911/DSA4.git
git remote set-url origin git@github.com:nooransari911/notes.git
echo "Enter commit message:"
read commit_message
echo ""
echo "Starting commit;"
git commit -m "$commit_message"
echo ""
echo "Starting push;"
git push -u origin main
