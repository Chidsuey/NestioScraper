import xlrd
import xlwt
from tkinter import *
import FileHandler
from xlutils.copy import copy


class DataComparison:
    CONST_ROW_BUFFER = 2
    change_style = xlwt.easyxf('pattern: pattern solid, fore_colour red; align: horiz center, vert center')
    comparison_file_text1 = Text
    comparison_file_import_button_1 = Button
    comparison_file_text2 = Text
    comparison_file_import_button_2 = Button
    compare_button = Button
    first_file = ""
    second_file = ""
    buttons_state = True

    def __init__(self, window):
        self.fileHandler = FileHandler.FileHandler()
        self.window = window

    def open_workbooks(self):
        old_workbook = xlrd.open_workbook(filename=self.first_file)
        new_workbook = xlrd.open_workbook(filename=self.second_file)
        return old_workbook, new_workbook

    def matrix_the_data_for_comparison(self, document_to_be_compared_to):
        excel_sheet = document_to_be_compared_to.sheet_by_index(0)
        data_matrix = []
        listings_count = self.get_number_of_listings(excel_sheet)
        for i in range(self.CONST_ROW_BUFFER, listings_count+self.CONST_ROW_BUFFER):
            data_matrix.append(excel_sheet.row_values(i))
        return data_matrix

    def get_number_of_listings(self, excel_sheet):
        i = 2
        try:
            while excel_sheet.cell(i, 0).value != '':
                i += 1
                if i > 1000:
                    print("The loop is broken.")
                    break
            return i-2
        except:
            return -1


    def comparison_window_layout(self):
        self.comparison_file_text1 = Text(self.window, height=1, width=53, state=DISABLED, font=("Arial", 8))
        self.comparison_file_text1.pack()
        self.comparison_file_import_button_1 = Button(self.window, text="Import", command=self.comparison_file_import_button_1_click)
        self.comparison_file_import_button_1.pack()
        self.comparison_file_text2 = Text(self.window, height=1, width=53, state=DISABLED, font=("Arial", 8))
        self.comparison_file_text2.pack()
        self.comparison_file_import_button_2 = Button(self.window, text="Import", command=self.comparison_file_import_button_2_click)
        self.comparison_file_import_button_2.pack()
        self.compare_button = Button(self.window, text="Compare", command=self.compare_files)
        self.compare_button.pack()

    def comparison_file_import_button_1_click(self):
        self.first_file = self.fileHandler.open_html_file(self.window)
        just_the_file_name = self.fileHandler.get_just_the_file_name(self.first_file)
        self.comparison_file_text1.config(state=NORMAL)
        self.comparison_file_text1.delete(1.0, END)
        self.comparison_file_text1.insert(INSERT, str(just_the_file_name))
        self.comparison_file_text1.config(state=DISABLED)


    def comparison_file_import_button_2_click(self):
        self.second_file = self.fileHandler.open_html_file(self.window)
        just_the_file_name = self.fileHandler.get_just_the_file_name(self.second_file)
        self.comparison_file_text2.config(state=NORMAL)
        self.comparison_file_text2.delete(1.0, END)
        self.comparison_file_text2.insert(INSERT, str(just_the_file_name))
        self.comparison_file_text2.config(state=DISABLED)

    def compare_files(self):
        self.freeze_and_unfreeze_buttons()
        file_check = self.check_for_both_files_and_format()
        new_listing = True
        if file_check:
            difference_matrix = []
            rented_listings = []
            tuple_of_workbooks = self.open_workbooks()
            old_file_being_compared = tuple_of_workbooks[0]
            new_file_being_compared = tuple_of_workbooks[1]
            old_file_being_compared_data_matrix = self.matrix_the_data_for_comparison(old_file_being_compared)
            new_file_being_compared_data_matrix = self.matrix_the_data_for_comparison(new_file_being_compared)

            for i in range(0, len(new_file_being_compared_data_matrix)):
                difference_matrix.append([])
                for j in range(0, len(old_file_being_compared_data_matrix)):
                    new_listing = True
                    if (new_file_being_compared_data_matrix[i][0] == old_file_being_compared_data_matrix[j][0]) and \
                            (new_file_being_compared_data_matrix[i][1] == old_file_being_compared_data_matrix[j][1]):
                        for k in range(0, len(new_file_being_compared_data_matrix[i])):
                            difference_matrix[i].append("same")
                            try:
                                if new_file_being_compared_data_matrix[i][k] != old_file_being_compared_data_matrix[j][k]:
                                    difference_matrix[i][k] = "changed"
                            except IndexError:
                                print("I dunno")
                        new_listing = False
                        break

                if new_listing:
                    difference_matrix[i].append("new")

            for i in range(0, len(old_file_being_compared_data_matrix)):
                rented_listing = True
                for j in range(0, len(new_file_being_compared_data_matrix)):
                    if old_file_being_compared_data_matrix[i][0] == new_file_being_compared_data_matrix[j][0] and \
                            old_file_being_compared_data_matrix[i][1] == new_file_being_compared_data_matrix[j][1]:
                        rented_listing = False
                        break
                if rented_listing:
                    rented_listings.append(old_file_being_compared_data_matrix[i][0])
                    rented_listings.append(old_file_being_compared_data_matrix[i][1])

            print(rented_listings)
            self.update_new_spreadsheet_with_comparison_data(new_file_being_compared, difference_matrix, rented_listings)
        self.freeze_and_unfreeze_buttons()

    def update_new_spreadsheet_with_comparison_data(self, excel_file, difference_matrix, rented_listings):
        workbook = copy(excel_file)
        worksheet = workbook.get_sheet(0)
        self.format_excel_file(worksheet)
        row_offset = 2

        listings_count = self.get_number_of_listings(excel_file.sheet_by_index(0))
        for i in range(self.CONST_ROW_BUFFER, listings_count + self.CONST_ROW_BUFFER):
            if difference_matrix[i-self.CONST_ROW_BUFFER][0] == "same":
                for j in range(0, len(difference_matrix[i-self.CONST_ROW_BUFFER])):
                    if difference_matrix[i-self.CONST_ROW_BUFFER][j] == "changed":
                        worksheet.write(i, j, excel_file.sheet_by_index(0).cell(i, j).value, self.change_style)

            if difference_matrix[i-self.CONST_ROW_BUFFER][0] == "new":
                worksheet.write(i, 0, excel_file.sheet_by_index(0).cell(i, 0).value, self.change_style)
            worksheet.row(row_offset).height_mismatch = True
            worksheet.row(row_offset).height = 256
            row_offset += 1

        self.print_rented_listings(rented_listings, worksheet, listings_count)
        workbook.save(worksheet.name + ' (Changes).xls')

    def print_rented_listings(self, rented_listings, worksheet, listings_count):
        counter = 5
        string = ""
        for i, j in enumerate(rented_listings):
            if i % 2 == 0:
                string = j
            else:
                worksheet.write(listings_count + counter, 1, "Rented: " + string + " - " + j)
                counter += 1

    def format_excel_file(self, worksheet):
        # I don't feel good about this because I'm just copy/pasting from ExcelFileHandler because I badly wrote it.
        # But. Here we are.
        CONST_COLUMN_WIDTH_UNIT = 256
        apartment_column = worksheet.col(0)
        apartment_column.width = CONST_COLUMN_WIDTH_UNIT * 5
        address_column = worksheet.col(1)
        address_column.width = CONST_COLUMN_WIDTH_UNIT * 30
        bed_column = worksheet.col(4)
        bed_column.width = CONST_COLUMN_WIDTH_UNIT * 5
        bath_column = worksheet.col(5)
        bath_column.width = CONST_COLUMN_WIDTH_UNIT * 5
        term_column = worksheet.col(7)
        term_column.width = CONST_COLUMN_WIDTH_UNIT * 20
        description_column = worksheet.col(9)
        description_column.width = CONST_COLUMN_WIDTH_UNIT * 120
        incentive_column = worksheet.col(8)
        incentive_column.width = CONST_COLUMN_WIDTH_UNIT * 30

    def freeze_and_unfreeze_buttons(self):
        if self.buttons_state:
            self.comparison_file_import_button_1.config(state=DISABLED)
            self.comparison_file_import_button_2.config(state=DISABLED)
            self.buttons_state = not self.buttons_state
        else:
            self.comparison_file_import_button_1.config(state=NORMAL)
            self.comparison_file_import_button_2.config(state=NORMAL)
            self.buttons_state = not self.buttons_state

    def check_for_both_files_and_format(self):
        if self.first_file == "" or self.second_file == "":
            print("Select two files to compare.")
            self.freeze_and_unfreeze_buttons()
            return False
        #else if check for proper file format as well
        else:
            return True
