# Installing scilab
cd ~/Downloads/DA/sci
wget https://www.scilab.org/download/2024.0.0/scilab-2024.0.0.bin.x86_64-linux-gnu.tar.xz
tar -xvf ./scilab-2024.0.0.bin.x86_64-linux-gnu.tar.xz


# Installing scilab kernel
sudo pip install scilab_kernel
python -m sclab_kernel install
jupyter kernelspec list

if "kernel.py::AttributeError: find_loader not found", remove those lines
