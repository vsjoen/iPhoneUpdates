import requests
import sys
import fileinput
import os.path
import glob
import time
from colorama import init, Fore, Back, Style

init()
aList = []
models = [
            'iphone1,1',   # iPhone 2G
            'iphone2,1',   # iPhone 3G
            'iphone3,1',   # iPhone 4
            'iphone4,1',   # iPhone 4s
            'iphone5,1',   # iPhone 5
            'iphone5,3',   # iPhone 5c
            'iphone6,1',   # iPhone 5s
            'iphone7,1',   # iPhone 6+
            'iphone7,2',   # iPhone 6
            'iphone8,1',   # iPhone 6s
            'iphone8,2',   # iPhone 6s+
            'iPhone8,4',   # iPhone SE
            'iphone9,1',   # iPhone 7
            'iphone9,2',   # iPhone 7+
            'iphone10,4',  # iPhone 8
            'iphone10,5',  # iPhone 8+
            'iphone10,6'   # iPhone X
        ]


# Download latest firmware
def downloadFile():
    with open(file_name, "wb") as f:
        print "Downloading %s" % file_name
        response = requests.get(link, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None:  # No content length header
            f.write(response.content)

        else:
            dl = 0
            total_length = int(total_length)

        for data in response.iter_content(chunk_size=4096):
            dl += len(data)
            f.write(data)
            done = int(50 * dl / total_length)
            sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)))
            sys.stdout.flush()

# For every model, check for latest firmware
for elem in reversed(models):
    url = 'http://api.ipsw.me/v2.1/' + elem + '/latest/url'
    sizeURL = 'http://api.ipsw.me/v2.1/' + elem + '/latest/filesize'
    r = requests.get(url)
    sizeR = requests.get(sizeURL)
    file_name = r.text.split('/')[-1]
    file_size = sizeR.text
    link = r.text
    delete_line = ''
    aList.append(file_name)

    # If no firmware exists for model, download new
    if (os.path.isfile(file_name) is False):
        downloadFile()

    elif (file_size != str(os.stat(file_name).st_size)):
        downloadFile()

    # Else, all is well with the cosmos
    else:
        print (Fore.GREEN + Style.BRIGHT + file_name + " already exists.")

# Filelist is the list of files in folder.
# Newlist is a list of the newest updates.
# Havelist is a list of files that are downloaded.
filelist = glob.glob("*.ipsw")
havelist = set(aList) & set(filelist)

# Delete all files not in havelist
for f in filelist:
    if f not in havelist:
        print (Fore.RED + Style.BRIGHT + f + " has been deleted")
        os.remove(f)

print (Style.RESET_ALL + "\n" + "Closing this window in 10 seconds.")
time.sleep(10)
