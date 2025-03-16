sudo apt install rsync python3 python3-venv
mkdir -p ./rootdir && cd ./rootdir
python3 -m venv venv && source ./venv/bin/activate
rsync --rsync-path="/usr/bin/rsync" -avz -e "ssh -i ~/.ssh/sq1" ~/Downloads/rootdir/ sshuser@34.126.191.220:/home/sshuser/rootdir/
gcloud run deploy
#download images from drive to image;




#download templates to templates;

