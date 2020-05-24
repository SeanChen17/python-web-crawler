from bs4 import BeautifulSoup
from Log import Log
import requests 
import re

class VendorManager():
    
    def __init__(self,vendor_url,odir):
        self.vendor_url = vendor_url
        self.odir = odir
        self.log_manager = Log()  

    #input: None
    #output: the first downloading url that located in the home page 
    def get_download_page_url(self):
        home_page = self.get_page(self.vendor_url)
        soup = BeautifulSoup(home_page,"html.parser")
        a = soup.find("a",title="Download") #searching for the url by the <a> tag which titled "Download"
        dowload_url = a["href"] #getting the ref of the <a> tag
        soup.decompose()
        return dowload_url

    #input: the page containing the downloading url of the firmware file
    #output: the downloading url of the firmware file
    def get_download_file_url(self,firmware_page_url):
        print("getting download url from {} ---> ".format(firmware_page_url),end="")
        firmware_page_content = self.get_page(self.vendor_url+firmware_page_url)
        soup = BeautifulSoup(firmware_page_content,"html.parser")
        search_by = self.vendor_url.split("https://")[1]
        #searching by the <a> tag which contains the vendor url in the href
        a = soup.find("a",href=lambda ref: ref and search_by in ref)
        soup.decompose()
        if a is not None: #checking for valid results
            ref = a["href"]
            print(ref)
            return ref
        else: #the url doesnt exits
            self.log_manager.log(firmware_page_url + "  --> No URL found")
            print("No URL found")
            return "No URL found"

    #input: url
    #output: the contents of that page
    #the function return the content of an html response
    def get_page(self,page_url):
        req = requests.get(url=page_url) #sending a GET request
        #making sure the 200 ok reponse is the response we got, else throwing an exception
        if req.status_code != 200:
            raise Exception("Status Code Exception: response isnt 200 ok, instead recieved {}".format(req.status_code))
        return req.content

    
    #input: the current downaloaing page
    #output: url for the next downloading page
    #the function gets the current download page and returns the url of the next downloading pag
    def get_next_download_page(self,curr_download_page):
        download_page_content = self.get_page(self.vendor_url+curr_download_page)
        soup = BeautifulSoup(download_page_content,"html.parser")
        #searching by <a> tag which titled with: "Go to next page"
        a = soup.find("a",title="Go to next page")
        soup.decompose()
        return a

    """
        input: the first downloading page (the one that was found in the home page)
        output: list of lists that contains the metadata for all the firmwares in that downloading url 

        this function does the scraping action.
        first, it gets all the files in the current downloading page
        then it searches for the next downloading page
        if there isnt onther downloading page, the function ends
        this function is a generator for memory efficient
    """
    def scrape(self,curr_download_page):
        print("starting to crawl...")
        while True:
            #getting the next doenload page url
            a = self.get_next_download_page(curr_download_page)
            
            #making sure there is next url
            if a is None: # if yes, exiting from the function
                break
            else: # if not, calling the function which get all the files
                yield self.get_nodes_in_page(self.vendor_url+curr_download_page)
                curr_download_page = a["href"]
        print("\nfinished crawling...")

    """
        input: the url of a downloading page
        output: list of lists

        this function gets all the files in a specific downloading page,
        the function returns list that contain list.
        the inner list contains the metadata of the files
    """
    def get_nodes_in_page(self,page_url):
        #getting all the metadata but the name and the download url
        class_names = ["views-field views-field-field-brand",
        "views-field views-field-field-model",
        "views-field views-field-field-stock-rom",
        "views-field views-field-field-android-version2",
        "views-field views-field-field-firmware-author"
        ]

        data = list() # [[list of brands],[list of android versions],...]
        firmware_metadata = list() # [[brnad,model,stock rom,android version,author,name,url]...]
        firmware_name = list() # list of firmware name
        firmware_download_page = list() # list of download page of the firmware

        download_page_content = self.get_page(page_url)
        soup = BeautifulSoup(download_page_content,"html.parser")
        
        for class_name in class_names:
            #getting all rows in the table of specific metadata 
            result = soup.find_all("td",class_=class_name)
            #the content of the row is in a list with len = 1 and contains other chars such like:
            #['\r\n ...data.. \r\n'] -> so everything which isnt letter/number is sptripped
            data.append(list( ''.join(re.findall("[a-zA-Z0-9]+",res.contents[0])) for res in result ))

        #getting list of the rows that containg the name of the firmware and the url download
        result = soup.find_all("td",class_="views-field views-field-title")
        #running on different loop for the name and downloading url
        for res in result:
            #getting all the downloading url's for all firmware files
            firmware_download_page.append(self.get_download_file_url(res.a["href"].replace("\\","/")))
            #getting all the names of all the firmware files
            firmware_name.append(res.a.contents[0])

        #appending the lists
        data.append(firmware_name)
        data.append(firmware_download_page)
        
        #packing all the data into list that contains the metadata
        #the list will contains: [brand_list[i],android_version[i],model[i]...]
        #then appending the list to the firmware_metadata list
        for i in range(len(data[0])):
            firmware_metadata.append(list( lst[i] for lst in data ))
                
        soup.decompose()
        return firmware_metadata

    # input: the download url for the firmrare
    # output: None
    # the function downloads the file and saves it by its name
    def download_file(self,file_name,file_url):
        content = self.get_page(file_url)
        with open(self.odir+file_name,"wb") as wfile:
            wfile.write(content)

