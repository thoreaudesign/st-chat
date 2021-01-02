import json
import os

network_inspect = os.popen("docker network inspect stchat_internal")
output = json.loads(network_inspect.read())

gateways = []
for config in output:
    if config["Name"] == "stchat_internal":
        for gws in config["IPAM"]["Config"]:
            gateways.append(gws["Gateway"])
        for sha1 in config["Containers"]:
            print("{name}: ".format(name=config["Containers"][sha1]["Name"]))
            print(" - {ip}".format(ip=config["Containers"][sha1]["IPv4Address"][:-3]))
                

print("Gateway:")
for g in gateways:
    print("  - {g}".format(g=g))
