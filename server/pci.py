import aiohttp

vendors = {}

def is_hex(c):
    return (c >= "0" and c <= "9") or (c >= "a" and c <= "f")

async def init():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://pci-ids.ucw.cz/v2.2/pci.ids") as resp:
            devs = await resp.text()
            cur = ""
            for line in devs.split("\n"):
                if len(line) < 1: continue
                if is_hex(line[0]):
                    vendors[line[:4]] = {"name": line[6:], "devices": {}}
                    cur = line[:4]
                elif line[0] == "\t" and is_hex(line[1]):
                    vendors[cur]["devices"][line[1:5]] = line[7:]

def pcis_to_str(pcis):
    return ", ".join([f"{vendors[x[:4]]['name']}: {vendors[x[:4]]['devices'][x[4:]]}" for x in pcis])
