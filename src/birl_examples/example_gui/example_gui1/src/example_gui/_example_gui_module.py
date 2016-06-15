import os
import rospy

import roslib
roslib.load_manifest('example_gui')

from qt_gui.plugin import Plugin
from python_qt_binding import loadUi

from python_qt_binding.QtGui import QWidget
from python_qt_binding.QtCore import Qt


class ExampleGui(Plugin):
   
    def __init__(self, context=None):
        super(ExampleGui, self).__init__(context)
        # Give QObjects reasonable names
        self.setObjectName('ExampleGui')    

        # Process standalone plugin command-line arguments
        from argparse import ArgumentParser
        parser = ArgumentParser()
        # Add argument(s) to the parser.
        parser.add_argument("-q", "--quiet", action="store_true",
                    dest="quiet",
                    help="Put plugin in silent mode")
        args, unknowns = parser.parse_known_args(context.argv())
        if not args.quiet:
            print 'arguments: ', args
            print 'unknowns: ', unknowns
  
        # Create QWidget
        self._widget = QWidget()
        # Get path to UI file which is a sibling of this file        
        pkg_dir = roslib.packages.get_pkg_dir('example_gui')
        ui_file_path = os.path.join(pkg_dir, 'ui/example_gui.ui')


        # Extend the widget with all attributes and children from UI file
        loadUi(ui_file_path, self._widget)
        # Give QObjects reasonable names
        self._widget.setObjectName('ExampleGuiUi')

	    # Show _widget.windowTitle on left-top of each plugin (when 
     	# it's set in _widget). This is useful when you open multiple
	    # plugins at once. Also if you open multiple instances of your 
	    # plugin at once, these lines add number to make it easy to
	    # tell from pane to pane.        
        if context.serial_number() > 1:
            self._widget.setWindowTitle(self._widget.windowTitle() + (' (%d)' % context.serial_number()))

        # Add widget to the user interface
        context.add_widget(self._widget)
    	
        # Now Set up our own interface:
        # ==> Connect the buttons to the functions
        self._widget.btn_ok.clicked.connect(self.btn_ok_clicked)
	
    def shutdown_plugin(self):
        """Kill all subscribers and publishers."""
	pass

    def save_settings(self, plugin_settings, instance_settings):
        # TODO save intrinsic configuration, usually using:
        # instance_settings.set_value(k, v)
    	pass
 
    def restore_settings(self, plugin_settings, instance_settings):
        # TODO restore intrinsic configuration, usually using:
        # v = instance_settings.value(k)
	pass    

     
    def btn_ok_clicked(self):
        #printing the word in terminal
        print "Hello World"
        #printing the word in the ui label box
        self._widget.StatusReturn.setText('Hello World')



