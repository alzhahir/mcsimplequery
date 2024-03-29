import logging
import sys
import json
from socket import gaierror, timeout
import schedule
import time
from mcstatus import MinecraftServer
from configmanager import InitConfig, ConfigurationManager, DirectoryManager

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Custom defined exceptions
class UserAborted(Exception):
    """User aborted crucial program process."""
    pass

class InvalidConfiguration(Exception):
    """Invalid configuration found."""
    pass

# print welcome message
print("Welcome to alzhahir's simple server status query application.\n")

# Load config.json
try:
    print("Loading configuration...")
    config = InitConfig()
    
    print("Successfully loaded configuration file, config.json")
except FileNotFoundError:
    print("ERROR: Cannot find and load config.json in program directory! Did you delete it?")

    print("\nInitializing...")

    print("Please enter the Minecraft Server address you will be using.")
    webAddress = str(input("Address: "))
    print("\nAlright, set {0} as your domain address.".format(webAddress))

    print("\nNext, please enter the server port.")
    srvport = int(input("Port: "))
    print("\nSet {0} as server port.".format(srvport))

    enableQueryOption = str(input("\nAlso, does the server support Querying? If you're unsure, just type 'N'. (Y/N) "))
    if enableQueryOption == "y" or enableQueryOption == "Y":
        print("Enabled querying.")
        enableQuery = 1
    elif enableQueryOption == "n" or enableQueryOption == "N":
        print("Using alternative 'status' method instead.")
        enableQuery = 0
    else:
        n = 0
        while n == 0:
            print("Invalid option.")
            enableQueryOption = str(input("\nAlso, does the server support Querying? If you're unsure, just type 'N'. (Y/N) "))
            if enableQueryOption == "y" or enableQueryOption == "Y":
                print("Enabled querying.")
                enableQuery = 1
                n = 1
            elif enableQueryOption == "n" or enableQueryOption == "N":
                print("Using alternative 'status' method instead.")
                enableQuery = 0
                n = 1
            else:
                print("Invalid option.")
                n = 0

    print("\nNext, let's set the requery frequency, in minutes.")
    refreshfreq = int(input("Refresh Frequency: "))

    if refreshfreq > 1:
        minstr = "minutes"
    elif refreshfreq < 1:
        print("Invalid frequency")
        n = 0
        while n == 0:
            print("\nPlease enter a valid frequency.")
            refreshfreq = int(input("Refresh Frequency: "))
            if refreshfreq < 1:
                print("Invalid frequency")
                n = 0
            elif refreshfreq > 1:
                minstr = "minutes"
                n = 1
            else:
                minstr = "minute"
                n = 1
    else:
        minstr = "minute"
    
    print("\nNice, set the app to requery every {0} {1}.".format(refreshfreq, minstr))

    print("\nLet's also set the output directory for the response json and js. Please set it the same as your status.html.")
    writedir = str(input("Output folder: "))
    print("\nCreating new config file...")

    config = ConfigurationManager(webAddress, srvport, refreshfreq, writedir, enableQuery)

    config.writeConfiguration()
    config.loadConfiguration()
except PermissionError:
    print("FATAL: Cannot read the specified directory due to missing permissions. Please restart the program with Administrator priviledges if the directory you specified is protected.")
    sys.exit(3)
except Exception as errorInfo:
    print("\nFATAL: {0} exception occured. Exiting program. This might be a bug, so please create an issue if you found this.".format(errorInfo.__class__.__name__))
    print("More information available below: \n")
    logger.exception(errorInfo)
    sys.exit(1)

# assign dict objects into variables
timesec = config.freq
domainSite = config.addr
outputDirectory = config.directory
port = config.prt
isQueryEnabled = config.query

# reassign minute string values since it could be changed directly
if timesec > 1:
    minstr = "minutes"
else:
    minstr = "minute"

print("\nConfiguration set successfully!")

print("\nStarting service...")
print("The service will refresh every {0} {1}.".format(timesec, minstr))

print("\nInitializing first query...")

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
            outputfile.write(textjs.format(isOnline, minstr, timesec))
        
        print("Done. Rechecking in {0} {1}.\n".format(timesec, minstr))
    except Exception as errorInfo:
        print("\nFATAL: {0} exception occured. Exiting program. This might be a bug, so please create an issue if you found this.".format(errorInfo.__class__.__name__))
        print("More information available below: \n")
        logger.exception(errorInfo)
        sys.exit(1)

# main
def main():
    try:
        print("\nLooking up {0} on port {1}...".format(domainSite, port))
        server = MinecraftServer(domainSite, port)

        if isQueryEnabled == 1:
            query = server.query()
            status = server.status()
            onlinePlayers = query.players.online
            playerList = query.players.names
            pingLatency = status.latency
        elif isQueryEnabled == 0:
            status = server.status()
            onlinePlayers = status.players.online
            playerList = "Not available since Query is not enabled."
            pingLatency = status.latency
        else:
            print('ERROR: Invalid option "{0}" found in "enableQuery" option in config.json.'.format(isQueryEnabled))
            raise InvalidConfiguration
        
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
            outputfile.write(textjs.format(isOnline, playerstr, minstr, onlinePlayers, playerList, pingLatency, timesec))

        print("Done. Refresh will occur in {0} {1}.\n".format(timesec, minstr))
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
        print('\nERROR: The specified directory "{0}" cannot be located. Proceeding to create a new directory in the defined location.'.format(outputDirectory))
        userDirChoice = str(input('\nATTENTION: Do you really want to create a new directory in "{0}"? (Y/N) '.format(outputDirectory)))
        try:
            if userDirChoice == 'y' or userDirChoice == 'Y':
                newDir = DirectoryManager(outputDirectory)
                newDir.createNewDir()
                print("Re-running the program again immediately.")
                main()
            elif userDirChoice == 'n' or userDirChoice == 'N':
                print("WARN: Directory creation canceled! Please check your configurations and make sure that it's valid.")
                raise UserAborted
            else:
                n = 0
                while n == 0:
                    print("Invalid input!")
                    userDirChoice = str(input('\nATTENTION: Do you really want to create a new directory in "{0}"? (Y/N) '.format(outputDirectory)))
                    if userDirChoice == 'y' or userDirChoice == 'Y':
                        n = 1
                        newDir = DirectoryManager(outputDirectory)
                        newDir.createNewDir()
                        print("Re-running the program again immediately.")
                        main()
                    elif userDirChoice == 'n' or userDirChoice == 'N':
                        n = 1
                        print("WARN: Directory creation canceled! Please check your configurations and make sure that it's valid.")
                        raise UserAborted
                    else:
                        n = 0
        except UserAborted:
            raise UserAborted
    except UserAborted:
        print("\nFATAL: User aborted crucial program routine. Exiting due to insufficient requirements met.")
        sys.exit(2)
    except InvalidConfiguration:
        print("\nFATAL: Invalid configuration.")
        sys.exit(3)
    except Exception as errorInfo:
        print("\nFATAL: {0} exception occured. Exiting program. This might be a bug, so please create an issue if you found this.".format(errorInfo.__class__.__name__))
        print("More information available below: \n")
        logger.exception(errorInfo)
        sys.exit(1)

# execute mainfunc() when the app first starts and then schedule repeat function calls.
main()
schedule.every(timesec).minutes.do(main)

while True:
    schedule.run_pending()
    time.sleep(1)
