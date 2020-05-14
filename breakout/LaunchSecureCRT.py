# Python script to launch Breakout and query labs.yaml file for appropriate ports, open in SecureCRT
# Designed for macOS (Unix) - can be optimized for Windows / other Linux distros

# Note that this is optimized for macOS. File paths may need to be changed depending on your environment.

import os
import yaml
import subprocess

subprocess.call(["rm", "/Users/username/breakoutfiles/labs.yaml"]) # Delete existing labs.yaml file if it exists
subprocess.call(["/Users/username/breakoutfiles/breakout", "-noverify", "-config", "config.yaml", "init"]) # Call breakout process to create labs.yaml file
    
stream = open('labs.yaml', 'r')
data = yaml.load(stream, Loader=yaml.FullLoader)
keys = list(data.keys())

if (len(keys) == 0): # Check if there are no labs running - if condition is satisfied, print msg and exit the program
    print("No labs active.")
    exit()

for key in keys:
    (data[key]['enabled']) = True

with open('labs.yaml', 'w') as file:
    yaml.dump(data, file)

nodes = {} # initialize the node dictionary

for key in keys:
    nodes = {key:list((data[key]['nodes']).keys())}

subprocess.Popen(['./breakout', 'run'])

for key in nodes:
    for node in nodes[key]:
        if (data[key]['nodes'][node]['devices'][0]['enabled']) == True:
            os.system('/Applications/SecureCRT.app/Contents/MacOS/SecureCRT /N ' + (data[key]['nodes'][node]['label']) + ' /T /TELNET 127.0.0.1 ' + str((data[key]['nodes'][node]['devices'][0]['listen_port'])))

def kill():
    killstatus = input("Type \"kill\" to kill the process.")
    if (killstatus == "kill"):
        output = os.system("pkill \"(.*)breakout(.*)\"")

kill()
