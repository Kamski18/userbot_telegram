# TODO: .start will activate a firewall for this wifi to prevent adam from playing roblox
import subprocess

router_online = True
ROUTER_IP = ""

async def check_router(message):
    global router_online

    #  Trying to use Ping method to check status of router
    try:
        subprocess.check_output(["ping", "-c", "1", "-W", "2", ROUTER_IP])
        ping_ok = True
    except subprocess.CalledProcessError:
        ping_ok = False

    is_online = ping_ok

    if is_online and not router_online:
        return "`Router is **Online**!`"
    elif not is_online and router_online:
        return "`Router is **Offline**!`"