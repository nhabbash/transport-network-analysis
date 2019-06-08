import urllib.request
from zipfile import ZipFile 

print("Downloading the Milan GTFS Dataset (from 4 March 2019)")
url = "https://transitfeeds.com/p/agenzia-mobilita-ambiente-territorio/341/20190304/download"
filename, _ = urllib.request.urlretrieve(url)

with ZipFile(filename, 'r') as zip:
    print("Extracting files in ./db/dataset")
    zip.extractall(path="./db/dataset")