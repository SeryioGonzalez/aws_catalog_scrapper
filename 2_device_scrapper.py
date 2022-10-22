from datetime import datetime
from os import listdir
from os.path import isfile, join
from scrapper_utils import *

import configparser
import json
import requests

#DATE
today_time = datetime.now()
today_time_format = today_time.strftime("%Y%m%d")

#CONFIG
config = configparser.ConfigParser()
config.read('config.ini')

#GET DEVICE URI
aws_catalog_device_url = config['AWS_CATALOG']['aws_catalog_device_url']

#OUTPUT FILES
aws_catalog_output_folder       = config['WEB_OUTPUT']['output_folder']
aws_catalog_output_file_pattern = config['WEB_OUTPUT']['main_catalog_output_file_name_pattern']
device_data_file_pattern        = config['WEB_OUTPUT']['device_output_file_name_pattern']

#GET THE LATEST CATALOG
catalog_files = ["{}/{}".format(aws_catalog_output_folder , f) for f in listdir(aws_catalog_output_folder) if isfile(join(aws_catalog_output_folder, f)) and f.startswith( aws_catalog_output_file_pattern) ]
catalog_files.sort(reverse=True)
latest_catalog_file = catalog_files[0]

#GET THE DEVICE IDs FROM THE CATALOG
catalog_file_pointer = open(latest_catalog_file)
catalog_json = json.load(catalog_file_pointer)

device_ids = [device_data['id'] for device_data in catalog_json['results']]
today_device_files = [ "{}/{}_{}.json".format(aws_catalog_output_folder, device_data_file_pattern, device_id) for device_id in device_ids]

#GET THE ALREADY DOWNLOADED FILES
downloaded_device_files = ["{}/{}".format(aws_catalog_output_folder , f) for f in listdir(aws_catalog_output_folder) if isfile(join(aws_catalog_output_folder, f)) and f.startswith( device_data_file_pattern) ]
device_files_to_download = [device_file for device_file in today_device_files if device_file not in downloaded_device_files]

print("Number of files to download: {}".format(len(device_files_to_download)))

for device_file_to_download in device_files_to_download:
  device_id = device_file_to_download[21:39]
  device_url = "{}/{}".format(aws_catalog_device_url, device_id)

  print("Downloading device id: {}".format(device_id))

  download_json_file(device_url, device_file_to_download)

