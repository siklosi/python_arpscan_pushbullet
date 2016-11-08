#! /usr/bin/python

# REQUIREMENTS:
# http://standards.ieee.org/regauth/oui/oui.txt needed for finding device vendor
# sudo apt-get install arp-scan 
# sudo pip install pushbullet.py

import os
import sys
import time
from pushbullet import Pushbullet
pb = Pushbullet("YOUR_PUSHBULLET_API_KEY")

pathname = os.path.dirname(sys.argv[0])        
fpath= os.path.abspath(pathname)

if not os.path.exists(fpath+"/known"):
    open('file', 'w').close() 

with open(fpath+"/known") as g:
    known = g.readlines()

arpscan=os.popen("sudo arp-scan --interface=eth0 --localnet|grep 192.168.0").read()
arpscan=arpscan.split("\n")

def do_something(foundmac):
	foundoui=0
	ouimac =  foundmac.split()[1].replace(":","-")[:8].upper()
	with open(fpath+"/oui.txt") as o:
		oui = o.readlines()
	for ouimacs in oui:
		if (ouimac in ouimacs):
			print foundmac.split()[0]+" - "+ foundmac.split()[1] + " - " + ouimacs[18:].rstrip()
			with open(fpath+"/known", "a") as myfile:
				myfile.write(foundmac.split()[1]+" NOT VERIFIED DEVICE "+foundmac.split()[0]+" - "+ ouimacs[18:].rstrip() + " *** Detected on: "+time.strftime("%d.%m.%Y %H:%M")+"\n" )
			push = pb.push_note("Unverified device on network", foundmac.split()[1]+" NOT VERIFIED DEVICE "+foundmac.split()[0]+" - "+ ouimacs[18:].rstrip() + " *** Detected on: "+time.strftime("%d.%m.%Y %H:%M"))
			foundoui=1
	if (foundoui==0):	
		with open(fpath+"/known", "a") as myfile:
			myfile.write(foundmac.split()[1]+" NOT VERIFIED DEVICE "+foundmac.split()[0]+" - "+" *** Detected on: "+time.strftime("%d.%m.%Y %H:%M")+"\n" )
		push = pb.push_note("Unverified device on network", foundmac.split()[1]+" NOT VERIFIED DEVICE "+foundmac.split()[0]+" - "+" *** Detected on: "+time.strftime("%d.%m.%Y %H:%M"))
	return


for arpmac in arpscan:
	found = 0
	for knownmac in known:
		if (len(knownmac.split(" "))>0):
			mac = knownmac.split(" ")[0]
			if (mac in arpmac):
				found = 1
	if (found == 0):
		if (len(arpmac)>2):
			do_something(arpmac)
		
