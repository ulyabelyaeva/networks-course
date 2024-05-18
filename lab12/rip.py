import json

from time import sleep
from threading import Thread

MAX_NUMBER_OF_HOPS = 15
MAX_NUMBER_OF_ROUTERS = 25
TIME_BETWEEN_UPDATES = 0.001  # got no time to wait 30sec

table_template = '''Final state of router {ip} table:
[Source IP]\t[Destination IP]\t[Next Hop]\t[Metric]
'''

perineal_table_template = '''Simulation step {step} of router {ip}
[Source IP]\t[Destination IP]\t[Next Hop]\t[Metric]
'''

row_template = '''{source}\t{dest}\t{next}\t{hops}
'''


def update_table(router):
    is_updated = False
    a = ip_to_id_map[router]
    for e in config:
        u, v = e
        # simulate that we don't know the other edges
        if router != u and router != v:
            continue

        if router == v:
            u, v = v, u

        b = ip_to_id_map[v]
        # update table #a with new info from #b
        for i in range(MAX_NUMBER_OF_ROUTERS):
            if routes[a][i] > routes[b][i] + 1:
                routes[a][i] = routes[b][i] + 1
                next_hop[a][i] = v
                is_updated = True
    return is_updated


def format_table(router, step=-1):
    if step == -1:
        table = table_template.format(ip=router)
    else:
        table = perineal_table_template.format(ip=router, step=step)
    a = ip_to_id_map[router]
    for ip in ip_to_id_map:
        if ip == router:
            continue
        b = ip_to_id_map[ip]
        table += row_template.format(source=router, dest=ip, next=next_hop[a][b], hops=routes[a][b])
    return table


def run_rip(router):
    last = ""
    for i in range(MAX_NUMBER_OF_HOPS):
        is_updated = update_table(router)
        if not is_updated:
            print(format_table(router))
            break
        table = format_table(router, step=i)
        print(table)
        sleep(TIME_BETWEEN_UPDATES)


# read config from json

with open("config.json", "r") as f:
    config = json.loads(f.read())

# assign numbers to ips

ip_to_id_map = dict()
for e in config:
    u, v = e
    if u not in ip_to_id_map.keys():
        ip_to_id_map[u] = len(ip_to_id_map)
    if v not in ip_to_id_map.keys():
        ip_to_id_map[v] = len(ip_to_id_map)

if len(ip_to_id_map) > MAX_NUMBER_OF_ROUTERS:
    print("MAX_NUMBER_OF_ROUTERS exceeded: network too large")

id_to_ip_map = dict()
for ip in ip_to_id_map:
    id_to_ip_map[ip_to_id_map[ip]] = ip

# create routing and next hop tables

routes = [[MAX_NUMBER_OF_HOPS + 1] * MAX_NUMBER_OF_ROUTERS for i in range(MAX_NUMBER_OF_ROUTERS)]
next_hop = [["unknown"] * MAX_NUMBER_OF_ROUTERS for i in range(MAX_NUMBER_OF_ROUTERS)]

for i in range(MAX_NUMBER_OF_ROUTERS):
    routes[i][i] = 0
    next_hop[i][i] = id_to_ip_map.get(i, None)

# run threads

threads = [Thread(target=run_rip, args=(router,)) for router in ip_to_id_map]

for router in ip_to_id_map:
    threads[ip_to_id_map[router]].start()

for thread in threads:
    thread.join()
