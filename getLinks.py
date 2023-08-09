import ssl
import argparse
import json
import concurrent.futures
import datetime
import re
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import subprocess
import sys
import os

def getBaseURL(server):
    if server == "nl":
        return "https://www1.pagefreezer.nl"
    elif server == "w1":
        return "https://www1.pagefreezer.com"
    elif server == "w3":
        return "https://www3.pagefreezer.com"
    elif server == "w4":
        return "https://www4.pagefreezer.com"
    else:
        raise NameError('Invalid server')  

def buildURL(server, snapshot):
    return getBaseURL(server) + "/ajax/?command=getSnapshotTree&sid=" + str(snapshot) + "&parent="

def writeResults(links, output_file):
    
    if (output_file):
        fileName = output_file
    else:
        ts = datetime.datetime.now()
        fileName = "scrapped_links_mt_" + ts.strftime('%Y%m%d%H%M%S')
    f = open(fileName, "w")

    for link in links:
        f.write(link)
        if link != links[-1]:
            f.write("\n")    
    
    f.close()

def scrapeLinksLN(url, links, server, snapshot, retryQueue, cookie, filterURL, filterPattern):
    print(".",end='')
    headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 GTB7.1 (.NET CLR 3.5.30729)",
                "Cookie": cookie}
    request = Request(url, headers=headers)
    html = '[]'

    try:    
        urlHandler = urlopen(request, timeout=20)
        html = urlHandler.read().decode("latin_1")

    except UnicodeDecodeError as err:
        print("UnicodeDecodeError: " + str(url) + " - trying a different decoding...")
        try:
            html = urlHandler.read().decode("utf-8")
        except UnicodeDecodeError as err2:
            print("Decoding failed for: " + str(url))

    except URLError as err:
        print("URLError: " + str(url))
        print(err.reason)
        retryQueue.append(url)
    except UnboundLocalError:
        print("Json Error")
        retryQueue.append(url)
    except Timeout:
        print("Timed out: " + str(url))
        retryQueue.append(url)
        

    if (html != '[]'):
        try:
            jsonContent = json.loads(html)
        except json.JSONDecodeError as err:
            print("JSONDecodeError: " + str(url))
    else: 
        return
    
    parentLinks = []
    for key in jsonContent:
        if (key['parent'] == True):
            parentLink = buildURL(server, snapshot) + key['fullName']
            parentLinks.append(parentLink)
        else:
            fullName = key['fullName']
            if (filterURL):
                if (not re.search(filterPattern, fullName)):
                    links.append(fullName)
                else:
                    continue
            elif (not filterURL):
                links.append(fullName)
    
    if not(parentLinks):
        return

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for url in parentLinks:
            futures.append(executor.submit(scrapeLinksLN, url=url, links=links, server=server, snapshot=snapshot, retryQueue=retryQueue, cookie=cookie, filterURL=filterURL, filterPattern=filterPattern))
        for future in concurrent.futures.as_completed(futures):
            print(".", end='')

def scrapeLinksL1(url, links, server, snapshot, domain, retryQueue, cookie, filterURL, filterPattern):    
    print(url)
    headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 GTB7.1 (.NET CLR 3.5.30729)",
                "Cookie": cookie}

    request = Request(url, headers=headers)
    urlHandler = urlopen(request,timeout=20)
    html = urlHandler.read().decode("latin_1")

    if (html == '[]'):
        links.append(domain)
        return
    elif (html == '{"message":"error","code":401}'):
        print("Unauthorized: 401, you need to be logged to retrieve results")
        exit() 

    try:
        jsonContent = json.loads(html)
    except json.JSONDecodeError as err:
        print("Couldn't find snapshot " + str(snapshot) + " on server " + server)
        exit()

    parentLinks = []

    for key in jsonContent:
        if (key['parent'] == True):
            parentLink = buildURL(server, snapshot) + key['fullName']
            parentLinks.append(parentLink)
        else:
            fullName = key['fullName']
            if (filterURL):
                if (not re.search(filterPattern, fullName)):
                    links.append(fullName)
                else:
                    continue
            elif (not filterURL):
                links.append(fullName)

    if not(parentLinks):
        return

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for url in parentLinks:
            futures.append(executor.submit(scrapeLinksLN, url=url, links=links, server=server, snapshot=snapshot, retryQueue=retryQueue, cookie=cookie, filterURL=filterURL, filterPattern=filterPattern))
        for future in concurrent.futures.as_completed(futures):
            print(".")

def retryFailedURLs(retryQueue, links, server, snapshot, cookie, filterURL, filterPattern):
    newQueue = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for url in retryQueue:
            futures.append(executor.submit(scrapeRetryQueue, url=url, links=links, server=server, snapshot=snapshot, retryQueue=retryQueue, newQueue=newQueue, cookie=cookie, filterURL=filterURL, filterPattern=filterPattern))
        for future in concurrent.futures.as_completed(futures):
            print(".")

def scrapeRetryQueue(url, links, server, snapshot, retryQueue, newQueue, cookie, filterURL, filterPattern):

    headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 GTB7.1 (.NET CLR 3.5.30729)",
                "Cookie": cookie}
    request = Request(url, headers=headers)
    html = '[]'

    try:    
        urlHandler = urlopen(request, timeout=20)
        html = urlHandler.read().decode("latin_1")

    except UnicodeDecodeError as err:
        print("UnicodeDecodeError: " + str(url) + " - trying a different decoding...")
        try:
            html = urlHandler.read().decode("utf-8")
        except UnicodeDecodeError as err2:
            print("Decoding failed for: " + str(url))
    except URLError as err:
        print("URLError: " + str(url))
        print(err.reason)
        newQueue.append(url)
    except UnboundLocalError:
        print("Json Error")
        newQueue.append(url)
    except Timeout:
        print("Timed out: " + str(url))
        newQueue.append(url)

    if (html != '[]'):
        try:
            jsonContent = json.loads(html)
        except json.JSONDecodeError as err:
            print("JSONDecodeError: " + str(url))
    else:
        return

    parentLinks = []
    for key in jsonContent:
        if (key['parent'] == True):
            parentLink = buildURL(server, snapshot) + key['fullName']
            parentLinks.append(parentLink)
        else:
            links.append(key['fullName'])
    
    if not(parentLinks):
        return

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for url in parentLinks:
            futures.append(executor.submit(scrapeRetryQueue, url=url, links=links, server=server, snapshot=snapshot, retryQueue=retryQueue, newQueue=newQueue))
        for future in concurrent.futures.as_completed(futures):
            print(".", end='')

    print("Retry finished. Retrieving remaining URLs")

    retryQueue.clear()
    for elem in newQueue:
        retryQueue.append(elem)

def main():
    ssl._create_default_https_context = ssl._create_unverified_context

    parser = argparse.ArgumentParser(
        description='Retrieve all links for a given snapshot ID',
        formatter_class=argparse.RawDescriptionHelpFormatter 
    )
    parser.add_argument('-s','--snapshot', help='snapshotId')
    parser.add_argument('-w', '--server', help='Server that hosts the snapshot [nl, w1, w3, w4]')
    parser.add_argument('-d', '--domain', help='Domain to retrieve links', default="")
    parser.add_argument('-c', '--cookie', help='JSESSIONID from Browser', default="")
    parser.add_argument('-o', '--output', help='Output file name', default="")
    parser.add_argument('-f', '--filter', help='Filter for billable content (PDFs, videos, HTML pages)', default=False)
    
    args = parser.parse_args()
    snapshot = int(args.snapshot)
    server = args.server
    domain = args.domain
    cookie = "JSESSIONID="+args.cookie
    output_file = args.output
    filterURL = bool(args.filter)

    filterPattern = '.*(\.png|\.css|\/css\?|\/css2\?|\.js|\.jpg|\.jpeg|\.mp3|\.ico|\.epub|\.mobi|\.svg|\.gif|\.woff|\.webp|\.txt|\.ttf|\.eot|\.mhtml|\.xml|\.zip|\.docx|\.xlsx|\.csv|frame\-[0-9A-Z]+|recaptcha|googleads|data:image).*'
    links = []
    retryQueue = []

    default_python_command = sys.executable
    python_filename = os.path.basename(default_python_command)

    url = buildURL(server, snapshot) + str(domain)    
    scrapeLinksL1(url, links, server, snapshot, domain, retryQueue, cookie, filterURL, filterPattern)

    links = list(dict.fromkeys(links))
    retryQueue = list(dict.fromkeys(retryQueue))

    print("\nSuccesfull Links: " + str(len(links)))
    command = f"{python_filename} results.py {str(len(links))}"
    try:
        subprocess.run(command, shell=True, check=True)
        print("Script executed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    print("Failed Links:" + str(len(retryQueue)))

    if (retryQueue):
        retry = 1
        print("Attempting a new fetch on failed URLs...")
    
        while ((retryQueue) and retry < 3):
            print("Retry " + str(retry))
            retryFailedURLs(retryQueue, links, server, snapshot, cookie, filterURL, filterPattern)

            links = list(dict.fromkeys(links))
            retryQueue = list(dict.fromkeys(retryQueue))

            print("\nSuccesfull Links: " + str(len(links)))
            print("Failed Links:" + str(len(retryQueue)))
            retry += 1

    links = list(dict.fromkeys(links))
    writeResults(links, output_file)

if __name__ == '__main__':
    main()