from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException


import time

MAX_WAIT = 10
class NewVisitorTest(LiveServerTestCase):


    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id("id_list_table")
                rows = table.find_elements_by_tag_name("tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except(AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
            time.sleep(0.5)


    def test_can_start_a_list_a_list_for_one_user(self):
        # Check out Home page
        self.browser.get(self.live_server_url)
        # look for correct page title and header
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", header_text)
        # User is prompted to input item straight away
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(
            inputbox.get_attribute("placeholder"),
            "Enter a to-do item"
        )
        # User Types "1: go shopping" into the prompt
        inputbox.send_keys("Go shopping")
        # User hits enter, the page updates and "1: go shopping" is an item on the lists
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Go shopping")
        # A text box to add another item is still present
        # User adds "2: Remember to pick up dry-cleaning" and enters
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("Go to bank")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("2: Go to bank")
        # Page updates again and both items appear on list
        self.wait_for_row_in_list_table("1: Go shopping")
        self.wait_for_row_in_list_table("2: Go to bank")
        # satisfied, user goes back to sleep

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # User starts a new to do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("Go to the shop")
        inputbox.send_keys(Keys.ENTER)

        # User notices that list has a unique URL
        first_user_url = self.browser.current_url
        self.assertRegex(first_user_url, "/lists/.+")

        # A second user enters the site!

        ## Use a new browser to make sure that no information from before
        ## is carried over to the new instance of the website
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Second user visits the home page.  There is no sign of
        # First user's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Go Shopping', page_text)
        self.assertNotIn('Go to bank', page_text)

        # Second user starts a new list by entering a new item.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Francis gets his own unique URL
        second_user_url = self.browser.current_url
        self.assertRegex(second_user_url, '/lists/.+')
        self.assertNotEqual(second_user_url, second_user_url)

        # Again, there is no trace of User 1's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Go shopping', page_text)
        self.assertIn('Buy milk', page_text)