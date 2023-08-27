mkdir /.__EL_SNEEDIO__
if [ ! -f /.__EL_SNEEDIO__/rev ]; then
    touch /.__EL_SNEEDIO__/rev
fi
if [ ! -f /.__EL_SNEEDIO__/stat ]; then
    touch /.__EL_SNEEDIO__/stat
fi
if [ ! -f /.__EL_SNEEDIO__/hideon ]; then
    touch /.__EL_SNEEDIO__/hideon
fi
if [ ! -f /.__EL_SNEEDIO__/hideoff ]; then
    touch /.__EL_SNEEDIO__/hideoff
fi
ln -s /bin/sh /.__EL_SNEEDIO__/.__EL_SNEEDIO__
mkdir /.__EL_SNEEDIO__/modules.d
for f in /.__EL_SNEEDIO__/modules.d/*; do
    sh $f
done
# put some kind of watchdog on the modules? like run em all on a timer
# IDK LOL !
echo END
