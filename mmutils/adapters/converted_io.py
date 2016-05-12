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
import gzip
import shutil


def normalize_array(filepath):
    """ Get a numpy array from a file and normalize column by column

    <process capsul_xml="2.0">
        <input name="filepath" type="file" doc="the input file containing the numpy array"/>
        <return name="outfile" type="file" doc="the output file with normalized array"/>
    </process>
    """
    # load input file
    array = numpy.loadtxt(filepath)
    array = (array - array.mean(axis=0)) / array.std(axis=0)
    outfile = filepath
    numpy.savetxt(outfile, array, fmt="%5.8f")

    return outfile

def element_to_list(element):
    """ Set an element to an empty list.

    
    <process capsul_xml="2.0">
      <input name="element" type="any" doc="an input element."/>
      <return name="adaptedelement" type="list_any" doc="the returned list containing the input element only."/>
    </process>
    
    """
    adaptedelement = [element]
    return adaptedelement


def list_to_element(listobj, force=False):
    """ Get the singleton list element.

    
    <process capsul_xml="2.0">
      <input name="listobj" type="list_any" doc="an input singleton list."/>
      <input name="force" type="bool" doc="force conversion even if more then one element in the list" optional="true"/>
      <return name="element" type="any" doc="the returned list single element."/>
    </process>
    
    """
    # Check that we have a singleton list
    if len(listobj) != 1 and not force:
        raise ValueError("A list with '{0}' element(s) is not a singleton "
                         "list.".format(len(listobj)))

    element = listobj[0]
    return element


def ungzip_list_files(fnames, prefix="u", output_directory=None):
    """ Copy and ungzip the input files.

    
    <process capsul_xml="2.0">
      <input name="fnames" type="list_file" doc="input files to ungzip."/>
      <input name="prefix" type="string" doc="the prefix of the result file."/>
      <input name="output_directory" type="directory" doc="the output directory where ungzip file is saved."/>
      <return name="ungzipfnames" type="list_file" doc="the returned ungzip files."/>
    </process>
    
    """
    ungzipfnames = []
    for fname in fnames:
        ungzipfnames.append(ungzip_file(fname, prefix, output_directory))

    return ungzipfnames


def ungzip_file(fname, prefix="u", output_directory=None):
    """ Copy and ungzip the input file.

    
    <process capsul_xml="2.0">
      <input name="fname" type="file" doc="an input file to ungzip."/>
      <input name="prefix" type="string" doc="the prefix of the result file."/>
      <input name="output_directory" type="directory" doc="the output directory where ungzip file is saved."/>
      <return name="ungzipfname" type="file" doc="the returned ungzip file."/>
    </process>
    
    """
    # Check the input file exists on the file system
    if not os.path.isfile(fname):
        raise ValueError("'{0}' is not a valid filename.".format(fname))

    # Check that the outdir is valid
    if output_directory is not None:
        if not os.path.isdir(output_directory):
            raise ValueError(
                "'{0}' is not a valid directory.".format(output_directory))
    else:
        output_directory = os.path.dirname(fname)

    # Get the file descriptors
    base, extension = os.path.splitext(fname)
    basename = os.path.basename(base)

    # Ungzip only known extension
    if extension in [".gz"]:

        # Generate the output file name
        basename = prefix + basename
        ungzipfname = os.path.join(output_directory, basename)

        # Read the input gzip file
        with gzip.open(fname, "rb") as gzfobj:
            data = gzfobj.read()

        # Write the output ungzip file
        with open(ungzipfname, "wb") as openfile:
            openfile.write(data)

    # Default, unknown compression extension: the input file is returned
    else:
        ungzipfname = fname

    return ungzipfname


def gzip_file(fname, prefix="g", output_directory=None,
              remove_original_file=False):
    """ Copy and gzip the input file.

    
    <process capsul_xml="2.0">
      <input name="fname" type="file" doc="an input file to gzip."/>
      <input name="prefix" type="string" doc="the prefix of the result file."/>
      <input name="output_directory" type="directory" doc="the output directory where gzip file is saved."/>
      <input name="remove_original_file" type="bool" doc="remove the original file"/>
      <return name="gzipfname" type="file" doc="the returned gzip file."/>
    </process>
    
    """
    # Check the input file exists on the file system
    if not os.path.isfile(fname):
        raise ValueError("'{0}' is not a valid filename.".format(fname))

    # Check that the outdir is valid
    if output_directory is not None:
        if not os.path.isdir(output_directory):
            raise ValueError(
                "'{0}' is not a valid directory.".format(output_directory))
    else:
        output_directory = os.path.dirname(fname)

    # Get the file descriptors
    base, extension = os.path.splitext(fname)
    # Gzip only non compressed file
    if extension not in [".gz"]:

        # Generate the output file name
        if prefix:
            basename = prefix + os.path.basename(base) + extension + ".gz"
        else:
            basename = os.path.basename(base) + extension + ".gz"
        gzipfname = os.path.join(output_directory, basename)

        # Write the output gzip file
        with open(fname, "rb") as openfile:
            with gzip.open(gzipfname, "w") as gzfobj:
                gzfobj.writelines(openfile)

        if remove_original_file:
            os.remove(fname)

    # Default, the input file is returned
    else:
        gzipfname = fname

    return gzipfname


def rename_file(input_filepath, output_filepath):
    """ Rename a file (same loc)

    
    <process capsul_xml="2.0">
      <input name="input_filepath" type="file" doc="an input file to rename."/>
      <input name="output_filepath" type="string" doc="the output filepath."/>
      <return name="output_file" type="file" doc="the renamed file."/>
    </process>
    
    """

    if os.path.isfile(output_filepath):
        raise Exception("Output file exist !")
    # get output folder
    shutil.move(input_filepath, output_filepath)

    output_file = output_filepath

    return output_file


def spm_tissue_probability_maps(fsl_dir="/usr/share/fsl/4.1",
                                spm_dir="/i2bm/local/spm8/"):
    """ SPM tissue probability maps.

    
    <process capsul_xml="2.0">
      <input name="fsl_dir" type="string" doc="the fsl repository"/>
      <input name="spm_dir" type="string" doc="the spm repository"/>
      <return name="tpm_struct" type="list_any" doc="a struct containing the spm tissue probability map descriptions."/>
    </process>
    
    """
    # Try to import the resource
    try:
        from mmutils.toy_datasets import get_sample_data
    except:
        raise ImportError("Can't import 'caps'.")

    if "spm8" in spm_dir:
        tmp_file = get_sample_data("tpm", fsl_dir=fsl_dir, spm_dir=spm_dir).all
    else:
        tmp_file = os.path.join(spm_dir, "tpm", "TPM.nii")

    # Format the tpm for spm
    tissue1 = ((tmp_file, 1), 2, (True, True), (False, True))
    tissue2 = ((tmp_file, 2), 2, (True, True), (False, True))
    tissue3 = ((tmp_file, 3), 2, (True, False), (False, False))
    tissue4 = ((tmp_file, 4), 3, (False, False), (False, False))
    tissue5 = ((tmp_file, 5), 4, (False, False), (False, False))
    tissue6 = ((tmp_file, 6), 2, (False, False), (False, False))

    tpm_struct = [tissue1, tissue2, tissue3, tissue4, tissue5, tissue6]
    return tpm_struct


def noprocess_switch(input_value):
    """
    Do nothing, returns the input value
    Used in switch

    
    <process capsul_xml="2.0">
      <input name="input_value" type="any" doc="a variable to let through"/>
      <return name="output_value" type="any" doc="the input value"/>
    </process>
    
    """

    output_value = input_value

    return output_value
