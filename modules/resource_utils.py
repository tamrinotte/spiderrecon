# -*- coding: utf-8 -*-

# MODULES AND/OR LIBRARIES
import sys
import pathlib

##############################

# LOAD RESOURCE PATH

##############################

def load_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = pathlib.Path(sys._MEIPASS)
    else:
        base_path = pathlib.Path.cwd()

    return pathlib.Path(base_path, relative_path)