import subprocess
import os
import re
import time
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


# Association is the list cotaining ordered pair of numbers (UE,APs) 
association=[]
for j in range(count):
    if r[0,j] > 0:
      association.append((0,j))
print('Association',association)

# Goal is the final destination set for Q-learning
goal = count+1
MATRIX_SIZE = count+2

# R is Reward matrix inintially set to -1
R = np.matrix(np.ones(shape=(MATRIX_SIZE, MATRIX_SIZE)))
R *= -1

# pac is the list containing the number of packets encountered at each access point
pac = []
#-------------------------------------------------- Reading csv file for load information generated using Kali Linux
train = pd.read_csv("myOutput-01.csv") 
df = pd.DataFrame(train)
for accesspoint in ap:
    packet = df.loc[df[' ESSID'] == accesspoint]
    packet = packet.head(1)
    load = packet[' # IV']
    strings = [str(integer) for integer in load.values.tolist()]
    a_string = "".join(strings)
    a_string = a_string + "0"
    an_integer = float(a_string)
    pac.append(an_integer)


#------------------------------------------------- Normalization of data packets at each access point

load = [] # it is the list containing normalised load
print("Number of packets encountered ")
print(pac)

amin = min(pac)
amax = 0
for num in pac:
    if (amax is None or num > amax):
        amax = num
# amax = max_value
for i, val in enumerate(pac):
    try:
        pac[i] = (val-amin) / (amax-amin)
    except:
        pac[i]=0


load = pac

#------------------------------------------------ Assigning Rewards 
for idx,point in enumerate(association):
    if pac[idx] > 0.75:
        packet = 0
    elif pac[idx] > 0.50:
        packet = 25
    elif pac[idx] > 0.25:
        packet = 50
    else:
        packet = 100 
    if r[point] >= 75:
        R[point[0],point[1]+1] = 100 + packet
    elif r[point] >= 50:
        R[point[0],point[1]+1] = 50 + packet
    elif r[point] < 50 :
        R[point[0],point[1]+1] = 0 + packet



print('\nRewards\n')
for i in range(1,count+2):
  R[i,count+1] = 150
print(R)
Q = np.matrix(np.zeros([MATRIX_SIZE,MATRIX_SIZE]))

# learning parameter
gamma = 0.8

initial_state = 1

def available_actions(state):
    current_state_row = R[state,]
    av_act = np.where(current_state_row >= 0)[1]
    return av_act

available_act = available_actions(initial_state) 
def sample_next_action(available_actions_range):
    next_action = int(np.random.choice(available_act,1))
    return next_action

action = sample_next_action(available_act)

def update(current_state, action, gamma):
    
  max_index = np.where(Q[action,] == np.max(Q[action,]))[1]
  
  if max_index.shape[0] > 1:
      max_index = int(np.random.choice(max_index, size = 1))
  else:
      max_index = int(max_index)
  max_value = Q[action, max_index]

#   /----------------------------------------------------------Updation of Q-table
  
  Q[current_state, action] = R[current_state, action] + gamma * max_value


  if (np.max(Q) > 0):
    return(np.sum(Q/np.max(Q)*100))
  else:
    return (0)
    
update(initial_state, action, gamma)

# ----------------------------------------------------Training Stage
scores = []
for i in range(700):
    current_state = np.random.randint(0, int(Q.shape[0]))
    # print(current_state)
    available_act = available_actions(current_state)
    action = sample_next_action(available_act)
    score = update(current_state,action,gamma)
    scores.append(score)
    # print ('Score:', str(score))
    
# --------------------------------------------Graph showing the scores for each iteration
plt.figure(figsize=(8,6))
plt.xlabel('# of Iterations')
plt.ylabel('score') 
plt.plot(scores, label = 'score value')
plt.legend(loc='best')
plt.show()

print("\nTrained Q matrix:\n")
# print(Q)
print(Q/np.max(Q)*100)
print("\nload rewards\n")
print(load)

# Testing
def walk(start,goal):
 current_state = start
 steps = [current_state]

 while current_state != goal:

    next_step_index = np.where(Q[current_state,] == np.max(Q[current_state,]))[1]
     
    if next_step_index.shape[0] > 1:
        next_step_index = int(np.random.choice(next_step_index, size = 1))
    else:
        next_step_index = int(next_step_index)
    
    steps.append(next_step_index)
    current_state = next_step_index
        

 print("\nMost efficient Association:")
 
 steps 
 
 print ("src...dst", start, goal)

 if goal > start: 
  steps
  print(steps)
 else:
  steps.reverse()
  print(steps)
 return steps

steps = walk(0,count+1)

print(steps[1])

index = steps[1]-1
final= ap[index]
final = final[1:]
print("Connecting to Network")
print(final)

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