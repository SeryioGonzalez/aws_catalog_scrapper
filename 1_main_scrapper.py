
from datetime import datetime
from scrapper_utils import *

import configparser

#DATE
time = datetime.now()
time_format = time.strftime("%Y%m%d")

#CONFIG
config = configparser.ConfigParser()
config.read('config.ini')

#DEFINE SEARCH URI
aws_catalog_search_url = config['AWS_CATALOG']['aws_catalog_search_url']
aws_catalog_init_size  = config['AWS_CATALOG']['aws_catalog_init_size']
aws_catalog_search_url_with_params = "{}?from={}&size={}".format(aws_catalog_search_url, 1, aws_catalog_init_size)


#DEFINE DATA OUTPUT FILES
aws_catalog_output_folder = config['WEB_OUTPUT']['output_folder']
aws_catalog_all_device_data_file_pattern = config['WEB_OUTPUT']['main_catalog_output_file_name_pattern']
aws_catalog_all_device_data_file = "{}/{}.{}.json".format(aws_catalog_output_folder, aws_catalog_all_device_data_file_pattern, time_format)

download_json_file(aws_catalog_search_url_with_params, aws_catalog_all_device_data_file)

