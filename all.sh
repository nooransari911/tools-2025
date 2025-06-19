# exec ssh-agent bash
ssh-add ~/.ssh/github_key_1

# Prompt for commit messages at the start
echo "Enter commit message for the 'notes' repository:"
read commit_message_notes

echo "Enter commit message for the 'tools-2025' repository:"
read commit_message_tools



cd /home/ansarimn/Downloads/notes/
echo "$(date '+%Y-%m-%d %H:%M:%S') Pushing notes dir"
ssh -T git@github.com

rsync -avz /home/ansarimn/.config/helix/ /home/ansarimn/Downloads/notes/system/helix/ > /dev/null
rsync -avz /home/ansarimn/.config/nvim/ /home/ansarimn/Downloads/notes/system/nvim/ > /dev/null
rsync -avz /home/ansarimn/.config/lvim /home/ansarimn/Downloads/notes/system/lvim/ > /dev/null

rsync -avz /home/ansarimn/.config/bat/ /home/ansarimn/Downloads/notes/system/bat/ > /dev/null

rsync -avz /home/ansarimn/Downloads/essays/themes/papermod/layouts/ /home/ansarimn/Downloads/tools-2025/projects/SSG/ > /dev/null
rsync -avz /home/ansarimn/Downloads/essays/themes/papermod/assets/css/ /home/ansarimn/Downloads/tools-2025/projects/SSG/ > /dev/null



# git add .gitignore
git add .
# git remote add origin https://github.com/nooransari911/tools-2025.git
git remote set-url origin git@github.com:nooransari911/notes.git
echo "Starting commit;"
git commit -m "$commit_message_notes"
echo ""
echo "Starting push;"
git push -u origin main

echo ""
echo ""
echo ""
echo ""

# exec ssh-agent bash
# ssh-add ~/.ssh/github_key_1

cd /home/ansarimn/Downloads/tools-2025/
echo "$(date '+%Y-%m-%d %H:%M:%S') Pushing main dir"
ssh -T git@github.com
git add .gitignore
git add .
git remote set-url origin git@github.com:nooransari911/tools-2025.git
# git remote add origin git@github.com:nooransari911/tools-2025.git
echo "Starting commit;"
git commit -m "$commit_message_tools"
echo ""
echo "Starting push;"
git push -u origin main
