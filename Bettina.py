"""
tr class=data
tr data-url= url
get all td text
cut off last three

"""
from ExcelFileHandler import ExcelFileAdapter
from time import sleep



class Bettina:


    def __init__(self, excel_file_handler, driver):
        self.excel_file_handler = excel_file_handler
        self.driver = driver
        pass

    def do_all_the_things(self, time_and_date):
        self.driver.get("https://www.bettinaequities.com/availabilities/")
        sleep(3)
        counter = 0
        load_more_button_exists = True
        pre_finalized_apartment_data = []
        while load_more_button_exists or counter < 50:
            load_more_button_exists = self.click_the_load_more_button()
            counter += 1
        apartment_links = self.find_all_apartment_links_on_main_page()
        for link in apartment_links:
            apartment_data = self.pull_data_from_each_link(link)
            pre_finalized_apartment_data.append(self.prettify_apartment_data(apartment_data))
        self.output_all_the_info(pre_finalized_apartment_data, time_and_date)

    def click_the_load_more_button(self):
        element = self.driver.find_element_by_class_name("load_more_btn")
        try:
            element.click()
            return True
        except:
            return False

    def find_all_apartment_links_on_main_page(self):
        links_container = self.driver.find_element_by_class_name("results_container_listing")
        apartment_links = [links.get_attribute('href') for links in links_container.find_elements_by_tag_name("a")]
        print("Number of apartments: " + str(len(apartment_links)))
        return apartment_links

    def pull_data_from_each_link(self, apartment_link):
        self.driver.get(apartment_link)
        apartment_data = []
        # Address/Apartment number - find class "apartment_1" then class "font_span"
        add_apt = self.driver.find_element_by_class_name("apartment_1")
        apartment_data.append(add_apt.find_element_by_class_name("font_span").text)
        # Availability - class "amenity_row.top" (maybe with space not dot) then class "amenity_large_text"
        data = self.driver.find_element_by_class_name("amenity_row.top")
        avail = [data2.text for data2 in data.find_elements_by_class_name("amenity_large_text")]
        apartment_data.append(avail)
        # Bed/Bath - class "amenity_row.bottom" then class "amenity_label" index 0 and 1
        data = self.driver.find_element_by_class_name("amenity_row.bottom")
        bed_bath = [data2.text for data2 in data.find_elements_by_class_name("amenity_label")]
        apartment_data.append(bed_bath)
        # Gross Rent/Net Rent/Incentive/Description/Lease Term - class "details"
        data = self.driver.find_element_by_class_name("details")
        details = data.text
        apartment_data.append(details)
        #print(apartment_data)
        return apartment_data

    def prettify_apartment_data(self, apartment_data):
        add_apt = self.fix_address_and_apartment(apartment_data[0])
        details = self.fix_details(apartment_data[3])
        apartment_data[0] = add_apt[0]
        apartment_data.insert(1, add_apt[1])
        apartment_data[2] = apartment_data[2][1]
        apartment_data.insert(3, apartment_data[3][0])
        apartment_data[4] = apartment_data[4][1]
        apartment_data[5] = details[1]
        apartment_data.append(details[2])
        apartment_data.append(details[3])
        apartment_data.append(details[4])
        return apartment_data


    def fix_details(self, details):
        remove_keys = []
        split_details = details.split("\n")
        for item in split_details:
            remove_keys.append(item.split(": "))
        final_list = [data[-1] for data in remove_keys]
        if final_list[1] == "$NAN" or final_list[1] is None:
            final_list[1] = final_list[0] + "G"
        return final_list

    def fix_address_and_apartment(self, add_apt):
        split_data = add_apt.split(" – ")
        return split_data

    # def matrix_data_from_website(self, driver):
    #     individual_apartments = []
    #     apartment_info = [data for data in driver.find_elements_by_tag_name("tr") if data.get_attribute("class") == "data"]
    #     for i in range(0, len(apartment_info)):
    #         individual_apartments.append([])
    #         for data in apartment_info[i].find_elements_by_tag_name("td"):
    #             if data.get_attribute("class") == "app_pending checked":
    #                 individual_apartments[i].append("App")
    #             else:
    #                 individual_apartments[i].append(data.text)
    #         del individual_apartments[i][7]
    #         del individual_apartments[i][5]
    #     return individual_apartments

    def format_data_into_dict(self, data_list):

        apartment_info_dict = {"Apartment": data_list[1],
                               "Address": data_list[0],
                               "Price": data_list[5],
                               "Available Date": data_list[2],
                               "Bedrooms": data_list[3],
                               "Bathrooms": data_list[4],
                               "Lease Term": data_list[8],
                               "Incentives": data_list[6],
                               "Description": data_list[7]}
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
        self.excel_file_handler.excel_file_setup("Bettina")
        self.excel_file_handler.update_spreadsheet(finalized_info_list)
        self.excel_file_handler.finalize_spreadsheet(self.excel_file_handler.row_offset, len(finalized_info_list), "Bettina" + time_and_date[0] + " " + time_and_date[1])






