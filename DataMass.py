import xlwt
import xlrd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import tkinter
from tkinter import *
from datetime import datetime
from tkinter import filedialog
import time
import os
import sys
import atexit

i = 0
j = 0
first_link = True;
link_parser = []
count = 2;
html_filename = "nothing"
options = Options()
options.headless = True
driver = ""
# log_file = open("ScraperLog.txt",'w+',encoding = 'utf-8')
sep = "\n"
no_detail_list = False
no_key_details_list = False
url_to_scrape = ('')
today = datetime.today()
now = datetime.now()
owner_name = 'default'
final_link_count = 0
final_formatted_filename = 'undefined'
excel_file_count = 0
new_wb = []
new_ws = []
# Styles
heading_style = xlwt.easyxf('font: bold on; align: wrap on, vert center, horiz center')
date_style = xlwt.easyxf('align: horiz center, vert center', num_format_str='MM/DD/YY', )
desc_style = xlwt.easyxf('align: wrap on')
reg_style = xlwt.easyxf('align: horiz center, vert center')


# ********************************************************************************

def exit_handler():
    driver.quit()


def log_file_manager(string):
    global log_file
    log_file.write(string + "\n")


def reset():  # Resets all necessary variable so the script can run again
    global i
    global j
    global first_link
    global link_parser
    global count
    i = 0
    j = 0
    link_parser = []
    first_link = True
    count = 2
    import_button.config(state=NORMAL)
    scrape_button.config(state=NORMAL)


def name_error_checker(strg):  # Removes characters Windows rejects in file names

    a = 0
    fixed_name = strg
    bad_characters = ["\\", "/", "?", "*", "|", ":", "\"", "<", ">"]
    for char in range(0, len(bad_characters)):
        a = fixed_name.find(bad_characters[char])
        if (a >= 0):
            fixed_name_split = fixed_name.split(bad_characters[char])
            fixed_name = " ".join(fixed_name_split)
        if (a == -1):
            a = 0;
    # log_file.write(fixed_name + '\n')
    return fixed_name


def open_file():  # Opens the dialog for choosing an html file
    global html_filename
    html_filename = filedialog.askopenfilename(parent=root, title='Choose a file')
    return str(html_filename)


def email_scrape():  # Parses email in html format to find all of the Nestio links to check
    global i
    global j
    global first_link
    global link_parser
    global count
    global html_filename
    global driver
    global final_link_count
    h3_string = ""
    coding_choice = coding.get()

    if html_filename != 'nothing':
        try:
            driver = webdriver.Firefox('K:/Nestio Email Scraper', options=options)
        except WebDriverException:
            print("Firefox may have needed update. Try again in a few seconds.")
            progress_text.set("Firefox may have needed update. Try again in a few seconds.")

        with open(html_filename, 'r', encoding=coding_choice) as html_file:
            soup = BeautifulSoup(html_file, 'html.parser')
        html_file.close()
        link_list = []
        final_link_list = []
        owner_name = []
        # find_incentives_in_email_body(soup)
        # for link in soup.find_all('a'):
        #	link_list.append(link.get('href'))

        for name in soup.find_all(alt=True):
            owner_name.append(name.get('alt'))
            i += 1;
        name_check = name_error_checker(owner_name[0])
        nameOwner(name_check)

        for tag in soup.find_all('h3'):
            h3_string = tag.get('class')
            if ((str(h3_string)) == "['listing-title']"):
                link_list.append(tag.a.get('href'))

        # for i in range(0,len(link_list)):

        #	if (link_list[i].startswith('https://urldefense.com/v3/__http:/email.nestio.com') or link_list[i].startswith('https://urldefense.com/v3/__http://email.nestio.com')):
        #		link_parser.append(link_list[i].split('-'))

        #		j+=1
        #		if (first_link):
        #			final_link_list.append(link_list[i])

        #			first_link = False;
        #			j-=1;
        #		elif (link_parser[j][3] != link_parser[j-1][3]):
        #			final_link_list.append(link_list[i])

        # final_link_list.pop() #There always seems to be two useless links that end up at the end of the list.
        # final_link_list.pop()
        final_link_count = len(link_list)
        length = len(link_list)
        for link in link_list:
            log_file_manager(link)
            scrape(link, count, length)
            count += 1;
            length -= 1;
    # length = len(link_list)#len(final_link_list)-1
    # for i in final_link_list:
    # scrape(i,count,length)
    # count += 1;
    # length -= 1;

    else:
        print('No or invalid file selected.')
        progress_text.set("No file selected to scrape.")


def scrape(scrape, count, length):  # Checks a single Nestio link and records the data on the worksheet
    links_left_text.set((str(length)) + " links to check.")
    root.update()
    global no_detail_list
    global no_key_details_list
    global excel_file_count
    log_file_manager("Link #" + str(count - 1) + ": " + scrape)
    url_to_scrape = scrape
    print("Accessing website...")
    progress_text.set("Accessing website...")
    root.update()

    print("Gathering data...")
    progress_text.set("Gathering data...")
    root.update()
    driver.get(url_to_scrape)
    time.sleep(7)  # delay to avoid some gathering issues

    # Data Gathering
    try:
        details = driver.find_element_by_class_name('detail-list')
        details_string = details.text
        details_list = details_string.splitlines()
    except NoSuchElementException:
        details_string = ("-")
        no_detail_list = True;
        log_file.write(" - details-list tag not found" + "\n")

    try:
        listing_key_details = driver.find_element_by_class_name('listing-key-details')
        listing_key_details_string = listing_key_details.text
        listing_key_details_list = listing_key_details_string.splitlines()
        for i in range(0, len(listing_key_details_list)):
            if (len(listing_key_details_list) < 3):
                listing_key_details_list.append('-')
    except NoSuchElementException:
        listing_key_details_string = ("-")
        listing_key_details_list = ['-', '-', '-']
        log_file.write(" - listing-key-details tag not found" + "\n")

    try:
        description = driver.find_element_by_xpath("//meta[@property='og:description']").get_attribute("content")
        description_string = description
        incentives_in_desc = incentiveFinder(description_string)


    except NoSuchElementException:
        description_string = ("-")
        incentives_in_desc = ["-"]
        log_file.write(" - description tag not found" + "\n")

    try:
        content = driver.find_element_by_class_name('check-list')
        content_string = content.text
    except NoSuchElementException:
        content = ("-")
        log_file.write(" - check-list tag not found" + "\n")

    try:
        listing_contact_info = driver.find_element_by_class_name('listing-contact-info')
        listing_contact_info_string = listing_contact_info.text
    except NoSuchElementException:
        listing_contact_info_string = ("-")
        log_file.write(" - listings-contact-info tag not found" + "\n")

    try:
        listing_title = driver.find_element_by_class_name('listing-title')
        listing_title_string = listing_title.text
        apt_num = listing_title_string.split('#')
    except NoSuchElementException:
        listing_title_string = ("-")
        apt_num = ['-', '-']
        log_file.write(" - listing-title tag not found" + "\n")

    try:
        lease_term = driver.find_element_by_class_name('lease-term')
        lease_term_string = lease_term.text
        lease_term_actual = lease_term_string.splitlines()
    except NoSuchElementException:
        lease_term_string = ("-")
        lease_term_actual = ["-", "-"]
        log_file.write(" - lease-term tag not found" + "\n")

    try:
        incentives = driver.find_element_by_class_name('incentives')
        incentives_string = incentives.text
        incentives_list = incentives_string.splitlines()

    except NoSuchElementException:
        incentives_list = ["-", "-"]
        log_file.write(" - incentives tag not found" + "\n")

    j = 0
    # "ListingID","Availablility","Price","Bed/Bath","Rooms","Floor","Lease Term","Pets","Updated","Features"
    details_list_parsed = ["No data", "No data", "No data", "No data", "No data", "No data", "No data", "No data",
                           "No data", "No data"]

    if (no_detail_list == False):
        for i in range(0, len(details_list)):
            if i % 2 != 0:
                details_list_parsed[j] = details_list[i]
                j += 1
    else:
        no_detail_list = False

    all_incentives = []
    for i in range(1, len(incentives_list)):
        all_incentives.append(incentives_list[i])
    for i in range(0, len(incentives_in_desc)):
        all_incentives.append(incentives_in_desc[i])

    print("Writing to file...")
    progress_text.set("Writing to file...")
    root.update()

    # Layout all the data into the excel file
    new_ws[excel_file_count].write(count, 0, apt_num[1], reg_style)
    new_ws[excel_file_count].write(count, 1, apt_num[0], reg_style)
    new_ws[excel_file_count].write(count, 2, details_list_parsed[2], reg_style)
    new_ws[excel_file_count].write(count, 3, details_list_parsed[1], date_style)
    new_ws[excel_file_count].write(count, 4, listing_key_details_list[0][0], reg_style)
    new_ws[excel_file_count].write(count, 5, listing_key_details_list[1][0], reg_style)
    new_ws[excel_file_count].write(count, 6, listing_key_details_list[2], reg_style)
    new_ws[excel_file_count].write(count, 7, lease_term_actual[1], reg_style)
    new_ws[excel_file_count].write(count, 8, sep.join(all_incentives), reg_style)
    new_ws[excel_file_count].write(count, 9, description_string, desc_style)
    new_ws[excel_file_count].row(count).height_mismatch = True
    new_ws[excel_file_count].row(count).height = 256

    if length <= 1:
        new_ws[excel_file_count].write(count + 2, 1, str(final_link_count) + " total listings", reg_style)
        new_wb[excel_file_count].save(final_formatted_filename + '.xls')
        print("Closing webdriver...")
        progress_text.set("Closing webdriver...")
        root.update()
        driver.quit()
        print("Finished!")
        progress_text.set("Finished!")
        links_left_text.set("")
        excel_file_count += 1;
        reset()
        root.update()
    else:
        print("Next link...")
        progress_text.set("Next link...")
        root.update()


def nameOwner(name):  # Gets the owner's name and formats the output file name
    new_ws[excel_file_count].name = name
    owner_name = name
    today_formatted = today.strftime("%b-%d-%y")
    time_formatted = now.strftime("%H%M%S")
    global final_formatted_filename
    final_formatted_filename = (owner_name + " (" + today_formatted + "_" + time_formatted + ")")
    new_wb[excel_file_count].save(final_formatted_filename + '.xls')
    global log_file
    log_file = open(final_formatted_filename + " Log.txt", 'w+', encoding='utf-8')


def incentiveFinder(description):  # Searches the incentives tag and the description for incentive phrases
    parse_list = []
    found_list = []
    search_list = ["one month free", "1 month free", "two month free", "2 month free", "two months free",
                   "2 months free", "one month op", "1 month op", "one month owner pays", "1 month owner pays"
        , "1.5 month free", "1.5 months free", "1/2 month free"]
    for i in search_list:
        parse_list.append(description.find(i))
    for i in range(0, len(parse_list)):
        if parse_list[i] != -1:
            found_list.append(description[parse_list[i]:parse_list[i] + len(search_list[i])])
    return found_list


def excel_file_setup():  # Preps the worksheet to receive data
    # Excel Export
    new_wb.append(xlwt.Workbook())
    new_ws.append(new_wb[excel_file_count].add_sheet('Owner Name'))
    # ownerName = new_ws.name

    # Column Widths
    apt_col = new_ws[excel_file_count].col(0)
    apt_col.width = 256 * 5
    address_col = new_ws[excel_file_count].col(1)
    address_col.width = 256 * 30
    bed_col = new_ws[excel_file_count].col(4)
    bed_col.width = 256 * 5
    bath_col = new_ws[excel_file_count].col(5)
    bath_col.width = 256 * 5
    term_col = new_ws[excel_file_count].col(7)
    term_col.width = 256 * 20
    desc_col = new_ws[excel_file_count].col(9)
    desc_col.width = 256 * 120
    ince_col = new_ws[excel_file_count].col(8)
    ince_col.width = 256 * 30

    # Column Headings
    heading = ["Apt", "Address", "Price", "Avail Date", "Bed", "Bath", "Size", "Term", "Incentives", "Description"]
    # Lays out all of the headings in the top row
    for i in range(0, len(heading)):
        new_ws[excel_file_count].write(0, i, heading[i], heading_style)


def find_incentives_in_email_body(s):
    soup = s;
    incentive_list = []
    test_link_list = []
    h3_string = "";
    for tag in soup.find_all('td'):
        if (str(tag.get('class')) == "['incentives-info']"):
            incentive_list.append(tag.text)


# GUI *************************************
root = Tk()
root.title("Nestio Scraper v1.0")
root.geometry("380x320")
root.resizable(0, 0)
progress_text = StringVar()
links_left_text = StringVar()
coding = StringVar()
coding.set('utf-8')

read_only_import_frame = Frame(root, height=35, width=380)
read_only_import_frame.grid()
scrape_button_frame = Frame(root, height=120, width=280)
scrape_button_frame.grid()
print_out_progress_frame = Frame(root, height=140, width=340)
print_out_progress_frame.grid()
import_text_box = Text(read_only_import_frame, height=1, width=53, state=DISABLED, font=("Arial", 8))
import_text_box.place(x=5, y=10)
print_out_progress_label = Label(print_out_progress_frame, height=10, width=20, textvariable=progress_text)
print_out_progress_label.place(x=100, y=10)
links_left_label = Label(print_out_progress_frame, height=1, width=20, textvariable=links_left_text)
links_left_label.place(x=100, y=5)


def import_button_click():
    global import_text_box
    open_file()
    import_text_box.config(state=NORMAL)
    import_text_box.delete(1.0, END)
    filename_parser = html_filename.split("/")
    parsed_filename = filename_parser.pop()
    import_text_box.insert(INSERT, str(parsed_filename))  # html_filename))
    import_text_box.config(state=DISABLED)


def scrape_button_click():
    import_button.config(state=DISABLED)
    scrape_button.config(state=DISABLED)
    excel_file_setup()
    email_scrape()


def options_button_click():
    options_window = Toplevel()
    ok_button = Button(options_window, text="Okay", command=options_window.destroy)
    radio_0 = Radiobutton(options_window, text="Outlook Encoding", variable=coding, value="utf-16")
    radio_1 = Radiobutton(options_window, text="Thunderbird Encoding", variable=coding, value="utf-8")
    radio_0.place(x=5, y=5)
    radio_1.place(x=5, y=30)
    ok_button.place(x=50, y=75)
    if (coding.get() == "utf-16"):
        radio_0.select()
    elif (coding.get() == "utf-8"):
        radio_1.select()

    options_window.mainloop()


# def test_button_click():


import_button = Button(read_only_import_frame, text="Import", command=import_button_click)
import_button.place(x=330, y=5)
scrape_button = Button(scrape_button_frame, text="Scrape!", height=3, width=20, command=scrape_button_click)
scrape_button.place(x=65, y=10)
quit_button = Button(print_out_progress_frame, text="Quit", command=sys.exit)
quit_button.place(x=300, y=115)
options_button = Button(print_out_progress_frame, text="Options", command=options_button_click)
options_button.place(x=5, y=115)
# test_button = Button(print_out_progress_frame, text= "Test", command = test_button_click)
# test_button.place(x=50, y=115)

root.mainloop()
atexit.register(exit_handler)

