import json
import os
import sys
import logging

logger = logging.getLogger(__name__)

class InitConfig:
    def __init__(self) -> None:
        try:
            print("Initializing configuration...")
            with open("./config.json") as conf_load:
                self.confdict = json.load(conf_load)
        
            self.addr = self.confdict["domainAddress"]
            self.prt = self.confdict["serverPort"]
            self.freq = self.confdict["rateRefresh"]
            self.directory = self.confdict["outputDir"]
            self.query = self.confdict["enableQuery"]

            print("Successfully loaded configuration file, config.json.")
        except PermissionError:
            raise PermissionError
        except FileNotFoundError:
            raise FileNotFoundError
        except Exception as err:
            print("\nFATAL: {0} exception occured. Exiting program. This might be a bug, so please create an issue if you found this.".format(err.__class__.__name__))
            print("Full information available below: \n")
            logger.exception(err)
            sys.exit(1)
            

class DirectoryManager:
    def __init__(self, directory):
        self.directory = directory
    
    def createNewDir(new):
        try:
            print("\nCreating directory {0}".format(new.directory))
            os.mkdir(new.directory)
            print("Done!")
            return
        except PermissionError:
            print("\nFATAL: Cannot write to the specified directory due to missing permissions. Please restart the program with Administrator priviledges if the directory you specified is protected.")
            sys.exit(3)
        except Exception as err:
            print("\nFATAL: {0} exception occured. Exiting program. This might be a bug, so please create an issue if you found this.".format(err.__class__.__name__))
            print("Full information available below: \n")
            logger.exception(err)
            sys.exit(1)

class ConfigurationManager:
    def __init__(self, addr=None, prt=None, freq=None, directory=None, query=None):
        try:
            initc = InitConfig()
            if addr is None:
                self.addr = initc.addr
            else:
                self.addr = addr
        
            if prt is None:
                self.prt = initc.prt
            else:
                self.prt = prt
        
            if freq is None:
                self.freq = initc.freq
            else:
                self.freq = freq
        
            if directory is None:
                self.directory = initc.directory
            else:
                self.directory = directory
        
            if query is None:
                self.query = initc.query
            else:
                self.query = query
        except FileNotFoundError:
            print("ERROR: Configuration file not found. Proceeding to recreate file.")
            self.createNewConfiguration()
        except Exception as err:
            print("\nFATAL: {0} exception occured. Exiting program. This might be a bug, so please create an issue if you found this.".format(err.__class__.__name__))
            print("Full information available below: \n")
            logger.exception(err)
            sys.exit(1)

    def writeConfiguration(write, addr, prt, freq, directory, query):
        try:
            print("\nWriting to configuration...")
            confdict = {
                "domainAddress" : addr,
                "serverPort" : prt,
                "rateRefresh" : freq,
                "outputDir" : directory,
                "enableQuery" : query
            }

            jsonwrite = json.dumps(confdict, indent = 4)

            with open("./config.json", "a") as conf_new:
                conf_new.write(jsonwrite)
            
            print("Writing to configuration succeeded!")
        except PermissionError:
            print("\nFATAL: Cannot write to the specified directory due to missing permissions. Please restart the program with Administrator priviledges if the directory you specified is protected.")
            sys.exit(3)
        except Exception as err:
            print("\nFATAL: {0} exception occured. Exiting program. This might be a bug, so please create an issue if you found this.".format(err.__class__.__name__))
            print("Full information available below: \n")
            logger.exception(err)
            sys.exit(1)
    
    def loadConfiguration(load):
        try:
            print("\nLoading configuration...")

            with open("./config.json") as conf_load:
                confdict = json.load(conf_load)

            load.addr = confdict["domainAddress"]
            load.prt = confdict["serverPort"]
            load.freq = confdict["rateRefresh"]
            load.directory = confdict["outputDir"]
            load.query = confdict["enableQuery"]
            
            print("Successfully loaded configuration file, config.json")
        except PermissionError:
            raise PermissionError
        except Exception as err:
            print("\nFATAL: {0} exception occured. Exiting program. This might be a bug, so please create an issue if you found this.".format(err.__class__.__name__))
            print("Full information available below: \n")
            logger.exception(err)
            sys.exit(1)

    def reloadConfiguration(reload, addr, prt, freq, directory, query):
        try:
            print("\nReloading configuration...")
            confdict = {
                "domainAddress" : addr,
                "serverPort" : prt,
                "rateRefresh" : freq,
                "outputDir" : directory,
                "enableQuery" : query
            }

            jsonwrite = json.dumps(confdict, indent = 4)

            with open("./config.json", "r+") as conf_reload:
                conf_reload.write(jsonwrite)
                conffile = json.load(conf_reload)
            
            reload.addr = conffile["domainAddress"]
            reload.prt = conffile["serverPort"]
            reload.freq = conffile["rateRefresh"]
            reload.directory = conffile["outputDir"]
            reload.query = conffile["enableQuery"]
            
            print("Reloading configuration succeeded!")
        except PermissionError:
            print("\nFATAL: Cannot read or write to the specified directory due to missing permissions. Please restart the program with Administrator priviledges if the directory you specified is protected.")
            sys.exit(3)
        except Exception as err:
            print("\nFATAL: {0} exception occured. Exiting program. This might be a bug, so please create an issue if you found this.".format(err.__class__.__name__))
            print("Full information available below: \n")
            logger.exception(err)
            sys.exit(1)
    
    def createNewConfiguration(self):
        try:
            print("Creating new configuration...")
            print("Please enter the Minecraft Server address you will be using.")
            self.addr = str(input("Address: "))
            print("\nAlright, set {0} as your domain address.".format(self.addr))

            print("\nNext, please enter the server port.")
            self.prt = int(input("Port: "))
            print("\nSet {0} as server port.".format(self.prt))

            enableQueryOption = str(input("\nAlso, does the server support Querying? If you're unsure, just type 'N'. (Y/N) "))
            if enableQueryOption == "y" or enableQueryOption == "Y":
                print("Enabled querying.")
                self.query = 1
            elif enableQueryOption == "n" or enableQueryOption == "N":
                print("Using alternative 'status' method instead.")
                self.query = 0
            else:
                n = 0
                while n == 0:
                    print("Invalid option.")
                    enableQueryOption = str(input("\nAlso, does the server support Querying? If you're unsure, just type 'N'. (Y/N) "))
                    if enableQueryOption == "y" or enableQueryOption == "Y":
                        print("Enabled querying.")
                        self.query = 1
                        n = 1
                    elif enableQueryOption == "n" or enableQueryOption == "N":
                        print("Using alternative 'status' method instead.")
                        self.query = 0
                        n = 0
                    else:
                        print("Invalid option.")
                        n = 0

            print("\nNext, let's set the requery frequency, in minutes.")
            self.freq = int(input("Refresh Frequency: "))

            if self.freq > 1:
                minstr = "minutes"
            else:
                minstr = "minute"
    
            print("\nNice, set the app to requery every {0} {1}.".format(self.freq, minstr))

            print("\nLet's also set the output directory for the response json and js. Please set it the same as your status.html.")
            self.directory = str(input("Output folder: "))
            print("\nCreating new config file...")

            self.reloadConfiguration(self.addr, self.prt, self.freq, self.directory, self.query)
        except Exception:
            raise Exception