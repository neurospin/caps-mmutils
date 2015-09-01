#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2015
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
import os
import sys
import unittest
import tempfile

# Capsul import
from capsul.study_config.study_config import StudyConfig
from capsul.process.loader import get_process_instance

# Mmutils import
# from mmutils.toy_datasets import get_sample_data


class TestMMutils(unittest.TestCase):
    """ Class to test dicom to nifti pipeline.
    """
    def setUp(self):
        self.outdir = tempfile.mkdtemp()

    def test_simple_run(self):
        """ Method to test a simple 1 cpu call with the scheduler.
        """
        # Configure the environment
        study_config = StudyConfig(
            modules=[],
            use_smart_caching=True,
            number_of_cpus=1,
            generate_logging=True,
            output_directory=self.outdir,
            use_scheduler=False)

        # Create pipes
        pipe1 = get_process_instance('mmutils.adapters.io.element_to_list')
        pipe2 = get_process_instance('mmutils.adapters.io.list_to_element')
        pipe3 = get_process_instance('mmutils.adapters.io.gzip_file')
        pipe4 = get_process_instance('mmutils.adapters.io.ungzip_file')
        pipe5 = get_process_instance('mmutils.adapters.io.spm_tissue_probability_maps')
        pipe6 = get_process_instance('mmutils.adapters.io.noprocess_switch')

        # Set pipeline input parameters
        # localizer_dataset = get_sample_data("localizer")
        pipe1.element = 'test_element(string)'
        pipe2.listobj = ["the_element"]
        pipe3.fname = os.path.join(os.path.dirname(os.path.realpath(
            __file__)), "test_file.txt")
        pipe4.fname = os.path.join(os.path.dirname(os.path.realpath(
            __file__)), "test_file.gz")
        pipe6.input_value = [["testing", ], 1, "str"]

        # View pipeline
        if 0:
            from capsul.qt_gui.widgets import PipelineDevelopperView
            from PySide import QtGui
            app = QtGui.QApplication(sys.argv)
            view1 = PipelineDevelopperView(pipe1)
            view1.show()
            app.exec_()
            app = QtGui.QApplication(sys.argv)
            view2 = PipelineDevelopperView(pipe2)
            view2.show()
            app.exec_()
            app = QtGui.QApplication(sys.argv)
            view3 = PipelineDevelopperView(pipe3)
            view3.show()
            app.exec_()
            app = QtGui.QApplication(sys.argv)
            view4 = PipelineDevelopperView(pipe4)
            view4.show()
            app.exec_()
            app = QtGui.QApplication(sys.argv)
            view4 = PipelineDevelopperView(pipe5)
            view4.show()
            app.exec_()
            app = QtGui.QApplication(sys.argv)
            view4 = PipelineDevelopperView(pipe6)
            view4.show()
            app.exec_()

        # Execute the pipeline in the configured study
        study_config.run(pipe1, executer_qc_nodes=True, verbose=1)
        study_config.run(pipe2, executer_qc_nodes=True, verbose=1)
        study_config.run(pipe3, executer_qc_nodes=True, verbose=1)
        study_config.run(pipe4, executer_qc_nodes=True, verbose=1)
        # study_config.run(pipe5, executer_qc_nodes=True, verbose=1)
        study_config.run(pipe6, executer_qc_nodes=True, verbose=1)


def test():
    """ Function to execute unitest
    """
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMMutils)
    runtime = unittest.TextTestRunner(verbosity=2).run(suite)
    return runtime.wasSuccessful()


if __name__ == "__main__":
    test()
