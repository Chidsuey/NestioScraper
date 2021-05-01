"""
tr class=data
tr data-url= url
get all td text
cut off last three

"""
from ExcelFileHandler import ExcelFileAdapter
import math


class Bettina:

    def __init__(self, excel_file_handler):
        self.excel_file_handler = excel_file_handler
        pass

    def matrix_data_from_website(self, driver):
        individual_apartments = []
        apartment_info = [data for data in driver.find_elements_by_tag_name("tr") if data.get_attribute("class") == "data"]
        for i in range(0, len(apartment_info)):
            individual_apartments.append([])
            for data in apartment_info[i].find_elements_by_tag_name("td"):
                if data.get_attribute("class") == "app_pending checked":
                    individual_apartments[i].append("App")
                else:
                    individual_apartments[i].append(data.text)
            del individual_apartments[i][7]
            del individual_apartments[i][5]
        return individual_apartments

    def format_data_into_dict(self, data_list):
        # Fix current website net rent
        # data_list[4] = data_list[4][0] + data_list[4][2:]
        # data_list[4] = float(data_list[4])*12/11
        # data_list[4] = int(data_list[4])
        # temp = str(data_list[4])
        # data_list[4] = temp[0] + "," + temp[1:] + ".00"
        #-------------------------------------------------

        apartment_info_dict = {"Apartment": data_list[1],
                               "Price": data_list[4],
                               "Address": data_list[0],
                               "Bedrooms": data_list[2],
                               "Application": data_list[5],
                               "Available Date": data_list[3]}
        return apartment_info_dict

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






