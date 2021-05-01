import time
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.firefox.options import Options

"""
Create new window for extra modules
"""


class LinkScraper:
    driver = webdriver
    info_dictionary = {'Details List': [], 'Key Listing Details': [], 'Description': '', 'Lease Term': ''
                       , 'Incentives': [], 'Apartment/Address': [], 'Application': ''}

    def __init__(self):
        self.link_counter = 0


    def open_webdriver(self, set_progress_text):
        options = Options()
        options.headless = True
        try:
            self.driver = webdriver.Firefox('C:/Users/Tim/Documents/NestioScraperClean', options=options)  # First arg is system location of Firefox
                                                                                # webdriver(geckodriver)
        except WebDriverException:
            set_progress_text("Firefox was updating. Try again in a few seconds.")


    def format_details_list(self, data_text):
        if data_text != '-':
            details_list_full = data_text.splitlines()
            details_list_titles_removed = []
            for i in range(0, len(details_list_full)):
                if i % 2 != 0:
                    details_list_titles_removed.append(details_list_full[i])
            return details_list_titles_removed


    def format_listing_key_details(self, data_text):
        if data_text != '-':
            list_of_key_details = data_text.splitlines()
            for i in range(0, len(list_of_key_details)):
                if len(list_of_key_details) < 3:
                    list_of_key_details.append('-')

            if list_of_key_details[0][0] == "F":
                list_of_key_details[0] = list_of_key_details[0][0] + list_of_key_details[0][-1]
            elif list_of_key_details[0][0] == "J":

                list_of_key_details[0] = list_of_key_details[0][0] + list_of_key_details[0][3]
            else:
                list_of_key_details[0] = list_of_key_details[0][0]

            temp = list_of_key_details[1].split(" ")
            list_of_key_details[1] = temp[0]
            return list_of_key_details


    def format_lease_term(self, lease_term):
            return lease_term.splitlines()


    def format_aptadd(self, aptadd):
        apartment_and_address_list = aptadd.split('#')
        return apartment_and_address_list

    def format_finalized_info(self):
        try:
            finalized_info_list = [self.info_dictionary['Apartment/Address'][1],
                                   self.info_dictionary['Apartment/Address'][0],
                                   self.info_dictionary['Details List'][2],
                                   self.info_dictionary['Details List'][1],
                                   self.info_dictionary['Key Listing Details'][0],
                                   self.info_dictionary['Key Listing Details'][1],
                                   self.info_dictionary['Key Listing Details'][2],
                                   self.info_dictionary['Lease Term'][1],
                                   self.info_dictionary['Incentives'],
                                   self.info_dictionary['Description'],
                                   self.info_dictionary['Application']
                                   ]
        except:
            finalized_info_list = ["X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"]
        return finalized_info_list

    def close_driver(self):
        self.driver.quit()

    def scrape_links_for_data(self, link_list, links_remaining_text, progress_text, log_handler, log_file, finalized_incentives_list):
        search_tags = ['detail-list', 'listing-key-details', 'description', 'lease-term', 'incentives', 'listing-title']
        found_tag_information = ['-', '-', '-', '-', '-', '-']
        self.open_webdriver(progress_text)
        current_list_length = len(link_list)
        finalized_info_list = []
        progress_text("Scraping...")
        for link in link_list:
            links_remaining_text(((str(current_list_length)) + " links to check."))
            log_handler.update_log(log_file, "Link #" + str(self.link_counter) + ": " + link_list[self.link_counter])
            self.driver.get(link)
            time.sleep(7)  # delay to avoid some gathering issues

            for i in range(0, len(search_tags)):
                try:
                    if search_tags[i] != 'description':
                        data_found_at_tag = self.driver.find_element_by_class_name(search_tags[i])
                        found_tag_information[i] = data_found_at_tag.text
                    if search_tags[i] == 'description':
                        data_found_at_tag = self.driver.find_element_by_xpath("//meta[@property='og:description']")\
                                            .get_attribute("content")
                        found_tag_information[i] = data_found_at_tag

                except Exception as e:
                    log_handler.update_log(log_file, '   ' + str(e) + ' - ' + search_tags[i] + " was not found.")
                    found_tag_information[i] = " \n  \n  \n  \n "


            self.info_dictionary['Details List'] = self.format_details_list(found_tag_information[0])
            self.info_dictionary['Key Listing Details'] = self.format_listing_key_details(found_tag_information[1])
            self.info_dictionary['Description'] = found_tag_information[2][0:30000]
            self.info_dictionary['Lease Term'] = self.format_lease_term(found_tag_information[3])
            self.info_dictionary['Incentives'] = finalized_incentives_list[self.link_counter]#self.format_incentives_list(found_tag_information[4])
            self.info_dictionary['Apartment/Address'] = self.format_aptadd(found_tag_information[5])

            found_tag_information = ['-', '-', '-', '-', '-', '-']
            finalized_info_list.append(self.format_finalized_info())
            self.link_counter += 1
            current_list_length -= 1
        links_remaining_text("0 links to check.")
        progress_text("Closing Scraper...")
        self.close_driver()
        return finalized_info_list


    """Old way of getting incentives"""


    # def format_incentives_list(self, incentives):
    #     incentives_list = incentives.splitlines()
    #     finalized_incentives_list = []
    #     incentives_in_description = self.search_description_for_incentives(self.info_dictionary['Description'])
    #     for incentive in range(1, len(incentives_list)):
    #         finalized_incentives_list.append(incentives_list[incentive])
    #     for incentive in range(0, len(incentives_in_description)):
    #         finalized_incentives_list.append(incentives_in_description[incentive])
    #     finalized_incentives_list = '\n'.join(finalized_incentives_list)
    #     return finalized_incentives_list


    # def search_description_for_incentives(self, description):
    #     parse_list = []
    #     found_list = []
    #     search_list = ["one month free", "1 month free", "two month free", "2 month free", "two months free"
    #                    , "2 months free", "one month op", "1 month op", "one month owner pays", "1 month owner pays"
    #                    , "1.5 month free", "1.5 months free", "1/2 month free"]
    #     for i in search_list:
    #         parse_list.append(description.find(i))
    #     for i in range(0, len(parse_list)):
    #         if parse_list[i] != -1:
    #             found_list.append(description[parse_list[i]:parse_list[i] + len(search_list[i])])
    #     return found_list

