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

# Nilearn import
from nilearn import plotting

# Matplotlib
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt


def plot_image(input_files, output_directory, edge_file=None, overlay_file=None,
               contour_file=None, name=None, overlay_cmap=None):
    """ Plot image with edge/overlay/contour on top (useful for checking
    registration).

    <unit>
        <input name="input_files" type="['List_File', 'File']" desc="An image 
            or a list of image to be displayed."/>
        <input name="output_directory" type="Directory" description="The
            destination folder."/>
        <input name="edge_file" type="File" description="The target image
            to extract the edges from."/>
        <input name="overlay_file" type="File" description="The target image
            to extract the overlay from."/>
        <input name="contour_file" type="File" description="The target image
            to extract the contour from."/>
        <input name="name" type="Str" description="The name of the plot."/>
        <input name="overlay_cmap" type="Str" description="The color map to
            use: 'cold_hot' or 'blue_red' or None."/>
        <output name="snap_file" type="File" description="A pdf snap of the
            image."/>
    </unit>
    """
    input_file = input_files[0]
    # Check the input images exist on the file system
    for in_file in [input_file, edge_file, overlay_file, contour_file]:
        if in_file is not None and not os.path.isfile(in_file):
            raise ValueError("'{0}' is not a valid filename.".format(in_file))

    # Create the 'snap_file' location
    snap_file = os.path.join(
        output_directory, os.path.basename(input_file).split(".")[0] + ".pdf")

    # Create the plot
    display = plotting.plot_anat(input_file, title=name or "")
    if edge_file is not None:
        display.add_edges(edge_file)
    if overlay_file is not None:
        cmap = plotting.cm.__dict__.get(
            overlay_cmap, plotting.cm.alpha_cmap((1, 1, 0)))
        display.add_overlay(overlay_file, cmap=cmap)
    if contour_file is not None:
        display.add_contours(contour_file, alpha=0.6, filled=True,
                             linestyles="solid")
    display.savefig(snap_file)
    display.close()

    return snap_file
