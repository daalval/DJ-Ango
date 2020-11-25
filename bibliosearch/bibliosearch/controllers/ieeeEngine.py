import json
import requests

def fromJson(url, file):
    data = requests.get(url, verify=False).json()

    with open(file, 'w') as outfile:
        json.dump(data, outfile)

def main():
    fromJson("https://ieeexploreapi.ieee.org/api/v1/search/articles?parameter&apikey=efv84mzqq6ydx4dbd59jhdcn&content_type=Books", 'static/ieeeXplore.json')

if __name__ == "__main__":
    main()