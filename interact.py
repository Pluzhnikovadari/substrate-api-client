import subprocess
import time
import os
import sys

def run_command(cmd,output="print",exit_on_error=False):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True,
        universal_newlines=True)
    o, e = p.communicate()
    if p.returncode != 0:
        if output == "print" : print("%s%s" % (o, e))
        if exit_on_error:
            print("Error. Exit script")
            quit()
        if output == "return": return("%s%s" % (o, e))
    else:
        if output == "return": return("%s%s" % (o, e))
        print("%s%s" % (o, e))

def to_string(ip_path):
    ip_path = ip_path.split('.')
    res = "1" + "0" * (3 - len(ip_path[0])) + ip_path[0] + "0" * (3 - len(ip_path[1])) + ip_path[1] + "0" * (3 - len(ip_path[2])) + ip_path[2]
    ip_path = ip_path[-1].split('/')
    res += "0" * (3 - len(ip_path[0])) + ip_path[0] + ip_path[-1]
    return res


our_ip = open('our_ip.txt', 'r')
cmd = "sudo cat /etc/quagga/bgpd.conf >> our_ip.txt"
run_command(cmd, "print")
our_way = our_ip.readlines()[4:6]
our_way = [our_way[0].split(' ')[-1][:-1], to_string(our_way[1].split(' ')[-1][:-1])]
run_command(cmd, "print")
tablewrite = open('bgptable.txt', 'w')
table = open('bgptable.txt', 'r')
update = open('bgptable_updates.txt', 'r')
updatewrite = open('bgptable_updates.txt', 'w')
event_get = open("substrate-api-client_1/events.txt", "r")
event = open("substrate-api-client_1/events.txt", "w")

send_data_write = open('substrate-api-client_1/data.txt', 'w')

event.truncate()
tablewrite.truncate()
updatewrite.truncate()


cmd = "sudo vtysh -c 'show ip bgp' >> bgptable.txt"
run_command(cmd, "print")

'''

while True:
    #работа с событиями и добавление пути в quagga

    ev = event_get.readlines()
    if len(ev) == 3:
        with open("substrate-api-client_1/events.txt", "w"):
            pass
        for i in range(3):
            ev[i] = ev[i].split(", ")[-1][:-2]
        print(our_way[0], ev[1])
        print(ev)
        if our_way[0] == ev[1]:
            if os.geteuid() == 0:
                print("We're root!")
                f = open('/etc/quagga/bgpd.conf', "r+")
                line = f.readlines()
                add = str(int(ev[0][1:4])) + "." + str(int(ev[0][4:7])) + "." + str(int(ev[0][7:10])) + "." + str(int(ev[0][10:13])) + '/' + str(int(ev[0][13:]))
                for i in range(len(line)):
                    print(line[i])
                    if ('neighbor' in line[i]) or ('network' in line[i]) or (i == len(line) - 1):
                        line = line[:i] + [' network ' + add + '\n'] + line[i:]
                        print(line)
                        f = open('/etc/quagga/bgpd.conf', "w+")
                        for el in line:
                            f.write(el)
            else:
                subprocess.call(['sudo', 'python3', *sys.argv])
                sys.exit()
            
        print(ev)
    
    updatewrite = open('bgptable_updates.txt', 'w')

    
    cmd = "sudo vtysh -c 'show ip bgp' >> bgptable_updates.txt"
    run_command(cmd, "print")
    
    tablefile = table.readlines()[6:-2]
    updatefile = update.readlines()[6:-2]
    t = set(tablefile)
    u = set(updatefile)
    t.difference_update(u)
    for elem in t:
        ip_path = elem.split()[1]
        ip_path = to_string(ip_path)
        print('send', ip_path) 
        print('send', our_way)

        with open('substrate-api-client_1/data.txt', 'w') as send_data_write:
            send_data_write.write(str(ip_path))
        cmd = "cd substrate-api-client_1/ && cargo +nightly-2020-10-01 run --example example_generic_extrinsic"
        run_command(cmd, "print")

        with open('substrate-api-client_1/data.txt', 'w') as send_data_write:
            send_data_write.write(our_way[0]) #send our number of router
        run_command(cmd, "print")

        with open('substrate-api-client_1/data.txt', 'w') as send_data_write:
            send_data_write.write(our_way[1]) #send our ip number
        run_command(cmd, "print")
    
    with  open('bgptable.txt', 'w') as tablewrite:
        data = update.read()
        tablewrite.write(data)
'''
