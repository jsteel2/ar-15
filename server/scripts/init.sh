mkdir /.__EL_SNEEDIO__
ln -s /bin/sh /.__EL_SNEEDIO__/.__EL_SNEEDIO__
mkdir /.__EL_SNEEDIO__/modules.d
for f in /.__EL_SNEEDIO__/modules.d/*; do
    sh $f
done
# put some kind of watchdog on the modules? like run em all on a timer
# IDK LOL !
echo END
