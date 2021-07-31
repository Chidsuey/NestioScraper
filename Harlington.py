# find class "result__info"
# then (possible h2 then ) a tag with href for building link
# address class="details__title"
# apt/avail/bed/bath/price - class = "avl__cols", then td
# desc - class="avl__notes"
import time

from ExcelFileHandler import ExcelFileAdapter
from time import sleep



class Harlington:


    def __init__(self, excel_file_handler, driver):
        self.excel_file_handler = excel_file_handler
        self.driver = driver
        self.building_address = ""
        self.apartment_info = []

    def do_all_the_things(self, time_and_date):
        final_list = []
        self.driver.get("https://harlington.com/residential?neighborhood=&rentmin=&rentmax=&openhouse=false")
        building_links = self.get_building_links()
        self.cycle_through_building_apartments(building_links)
        for i in range(0, len(self.apartment_info)):
            temp_dict = self.turn_info_into_dict(i)
            final_list.append(self.adapt_data_for_output(temp_dict))
        self.output_all_the_info(final_list, time_and_date)


    def get_building_links(self):
        links = []
        for parent_tag in self.driver.find_elements_by_class_name("result__info"):
            links.append(parent_tag.find_element_by_tag_name("a").get_attribute("href"))
        return links

    def cycle_through_building_apartments(self, building_links):
        for link in building_links:
            self.driver.get(link)
            self.get_building_address()
            temporary_desc_holder = []
            for desc_tag in self.driver.find_elements_by_class_name("avl__notes"):
                temporary_desc_holder.append(desc_tag.text)
            for index, parent_tag in enumerate(self.driver.find_elements_by_class_name("avl__cols")):
                apt_avail_bed_bath_price = self.get_apartment_info(parent_tag)
                apt_avail_bed_bath_price.append(temporary_desc_holder[index])
                apt_avail_bed_bath_price[5] = self.fix_price(apt_avail_bed_bath_price[5])
                apt_avail_bed_bath_price[1] = self.fix_apt(apt_avail_bed_bath_price[1])
                self.apartment_info.append(apt_avail_bed_bath_price)

    def get_building_address(self):
        self.building_address = self.driver.find_element_by_class_name("details__title").text.split(",")

    def get_apartment_info(self, parent_tag):
        apt_avail_bed_bath_price = [self.building_address[0]]
        for info in parent_tag.find_elements_by_tag_name("td"):
            apt_avail_bed_bath_price.append(info.text)
        return apt_avail_bed_bath_price

    def fix_price(self, price):
        fixed_price = price.split("/")
        return fixed_price[0]

    def fix_apt(self, apt):
        fixed_apt = apt.split(" ")
        return fixed_apt[1]

    def turn_info_into_dict(self, i):
        return {"Apartment": self.apartment_info[i][1],
                "Address": self.apartment_info[i][0],
                "Price": self.apartment_info[i][5],
                "Available Date": self.apartment_info[i][2],
                "Bedrooms": self.apartment_info[i][3],
                "Bathrooms": self.apartment_info[i][4],
                "Description": self.apartment_info[i][6]}

    def adapt_data_for_output(self, data_dict):
        adapter = ExcelFileAdapter(data_dict)
        formatted_single_entry_list = adapter.adapt_info_for_output()
        return formatted_single_entry_list

    def output_all_the_info(self, finalized_info_list, time_and_date):
        self.excel_file_handler.excel_file_setup("Harlington")
        self.excel_file_handler.update_spreadsheet(finalized_info_list)
        self.excel_file_handler.finalize_spreadsheet(self.excel_file_handler.row_offset, len(finalized_info_list), "Harlington " + time_and_date[0] + " " + time_and_date[1])