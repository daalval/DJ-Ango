import json
import requests

def query(url, file, our_content_types, our_start_year, our_end_year):
    params = dict(
        content_types = our_content_types,
        start_year = our_start_year,
        end_year = our_end_year,
        max_records = '200',
    )

    if len(our_content_types) == 1:
        params = dict(
            content_type = our_content_types[0],
            start_year = our_start_year,
            end_year = our_end_year,
            max_records = '200',
        )
        data = requests.get(url, verify=False, params=params).json()
        with open(file, 'w') as outfile:
            json.dump(data, outfile)
    else:
        for type in our_content_types:
            params = dict(
                content_type = type,
                start_year = our_start_year,
                end_year = our_end_year,
                max_records = '200',
            )
            data = requests.get(url, verify=False, params=params).json()
            with open(file, 'a+') as outfile:
                json.dump(data, outfile)
    
    

def main():
    query("https://ieeexploreapi.ieee.org/api/v1/search/articles?parameter&apikey=efv84mzqq6ydx4dbd59jhdcn", 'static/ieeeXplore.json', ['Books', 'Conferences'], '2010', '2015')

if __name__ == "__main__":
    main()








# for article in data['articles']:
#         print(article['title'])
#         print(article['rank'])