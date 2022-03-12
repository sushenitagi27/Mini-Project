import subprocess
import os 

try:
    returned_speed = subprocess.check_output("ping www.google.com", shell=True, universal_newlines=True)
    print(returned_speed)
    returned_speed = returned_speed.split()
except:
    exec(open('client.py').read())

for i in returned_speed:
    if i.endswith('ms'):
        f= (i[:-2])

f = int(f)

# f = 12
print("\nAverage Latency ",f)
if f > 100:
    print("\nThe network speed is not optimal\nConnecting to another access point...\n")
    exec(open('client.py').read())

