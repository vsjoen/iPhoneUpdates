import requests
import sys
import fileinput
import os.path
import glob
import time
import re

aList = []
models = []

file = open("models", "a+")
for line in file:
    models.append(line.splitlines()[0].split(","))


# Find new GSM iPhone models and save to file
def findGSM(a, b):
    print "\n+------------------------------------------------------+"
    print "|                                                      |"
    print "|    Checking for new iPhone models, please wait...    |"
    print "|                                                      |"
    print "+------------------------------------------------------+\n"

    kill = 0
    i = int(a)
    start = int(b)+1
    while kill < 10:
        for j in range(start, 11):

            r = requests.get(
                "http://api.ipsw.me/v2.1/iphone" +
                str(i) + "," + str(j) + "/latest/url"
                )

            rN = requests.get(
                "http://api.ipsw.me/v2.1/iphone" +
                str(i) + "," + str(j) + "/latest/name"
                )

            Global = re.search("Global", rN.text)
            CDMA = re.search("CDMA", rN.text)

            if (str(r) == "<Response [200]>") and not Global and not CDMA:
                print "  Added new model: " + rN.text
                file.write(str(i) + "," + str(j) + "\n")
                kill = 0

            else:
                kill += 1

            start = 1

        i += 1

    file.close()
    print "\n  No more models to add"


# For every model, check for latest firmware
def check():
    print "\n+------------------------------------------------------+"
    print "|                                                      |"
    print "|        Downloading new firmware, please wait...      |"
    print "|                                                      |"
    print "+------------------------------------------------------+\n"

    file = open("models", "r")
    for line in file:
        mod = line.splitlines()[0]
        url = 'http://api.ipsw.me/v2.1/iphone' + mod + '/latest/url'
        sizeURL = 'http://api.ipsw.me/v2.1/iphone' + mod + '/latest/filesize'
        r = requests.get(url)
        sizeR = requests.get(sizeURL)
        file_name = r.text.split('/')[-1]
        file_size = sizeR.text
        link = r.text
        delete_line = ''
        aList.append(file_name)

        # If no firmware exists for model, download new
        if (os.path.isfile(file_name) is False):
            downloadFile(link, file_name)

        elif (file_size != str(os.stat(file_name).st_size)):
            downloadFile(link, file_name)

    # Filelist is the list of files in folder.
    # Newlist is a list of the newest updates.
    # Havelist is a list of files that are downloaded.
    filelist = glob.glob("*.ipsw")
    havelist = set(aList) & set(filelist)

    print "\n  All firmware files are up to date"
    deleteOld(filelist, havelist)


# Download latest firmware
def downloadFile(link, filename):
    with open(filename, "wb") as f:
        print "  Downloading %s" % filename
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
            sys.stdout.write("\r  [%s%s]" % ('=' * done, ' ' * (50-done)))
            sys.stdout.flush()

    print "\n"


# Delete all files not in havelist
def deleteOld(filelist, havelist):
    print "\n+------------------------------------------------------+"
    print "|                                                      |"
    print "|              Deleting old firmware files             |"
    print "|                                                      |"
    print "+------------------------------------------------------+\n"

    for f in filelist:
        if f not in havelist:
            print ("  " + f + " deleted")
            os.remove(f)

    print "\n  Old firmware files deleted\n"


if not models:
    findGSM(3, 0)

else:
    findGSM(*models[-1])

check()
time.sleep(10)
