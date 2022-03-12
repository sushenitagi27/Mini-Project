import subprocess
import os
import re
import time
from typing import final
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pylab as plt
from numpy import matrix, maximum

# ---------------------------------------------------Discovering the AP Networks visible to the Station
returned_text = subprocess.check_output("netsh wlan show networks mode= Bssid", shell=True, universal_newlines=True)
print("Showing networks")
print(returned_text)

# Parsing the output of command prompt window 
split_string = returned_text.split(':' and '\n')
split_string.remove(" ")

# ssf is the list containing singal strength of each access point
ssf=[] 

# ap is the list containing all Essid (Eletronic marker or identifier)  of APs
ap=[]

flag=0
max = 0
submax=0
for idx,i in enumerate(split_string):
    if i.startswith("S"):
        bssid = []
        flag=1
        print(i)
        AP = i.split(":")
        res = re.sub(' +', ' ', AP[1])
        res.strip()
        ap.append(res)
        submax=0
    if i.endswith("%  "):
        print(i)
        strength = i.split(":")
        res = re.sub(' +', ' ', strength[1])
        res = res.strip()
        res = res[0:-1]
        res = int(res)
        if flag == 0:
            bssid.append(res)
            bssid.sort()
            max = bssid[-1]
            ssf.pop()
            ssf.append(max)
            print(bssid)
            res=submax
        else:
            bssid.append(res)
            max=res
            print(max)
            ssf.append(max)
            flag=0




print("APs ",ap)
r = matrix(ssf)
print("Signal Strength ",r)
count = len(ssf)

string =''
string2 = ''
for i in ap:
    string = string +","+ str(i)
for j in ssf:
    string2 = string2 +","+ str(j)

#----- A simple TCP client program in Python using send() function -----

import socket

 

# Create a client socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);


 

# Connect to the server

clientSocket.connect(("192.168.43.208",9090));

 

# Send data to server

data1 = string ; #storing ap list into data1
data2 = string2; #storing signal strength list into data2

clientSocket.send(data1.encode());
clientSocket.send(data2.encode());

 

# Receive Optimal AP to connect with from server

final = clientSocket.recv(1024);
final = final.decode();
# Print to the console
print(final);

# Connect to the AP given by the Controller

# function to establish a new connection
def createNewConnection(name, SSID, password):
	config = """<?xml version=\"1.0\"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
	<name>"""+name+"""</name>
	<SSIDConfig>
		<SSID>
			<name>"""+SSID+"""</name>
		</SSID>
	</SSIDConfig>   
	<connectionType>ESS</connectionType>
	<connectionMode>auto</connectionMode>
	<MSM>
		<security>
			<authEncryption>
				<authentication>WPA2PSK</authentication>
				<encryption>AES</encryption>
				<useOneX>false</useOneX>
			</authEncryption>
			<sharedKey>
				<keyType>passPhrase</keyType>
				<protected>false</protected>
				<keyMaterial>"""+password+"""</keyMaterial>
			</sharedKey>
		</security>
	</MSM>
</WLANProfile>"""
	command = "netsh wlan add profile filename=\""+name+".xml\""+" interface=Wi-Fi"
	with open(name+".xml", 'w') as file:
		file.write(config)
	os.system(command)

# function to connect to a network
def connect(name, SSID):
	command = "netsh wlan connect name=\""+name+"\" ssid=\""+SSID+"\" interface=Wi-Fi"
	os.system(command)

# function to display avavilabe Wifi networks
def displayAvailableNetworks():
	command = "netsh wlan show networks interface=Wi-Fi"
	os.system(command)


password = input("Password: ")

# establish new connection
createNewConnection(final, final, password)

# connect to the wifi network
connect(final, final)
print("Connecting...")
time.sleep(5)

exec(open('status.py').read())

