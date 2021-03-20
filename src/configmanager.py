import json
import os
import sys
import logging

logger = logging.getLogger(__name__)

class LoadConfig:
    def __init__(self):
        try:
            with open("./config.json") as conf_load:
                self.confdict = json.load(conf_load)
            
            self.addr = self.confdict["domainAddress"]
            self.prt = self.confdict["serverPort"]
            self.freq = self.confdict["rateRefresh"]
            self.directory = self.confdict["outputDir"]
            self.query = self.confdict["enableQuery"]
        except PermissionError:
            raise PermissionError
        except FileNotFoundError:
            raise FileNotFoundError
        except Exception as err:
            print("\nFATAL: {0} exception occured. Exiting program. This might be a bug, so please create an issue if you found this.".format(err.__class__.__name__))
            print("Full information available below: \n")
            logger.exception(err)
            sys.exit(1)

class WriteConfig:
    def __init__(self, writeNew, *args) -> None:
        if writeNew is True:
            print("Creating new configuration file...")
            try:
                print("Please enter the Minecraft Server address you will be using.")
                addr = str(input("Address: "))
                print("\nAlright, set {0} as your domain address.".format(addr))
                print("\nNext, please enter the server port.")
                prt = int(input("Port: "))
                print("\nSet {0} as server port.".format(prt))
                enableQueryOption = str(input("\nAlso, does the server support Querying? If you're unsure, just type 'N'. (Y/N) "))
                if enableQueryOption == "y" or enableQueryOption == "Y":
                    print("Enabled querying.")
                    query = 1
                elif enableQueryOption == "n" or enableQueryOption == "N":
                    print("Using alternative 'status' method instead.")
                    query = 0
                else:
                    n = 0
                    while n == 0:
                        print("Invalid option.")
                        enableQueryOption = str(input("\nAlso, does the server support Querying? If you're unsure, just type 'N'. (Y/N) "))
                        if enableQueryOption == "y" or enableQueryOption == "Y":
                            print("Enabled querying.")
                            query = 1
                            n = 1
                        elif enableQueryOption == "n" or enableQueryOption == "N":
                            print("Using alternative 'status' method instead.")
                            query = 0
                            n = 0
                        else:
                            print("Invalid option.")
                            n = 0
                print("\nNext, let's set the requery frequency, in minutes.")
                freq = int(input("Refresh Frequency: "))
                if freq > 1:
                    minstr = "minutes"
                else:
                    minstr = "minute"
    
                print("\nNice, set the app to requery every {0} {1}.".format(freq, minstr))
                print("\nLet's also set the output directory for the response json and js. Please set it the same as your status.html.")
                directory = str(input("Output folder: "))
                print("\nCreating new config file...")

                confdict = {
                    "domainAddress" : addr,
                    "serverPort" : prt,
                    "rateRefresh" : freq,
                    "outputDir" : directory,
                    "enableQuery" : query
                }
                jsonwrite = json.dumps(confdict, indent = 4)
                with open("./config.json", "w") as conf_reload:
                    conf_reload.write(jsonwrite)
            except Exception as err:
                print("\nFATAL: {0} exception occured. Exiting program. This might be a bug, so please create an issue if you found this.".format(err.__class__.__name__))
                print("Full information available below: \n")
                logger.exception(err)
                sys.exit(1)
        else:
            print("Writing into configuration...")

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