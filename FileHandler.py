from tkinter import filedialog
from tkinter import StringVar
from datetime import datetime
from os import walk


class FileHandler:

    def __init__(self):
        self.prior_selected_file = "null"
        #self.file_path = StringVar()
        #self.folder_path = StringVar()



    def open_html_file(self, root):
        html_file = filedialog.askopenfilename(parent=root, title='Choose a file')
        return self.check_if_file_or_folder_already_selected(html_file)


    def open_directory(self, root):
        html_file_directory = filedialog.askdirectory(parent=root, title='Choose a folder')
        return self.check_if_file_or_folder_already_selected(html_file_directory)


    def check_if_file_or_folder_already_selected(self, fifo):
        if fifo:
            self.prior_selected_file = fifo
        if not fifo:
            if self.prior_selected_file == "null":
                fifo = "No file or folder selected"
            else:
                fifo = self.prior_selected_file
        return fifo

    def create_list_of_files_in_directory(self, directory):
        list_of_files_in_directory = []
        for folders, sub_folders, files in (walk(directory)):
            for file in files:
                if '.html' in file or '.htm' in file:
                    list_of_files_in_directory.append(folders + '/' + file)
        return list_of_files_in_directory



    def get_just_the_file_name(self, html_file):
        filename_parser = html_file.split("/")
        just_the_file_name = filename_parser.pop()
        return just_the_file_name

    def format_file_name_output(self, owner_name):
        date_and_time = self.date_and_time_snapshot()
        final_formatted_filename = (owner_name + " (" + date_and_time[0] + "_" + date_and_time[1] + ")")
        return final_formatted_filename

    def date_and_time_snapshot(self):
        date = datetime.today()
        time = datetime.now()
        date_formatted = date.strftime("%b-%d-%y")
        time_formatted = time.strftime("%H%M%S")
        return date_formatted, time_formatted