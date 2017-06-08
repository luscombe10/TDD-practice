from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase


import time


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn(row_text, [row.text for row in rows])


    def test_can_start_a_list_and_retrieve_it_later(self):
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
        time.sleep(1)
        # A text box to add another item is still present
        # User adds "2: Remember to pick up dry-cleaning" and enters
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("Go to bank")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        # Page updates again and both items appear on list
        self.check_for_row_in_list_table("1: Go shopping")
        self.check_for_row_in_list_table("2: Go to bank")
        # Website generates a unique url for the list, it is explained
        # Once URL is visted, the list is there
        self.fail("Finish the test!")
