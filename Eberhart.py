"""
id = resultRow# - Try string literal to change numbers. Run try and except to make sure it stops when it runs out of listings.
within the id - div class="prop-address">
                        <span class="propertyAddress">316 East 84th Street 5R</span> - Split at last space

                 <div class="display-icons row-fluid">
                            <ul>
                                <li data-selenium-id="LVRents" class="prop-rent featured-rent-text">$2,875.00</li>
                                <li data-selenium-id="LVSQFTs" class="prop-area" style="height: 25px;"></li>
                                <li data-selenium-id="LVBeds" class="prop-beds ">2</li>
                                <li data-selenium-id="LVBaths" class="prop-baths ">1.00</li>
                <div class="hidden specials-popover-content popover-content">
                                2 Months Free Rent
                            </div>
This is the "Next" button for getting to more results. <a href="javascript:void(0)" class="paginationNumber" onclick="PSMapPaginationClick(4)">Next</a>
"""


class Eberhart:

    def __init__(self, just_scrape_one_link):
        self.just_scrape_one_link = just_scrape_one_link
        self.page_data = ""

    def open_link_to_get_data(self):
        return self.just_scrape_one_link("https://www.eberhartbros.com/searchlisting.aspx?ftst=&txtCity=Manhattan&cmbBeds=-1&cmbBeds1=-1&cmbBeds2=-1&cmbBeds3=-1&cmbBeds4=-1&cmbBeds5=-1&cmbBaths=-1&cmbBaths2=-1&cmbBaths3=-1&cmbBaths4=-1&cmbBaths5=-1&cmb_PetPolicy=-1&LocationChanged=false&LocationGeoId=663687&zoom=10&GeoLatitude=34.4296&GeoLongitude=-119.8612&autoCompleteCorpPropSearchlen=3&renewpg=1&LatLng=(40.7830603,-73.97124880000001)&")

    def pull_out_relevant_data(self):

        pass

    def click_next_button(self):
        pass

    def do_all_the_things(self):
        self.page_data = self.open_link_to_get_data()

        pass

