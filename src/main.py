import sys
import os
import json
from socket import gaierror, timeout
import schedule
import time
from mcstatus import MinecraftServer

# Custom defined exceptions
class UserAborted(Exception):
    """User aborted crucial program process."""
    pass

print("Welcome to alzhahir's simple server status query application.\n")

# Load config.json
try:
    print("Loading configuration...")
    with open("./config.json") as conf_file:
        config = json.load(conf_file)
    
    print("Successfully loaded configuration file, config.json")
except:
    print("ERROR: Cannot find or load config.json in program directory! Did you delete it?")

    print("\nInitializing...")

    print("Please enter the Minecraft address you will be using.")
    webAddress = str(input())
    print("\nAlright, set {0} as your domain address.".format(webAddress))

    print("\nNext, please enter the server port.")
    srvport = int(input())
    print("\nSet {0} as server port.".format(srvport))

    print("\nNext, let's set the requery frequency, in minutes.")
    refreshfreq = int(input())

    if refreshfreq > 1:
        minstr = "minutes"
    else:
        minstr = "minute"
    
    print("\nNice, set the app to requery every {0} {1}.".format(refreshfreq, minstr))

    print("\nLet's also set the output directory for the response json and js. Please set it the same as your status.html.")
    outputdir = str(input())
    print("\nCreating new config file...")

    config_init = {
	        "domainAddress" : webAddress,
            "serverPort" : srvport,
            "rateRefresh" : refreshfreq,
            "outputDir" : outputdir
    }

    config_formatted = json.dumps(config_init, indent = 4)

    with open("./config.json", "w") as conf_new:
        conf_new.write(config_formatted)
    
    print("Successfully created new configuration file. Loading file...")

    with open("./config.json") as conf_file:
        config = json.load(conf_file)
    
    print("\nSuccessfully loaded configuration file, config.json")

# import config.json and assign dict objects into variables
timesec = config['rateRefresh']
domainSite = config['domainAddress']
outputDirectory = config['outputDir']
port = config['serverPort']

if timesec > 1:
    minutestr = "minutes"
else:
    minutestr = "minute"

print("\nConfiguration set successfully.")
print("\nStarting service...")
print("The service will refresh every {0} {1}.".format(timesec, minutestr))
print("\nInitializing first query...")

# create new dir func
def newDir():
    try:
        print("\nCreating directory {0}".format(outputDirectory))
        os.mkdir(outputDirectory)
        print("Done!")
        return
    except PermissionError:
        print("\nFATAL: Cannot write to the specified directory due to missing permissions. Please restart the program with Administrator priviledges if the directory you specified is protected.")
        sys.exit(3)
    except Exception as errorInfo:
        print("\nFATAL: {0} exception occured. Exiting program. This might be a bug, so please create an issue if you found this.".format(errorInfo.__class__.__name__))
        sys.exit(1)

# offline read/write
def offlinerw():
    try:
        isOnline = "Offline"
        serverResponse = {
            "serverHealth" : isOnline,
            "playerOnline" : 0,
            "playersAvailable" : "Server offline",
            "serverLatency" : 0,
            "refreshRate" : timesec
        }

        print("\nAssuming the server is offline, writing server offline status to serverstatusjson.json and serverstatus.js")

        savejson = json.dumps(serverResponse, indent = 4)

        with open("{0}serverstatusjson.json".format(outputDirectory), "w") as outputfile:
            outputfile.write(savejson)

        textjs = "var servHealth = '{0}'\nvar playStr = 'players'\nvar minStr = '{1}'\nvar playOn = 0\nvar playAvail = 'Offline'\nvar servLat = 0\nvar refRate = {2}\nexport {{\n\tservHealth,\n\tplayStr,\n\tminStr,\n\tplayOn,\n\tplayAvail,\n\tservLat,\n\trefRate\n}}"

        with open("{0}serverstatus.js".format(outputDirectory), "w") as outputfile:
            outputfile.write(textjs.format(isOnline, minutestr, timesec))
        
        print("Done. Rechecking in {0} {1}.\n".format(timesec, minutestr))
    except Exception as errorInfo:
        print("FATAL: {0} occured. Exiting program. This might be a bug, so please create an issue if you found this.".format(errorInfo.__class__.__name__))
        sys.exit(2)

# main
def mainfunc():
    try:
        print("\nQuerying {0} on port {1}...".format(domainSite, port))
        server = MinecraftServer(domainSite, port)

        status = server.status()
        query = server.query()

        onlinePlayers = status.players.online
        latency = status.latency
        playerList = query.players.names
        pingLatency = server.ping()

        isOnline = "Online"

        if onlinePlayers > 1:
            playerstr = 'players'
        else:
            playerstr = 'player'
        
        if onlinePlayers == 0:
            playerstr = 'players'

        serverResponse = {
	        "serverHealth" : isOnline,
            "playerOnline" : onlinePlayers,
            "playersAvailable" : playerList,
            "serverLatency" : pingLatency,
            "refreshRate" : timesec
        }

        print("Query successful!")
        print("\nServer has {0} players online".format(onlinePlayers))
        print("The server replied in {0}ms\n".format(pingLatency))

        print("Writing to serverstatusjson.json and serverstatus.js...")

        savejson = json.dumps(serverResponse, indent = 4)

        with open("{0}serverstatusjson.json".format(outputDirectory), "w") as outputfile:
            outputfile.write(savejson)

        textjs = "var servHealth = '{0}'\nvar playStr = '{1}'\nvar minStr = '{2}'\nvar playOn = {3}\nvar playAvail = {4}\nvar servLat = {5}\nvar refRate = {6}\nexport {{\n\tservHealth,\n\tplayStr,\n\tminStr,\n\tplayOn,\n\tplayAvail,\n\tservLat,\n\trefRate,\n}}"

        with open("{0}serverstatus.js".format(outputDirectory), "w") as outputfile:
            outputfile.write(textjs.format(isOnline, playerstr, minutestr, onlinePlayers, playerList, pingLatency, timesec))

        print("Done. Refresh will occur in {0} {1}.\n".format(timesec, minutestr))
    except gaierror:
        print("\nERROR: Error resolving address. Please check your network connection configuration and make sure that the address is typed correctly.")
        offlinerw()
    except timeout:
        print("\nERROR: Timeout error occured. Please check your network connection configuration and make sure that the address is typed correctly.")
        offlinerw()
    except PermissionError:
        print("\nFATAL: Cannot write to the specified directory due to missing permissions. Please restart the program with Administrator priviledges if the directory you specified is protected.")
        sys.exit(3)
    except FileNotFoundError:
        print("\nERROR: The specified directory cannot be located. Proceeding to create a new directory in the defined location.")
        print('\nATTENTION: Do you really want to create a new directory in "{0}"? (Y/N)'.format(outputDirectory))
        userDirChoice = str(input())
        try:
            if userDirChoice == 'y' or userDirChoice == 'Y':
                newDir()
                print("Re-running the program again immediately.")
                mainfunc()
            elif userDirChoice == 'n' or userDirChoice == 'N':
                print("WARN: Directory creation canceled! Please check your configurations and make sure that it's valid.")
                raise UserAborted
            else:
                n = 0
                while n == 0:
                    print("Invalid input!")
                    print('\nATTENTION: Do you really want to create a new directory in "{0}"? (Y/N)'.format(outputDirectory))
                    userDirChoice = str(input())
                    if userDirChoice == 'y' or userDirChoice == 'Y':
                        n == 1
                        newDir()
                        print("Re-running the program again immediately.")
                        mainfunc()
                    elif userDirChoice == 'n' or userDirChoice == 'N':
                        n == 1
                        print("WARN: Directory creation canceled! Please check your configurations and make sure that it's valid.")
                        raise UserAborted()
                    else:
                        n == 0
        except UserAborted:
            print("\nFATAL: User aborted crucial program routine. Exiting due to insufficient requirements met.")
            sys.exit(2)
    except UserAborted:
        print("\nFATAL: User aborted crucial program routine. Exiting due to insufficient requirements met.")
        sys.exit(2)
    except Exception as errorInfo:
        print("\nFATAL: {0} exception occured. Exiting program. This might be a bug, so please create an issue if you found this.".format(errorInfo.__class__.__name__))
        sys.exit(1)

# execute mainfunc() when the app first starts and then schedule repeat function calls.
mainfunc()
schedule.every(timesec).minutes.do(mainfunc)

while True:
    schedule.run_pending()
    time.sleep(1)
