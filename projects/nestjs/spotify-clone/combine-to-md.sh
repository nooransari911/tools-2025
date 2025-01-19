mkdir -p ./md
find ./src/ -type f -name "*.ts" -exec bash -c 'cp "$0" "./md/$(basename "$0" .ts).md"' {} \;
cat ./md/*.md > /home/ansarimn/Downloads/tools-2025/projects/Knowledge\ Base/md/combined_file.md
cp /home/ansarimn/Downloads/tools-2025/projects/Knowledge\ Base/md/combined_file.md /home/ansarimn/Downloads/combined_file.md
rm -rf ./md
