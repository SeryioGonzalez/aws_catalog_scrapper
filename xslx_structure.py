

class xslx_structure:
    
    section_headers = []

    device_data_headers_row = {
        "first_cell_row": 1,
        "first_cell_column": 1,
        "columns": {
            "Device Vendor": {
                "name_mapping": "partner_name",
                "column_width": 20
            },
            "Device Name": {
                "name_mapping": "device_name",
                "column_width": 50
            },
            "Device Type": {
                "name_mapping": "device_type",
                "column_width": 20
            },
            "AWS Service": {
                "name_mapping": "aws_service",
                "column_width": 28
            },
            "Silicon vendor": {
                "name_mapping": "silicon_vendor",
                "column_width": 30
            },
            "Industry": {
                "name_mapping": "industry", 
                "column_width": 60
            },
            "Operating environments": {
                "name_mapping": "operating_temperature",
                "column_width": 40
            },
            "Availability": {
                "name_mapping": "availability",
                "column_width": 40
            },
            "Device Link": {
                "name_mapping": "device_id",
                "column_width": 12
            },
            "Product data sheet": {
                "name_mapping": "product_data_sheet",
                "column_width": 18
            },
            "Product URL": {
                "name_mapping": "product_url",
                "column_width": 12
            }
        }
    }

    section_headers.append(device_data_headers_row)


    def fill_section_header(xslx_tab, section_data, header_style):
        first_section_row    = section_data['first_cell_row']
        first_section_column = section_data['first_cell_column']

        #HORIZONTAL SECTION
        if 'columns' in section_data:
            for column_index, column_value in enumerate(section_data['columns']):
                column_width = section_data['columns'][column_value]['column_width']
                xslx_tab.set_column(first_section_column + column_index, first_section_column + column_index, column_width)
                xslx_tab.write(first_section_row, first_section_column + column_index, column_value, header_style)
        
        #VERTICAL SECTION
        if 'rows' in section_data:
            for row_index, row_value in enumerate(section_data['rows']):
                xslx_tab.write(first_section_row + row_index, first_section_column, row_value, header_style)
