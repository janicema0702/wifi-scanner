import subprocess
from mac_vendor_lookup import MacLookup

# for loop for each ip address
start = 200
end = 250

all_ips = []
for i in range (int(start), int(end)):
    x = '192.168.1.' + str(i)
    all_ips.append(x)

connected_devices = []

'''for i, ip in enumerate (all_ips): 
    p1 = subprocess.run(['ping', '-c', '1', ip], stdout = subprocess.PIPE)
    if p1.returncode != 0:
        print ( ip + " fail")
    else:
        connected_devices.append(ip)
        print(ip + " success")'''


for i, ip in enumerate (all_ips): 
    try: 
        p1 = subprocess.run(['ping', '-c', '1', ip], stdout = subprocess.PIPE,timeout=0.05)
    except:
        print (ip + " is disconnected")
    else:
        connected_devices.append(ip)
        print(ip + " is connected")

print (connected_devices)


# get mac addresses
ARP_cache = subprocess.run(['arp', '-a'], stdout = subprocess.PIPE)
ARPlist = (ARP_cache.stdout.decode()).split("?")
mac_addresses = []
incomplete_on_addresses = []


for i in range(len(ARPlist)):
    for x in range(len(connected_devices)):
        if ARPlist[i].find(connected_devices[x]) != -1:
            if '(incomplete) on' in ARPlist[i][19:36]:
                incomplete_on_addresses.append(ARPlist[i][19:36])
            else:
                mac_addresses.append(ARPlist[i][19:36])
                

print (mac_addresses)


for i, x in enumerate (mac_addresses):
    y= x.strip()
    try: 
        type = MacLookup().lookup(y)
    except:
        print ( "ip - " + connected_devices[i] + " | mac address - " + y + " | No assignment is found for this MAC")
    else:
        print("ip - " + connected_devices[i] + " | mac address - " + y + " | " + type)
        
    









       
