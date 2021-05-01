from Main import Main

class Buttons:

    @staticmethod
    def import_button_click():

        print("something finally happened")
        Main.html_file = Main.fileHandler.open_html_file(Main.gui)
        just_the_file_name = Main.fileHandler.get_just_the_file_name()
        Main.gui.import_text_box.config(state=NORMAL)
        Main.gui.import_text_box.delete(1.0, END)
        Main.gui.import_text_box.insert(INSERT, str(just_the_file_name))
        Main.gui.import_text_box.config(state=DISABLED)


    def scrape_button_click(self):
        Main.gui.import_button.config(state=DISABLED)
        Main.gui.scrape_button.config(state=DISABLED)
        Main.excelFileHandler.excel_file_setup()
        link_list = Main.htmlFileScraper.scrape_html_file_for_links(Main.html_file, Main.coding)
        Main.owner_name = Main.htmlFileScraper.owner_name_checked_for_errors
        final_formatted_file_name = Main.fileHandler.format_file_name_output(Main.owner_name)
        Main.log_file = Main.logHandler.create_new_log(final_formatted_file_name)
        finalized_info_list = Main.linkScraper.scrape_links_for_data(link_list, Main.gui.links_remaining_text)
        Main.excelFileHandler.update_spreadsheet(finalized_info_list)

    def options_button_click(self):
        options_window = Main.gui.options_window()
        if Main.coding.get() == "utf-16":
            options_window.radio_0.select()
        elif Main.coding.get() == "utf-8":
            options_window.radio_1.select()

        options_window.mainloop()