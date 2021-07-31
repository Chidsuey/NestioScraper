from bs4 import BeautifulSoup



class HTMLFileScraper:

    final_formatted_file_name = ""
    owner_name_checked_for_errors = ""

    def __init__(self):
        self.soup = BeautifulSoup(features="html.parser")

    def convert_html_to_beautiful_soup_file(self, html_file, coding):
        with open(html_file, 'r', encoding=coding.get()) as html_file:
            self.soup = BeautifulSoup(html_file, 'lxml')
        html_file.close()

    def find_owner_name(self):
        try:
            owner_name = self.soup.find("title").text
        except AttributeError:
            owner_name = "NotFound"
        if (owner_name == "NotFound"):
            for tag in self.soup.find_all('p'):
                #try:
                if tag.span.text == "Subject: ":
                    owner_name = (tag.span.parent.next_sibling.text)
                    break


        return owner_name.replace("Current Listings", '')

        #owner_name = []
        #for name in self.soup.find_all(alt=True):
        #    owner_name.append(name.get('alt'))
        #return owner_name

    def owner_name_error_checker(self, name_to_check):
        fixed_name = name_to_check
        bad_characters = ["\\", "/", "?", "*", "|", ":", "\"", "<", ">"]
        for char in range(0, len(bad_characters)):
            bad_character_number = fixed_name.find(bad_characters[char])
            if bad_character_number >= 0:
                fixed_name_split = fixed_name.split(bad_characters[char])
                fixed_name = " ".join(fixed_name_split)
            if bad_character_number == -1:
                bad_character_number += 1
        fixed_name = self.return_stripper(fixed_name)
        return fixed_name

    def link_finder(self):
        link_list = []
        for tag in self.soup.find_all('h3'):
            #Thunderbird link finder
            h3_html_tag = tag.get('class')
            if (str(h3_html_tag)) == "['listing-title']" or (str(h3_html_tag)) == "['x_listing-title']":
                link_list.append(tag.a.get('href'))
            else:
                #Outlook link finder
                link_list.append(tag.a.get('href'))
        return link_list

    @staticmethod
    def return_stripper(string_to_be_stripped):
        return string_to_be_stripped.replace('\n', "")

    def scrape_html_file_for_links(self, html_file, coding):

        self.convert_html_to_beautiful_soup_file(html_file, coding)
        owner_name = self.find_owner_name()
        try:
            #self.owner_name_checked_for_errors = self.owner_name_error_checker(owner_name[0]) for old owner name finding delete on (8/1/20)
            self.owner_name_checked_for_errors = self.owner_name_error_checker(owner_name)
        except IndexError:
            print("Couldn't get owner name")
        link_list = self.link_finder()
        return link_list

    def find_incentives_in_email_body(self):
        incentive_list = []
        finalized_incentive_list = []
        found_incentives_checker = False
        i = 0
        #Thunderbird incentive finder
        for tag in self.soup.find_all('td'):
            if str(tag.get('class')) == "['key-details']" or str(tag.get('class')) == "['x_key-details']":
                incentive_list.append([])
                children = tag.findChildren('td')
                for child in children:
                    if str(child.get('class')) == "['incentives-info']" or str(child.get('class')) == "['x_incentives-info']":
                        stripped_of_return = child.text
                        stripped_of_return = self.return_stripper(stripped_of_return)
                        incentive_list[i].append(stripped_of_return)
                        found_incentives_checker = True
                    else:
                        incentive_list[i].append(" - ")
                i += 1
        #Outlook incentive finder
        # for tag in self.soup.find_all('td'):
        #     if tag.findChild('p'):
        #         if tag.findChild('p').text == "Incentives:":
        #             incentive_list.append([])
        #             incentive_list[i].append(tag.find_next_sibling('td').findChild('p').text)
        #             found_incentives_checker = True
        #         else:
        #             incentive_list[i].append(" - ")
        #         print(incentive_list[i])
        #         i += 1


        if found_incentives_checker:
            for incentives in incentive_list:
                try:
                    finalized_incentive_list.append(incentives[1])
                except IndexError:
                    #I know this is bad.
                    incentives.append(" - ")
                    incentives.append(" - ")
                    finalized_incentive_list.append(incentives[1])
            return finalized_incentive_list
        else:
            return incentive_list


