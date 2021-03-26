import requests
from Utils import getConfig, getHeader, cprint, FG

guildID = input('Guild ID: ')
token = getConfig()['token']

guild = requests.get(f'https://discord.com/api/v6/guilds/{guildID}?with_counts=true', headers=getHeader(token=token)).json()
channels = requests.get(f'https://discord.com/api/v6/guilds/{guildID}/channels', headers=getHeader(token=token)).json()

roles = guild['roles']

def getRolename(id: str) -> str:
    for role in roles:
        if role['id'] == id:
            return role['name']

def getChannel(id: str) -> str:
    for chan in channels:
        if chan['id'] == id:
            return channel['name']

usercache = {}
def getUsername(id: str) -> str:
    if id in usercache:
        return usercache[id]
    j = requests.get(f'https://discord.com/api/v6/users/{id}', headers=getHeader(token=token)).json()
    result = f"{j['username']}#{j['discriminator']}"
    usercache[id] = result
    return result

a = FG.cyan
b = FG.brightcyan
c = FG.magenta

cprint(f"{FG.magenta}Server information:")
cprint(f"{a}  Name          →{b}{guild['name']}")
cprint(f"{a}  Members       →{b}{guild['approximate_presence_count']}/{guild['approximate_member_count']}")
if 'vanity_url_code' in guild:
    cprint(f"{a}  Vanity URL    →{b}{guild['vanity_url_code']}")
print()
for channel in channels:
    cprint(f"{a}  Channel Name      →{b}{channel['name']}")
    if 'parent_id' in channel:
        cprint(f"{a}  Category          →{b}{getChannel(channel['parent_id'])}")
    if 'topic' in channel:
        cprint(f"{a}  Topic             →{b}{channel['topic']}")
    cprint(f"{a}  Permissions")
    for perm in channel['permission_overwrites']:
        if perm['allow'] == 0 and perm['deny'] == 0: continue
        if perm['type'] == 'role':
            cprint(f"{FG.magenta}    Role: {getRolename(perm['id'])}")
        elif perm['type'] == 'member':
            cprint(f"{FG.magenta}    Member: {getUsername(perm['id'])}")

        if perm['allow'] != 0:
            cprint(f"{FG.green}    +{perm['allow']}")
        if perm['deny'] != 0:
            cprint(f"{FG.red}    -{perm['deny']}")
print()
for role in guild['roles']:
    cprint(f"{a}  Role Name        →{b}{role['name']}")
    cprint(f"{a}  Permissions      →{b}{role['permissions']}")
    cprint(f"{a}  Color            →{b}{role['color']}")
