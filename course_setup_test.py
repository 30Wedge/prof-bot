import unittest
import course_setup

class test_setup_methods(unittest.TestCase):

    def test_get_full_code_fall(self):
        code = "CSC108 Fall"
        expected_code_list = ["CSC108H1F", "CSC108H3F", "CSC108H5F"]
        actual_code_list = course_setup.Course_extractor.get_full_code(code)
        self.assertEqual(expected_code_list, actual_code_list, "Not getting the correct possible course codes for fall")

    def test_get_full_code_winter(self):
        code = "CSC108 winter"
        expected_code_list = ["CSC108H1S", "CSC108H3S", "CSC108H5S"]
        actual_code_list = course_setup.Course_extractor.get_full_code(code)
        self.assertEqual(expected_code_list, actual_code_list, "Not getting the correct possible course codes for winter")

    def test_get_full_code_year(self):
        code = "ECO100 YEAR"
        expected_code_list = ["ECO100Y1", "ECO100Y3", "ECO100Y5"]
        actual_code_list = course_setup.Course_extractor.get_full_code(code)
        self.assertEqual(expected_code_list, actual_code_list, "Not getting the correct possible course codes for full year")

    def test_is_json_file(self):
        file_name = "abc.json"
        self.assertTrue(course_setup.Course_extractor.is_json_file(file_name), "should be json file")
        file_name = "123json"
        self.assertFalse(course_setup.Course_extractor.is_json_file(file_name), "should not be json file")

    def test_load_old_data(self):
        course_code = "CSC108H1F"
        self.assertIsNotNone(course_setup.Course_extractor.load_old_data(course_code), "Course file not found")
        course_code = "CSG188H"
        self.assertIsNone(course_setup.Course_extractor.load_old_data(course_code), "Course shouldn't exist")

    def test_get_commet(self):
        course_code = "CSC108 Fall"
        course_extractor = course_setup.Course_extractor(course_code)
        comment = course_extractor.get_comment()
        self.assertTrue("CSC108H1F" in comment, "CSC108H1F should be valid course in st.george")
        self.assertTrue("CSC108H5F" in comment, "CSC108H5F should be valid course in scraborough")
        self.assertFalse("CSC108H3F" in comment, "CSC108H3F should not be a course in mississague")
