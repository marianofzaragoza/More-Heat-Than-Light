#!/usr/bin/env bash
#
#
set -eux
sudo usermod -aG lp user
sudo apt install -y vim git cmake libgirepository1.0-dev   gir1.2-gst-plugins-bad-1.0 gir1.2-gst-plugins-base-1.0 gir1.2-gst-rtsp-server-1.0 gir1.2-gstreamer-1.0 libgstrtspserver-1.0-0
sudo apt install -y libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gtk-doc-tools

sudo apt install -y screen tshark tcpdump protobuf-compiler python3-gst-1.0 python3-venv ffmpeg alsa-utils

cp screenrc ~/.screenrc

sudo apt install -y  dh-exec dh-python fonts-font-awesome fonts-lato libblkid-dev libbrotli-dev libcairo-script-interpreter2 libcairo2-dev libffi-dev libfontconfig-dev libfreetype-dev libglib2.0-dev libglib2.0-dev-bin libjson-perl libmount-dev libpcre2-32-0 libpcre2-dev libpcre2-posix3 libpixman-1-dev libpython3-all-dev libselinux1-dev libsepol-dev libxcb-render0-dev libxcb-shm0-dev libxrender-dev python3-alabaster python3-all python3-all-dev python3-attr python3-imagesize python3-iniconfig python3-packaging python3-pluggy python3-py python3-pytest python3-snowballstemmer python3-sphinx python3-sphinx-rtd-theme sphinx-common sphinx-rtd-theme-common uuid-dev  at-spi2-core gnome-pkg-tools gobject-introspection libgirepository1.0-dev libpython3-all-dbg libpython3-dbg libpython3.11-dbg python3-all-dbg python3-cairo-dev python3-dbg python3-flake8 python3-mako python3-markdown python3-pycodestyle python3-pyflakes python3.11-dbg xvfb   gir1.2-gstreamer-1.0 libqt5glib-2.0-0 libqt5gstreamer-1.0-0   gir1.2-gst-plugins-bad-1.0 gir1.2-gst-plugins-base-1.0 gir1.2-gst-rtsp-server-1.0 libgstrtspserver-1.0-0 gstreamer1.0-omx-generic gstreamer1.0-omx-generic-config gstreamer1.0-omx-bellagio-config



sudo apt install -y gstreamer1.0-tools gstreamer1.0-plugins-base-apps gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-alsa   gstreamer1.0-gl gstreamer1.0-gtk3 libgraphene-1.0-0
sudo apt install vlc -y

sudo usermod -aG lp user

sudo apt install - libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio

sudo apt install -y autoconf automake autopoint autotools-dev debhelper dh-autoreconf dh-exec dh-python dh-strip-nondeterminism dwz fonts-font-awesome fonts-lato gettext intltool-debian libarchive-zip-perl libblkid-dev libbrotli-dev libcairo-script-interpreter2 libcairo2-dev libdebhelper-perl libffi-dev libfile-stripnondeterminism-perl libfontconfig-dev libfreetype-dev libglib2.0-dev libglib2.0-dev-bin libjson-perl libmount-dev libpcre2-32-0 libpcre2-dev libpcre2-posix3 libpixman-1-dev libpng-dev libpython3-all-dev libselinux1-dev libsepol-dev libsub-override-perl libtool libxcb-render0-dev libxcb-shm0-dev libxrender-dev m4 po-debconf python3-alabaster python3-all python3-all-dev python3-attr python3-imagesize python3-iniconfig python3-packaging python3-pluggy python3-py python3-pytest python3-snowballstemmer  python3-sphinx python3-sphinx-rtd-theme sphinx-common sphinx-rtd-theme-common uuid-dev

python3 -m venv venv
#venv/bin/python3 -m pip install StarTspImage
./venv/bin/python3 -m pip install . 
./venv/bin/python3 -m ipykernel install --user --name=moreheat

