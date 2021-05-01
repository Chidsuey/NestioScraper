from xlwt import Workbook, easyxf


class ExcelFileHandler:

    new_workbook = []
    new_worksheet = []
    new_workbook_counter = 0
    heading_style = easyxf('font: bold on; align: wrap on, vert center, horiz center')
    date_style = easyxf('align: horiz center, vert center', num_format_str='MM/DD/YY', )
    desc_style = easyxf('align: wrap on')
    reg_style = easyxf('align: horiz center, vert center')


    def __init__(self):
        self.row_offset = 2

    def excel_file_setup(self, owner_name):
        CONST_COLUMN_WIDTH_UNIT = 256
        self.new_workbook.append(Workbook())
        self.new_worksheet.append(self.new_workbook[self.new_workbook_counter]
                                  .add_sheet('sheet' + str(self.new_workbook_counter), cell_overwrite_ok=True))
        self.new_worksheet[self.new_workbook_counter].name = owner_name[0:31]
        """
        XLWT does not allow new worksheets to be created with a name longer than 31 characters (apparently an Excel
        limit). This bypasses the issue.
        """

        apartment_column = self.new_worksheet[self.new_workbook_counter].col(0)
        apartment_column.width = CONST_COLUMN_WIDTH_UNIT * 5
        address_column = self.new_worksheet[self.new_workbook_counter].col(1)
        address_column.width = CONST_COLUMN_WIDTH_UNIT * 30
        bed_column = self.new_worksheet[self.new_workbook_counter].col(4)
        bed_column.width = CONST_COLUMN_WIDTH_UNIT * 5
        bath_column = self.new_worksheet[self.new_workbook_counter].col(5)
        bath_column.width = CONST_COLUMN_WIDTH_UNIT * 5
        term_column = self.new_worksheet[self.new_workbook_counter].col(7)
        term_column.width = CONST_COLUMN_WIDTH_UNIT * 20
        description_column = self.new_worksheet[self.new_workbook_counter].col(9)
        description_column.width = CONST_COLUMN_WIDTH_UNIT * 120
        incentive_column = self.new_worksheet[self.new_workbook_counter].col(8)
        incentive_column.width = CONST_COLUMN_WIDTH_UNIT * 30

        column_headings = ["Apt", "Address", "Price", "Avail Date", "Bed", "Bath", "Size", "Term", "Incentives"
                           , "Description"]

        for i in range(0, len(column_headings)):
            self.new_worksheet[self.new_workbook_counter].write(0, i, column_headings[i], self.heading_style)


    def update_spreadsheet(self, finalized_info_list):
        change_style = easyxf('pattern: pattern solid, fore_colour green; align: horiz center, vert center')
        for i in range(0, len(finalized_info_list)):
            self.new_worksheet[self.new_workbook_counter].write(self.row_offset, 0, finalized_info_list[i][0], self.reg_style)
            self.new_worksheet[self.new_workbook_counter].write(self.row_offset, 1, finalized_info_list[i][1], self.reg_style)
            self.new_worksheet[self.new_workbook_counter].write(self.row_offset, 2, finalized_info_list[i][2], self.reg_style)
            self.new_worksheet[self.new_workbook_counter].write(self.row_offset, 3, finalized_info_list[i][3], self.date_style)
            self.new_worksheet[self.new_workbook_counter].write(self.row_offset, 4, finalized_info_list[i][4], self.reg_style)
            self.new_worksheet[self.new_workbook_counter].write(self.row_offset, 5, finalized_info_list[i][5], self.reg_style)
            self.new_worksheet[self.new_workbook_counter].write(self.row_offset, 6, finalized_info_list[i][6], self.reg_style)
            self.new_worksheet[self.new_workbook_counter].write(self.row_offset, 7, finalized_info_list[i][7], self.reg_style)
            self.new_worksheet[self.new_workbook_counter].write(self.row_offset, 8, finalized_info_list[i][8], self.reg_style)
            self.new_worksheet[self.new_workbook_counter].write(self.row_offset, 9, finalized_info_list[i][9], self.desc_style)
            self.new_worksheet[self.new_workbook_counter].row(self.row_offset).height_mismatch = True
            self.new_worksheet[self.new_workbook_counter].row(self.row_offset).height = 256
            if finalized_info_list[i][10] == "App":
                self.new_worksheet[self.new_workbook_counter].write(self.row_offset, 0, finalized_info_list[i][0], change_style)
            self.row_offset += 1

    def setup_generic_excel_file(self):
        self.new_workbook.append(Workbook())
        self.new_worksheet.append(self.new_workbook[self.new_workbook_counter]
                                  .add_sheet('sheet' + str(self.new_workbook_counter), cell_overwrite_ok=True))
        self.new_worksheet[self.new_workbook_counter].name = "Generic Name"

    def write_to_excel_file(self, row, column, data):
        self.new_worksheet[self.new_workbook_counter].write(row, column, data, self.reg_style)

    def finalize_spreadsheet(self, offset, total_listings, save_file_name):
        self.new_worksheet[self.new_workbook_counter]\
            .write(offset, 1, str(total_listings) + " total listings", self.reg_style)
        print(save_file_name[0:100])
        self.new_workbook[self.new_workbook_counter].save(save_file_name + '.xls')
        self.prepare_for_new_workbook()

    def prepare_for_new_workbook(self):
        self.new_workbook_counter += 1



class ExcelFileAdapter:
    finalized_data_dictionary = {"Apartment": "", "Address": "", "Price": "", "Available Date": "", "Bedrooms": ""
                                 , "Bathrooms": "", "Size": "", "Lease Term": "", "Incentives": "", "Description": ""
                                 , "Application": ""}
    finalized_data_list_for_single_entry = []

    def __init__(self, dict_of_data_to_be_formatted):
        self.dict_of_data_to_be_formatted = dict_of_data_to_be_formatted


    def adapt_info_for_output(self):
        """Takes a dictionary and returns a list"""
        for key in self.finalized_data_dictionary:
            if key in self.dict_of_data_to_be_formatted:
                self.finalized_data_dictionary[key] = self.dict_of_data_to_be_formatted[key]
        self.finalized_data_list_for_single_entry = [value for value in self.finalized_data_dictionary.values()]
        return self.finalized_data_list_for_single_entry

