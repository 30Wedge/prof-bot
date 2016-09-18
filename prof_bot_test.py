import unittest
import prof_bot

class test_prof_bot(unittest.TestCase):

    def test_is_command(self):
        command = "!prof (prof 1)(prof 2) (prof3)"
        self.assertTrue(prof_bot.is_command(command), "This command should be valid")
        command = "!notprof (prof1)"
        self.assertFalse(prof_bot.is_command(command), "This command should be invalid")

    def test_get_wanted_prof_and_course(self):
        command = "!prof (prof 1)(prof 2) (profx)"
        expected_list = ["prof 1", "prof 2", "profx"]
        actual_list = prof_bot.get_wanted_prof_and_course(command)
        self.assertEqual(expected_list, actual_list, "Not parsing command correctly")

    def test_is_course_name(self):
        name = "csc108"
        self.assertTrue(prof_bot.is_course_name(name), "csc108 should be a valid course name")
        name = "CSC108"
        self.assertTrue(prof_bot.is_course_name(name), "Should not be case sensitive")
        name = "CSCA08"             #utsc courses may have their fourth character as a letter
        self.assertTrue(prof_bot.is_course_name(name), "4th character may be a character")
        name = "cs1010"
        self.assertFalse(prof_bot.is_course_name(name), "cs1010 should not be a valid course name")
        name = "danny heap"
        self.assertFalse(prof_bot.is_course_name(name), "A prof name definitely should not be a course name")

