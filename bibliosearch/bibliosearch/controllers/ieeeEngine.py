import json
import requests

def fromJson(url, file, params):
    data = requests.get(url, verify=False, params = params).json()

    with open(file, 'w') as outfile:
        json.dump(data, outfile)

def main():
    params = dict(
        content_type = 'Conferences',
        max_records = '200',
        start_year = '2005',
        end_year = '2010'
    )
    fromJson("https://ieeexploreapi.ieee.org/api/v1/search/articles?parameter&apikey=efv84mzqq6ydx4dbd59jhdcn", 'static/ieeeXplore.json', params)

if __name__ == "__main__":
    main()