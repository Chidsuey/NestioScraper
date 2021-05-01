from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.touch_actions import TouchActions
import ExcelFileHandler
import time


class TheEugene:

    def __init__(self):
        self.excel_file_handler = ExcelFileHandler.ExcelFileHandler()


    def click_on_an_element(self, clickable_element, driver):
        try:
            clickable_element.send_keys(Keys.ENTER)
        except:
            try:
                #clickable_element.location_once_scrolled_into_view
                WebElement.click(clickable_element)
            except:

                actions = ActionChains(driver)
                actions.move_to_element(clickable_element).click().perform()


    def scrape_data(self, driver, progress_text):
        raw_apartment_list = []
        finalized_info_list = []
        apartment_details = []
        driver.maximize_window()
        self.deal_with_accepting_cookies(driver)
        progress_text("Waiting for website to load...")
        time.sleep(15)
        floorplans_links = [data for data in driver.find_elements_by_tag_name("div") if data.get_attribute("class") == "floorplan-detail-toggle fp-col-6"]
        for link in floorplans_links:
            self.click_on_an_element(link, driver)
            close_button = driver.find_element_by_class_name("close-detail")
            for data in driver.find_elements_by_tag_name('ul'):
                if data.get_attribute('class') == 'fp-detail-unit':
                    apartment_details = data.text.split('\n')
                    bed_and_bath = [data.text for data in driver.find_elements_by_tag_name("span")
                                    if data.get_attribute("class") == "bed-count"
                                    or data.get_attribute("class") == "bath-count"]
                    apartment_details[3] = bed_and_bath[-2]
                    apartment_details.append(bed_and_bath[-1])
                    polished_data = self.polish_data(apartment_details)
                    dict_apartment_info = self.format_data_into_dict(polished_data)
                    excel_handler = ExcelFileHandler.ExcelFileAdapter(dict_apartment_info)
                    finalized_info_list.append(excel_handler.adapt_info_for_output())
            self.click_on_an_element(close_button, driver)

        return finalized_info_list

    def format_data_into_dict(self, data_list):
        apartment_info_dict = {"Apartment": data_list[0],
                               "Size": data_list[1],
                               "Price": data_list[2],
                               "Lease Term": data_list[5],
                               "Bedrooms": data_list[3],
                               "Bathrooms": data_list[4]}
        return apartment_info_dict


    def polish_data(self, data_to_be_polished):
        polished_data = []
        data_to_be_polished[0] = data_to_be_polished[0].split(' ')
        data_to_be_polished[1] = data_to_be_polished[1].split(' ')
        data_to_be_polished[2] = data_to_be_polished[2].split(" on a ")

        polished_data.append(data_to_be_polished[0][1]) #Apartment
        polished_data.append(data_to_be_polished[1][0]) #Size
        polished_data.append(data_to_be_polished[2][0]) #Price
        polished_data.append(data_to_be_polished[3]) #Beds
        polished_data.append(data_to_be_polished[4]) #Baths
        polished_data.append(data_to_be_polished[2][1]) #Lease Term

        return polished_data

    def deal_with_accepting_cookies(self, driver):
        cookie_button = driver.find_element_by_id("onetrust-accept-btn-handler")
        self.click_on_an_element(cookie_button, driver)


    def output_all_the_info(self, finalized_info_list, time_and_date):
        self.excel_file_handler.excel_file_setup("The Eugene")
        self.excel_file_handler.update_spreadsheet(finalized_info_list)
        self.excel_file_handler.finalize_spreadsheet(len(finalized_info_list), "The Eugene" + time_and_date[0] + " " + time_and_date[1])
        pass
