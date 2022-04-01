from selenium.webdriver.chrome.webdriver import WebDriver

from django.test import LiveServerTestCase

class TitleTesT(LiveServerTestCase):

    # setup method
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    # tear down method
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    # tests to check if the homepage title contains the correct string
    def test_title_on_homepage(self):
        self.selenium.get(self.live_server_url)
        self.assertIn('Travel Wishlist', self.selenium.title)

class AddPlacesTesT(LiveServerTestCase):

    fixtures = ['test_places'] # loads preset data from test_places.json, which contains test data

    # setup method
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    # tear down method
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    # tests adding new places when running the program in the browser
    def test_add_new_place(self):

        self.selenium.get(self.live_server_url) # get the correct page
        input_name = self.selenium.find_element_by_id('id_name')
        # type into the input box, id_name can be found in the development console
        input_name.send_keys('Denver')
        # type Denver into input box

        add_button = self.selenium.find_element_by_id('add-new-place')
        # find the add-new-place button
        add_button.click()
        # click add-new-place button

        denver = self.selenium.find_element_by_id('place-name-5')
        self.assertEqual('Denver', denver.text) # denver.text is the text in the element
        # assert that the information selenium entered corresponds with pk key 5

        self.assertIn('Denver', self.selenium.page_source)
        self.assertIn('New York', self.selenium.page_source)
        self.assertIn('Tokyo', self.selenium.page_source)
        # assert that the text is on the page itself
