## vnstat
`sudo chown vnstat:vnstat /var/lib/vnstat`
`sudo chown vnstat:vnstat /var/lib/vnstat/*`


## Multimedia (vlc, mpv,....)

sudo dnf install https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm

sudo dnf config-manager --enable fedora-cisco-openh264

sudo dnf update @core

sudo dnf swap ffmpeg-free ffmpeg --allowerasing

sudo dnf update @multimedia --setopt="install_weak_deps=False" --exclude=PackageKit-gstreamer-plugin


sudo dnf update @sound-and-video


sudo dnf install intel-media-driver
