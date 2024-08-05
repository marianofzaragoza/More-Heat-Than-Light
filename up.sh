#!/usr/bin/env bash
#
#

sudo apt install -y vim git cmake libgirepository1.0-dev   gir1.2-gst-plugins-bad-1.0 gir1.2-gst-plugins-base-1.0 gir1.2-gst-rtsp-server-1.0 gir1.2-gstreamer-1.0 libgstrtspserver-1.0-0


apt install -y  dh-exec dh-python fonts-font-awesome fonts-lato libblkid-dev libbrotli-dev libcairo-script-interpreter2 libcairo2-dev libffi-dev libfontconfig-dev libfreetype-dev libglib2.0-dev libglib2.0-dev-bin libjson-perl libmount-dev libpcre2-32-0 libpcre2-dev libpcre2-posix3 libpixman-1-dev libpython3-all-dev libselinux1-dev libsepol-dev libxcb-render0-dev libxcb-shm0-dev libxrender-dev python3-alabaster python3-all python3-all-dev python3-attr python3-imagesize python3-iniconfig python3-packaging python3-pluggy python3-py python3-pytest python3-snowballstemmer python3-sphinx python3-sphinx-rtd-theme sphinx-common sphinx-rtd-theme-common uuid-dev  at-spi2-core gnome-pkg-tools gobject-introspection libgirepository1.0-dev libpython3-all-dbg libpython3-dbg libpython3.11-dbg python3-all-dbg python3-cairo-dev python3-dbg python3-flake8 python3-mako python3-markdown python3-pycodestyle python3-pyflakes python3.11-dbg xvfb   gir1.2-gstreamer-1.0 libqt5glib-2.0-0 libqt5gstreamer-1.0-0   gir1.2-gst-plugins-bad-1.0 gir1.2-gst-plugins-base-1.0 gir1.2-gst-rtsp-server-1.0 libgstrtspserver-1.0-0

sudo apt install -y gstreamer1.0-tools gstreamer1.0-plugins-base-apps gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-alsa   gstreamer1.0-gl gstreamer1.0-gl-dbgsym gstreamer1.0-gtk3 gstreamer1.0-gtk3-dbgsym libgraphene-1.0-0

sudo usermod -aG lp user



sudo apt -y install autoconf automake autopoint autotools-dev debhelper dh-autoreconf dh-exec dh-python dh-strip-nondeterminism dwz fonts-font-awesome fonts-lato gettext intltool-debian libarchive-zip-perl libblkid-dev libbrotli-dev libcairo-script-interpreter2 libcairo2-dev libdebhelper-perl libffi-dev libfile-stripnondeterminism-perl libfontconfig-dev libfreetype-dev libglib2.0-dev libglib2.0-dev-bin libjson-perl libmount-dev libpcre2-32-0 libpcre2-dev libpcre2-posix3 libpixman-1-dev libpng-dev libpython3-all-dev libselinux1-dev libsepol-dev libsub-override-perl libtool libxcb-render0-dev libxcb-shm0-dev libxrender-dev m4 po-debconf python3-alabaster python3-all python3-all-dev python3-attr python3-imagesize python3-iniconfig python3-packaging python3-pluggy python3-py python3-pytest python3-snowballstemmer  python3-sphinx python3-sphinx-rtd-theme sphinx-common sphinx-rtd-theme-common uuid-dev

python3 -m venv venv
#venv/bin/python3 -m pip install StarTspImage
./venv/bin/pip install . 

