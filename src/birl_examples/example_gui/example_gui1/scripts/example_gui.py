#!/usr/bin/env python

import sys
import os

pkg_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../src')
sys.path.insert(0, pkg_path)

from example_gui import _example_gui_module
from rqt_gui.main import Main

plugin = 'ExampleGui'
main = Main(filename=plugin)
sys.exit(main.main(standalone=plugin))

