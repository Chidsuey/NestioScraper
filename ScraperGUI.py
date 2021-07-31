from tkinter import *
from _io import TextIOWrapper
import FileHandler
import LCLemle
import LogHandler
import ExcelFileHandler
import HTMLFileScraper
import LinkScraper
import DataComparison
import ElevenThirteenManhattan
import Paley
import TheEugene
import CitySkyline
import Bettina
import R9300
import Solil
import Eberhart
import Metronest
import Harlington
import time
import sys


fileHandler = FileHandler.FileHandler()
logHandler = LogHandler.LogHandler()
excelFileHandler = ExcelFileHandler.ExcelFileHandler()
htmlFileScraper = HTMLFileScraper.HTMLFileScraper()
linkScraper = LinkScraper.LinkScraper()
ETManhattan = ElevenThirteenManhattan.ElevenThirteenManhattan()
theEugene = TheEugene.TheEugene()


class GUI:

    progress_text = StringVar
    links_remaining_text = StringVar
    coding = StringVar
    file_folder_import_switch = StringVar

    owner_name = 'owner_name'
    html_file = 'html_file'
    html_file_directory = 'html_file_directory'
    log_file = TextIOWrapper


    import_button = Button
    scrape_button = Button
    quit_button = Button
    options_button = Button
    link_button = Button
    test_button = Button
    modules_button = Button
    comparison_button = Button
    root = Tk
    radio_file = Radiobutton
    radio_folder = Radiobutton

    read_only_import_frame = Frame
    scrape_button_frame = Frame
    print_out_progress_frame = Frame
    import_text_box = Text
    print_out_progress_label = Label
    links_remaining_label = Label



    def __init__(self):
        self.root = self.create_root_window()
        self.create_frames()
        self.create_stringVars()
        self.create_buttons()
        self.create_labels()


    def create_stringVars(self):
        self.progress_text = StringVar()
        self.progress_text.set('Waiting to begin!')
        self.links_remaining_text = StringVar()
        self.links_remaining_text.set("")
        self.coding = StringVar()
        self.coding.set('cp1252')
        self.file_folder_import_switch = StringVar()
        self.file_folder_import_switch.set('file')

    def create_root_window(self):
        root = Tk()
        root.title("Nestio Scraper v 1.2")
        root.geometry("380x320")
        root.resizable(0, 0)
        return root

    def create_frames(self):
        self.read_only_import_frame = Frame(self.root, height=50, width=380)
        self.read_only_import_frame.grid()
        self.scrape_button_frame = Frame(self.root, height=120, width=280)
        self.scrape_button_frame.grid()
        self.print_out_progress_frame = Frame(self.root, height=140, width=340)
        self.print_out_progress_frame.grid()
        self.import_text_box = Text(self.read_only_import_frame, height=1, width=53, state=DISABLED, font=("Arial", 8))
        self.import_text_box.place(x=5, y=10)


    def create_labels(self):
        self.print_out_progress_label = Label(self.print_out_progress_frame, height=10, width=20,
                                              textvariable=self.progress_text)
        self.print_out_progress_label.place(x=100, y=10)
        self.links_remaining_label = Label(self.print_out_progress_frame, height=1, width=20,
                                           textvariable=self.links_remaining_text)
        self.links_remaining_label.place(x=100, y=5)

    def create_buttons(self):
        self.import_button = Button(self.read_only_import_frame, text="Import", command=self.import_button_click)
        self.import_button.place(x=330, y=5)
        self.radio_file = Radiobutton(self.read_only_import_frame, text="Fi", variable=self.file_folder_import_switch, value="file", command=lambda: self.set_import_box_text("No file or folder selected"))
        self.radio_file.place(x=300, y=30)
        self.radio_folder = Radiobutton(self.read_only_import_frame, text="Fo", variable=self.file_folder_import_switch, value="folder", command=lambda: self.set_import_box_text("No file or folder selected"))
        self.radio_folder.place(x=340, y=30)
        self.scrape_button = Button(self.scrape_button_frame, text="Scrape!", height=3, width=20,
                                    command=self.scrape_button_click)
        self.scrape_button.place(x=65, y=10)
        self.quit_button = Button(self.print_out_progress_frame, text="Quit", command=self.quit_button_click)
        self.quit_button.place(x=300, y=115)
        self.options_button = Button(self.print_out_progress_frame, text="Options", command=self.options_button_click)
        self.options_button.place(x=5, y=115)
        self.link_button = Button(self.print_out_progress_frame, text="Soup", command=self.link_window)
        self.link_button.place(x=5, y=85)
        self.test_button = Button(self.print_out_progress_frame, text="Test",command=self.test_something)
        self.test_button.place(x=5, y=55)
        self.modules_button = Button(self.print_out_progress_frame,text="Modules", command=self.modules_window)
        self.modules_button.place(x=5, y=85)
        self.comparison_button = Button(self.print_out_progress_frame, text="Compare", command=self.comparison_window)
        self.comparison_button.place(x=5, y=25)

    def set_progress_text(self, text):
        self.progress_text.set(text)
        self.root.update()

    def set_links_remaining_text(self, text):
        self.links_remaining_text.set(text)
        self.root.update()

    def set_import_box_text(self, text):
        self.import_text_box.config(state=NORMAL)
        self.import_text_box.delete(1.0, END)
        self.import_text_box.insert(INSERT, str(text))
        self.import_text_box.config(state=DISABLED)

    def import_button_click(self):
        just_the_file_name = ""
        self.set_progress_text("Waiting to begin!")
        if self.file_folder_import_switch.get() == 'file':
            self.html_file = fileHandler.open_html_file(self.root)
            just_the_file_name = fileHandler.get_just_the_file_name(self.html_file)
        elif self.file_folder_import_switch.get() == 'folder':
            self.html_file_directory = fileHandler.open_directory(self.root)
            just_the_file_name = fileHandler.get_just_the_file_name(self.html_file_directory)
        self.set_import_box_text(just_the_file_name)

    def scrape_button_click(self):
        self.import_button.config(state=DISABLED)
        self.scrape_button.config(state=DISABLED)
        if self.file_folder_import_switch.get() == "file":
            link_list = htmlFileScraper.scrape_html_file_for_links(self.html_file, self.coding)
            incentives_list = htmlFileScraper.find_incentives_in_email_body()
            self.set_progress_text('Preparing to scrape...')
            self.owner_name = htmlFileScraper.owner_name_checked_for_errors
            final_formatted_file_name = fileHandler.format_file_name_output(self.owner_name)
            self.log_file = logHandler.create_new_log(final_formatted_file_name)
            finalized_info_list = linkScraper.scrape_links_for_data(link_list, self.set_links_remaining_text,
                                                                    self.set_progress_text, logHandler, self.log_file, incentives_list)

            self.set_progress_text('Finalizing spreadsheet...')
            excelFileHandler.excel_file_setup(self.owner_name)
            excelFileHandler.update_spreadsheet(finalized_info_list)
            excelFileHandler.finalize_spreadsheet(excelFileHandler.row_offset + 1, len(finalized_info_list), final_formatted_file_name)
            self.reset()
        elif self.file_folder_import_switch.get() == "folder":
            list_of_files_in_directory = fileHandler.create_list_of_files_in_directory(self.html_file_directory)
            for file in list_of_files_in_directory:
                try:
                    self.html_file = file
                    link_list = htmlFileScraper.scrape_html_file_for_links(self.html_file, self.coding)
                    incentives_list = htmlFileScraper.find_incentives_in_email_body()
                    self.set_progress_text('Preparing to scrape...')
                    self.owner_name = htmlFileScraper.owner_name_checked_for_errors
                    final_formatted_file_name = fileHandler.format_file_name_output(self.owner_name)
                    self.log_file = logHandler.create_new_log(final_formatted_file_name)
                    finalized_info_list = linkScraper.scrape_links_for_data(link_list, self.set_links_remaining_text,
                                                                            self.set_progress_text, logHandler,
                                                                            self.log_file, incentives_list)

                    self.set_progress_text('Finalizing spreadsheet...')
                    excelFileHandler.excel_file_setup(self.owner_name)
                    excelFileHandler.update_spreadsheet(finalized_info_list)
                    excelFileHandler.finalize_spreadsheet(excelFileHandler.row_offset + 1, len(finalized_info_list), final_formatted_file_name)
                    self.reset()
                except:
                    continue

    def options_button_click(self):
        options_window = Toplevel()
        ok_button = Button(options_window, text="Okay", command=options_window.destroy)
        radio_0 = Radiobutton(options_window, text="Outlook", variable=self.coding, value="utf-16")
        radio_1 = Radiobutton(options_window, text="Thunderbird Encoding", variable=self.coding, value="cp1252")
        radio_2 = Radiobutton(options_window, text="City Skyline", variable=self.coding, value="utf-8")
        radio_0.place(x=5, y=5)
        radio_1.place(x=5, y=30)
        radio_2.place(x=5, y=55)
        ok_button.place(x=50, y=75)

    def quit_button_click(self):
        sys.exit()


    def link_window(self):
        link_window = Toplevel()
        link_entry = StringVar()
        ok_button = Button(link_window, text="Okay", command=lambda: [self.just_scrape_one_link(link_entry.get()), link_window.destroy()])
        ok_button.pack()
        link_entry_box = Entry(link_window, textvariable=link_entry)
        link_entry_box.pack()

    def modules_window(self):
        modules_window = Toplevel()
        self.module_buttons(modules_window)


    def module_buttons(self, window):
        paley_button = Button(window, text="Paley", command=self.paley)
        paley_button.pack()
        lclemle_button = Button(window, text="LC Lemle", command=self.lclemle)
        lclemle_button.pack()
        harlington_button = Button(window, text="Harlington", command=self.harlington)
        harlington_button.pack()
        e_t_manhattan_button = Button(window, text="1133 Manhattan", command=self.scrape_eleven_thirteen_manhattan)
        e_t_manhattan_button.pack()
        the_eugene_button = Button(window, text="The Eugene", command=self.scrape_the_eugene)
        the_eugene_button.pack()
        city_skyline_button = Button(window, text="City Skyline", command=self.city_skyline)
        city_skyline_button.pack()
        bettina_button = Button(window, text="Bettina", command=self.bettina)
        bettina_button.pack()
        realty_9300_button = Button(window, text="9300 Realty", command=self.realty_9300)
        realty_9300_button.pack()
        solil = Button(window, text="Solil", command=self.solil)
        solil.pack()



    def just_scrape_one_link(self, link_entry):
        linkScraper.open_webdriver(self.set_progress_text)
        link_log = logHandler.create_new_log("Link")
        linkScraper.driver.get(link_entry)
        time.sleep(3)
        logHandler.update_log(link_log, linkScraper.driver.page_source)
        linkScraper.close_driver()
        link_log.close()
        return linkScraper.driver.page_source

    def scrape_eleven_thirteen_manhattan(self):
        linkScraper.open_webdriver(self.set_progress_text)
        linkScraper.driver.get("https://www.1133manhattan.com/apartments/ny/brooklyn/floor-plans#/categories/all/floorplans")
        time.sleep(3)
        finalized_info_list = ETManhattan.get_apartment_links(linkScraper.driver)
        ETManhattan.output_all_the_info(finalized_info_list, fileHandler.date_and_time_snapshot())
        linkScraper.close_driver()
        pass

    def scrape_the_eugene(self):
        linkScraper.open_webdriver(self.set_progress_text)
        linkScraper.driver.get("https://theeugenenyc.com/availability/")
        finalized_info_list = theEugene.scrape_data(linkScraper.driver, self.set_progress_text)
        theEugene.output_all_the_info(finalized_info_list, fileHandler.date_and_time_snapshot())
        linkScraper.close_driver()

    def lclemle(self):
        linkScraper.open_webdriver(self.set_progress_text)
        lclemle = LCLemle.LCLemle(excelFileHandler, linkScraper.driver)
        lclemle.do_all_the_things(fileHandler.date_and_time_snapshot())

    def paley(self):
        linkScraper.open_webdriver(self.set_progress_text)
        paley = Paley.Paley(excelFileHandler, linkScraper.driver)
        paley.do_all_the_things(fileHandler.date_and_time_snapshot())

    def test_something(self):
        pass
        # linkScraper.open_webdriver(self.set_progress_text)
        # paley = Paley.Paley(excelFileHandler, linkScraper.driver)
        # paley.do_all_the_things(fileHandler.date_and_time_snapshot())
        #self.just_scrape_one_link("https://nestiolistings.com/p/listing/105/3402078/10/5kj-2f285a46f408e4bdf6b0/?utm_source=email-blast&utm_medium=inline")
        #with open(self.html_file) as f:

        #    print(f.encoding)
        # pass
    def harlington(self):
        linkScraper.open_webdriver(self.set_progress_text)
        harlington = Harlington.Harlington(excelFileHandler, linkScraper.driver)
        harlington.do_all_the_things(fileHandler.date_and_time_snapshot())


    def Metronest(self):
        metronest = Metronest.Metronest(self.root, self.coding)
        metronest.open_html()
        metronest.turn_email_into_soup()
        old_data = metronest.gather_data()
        metronest.open_html()
        metronest.turn_email_into_soup()
        new_data = metronest.gather_data()
        metronest.compare_email_data(old_data, new_data)

    def comparison_window(self):
        comparison_window = Toplevel()
        dataComparison = DataComparison.DataComparison(comparison_window)
        dataComparison.comparison_window_layout()

    def city_skyline(self):
        citySkyline = CitySkyline.CitySkyline(self.root, self.coding)
        citySkyline.open_email()
        citySkyline.turn_email_into_soup()
        old_email_data = citySkyline.matrix_email_data()
        citySkyline.open_email()
        citySkyline.turn_email_into_soup()
        new_email_data = citySkyline.matrix_email_data()
        citySkyline.compare_email_data(old_email_data, new_email_data)

    def realty_9300(self):
        realty_9300 = R9300.Realty9300(self.root, self.coding)
        realty_9300.open_email()
        realty_9300.turn_email_into_soup()
        old_ml_data = realty_9300.matrix_email_data()
        realty_9300.open_email()
        realty_9300.turn_email_into_soup()
        new_ml_data = realty_9300.matrix_email_data()
        realty_9300.compare_email_data(old_ml_data, new_ml_data)

    def solil(self):
        solil = Solil.Solil(self.root, self.coding)
        solil.open_html()
        solil.turn_email_into_soup()
        old_data = solil.gather_data()
        solil.open_html()
        solil.turn_email_into_soup()
        new_data = solil.gather_data()
        solil.compare_email_data(old_data, new_data)


    def bettina(self):
        linkScraper.open_webdriver(self.set_progress_text)
        linkScraper.driver.get("https://www.bettinaequities.com/availabilites/")
        bettina = Bettina.Bettina(excelFileHandler, linkScraper.driver)
        bettina.do_all_the_things(fileHandler.date_and_time_snapshot())
        # pre_finalized_info_list = bettina.matrix_data_from_website(linkScraper.driver)
        # bettina.output_all_the_info(pre_finalized_info_list, fileHandler.date_and_time_snapshot())
        # linkScraper.close_driver()

    def eberhart(self):
        eberhart = Eberhart.Eberhart(self.just_scrape_one_link)

    def reset(self):
        self.import_button.config(state=NORMAL)
        self.scrape_button.config(state=NORMAL)
        logHandler.finalize_log(self.log_file)
        self.set_progress_text("Waiting to begin!")
        self.set_links_remaining_text(" ")
        linkScraper.link_counter = 0
        excelFileHandler.row_offset = 2

