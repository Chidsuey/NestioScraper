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



class LCLemle:


    def __init__(self, excel_file_handler, driver):
        self.excel_file_handler = excel_file_handler
        self.driver = driver
        pass

    def do_all_the_things(self, time_and_date):
        self.driver.get("https://lclemle.com/apartments/")
        pre_finalized_apartment_data = []
        apartment_links = self.find_all_apartment_links_on_main_page()
        for link in apartment_links:
            apartment_data = self.pull_data_from_each_link(link)
            pre_finalized_apartment_data.append(self.prettify_apartment_data(apartment_data))
        self.output_all_the_info(pre_finalized_apartment_data, time_and_date)
        print(pre_finalized_apartment_data)

    def find_all_apartment_links_on_main_page(self):
        apartment_links = [links.get_attribute('href') for links in self.driver.find_elements_by_class_name("item-link")]
        print("Number of apartments: " + str(len(apartment_links)))
        return apartment_links

    def pull_data_from_each_link(self, apartment_link):
        self.driver.get(apartment_link)
        apartment_data = []
        # Address/Apartment number - class "listing-location""
        add_apt = self.driver.find_element_by_id("listing-overview")
        add_apt = add_apt.find_element_by_tag_name("h1").text
        apartment_data.append(add_apt)
        # Bed = class "listing-bedrooms"
        bed = self.driver.find_element_by_class_name("listing-bedrooms").text
        apartment_data.append(bed)
        # bath = class "listing-bathrooms"
        bath = self.driver.find_element_by_class_name('listing-bathrooms').text
        apartment_data.append(bath)
        # price = class "listing-price"
        price = self.driver.find_element_by_class_name('listing-price').text
        apartment_data.append(price)
        #desc = class "listing-key-features"
        desc = self.driver.find_element_by_class_name('tagged-features').text
        apartment_data.append(desc)
        # incentive = class "listing-details"
        incentive = self.driver.find_element_by_class_name('listing-content').text
        apartment_data.append(incentive)
        #print(apartment_data)
        return apartment_data

    def prettify_apartment_data(self, apartment_data):
        add_apt = self.fix_address_and_apartment(apartment_data[0])
        details = self.fix_details(apartment_data[4])
        beds = self.fix_beds(apartment_data[1])
        baths = self.fix_baths(apartment_data[2])
        price = self.fix_price(apartment_data[3])
        incentives = self.fix_incentives(apartment_data[5])
        apartment_data[0] = add_apt[0]
        apartment_data.insert(1, add_apt[1])
        apartment_data[2] = beds
        apartment_data[3] = baths
        apartment_data[4] = price
        apartment_data[5] = details
        apartment_data[6] = incentives
        return apartment_data

    def fix_baths(self, baths):
        split_baths = baths.split(" ")
        return split_baths[0]

    def fix_beds(self, beds):
        split_beds = beds.split(" ")
        return split_beds[0]

    def fix_price(self, price):
        split_price = price.split(" / ")
        return split_price[0]

    def fix_incentives(self, incentives):
        split_incentives = incentives.split("\n")
        return split_incentives[1]

    def fix_details(self, details):
        split_details = details.split("\n")
        return split_details

    def fix_address_and_apartment(self, add_apt):
        split_data = add_apt.split(", #")
        return split_data

    def format_data_into_dict(self, data_list):

        apartment_info_dict = {"Apartment": data_list[1],
                               "Address": data_list[0],
                               "Price": data_list[4],
                               "Bedrooms": data_list[2],
                               "Bathrooms": data_list[3],
                               "Incentives": data_list[6],
                               "Description": data_list[5]}
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
        self.excel_file_handler.excel_file_setup("LC Lemle")
        self.excel_file_handler.update_spreadsheet(finalized_info_list)
        self.excel_file_handler.finalize_spreadsheet(self.excel_file_handler.row_offset, len(finalized_info_list), "LC Lemle " + time_and_date[0] + " " + time_and_date[1])






