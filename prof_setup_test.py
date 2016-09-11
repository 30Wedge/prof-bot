import unittest
import prof_setup
class test_setup_methods(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.extractor = prof_setup.Data_Extractor()
        try:
            self.extractor.setup()
        except:
            self.fail("set-up failed. Check RMF website or internet connection")

    @classmethod
    def tearDownClass(self):
        pass

    '''
    The follow methods are for testing match name function
    '''
    def help_test_match_name(self, first, last, name_to_match, should_match, error_msg):
        result = self.extractor.match_name(first, last, name_to_match)
        if should_match:
            self.assertTrue(result, error_msg)
        else:
            self.assertFalse(result, error_msg)

    def test_match_name_firstInitial_last(self):
        name_to_match = "S. Uppal"
        self.help_test_match_name("Sean", "Uppal", name_to_match, True, "Initial dot space last name did not match")

        name_to_match = "S Uppal"
        self.help_test_match_name("Sean", "Uppal", name_to_match, True, "Initial space last name did not match")

        name_to_match = "S.Uppal"
        self.help_test_match_name("Sean", "Uppal", name_to_match, False, "Initial last name matched")

    def test_match_name_first_last(self):
        name_to_match = "Sean Uppal"
        self.help_test_match_name("Sean", "Uppal", name_to_match, True, "First name last name did not match")

        name_to_match = "Seen Uppal"
        self.help_test_match_name("Sean", "Uppal", name_to_match, False, "Wrong name matched in first_last")

    def test_match_name_last_first(self):
        name_to_match = "Uppal Sean"
        self.help_test_match_name("Sean", "Uppal", name_to_match, True, "Last name first name did not match")

        name_to_match = "Upper Sean"
        self.help_test_match_name("Sean", "Uppal", name_to_match, False, "Wrong name matched in last_first")

    def test_match_name_case_sensitive(self):
        name_to_match = "SEan UPpAL"
        self.help_test_match_name("Sean", "Uppal", name_to_match, True, "Case sensitivity failed")

    '''
    The following methods are for testing the search_prof function
    '''
    def test_search_prof_found(self):
        name_to_search = "Danny Heap"
        result = "not found" in self.extractor.search_prof(name_to_search).lower()
        self.assertFalse(result, msg="Prof not found")

    def test_search_prof_not_found(self):
        name_to_search = "Dan Heap"
        result = "not found" not in self.extractor.search_prof(name_to_search).lower()
        self.assertTrue(result, msg="Wrong prof found")

if __name__ == "__main__":
    unittest.main()