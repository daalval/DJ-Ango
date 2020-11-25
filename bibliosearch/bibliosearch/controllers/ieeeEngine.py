import json
import requests

def fromJsonBooks(url, file):
    data = requests.get(url, verify=False).json()

    with open(file, 'w') as outfile:
        json.dump(data, outfile)

def fromJsonConferences(url, file):
    data = requests.get(url, verify=False).json()

    with open(file, 'w') as outfile:
        json.dump(data, outfile)

def main():
    fromJsonBooks("https://ieeexploreapi.ieee.org/api/v1/search/articles?parameter&apikey=efv84mzqq6ydx4dbd59jhdcn&content_type=Books", 'static/ieeeXploreBooks.json')
    fromJsonConferences("https://ieeexploreapi.ieee.org/api/v1/search/articles?parameter&apikey=efv84mzqq6ydx4dbd59jhdcn&content_type=Conferences", 'static/ieeeXploreConferences.json')

if __name__ == "__main__":
    main()