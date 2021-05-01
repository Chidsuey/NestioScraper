from selenium.webdriver.common.keys import Keys
import ExcelFileHandler


"""
Order as follows:
Preliminary check of floor plan links to gather the exact number.
Run floor plan links, check link, rerun floor plan links to gather exact number of apartments
Run floor plan links, check first link, rerun apartment links, check first apartment, rerun apartment links
    until all apartments at floor plan are checked.

"""


class ElevenThirteenManhattan:

    def __init__(self):
        self.excel_file_handler = ExcelFileHandler.ExcelFileHandler()

    def get_apartment_links(self, driver):
        finalized_info_list = []
        list_of_apartment_links = []
        available_floorplans = self.does_floorplan_have_apartments_available(driver)
        total_floorplans_to_check = len(available_floorplans)
        for i in range(0, total_floorplans_to_check):
            select_floor_plan_element = driver.find_element_by_id("step2")
            available_floorplans = self.does_floorplan_have_apartments_available(driver)
            list_of_apartment_links.append(self.find_all_apartments_from_floorplans(available_floorplans[i], driver))
            single_entry_dict = self.scrape_apartment_link(list_of_apartment_links[i][0], driver)
            excel_adapter = ExcelFileHandler.ExcelFileAdapter(single_entry_dict)#, "1133 Manhattan")
            finalized_info_list.append(excel_adapter.adapt_info_for_output())
            self.click_on_an_element(select_floor_plan_element)
        return finalized_info_list

    def click_on_an_element(self, clickable_element):
        clickable_element.send_keys(Keys.ENTER)

    def does_floorplan_have_apartments_available(self, driver):
        aTags = driver.find_elements_by_tag_name('a')
        floorplans_to_click_on = [tag for tag in aTags if tag.get_attribute("class") == 'floorplan-card-cta no-cta ember-view']
        return floorplans_to_click_on

    def find_all_apartments_from_floorplans(self, apartments, driver):
        apartment_details_links = []
        self.click_on_an_element(apartments)
        list_of_a_tags = driver.find_elements_by_tag_name('a')
        for aTag in list_of_a_tags:
            if aTag.get_attribute('class') == "apartment-details ember-view":
                apartment_details_links.append(aTag)
        return apartment_details_links

    def scrape_apartment_link(self, link, driver):
        apartment_info_dict = {"Apartment": "", "Price": "", "Available Date": "", "Bedrooms": ""
                               , "Bathrooms": "", "Size": "", "Incentives": ""}
        self.click_on_an_element(link)
        h4_tags = driver.find_elements_by_tag_name('h4')
        div_tags = driver.find_elements_by_tag_name('div')
        for tag in h4_tags:
            if tag.get_attribute('class') == "display-name":
                apartment_info_dict["Apartment"] = tag.text

            if tag.get_attribute('class') == "availability-text":
                apartment_info_dict["Available Date"] = tag.text

        for tag in div_tags:
            if tag.get_attribute('class') == "unit-beds":
                apartment_info_dict["Bedrooms"] = tag.text
            if tag.get_attribute('class') == "unit-baths":
                apartment_info_dict["Bathrooms"] = tag.text
            if tag.get_attribute('class') == "unit-size":
                apartment_info_dict["Size"] = tag.text
            if tag.get_attribute('class') == "unit-rate":
                apartment_info_dict["Price"] = tag.text
        return apartment_info_dict

    def output_all_the_info(self, finalized_info_list, time_and_date):
        self.polish_data(finalized_info_list)
        self.excel_file_handler.excel_file_setup("1133 Manhattan")
        self.excel_file_handler.update_spreadsheet(finalized_info_list)
        self.excel_file_handler.finalize_spreadsheet(len(finalized_info_list), "1133 Manhattan" + time_and_date[0] + " " + time_and_date[1])

    def polish_data(self, data_to_polish):
        for i in range(0, len(data_to_polish)):
            data_to_polish[i][0] = data_to_polish[i][0].replace("Apartment #", "")
            data_to_polish[i][2] = data_to_polish[i][2].replace("From ", "")
            data_to_polish[i][3] = data_to_polish[i][3].replace("Available ", "")
            data_to_polish[i][4] = (data_to_polish[i][4])[0]
            data_to_polish[i][5] = (data_to_polish[i][5])[0]


