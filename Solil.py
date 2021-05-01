import HTMLFileScraper
import FileHandler
import ExcelFileHandler
html_file_scraper = HTMLFileScraper.HTMLFileScraper()
file_handler = FileHandler.FileHandler()


class Solil:

    def __init__(self, root, coding):
        self.root = root
        self.coding = coding
        self.solil_file = ""
        self.total_listings = 0

    def open_html(self):
        self.solil_file = file_handler.open_html_file(self.root)

    def turn_email_into_soup(self):
        html_file_scraper.convert_html_to_beautiful_soup_file(self.solil_file, self.coding)

    def gather_data(self):
        data_matrix = []
        for tag in html_file_scraper.soup.find_all('tr'):
            listing_list = [n.text for n in tag.find_all('td')]
            if self.data_exceptions(listing_list):
                continue
            if "bgcolor" in tag.find('td').attrs:
                listing_list.append(self.color_converter(tag.find('td').attrs["bgcolor"]))
            else:
                listing_list.append("Colorless")
            data_matrix.append(listing_list)
        self.total_listings = self.correct_listings_count(data_matrix)
        return data_matrix

    def correct_listings_count(self, listings):
        corrected_listings = [listing for listing in listings if "TBD" not in listing[4]]
        return len(corrected_listings)

    def data_exceptions(self, listing_list):
        if len(listing_list) < 8:
            return True
        if listing_list[0] == "Address":
            return True
        if listing_list[4] == "TBD":
            return True

    def color_converter(self, color):
        try:
            color_dict = {"#FFFF00": "1 OP or 13th Free",
                          "#FFFF81": "1 OP or 13th Free",
                          "#BCD6ED": "1 OP and 13th Free",
                          "#D9D9D9": "Gray",
                          "#DDEBF7": "1 OP and 13th Free",
                          "#F4AF84": "1 OP and 13th Free",
                          "#F8CAAC": "1 OP and 13th Free",
                          "#FFC000": "1 OP and 13th Free",
                          "#FFDA64": "1 OP and 13th Free"}
            return color_dict[color]
        except KeyError:
            return "Color Not Found"

    def compare_email_data(self, old_email_data, new_email_data):
        difference_matrix = []
        rented_list = []
        new_listings = []
        data_types = ["Address: ", "Apt: ", "Bed: ", "Bath: ", "Price: ", "Avail: ", "Super: ", "Access: ",
                      "Incentives: "]
        difference_count = 0
        for i in range(0, len(old_email_data)):
            if len(old_email_data[i]) < 2:
                old_email_data[i].append("dummy")
            old_listing = False
            first_difference = True
            for j in range(0, len(new_email_data)):
                if len(new_email_data[j]) < 2:
                    new_email_data[j].append("dummy")
                if old_email_data[i][0] == new_email_data[j][0] and old_email_data[i][1] == new_email_data[j][1]:
                    old_listing = True
                    for k in range(2, len(new_email_data[j])):
                        if old_email_data[i][k] != new_email_data[j][k]:
                            if first_difference:
                                difference_matrix.append([])
                                difference_matrix[difference_count].append(new_email_data[j][0])
                                difference_matrix[difference_count].append(new_email_data[j][1])
                                first_difference = False
                            if new_email_data[j][k] is not None:
                                difference_matrix[difference_count].append(data_types[k] + " " + new_email_data[j][k])

                    if not first_difference:
                        difference_count += 1
                    break
            if not old_listing:
                rented_list.append(old_email_data[i])

        for i in range(0, len(new_email_data)):
            new_listing = True
            for j in range(0, len(old_email_data)):
                if new_email_data[i][0] == old_email_data[j][0] and new_email_data[i][1] == old_email_data[j][1]:
                    new_listing = False
                    break
            if new_listing:
                new_listings.append(new_email_data[i])

        #self.print_data(difference_matrix, rented_list, new_listings)
        self.adapt_data_for_output(difference_matrix, rented_list, new_listings)


    def print_data(self, difference_matrix, rented_list, new_listings):
        for g in difference_matrix:
            print(g)
        for h in rented_list:
            print("Rented: " + h[0] + " - " + h[1])
        for i in new_listings:
            print("New listing: ")
            print(i)

    def adapt_data_for_output(self, changed_listings, rented_listings, new_listings):
        excel_file_handler = ExcelFileHandler.ExcelFileHandler()
        excel_file_handler.setup_generic_excel_file()
        row_offset = 0
        excel_file_handler.write_to_excel_file(row_offset, 0, "Changed listings:")
        row_offset += 2
        for i in range(0, len(changed_listings)):
            for j, k in enumerate(changed_listings[i]):
                excel_file_handler.write_to_excel_file(i + row_offset, j, k)
        row_offset += len(changed_listings) + 1
        excel_file_handler.write_to_excel_file(row_offset, 0, "Rented listings:")
        row_offset += 2
        for i in range(0, len(rented_listings)):
            excel_file_handler.write_to_excel_file(i + row_offset, 0, rented_listings[i][0] + " - " + rented_listings[i][1])
        row_offset += len(rented_listings) + 1
        excel_file_handler.write_to_excel_file(row_offset, 0, "New listings:")
        row_offset += 2
        for i in range(0, len(new_listings)):
            for j, k in enumerate(new_listings[i]):
                excel_file_handler.write_to_excel_file(i + row_offset, j, k)
        row_offset += len(new_listings) + 1
        excel_file_handler.finalize_spreadsheet(row_offset + 2, self.total_listings, "Solil")