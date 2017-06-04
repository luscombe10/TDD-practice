from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Check out Home page
        self.browser.get("http://localhost:8000")
        #look for correct page title
        self.assertIn("To-Do", self.browser.title)
        self.fail("Finish the test!")
    # User is prompted to input item straight away
    # User Types "1: go shopping" into the prompt
    # User hits enter, the page updates and "1: go shopping is an item on the list
    # A text box to add another item is still present
    # User adds "2: Remember to pick up dry-cleaning" and enters
    # Page updates again and both items appear on list
    # Website generates a unique url for the list, it is explained
    # Once URL is visted, the list is there

if __name__ == "__main__":
    unittest.main(warnings="ignore")
