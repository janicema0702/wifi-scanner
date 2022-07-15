import PySimpleGUI as sg
import subprocess
from mac_vendor_lookup import MacLookup
import socket   

hostname=socket.gethostname()   
these_name_list = sg.theme_list()
sg.theme('DarkTeal6')
 

toplayout = [
        [sg.Text("IP Address Lookup", font=("Helvetica", 20))], 
        [sg.Text("Start"), sg.Input("", key = '-START-', do_not_clear = False, size =(5, 1)), 
        sg.Text("End"), sg.Input("", key = '-END-', do_not_clear = False ,size =(5, 1)),
        sg.Text(" "),
        sg.Button('Scan', font=("Helvetica", 7 )),
        sg.Text("  "),
        sg.Text("Unkown IP Address", font=("Helvetica", 12), key = "-IP OUTPUT-"),
        sg.Button("Find IP", font=("Helvetica", 7 ))], 
        #[sg.ProgressBar(max_value=100, size=(35,10), key='bar')],
        [sg.Listbox(values = [], enable_events = True, size = (40,20), font=("Helvetica", 15), key = "-TYPE LIST-")]
]

info_viewer_column = [
    [sg.Text("Device Type: ", font=("Helvetica", 15))],
    [sg.Text(size = (40,1), key = "-DEVICE TYPE OUTPUT-")],
    [sg.Text("  ")],
    [sg.Text("IP Address: ", font=("Helvetica", 15))],
    [sg.Text(size = (40,1), key = "-IP ADDRESS OUTPUT-")],
    [sg.Text("  ")],
    [sg.Text("MAC Address: ", font=("Helvetica", 15))],
    [sg.Text(size = (40,1), key = "-MAC ADDRESS OUTPUT-")]
      
]

layout = [
    [
        sg.Column (toplayout),
        sg.VSeperator(),
        sg.Column(info_viewer_column),
    ]
]

window = sg.Window("Wifi Scanner", layout, size=(600, 400))

#progress = 0
# event loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    elif event == "Find IP":
        hostname=socket.gethostname()   
        try:
            global IPAddr ; IPAddr = socket.gethostbyname_ex(hostname)[2][1]
            window["-IP OUTPUT-"].update(str(IPAddr),font=("Helvetica", 12))

        except:
            IPAddr = socket.gethostbyname_ex(hostname)[2][0]
            window["-IP OUTPUT-"].update(str(IPAddr),font=("Helvetica", 12))
           
        
    elif event == "Scan":
        # for loop for each ip address
        
        global start; start = int([values['-START-']][0])
        global end; end = int([values['-END-']][0])
        
        #step = 35/(end - start)
        #progress += step
        #window['bar'].update_bar(progress)
	    

        all_ips = []
        for i in range (int(start), int(end)):
            global z; z = str(i) 
            fullip = (str(IPAddr)).split(".")
            x = fullip.pop()
            y   = '.'.join(fullip) + "." + z
            all_ips.append(y)
        

        connected_devices = []


        for i, ip in enumerate (all_ips): 
            try: 
                p1 = subprocess.run(['ping', '-c', '1', ip], stdout = subprocess.PIPE,timeout=0.1)
            except:
                print (ip + " is disconnected")
            else:
                connected_devices.append(ip)
                print(ip + " is connected")
        


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
        
        #print (mac_addresses)
        typelist = []
        all_info = {"IP":[],"MAC":[],"TYPE":[]};

 
        for i, x in enumerate (mac_addresses):
            y = x.strip()
            try: 
                type = MacLookup().lookup(y)
            except:
                print ( "ip - " + connected_devices[i] + " | mac address - " + y + " | No assignment is found for this MAC")
                typelist.append( str(i +1) + ": Vendor not found")
                all_info["IP"]. append(connected_devices [i])
                all_info["MAC"]. append(y)
                all_info["TYPE"]. append(str(i + 1) + ": Vendor not found")
            else:
                print("ip - " + connected_devices[i] + " | mac address - " + y + " | " + type)
                typelist.append(str(i + 1) +  ": " + type)
                all_info["IP"]. append(connected_devices [i])
                all_info["MAC"]. append(y)
                all_info["TYPE"]. append(str(i + 1) +  ": " + type)
            window["-TYPE LIST-"].update(typelist)

    elif event == "-TYPE LIST-":
        type_selection = values["-TYPE LIST-"]
        i = all_info["TYPE"].index(type_selection[0])
        window["-DEVICE TYPE OUTPUT-"].update (all_info["TYPE"][i], font=("Helvetica", 12))
        window["-IP ADDRESS OUTPUT-"].update (all_info["IP"][i], font=("Helvetica", 12))
        window["-MAC ADDRESS OUTPUT-"].update ( all_info["MAC"][i], font=("Helvetica", 12))
            

window.close()

# add progress bar
# try catch loop for error (input for range, click out of the window, scanning nothing)