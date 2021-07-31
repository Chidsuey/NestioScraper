"""
get all links - class "item-link" get href
add-apt - class "listing-location"
bed = class "listing-bedrooms"
bath = class "listing-bathrooms"
price = class "listing-price"
desc = class "listing-key-features"
incentive = class "listing-details"
"""

from ExcelFileHandler import ExcelFileAdapter
from time import sleep



class Paley:


    def __init__(self, excel_file_handler, driver):
        self.excel_file_handler = excel_file_handler
        self.driver = driver

    def do_all_the_things(self, time_and_date):
        self.driver.get("https://paleymanagement.com/apartmentsavailable.htm")
        pre_finalized_apartment_data = self.get_apartment_data()
        finalized_apartment_data = [self.prettify_apartment_data(data) for data in pre_finalized_apartment_data]
        self.output_all_the_info(finalized_apartment_data, time_and_date)

    def get_apartment_data(self):
        apartment_data = []
        tbody = self.driver.find_element_by_id("example")
        tbody = tbody.find_element_by_tag_name("tbody")
        for tr in tbody.find_elements_by_tag_name("tr"):
            data = [td.text for td in tr.find_elements_by_tag_name("td")]
            apartment_data.append(data)
        return apartment_data

    def prettify_apartment_data(self, apartment_data):
        add_apt = self.fix_address_and_apartment(apartment_data[2])
        price = self.fix_price(apartment_data[0])
        apartment_data[2] = add_apt[0]
        apartment_data[3] = add_apt[1]
        apartment_data[0] = price
        apartment_data.pop()
        return apartment_data

    def fix_price(self, price):
        split_price = price.split("/")
        return split_price[0]

    def fix_incentives(self, incentives):
        split_incentives = incentives.split("\n")
        return split_incentives[1]

    def fix_address_and_apartment(self, add_apt):
        split_data = add_apt.split(" - ")
        return split_data

    def format_data_into_dict(self, data_list):

        apartment_info_dict = {"Apartment": data_list[3],
                               "Address": data_list[2],
                               "Price": data_list[0],
                               "Bedrooms": data_list[1]}
        return apartment_info_dict

    #Run all through adapt

    def adapt_data_for_output(self, data_dict):
        adapter = ExcelFileAdapter(data_dict)
        formatted_single_entry_list = adapter.adapt_info_for_output()
        return formatted_single_entry_list


    def output_all_the_info(self, pre_finalized_info_list, time_and_date):
        finalized_info_list = []
        for i in range(0, len(pre_finalized_info_list)):
            single_dict = self.format_data_into_dict(pre_finalized_info_list[i])
            finalized_info_list.append(self.adapt_data_for_output(single_dict))
        self.excel_file_handler.excel_file_setup("Paley")
        self.excel_file_handler.update_spreadsheet(finalized_info_list)
        self.excel_file_handler.finalize_spreadsheet(self.excel_file_handler.row_offset, len(finalized_info_list), "Paley  " + time_and_date[0] + " " + time_and_date[1])






