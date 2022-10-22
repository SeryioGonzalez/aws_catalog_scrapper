import json
import requests 

def download_json_file(file_url, file_destinaton):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }

    
    response = requests.request("GET", file_url, headers=headers)
    json_response = response.text

    with open(file_destinaton, "w") as outfile:
        outfile.write(json_response)


def read_json_file(json_file):
    with open(json_file, "r") as input_file:
        json_data = json.load(input_file)
    
    return json_data
