from datetime import datetime
from xslx_structure import xslx_structure as xslx
from os import listdir
from os.path import isfile, join
from scrapper_utils import *

import configparser
import json
import operator
import requests
import xlsxwriter

#DATE
today_time = datetime.now()
today_time_format = today_time.strftime("%Y%m%d")

#CONFIG
config = configparser.ConfigParser()
config.read('config.ini')

#GET DEVICE URI
aws_catalog_device_url = config['AWS_CATALOG']['aws_catalog_device_url']

#OUTPUT FILES
aws_catalog_output_folder = config['WEB_OUTPUT']['output_folder']
device_data_file_pattern  = config['WEB_OUTPUT']['device_output_file_name_pattern']

#INIT WORKBOOK
excel_folder    = config['EXCEL_OUTPUT']['excel_folder']
excel_file_name = config['EXCEL_OUTPUT']['excel_file_name']
excel_file = "{}/{}".format(excel_folder, excel_file_name)
workbook = xlsxwriter.Workbook(excel_file)

#DEFINE EXCEL STYLES
header_style = workbook.add_format()
header_style.set_bold()
header_style.set_align('center')
header_style.set_border(1)
header_style.set_bg_color('#31869B')

data_style = workbook.add_format()
data_style.set_border(1)
data_style.set_bg_color('#EBF1DE')

data_hyperlink_style = workbook.add_format()
data_hyperlink_style.set_hyperlink(True)
data_hyperlink_style.set_border(1)
data_hyperlink_style.set_bg_color('#EBF1DE')

catalog_tab = workbook.add_worksheet(config['EXCEL_OUTPUT']['data_tab'])

#FILL WORKBOOK SECTIONS HEADERS
for xslx_section in xslx.section_headers:
  xslx.fill_section_header(catalog_tab, xslx_section, header_style)

#GET DEVICE FILES
device_files = ["{}/{}".format(aws_catalog_output_folder , f) for f in listdir(aws_catalog_output_folder) if isfile(join(aws_catalog_output_folder, f)) and f.startswith( device_data_file_pattern) ]

#LOAD DEVICE DATA
raw_device_data      = []
filtered_device_data = []

for device_file in device_files:
  device_json_data = read_json_file(device_file)
  raw_device_data.append(device_json_data)

#GET DEVICE KEYS OF INTEREST
device_fields_of_interest = [xslx.device_data_headers_row['columns'][device_data_item_column]['name_mapping'] for device_data_item_column in xslx.device_data_headers_row['columns'] ]

#ITERATE AND FILTER DEVICES
for device_item in raw_device_data:
  #SELECT FIELDS OF INTEREST
  filtered_device_item = {key_of_interest: device_item[key_of_interest] for key_of_interest in device_fields_of_interest}
  #FILTER KEY FIELDS
  filtered_device_item['device_id'] = '{}/{}'.format(config['AWS_CATALOG']['aws_catalog_device_detail_url'], filtered_device_item['device_id'])
  filtered_device_data.append(filtered_device_item)

#SORT THE LIST BY VENDOR
filtered_device_data.sort(key=operator.itemgetter('partner_name'))

#WRITE DATA FROM EACH DEVICE
for filtered_device_index, filtered_device_item in enumerate(filtered_device_data):
  this_row = xslx.device_data_headers_row['first_cell_row'] + 1 + filtered_device_index
  
  #ITERATE EACH DEVICE DATA COLUMN
  for filtered_device_data_item_index, filtered_device_data_item_value in enumerate(list(filtered_device_item.values())):
    this_column = xslx.device_data_headers_row['first_cell_column'] + filtered_device_data_item_index
    
    if  isinstance(filtered_device_data_item_value, str) and (filtered_device_data_item_value.startswith('http') or filtered_device_data_item_value.startswith('ftp://') or filtered_device_data_item_value.startswith('www.') or filtered_device_data_item_value.startswith('renesas.com')):
      current_column_title = list(xslx.device_data_headers_row['columns'])[this_column - 1]
      catalog_tab.write_url(this_row, this_column, filtered_device_data_item_value, string=current_column_title, cell_format=data_hyperlink_style)
    else:
      #Value can be a list
      if isinstance(filtered_device_data_item_value, list):
        filtered_device_data_item_value = ",". join(filtered_device_data_item_value)
      
      catalog_tab.write(this_row, this_column, filtered_device_data_item_value, data_style)

workbook.close()    

