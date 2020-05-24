from VendorManager import VendorManager
from DataBaseManager import DBManager
import sys, threading

EXIT_FALIURE_CODE = 1
SECOND_ARGUMENT = 1
AMOUNT_OF_ARGS = 5

VENDOR_URL_INDEX = -1
LAST_ARGUMENT = -1
FIRMWARE_NAME_INDEX = -2
FIRMWARE_DOWNLOAD_INDEX = -1

"""
this function gets list of arguments
it returns the vendor url, the ip and port of the mongodb 
"""
def read_args(args):
    arg_info = {}
    #running on all the args but the first (name of the program) and last (the vendor url) args
    for arg in args[SECOND_ARGUMENT:LAST_ARGUMENT]:
        #the args expected to the following format: dbip:127.0.0.1
        key,value = arg.split("=")
        arg_info[key] = value

    return args[VENDOR_URL_INDEX],arg_info["odir"],(arg_info["dbip"],int(arg_info["dbport"]))

def main(vendor_url,odir,db_info):
    vendor_manager = VendorManager(vendor_url,odir)
    db_manager = DBManager(db_info)
    download_page_url = vendor_manager.get_download_page_url()

    #vendor_manager.scrape is a generator function for memory efficient
    for data in vendor_manager.scrape(download_page_url):
        #data is list the contains other lists in it
        for firmware_metadata in data:
            #firmware_metadata is list containing the metadata of the firmware
            #such as: model, name, brand, android version, author and download url 
            db_manager.insert(firmware_metadata)

            """
                its an arbitrary condition
                the download time can reach up to minutes, due to big file sizes
                to speed up the process im using threads 
                to download the file while more files are searched
                if you want to create threads for all the files,
                delete the condition statement
            """
            if firmware_metadata[FIRMWARE_NAME_INDEX] == "CHERRY_M-1038_ROM_FINLESSV1.8":
                download_thread = threading.Thread(target=vendor_manager.download_file,
                args=(firmware_metadata[FIRMWARE_NAME_INDEX],
                    firmware_metadata[FIRMWARE_DOWNLOAD_INDEX]))
                
                download_thread.start()

if __name__ == "__main__":

    #making sure the program wont crash
    try:
        #getting list of all the args
        args = sys.argv
        if len(args) != AMOUNT_OF_ARGS:
            print("see readme file for usage")
            sys.exit(EXIT_FALIURE_CODE)
        
        vendor_url,odir,db_info = read_args(args)
        main(vendor_url,odir,db_info)
    
    except Exception as e:
        print("error:{}".format(e))
