#!/usr/bin/env python3

# networkFileRW.py
# Joy Dill
# April 20, 2022
# Update routers and switches;
# read equipment from a file, write updates & errors to file
# Testing Git 

try:
    import json
except ImportError:
    print("There was an error importing")


# Constants for file names
ROUTER_EQUIP = 'equip_r.txt'
SWITCH_EQUIP = 'equip_s.txt'
UPDATED = 'updated.txt'
INVALID = 'invalid.txt'

# Prompt constants
UPDATE = "\nWhich device would you like to update "
QUIT = "(enter x to quit)? "
NEW_IP = "What is the new IP address (111.111.111.111) "
SORRY = "Sorry, that is not a valid IP address\n"

# Function to get valid device
def getValidDevice(routers, switches):
    validDevice = False
    while not validDevice:
        # Prompt for device to update
        device = input(UPDATE + QUIT).lower()
        if device in routers.keys():
            return device
        elif device in switches.keys():
            return device
        elif device == 'x':
            return device  
        else:
            print("That device is not in the network inventory.")

# Function to get valid IP address
def getValidIP(invalidIPCount, invalidIPAddresses):
    validIP = False
    while not validIP:
        ipAddress = input(NEW_IP)
        octets = ipAddress.split('.')
        for byte in octets:
            byte = int(byte)
            if byte < 0 or byte > 255:
                invalidIPCount += 1
                invalidIPAddresses.append(ipAddress)
                print(SORRY)
                break
        else:
            # validIP = True
            return ipAddress, invalidIPCount
        
def main():

    ##---->>>> open files here
    #open(ROUTER_EQUIP)
    #open(SWITCH_EQUIP)

    # Read the router file into the routers dictionary
    routers = {}
    with open(ROUTER_EQUIP) as rfile:
        for line in rfile:
            routers = line
            routers = json.loads(routers)
            print(routers)
            print(type(routers))
            print('test')

    # Read the switches file into the switches dictionary
    switches = {}
    with open(SWITCH_EQUIP) as file:
        for line in file:
            switches = line
            switches = json.loads(switches)
            print(switches)
            print(type(switches))
            print('test 2')

    #the updated dictionary holds the device name and new ip address
    updated = {}

    #list of bad addresses entered by the user
    invalidIPAddresses = []

    #accumulator variables
    devicesUpdatedCount = 0
    invalidIPCount = 0

    #flags and sentinels
    quitNow = False
    validIP = False

    print("Network Equipment Inventory\n")
    print("\tequipment name\tIP address")
    for router, ipa in routers.items(): 
        print("\t" + router + "\t\t" + ipa)
    for switch, ipa in switches.items():
        print("\t" + switch + "\t\t" + ipa)

    while not quitNow:

        #function call to get valid device
        device = getValidDevice(routers, switches)
        
        if device == 'x':
            quitNow = True
            break
        
        #function call to get valid IP address
        ipAddress, invalidIPCount = getValidIP(invalidIPCount, invalidIPAddresses)
  
        #update device
        if 'r' in device:
            #modify the value associated with the key
            routers[device] = ipAddress 
            
        else:
            switches[device] = ipAddress

        devicesUpdatedCount += 1
        #add the device and ipAddress to the dictionary
        updated[device] = ipAddress

        print(device, "was updated; the new IP address is", ipAddress)
        #loop back to the beginning

    #user finished updating devices
    print("\nSummary:")
    print()
    print("Number of devices updated:", devicesUpdatedCount)

    # Write the updated equipment dictionary to a file
    with open(UPDATED, 'w') as file:
        file.write(str(updated))
    
    print("Updated equipment written to file 'updated.txt'")
    print()
    print("\nNumber of invalid addresses attempted:", invalidIPCount)

    # Write the list of invalid addresses to a file
    with open(INVALID, 'w') as file:
        file.write(str(invalidIPAddresses))

    print("List of invalid addresses written to file 'errors.txt'")

# top-level scope check
if __name__ == "__main__":
    main()
