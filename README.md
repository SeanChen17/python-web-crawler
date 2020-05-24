# python-web-crawler
python web crawler

The repo conatains main.py and 3 more .py files.
Put all the files in the same dir.

The tool recives 3 additional parameters + the url of the vendor web site.
The params are the ouput dir for the downloaded files, the port and ip of the mongodb service.
At the end, a log.txt file is created for firmware files that dont have a downloading url.

Requirement Modules:
1. requests
2. bs4 (BeautifulSoup)

Invoke the tool with the following command:
python3 main.py odir=<path_to_your_output_dir> dbip=<ip_of_mongo_service> dbport=<port_of_mongo_service> website_url

Example:
python3 main.py odir=./file/ dbip=127.0.0.1 dbport=27017 https://www.rockchipfirmware.com/

Notes:
  1. Make sure mongodb service that can handle connections is up and running.
  2. The database name will be VendorDB, and the collection name will be MetaData.
  3. When specifing the vendor website url and the oupout directory, make sure to end with a forward slash ("/"). 
