import sys #to read the command line arg
import json
import urllib.request

def fetch(url:str,outpath:str):
    with urllib.request.urlopen(url) as response:
        data=json.loads(response.read())
    with open(outpath, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved schema from {url} -> {outpath}")

if __name__=="__main__":
    if len(sys.argv) != 3:
        print("Usage: python fetch_schema.py <url> <out_path>")
        sys.exit(1)
    fetch(sys.argv[1], sys.argv[2])


