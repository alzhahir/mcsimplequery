import json
import os
import sys
import logging

logger = logging.getLogger(__name__)

class InitConfig:
    def __init__(self) -> None:
        try:
            with open("./config.json") as conf_load:
                self.confdict = json.load(conf_load)
        
            self.addr = self.confdict["domainAddress"]
            self.prt = self.confdict["serverPort"]
            self.freq = self.confdict["rateRefresh"]
            self.directory = self.confdict["outputDir"]
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
    def __init__(self, addr, prt, freq, directory):
        self.addr = addr
        self.prt = prt
        self.freq = freq
        self.directory = directory

    def writeConfiguration(write):
        try:
            print("\nWriting to configuration...")
            write.confdict = {
                "domainAddress" : write.addr,
                "serverPort" : write.prt,
                "rateRefresh" : write.freq,
                "outputDir" : write.directory
            }

            jsonwrite = json.dumps(write.confdict, indent = 4)

            with open("./config.json", "w") as conf_new:
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
                load.confdict = json.load(conf_load)

            load.addr = load.confdict["domainAddress"]
            load.prt = load.confdict["serverPort"]
            load.freq = load.confdict["rateRefresh"]
            load.directory = load.confdict["outputDir"]
            
            print("Successfully loaded configuration file, config.json")
        except PermissionError:
            raise PermissionError
        except Exception as err:
            print("\nFATAL: {0} exception occured. Exiting program. This might be a bug, so please create an issue if you found this.".format(err.__class__.__name__))
            print("Full information available below: \n")
            logger.exception(err)
            sys.exit(1)

    def reloadConfiguration(reload):
        try:
            print("\nReloading configuration...")
            reload.confdict = {
                "domainAddress" : reload.addr,
                "serverPort" : reload.prt,
                "rateRefresh" : reload.freq,
                "outputDir" : reload.directory
            }

            jsonwrite = json.dumps(reload.confdict, indent = 4)

            with open("./config.json", "w") as conf_reload:
                conf_reload.write(jsonwrite)
                reload.conffile = json.load(conf_reload)
            
            reload.addr = reload.conffile["domainAddress"]
            reload.prt = reload.conffile["serverPort"]
            reload.freq = reload.conffile["rateRefresh"]
            reload.directory = reload.conffile["outputDir"]
            
            print("Reloading configuration succeeded!")
        except PermissionError:
            print("\nFATAL: Cannot read or write to the specified directory due to missing permissions. Please restart the program with Administrator priviledges if the directory you specified is protected.")
            sys.exit(3)
        except Exception as err:
            print("\nFATAL: {0} exception occured. Exiting program. This might be a bug, so please create an issue if you found this.".format(err.__class__.__name__))
            print("Full information available below: \n")
            logger.exception(err)
            sys.exit(1)
