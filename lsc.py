import os
import json
import requests
import pyperclip
import vt
import time
from win11toast import toast
from dotenv import load_dotenv

load_dotenv()
APIKEY = os.getenv("VT_API_KEY")
if not APIKEY:
    print("Error: VT_API_KEY environment variable is not set ")
    exit()

json_log_path = f"{os.path.expanduser("~")}\\AppData\\Local\\lsclogs.json"

def clipBoard():
    try:
        new = pyperclip.waitForNewPaste()
        return new
    except pyperclip.PyperclipException as e:
        return ""

def  urlCheck(new):
    links = []
    links_id = []
    for url in new.split():
        if "." in url:
            links += [url]
            try:
                url_id = vt.url_id(url)
                links_id += [url_id] 
            except vt.error.APIError as e:
                return [], []
    return links, links_id

def urlSubmit(links):
    ids = []
    for q in links:
        url = "https://www.virustotal.com/api/v3/urls"
        headers = {"accept": "application/json",
                   "X-Apikey": APIKEY}
        try:
            response = requests.post(url, headers=headers, data={'url': q})
            ids += [response.json()]
        except requests.exceptions.RequestException as e:
            return []
    return ids

def urlReport(links_id):
    time.sleep(2)
    data = []
    for w in links_id:
        url = f"https://www.virustotal.com/api/v3/urls/{w}"
        headers = {"accept": "application/json",
                   "X-Apikey": APIKEY}
        try:
            response = requests.get(url, headers=headers)
            data += [response.json()]
        except requests.exceptions.RequestException as e:
            return []
    return data

def stats(data):
    urlStats = []
    for e in data:
        if "data" in e.keys():
            now = time.ctime(time.time())
            url = e["data"]["attributes"]["url"]
            mal = e["data"]["attributes"]["last_analysis_stats"]["malicious"]
            sus = e["data"]["attributes"]["last_analysis_stats"]["suspicious"]
            urlStats += [now, url, mal, sus]
        else:
            return []
    return urlStats

def output(urlStats):
    if len(urlStats) < 4:
        return 0
    elif len(urlStats) == 4:
        logstats = {
            "Date and Time": urlStats[0],
            "url": urlStats[1],
            "malicious": urlStats[2],
            "suspicious": urlStats[3]
        }
        with open(json_log_path, "a") as file:
            fileSize = os.path.getsize(json_log_path)
            if fileSize == 0:
                file.write("[")
                json.dump(logstats, file)
                file.write("]")
            else:
                file_size = os.fstat(file.fileno()).st_size
                os.ftruncate(file.fileno(), file_size - 1)
                file.write(",\n")
                json.dump(logstats, file)
                file.write("]")
        if urlStats[2] == 0:
            toast("Safe link", buttons=[{"activationType": "protocol", "arguments": urlStats[1], "content": "Click to open URL"}, "Dismiss"])
        elif urlStats[2] > 0 or urlStats[3] > 0:
            toast("Malicious link", button="Dismiss")
    elif len(urlStats) > 4:
        while len(urlStats) > 3:
            logstats = {
                "Date and Time": urlStats[0],
                "url": urlStats[1],
                "malicious": urlStats[2],
                "suspicious": urlStats[3]
            }
            with open(json_log_path, "a") as file:
                fileSize = os.path.getsize(json_log_path)
                if fileSize == 0:
                    file.write("[")
                    json.dump(logstats, file)
                    file.write("]")
                else:
                    file_size = os.fstat(file.fileno()).st_size
                    os.ftruncate(file.fileno(), file_size - 1)
                    file.write(",\n")
                    json.dump(logstats, file)
                    file.write("]") 
            if urlStats[2] == 0:
                toast("Safe link", buttons=[{"activationType": "protocol", "arguments": urlStats[1], "content": "Click to open URL"}, "Dismiss"])
            elif urlStats[2] > 0 or urlStats[3] > 0:
                toast("Malicious link", button="Dismiss")
            del urlStats[0], urlStats[0], urlStats[0], urlStats[0]

while True:
    w = clipBoard()
    if w:
        x, y = urlCheck(w)
        if x and y:
            urlSubmit(x)
            z = stats(urlReport(y))
            output(z)