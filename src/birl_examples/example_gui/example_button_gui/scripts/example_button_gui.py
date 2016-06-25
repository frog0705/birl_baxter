#!/usr/bin/env python

import sys
import os

pkg_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../src')
sys.path.insert(0, pkg_path)

# From the package import the module located in the src folder
from example_button_gui import _example_button_gui_module
from rqt_gui.main import Main

# Plugin below needs to match:
# (i)  the class name placed in the plugin.xml file, and
# (ii) the class name given in the module at src/example_button_gui/_example_button_gui_module.py 
plugin = 'ExampleBtnGUI'
main = Main(filename=plugin)
sys.exit(main.main(standalone=plugin))

