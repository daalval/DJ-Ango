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

def fromJsonJournals(url, file):
    data = requests.get(url, verify=False).json()

    with open(file, 'w') as outfile:
        json.dump(data, outfile)

def main():
    fromJsonBooks("https://ieeexploreapi.ieee.org/api/v1/search/articles?parameter&apikey=efv84mzqq6ydx4dbd59jhdcn&content_type=Books&max_records=200", 'static/ieeeXploreBooks.json')
    fromJsonConferences("https://ieeexploreapi.ieee.org/api/v1/search/articles?parameter&apikey=efv84mzqq6ydx4dbd59jhdcn&content_type=Conferences&max_records=200", 'static/ieeeXploreConferences.json')
    fromJsonJournals("https://ieeexploreapi.ieee.org/api/v1/search/articles?parameter&apikey=efv84mzqq6ydx4dbd59jhdcn&content_type=Journals&max_records=200", 'static/ieeeXploreJournals.json')

if __name__ == "__main__":
    main()