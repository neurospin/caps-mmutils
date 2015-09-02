#! /usr/bin/env python
##########################################################################
# Bredala - Copyright (C) AGrigis, 2015
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
import unittest
import os
import tempfile

# mmutils import
from mmutils.adapters.io import (element_to_list,
                                 list_to_element,
                                 ungzip_file,
                                 gzip_file)


class TestUtils(unittest.TestCase):
    """ Test the module functionalities.
    """

    def setUp(self):
        self.outdir = tempfile.mkdtemp()

    def test_specific_functions(self):
        """ Test functions execution follow up.
        """
        # element_to_list tests
        out_list = element_to_list("element_test")
        self.assertIsInstance(out_list, list)
        self.assertEqual(out_list, ["element_test"])

        # list_to_element tests
        with self.assertRaises(ValueError):
            list_to_element([1, 2, 3])
        with self.assertRaises(ValueError):
            list_to_element("no_list")
        out_element = list_to_element(["singleton_element"])
        self.assertIn(out_element, ["singleton_element"])
        self.assertIsInstance(out_element, str)

        # ungzip_file tests
        out_file = ungzip_file(os.path.join(os.path.dirname(
            os.path.realpath(__file__)),
            "test_file.gz"),
            output_directory=self.outdir,
            prefix="u")
        self.assertTrue(os.path.isfile(out_file))
        self.assertEqual("u", os.path.basename(out_file)[0])

        with self.assertRaises(ValueError):
            ungzip_file("no_file",
                        output_directory=self.outdir,
                        prefix="u")
        with self.assertRaises(ValueError):
            ungzip_file(os.path.join(os.path.dirname(
                os.path.realpath(__file__)),
                "test_file.gz"),
                output_directory="non_existent",
                prefix="u")

        # gzip file tests
        out_file = gzip_file(os.path.join(os.path.dirname(
            os.path.realpath(__file__)),
            "test_file.txt"),
            output_directory=self.outdir,
            prefix="g")
        self.assertTrue(os.path.isfile(out_file))
        self.assertEqual("g", os.path.basename(out_file)[0])

        with self.assertRaises(ValueError):
            ungzip_file("no_file",
                        output_directory=self.outdir,
                        prefix="g")
        with self.assertRaises(ValueError):
            ungzip_file(os.path.join(os.path.dirname(
                os.path.realpath(__file__)),
                "test_file.gz"),
                output_directory="non_existent",
                prefix="g")


def test():
    """ Function to execute unitest
    """
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtils)
    runtime = unittest.TextTestRunner(verbosity=2).run(suite)
    return runtime.wasSuccessful()


if __name__ == "__main__":
    test()
