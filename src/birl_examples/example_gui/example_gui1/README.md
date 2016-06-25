# example_gui

A minimal example of a GUI design for RQT in Python.  

This is a step-by-step explanation of how to create a Python GUI in ROS.
It is based on a simple example, example_gui, from Reeve Chong at HKU

1) create an XML file that describes your graphical interface.  This is done using a separate tool:
QT Creator.  The result is a "user interface" (*.ui) file.  Design of the graphical interface is
described separately.  The instructions below assume this *.ui file already exists.


2) do the following to create a new package called "example_gui2"
  `hku_create_pkg example_gui2 rospy qt_gui rqt_gui`


3)  in the new package directory (.../example_gui2, in this case), copy over an example of
  plugin.xml (e.g., from this example, or from:  http://wiki.ros.org/rqt/Tutorials/Create%20your%20new%20rqt%20plugin)
  Inside this file, edit the line:
 "<class name="Example Gui2" type="example_gui2._example_gui2_module.ExampleGui2" base_class_type="rqt_gui_py::Plugin">"
 
The first name (Example Gui2) will show up on a list of plugins when you try to find and run your application.  It must be
a unique name among all of your plug-ins.  


The second name, (class type):
  "example_gui2._example_gui2_module.ExampleGui2"

is the concatenated name of the package, module and class, 
which is used for the import statement. (Form: package.module.class) 

In this example,our package name is "example_gui2".  The designer writes a module, in this case called
"_example_gui2_module.py", and within this module a class name is defined, in this case:  "ExampleGui2" (see step 10)

In plugin.xml, also edit the lines:
     " <label>Example Gui Hello</label>  "
  (when running the GUI, it will show up with the above name in the list of plug-ins)

The next line:
      "<statustip>Simple GUI to greet the world</statustip>"
should display the message "Simple GUI to greet the world" when hovering over the plugin label.  However, I could
not get this work.


4) create a directory under your package name (example_gui2, in this case), called "ui":
   ```roscd example_gui2
   mkdir ui```

5) create a "scripts" directory within your package; e.g., for the example package: example_gui2:
  ```roscd example_gui2
  mkdir scripts```

6) create a subdirectory under src with the same name as your package; in this example:
  ```roscd example_gui2/src
  mkdir example_gui2```

7) put your *.ui file in the "ui" directory.  For the current example, this file is called: example_gui2.ui
  Looking inside this file, there is a line:
" <widget class="QPushButton" name="btn_ok">"

 We will need to refer to the name "btn_ok" to write callbacks to respond to this button.
(If you add more GUI elements, you will see more names added, corresponding to each)


8) copy an example python program into your "scripts" directory from another gui package's "scripts" folder
(or from here: http://wiki.ros.org/rqt/Tutorials/Writing%20a%20Python%20Plugin), and use the package 
name to name it.  In the current example (package example_gui2) this file is called:
   example_gui2.py
   
9) edit this file: 
  the line:
    "from example_gui2 import _example_gui2_module"

    should have the first name set to your package name ("example_gui2", in this case) 
    the second name is the name of the module that you will write (see step 10, below)

  also, the line:   
   "plugin = 'ExampleGui2'"

   Should match the class name in step 3: example_gui2._example_gui2_module.ExampleGui2
   This must also match the class name in your module, described in step 10.

9)  create an init script in your src subdirectory:
  ```roscd example_gui2/src/example_gui2
     touch __init__.py```

    This file is empty, but its existence is necessary to inform Python to treat the directory as containing packages.

10) in this same subdirectory, example_gui2/src/example_gui2, create your Python module with callbacks
  This is where the interesting work is done.
  create a module called: _example_gui2_module (start by copying over an example, or copying from:
  http://wiki.ros.org/rqt/Tutorials/Writing%20a%20Python%20Plugin)

  This name of this module must match the module name in step (3) above

In the following line:
  "roslib.load_manifest('example_gui2')"
make sure the argument is your package name.

Edit the class name:
  `class ExampleGui2(Plugin):`

The class name used must match that of step2 (3) and (9) above.

Use the same name in the following lines:
    ```super(ExampleGui2, self).__init__(context)
        # Give QObjects reasonable names
        self.setObjectName('ExampleGui2')  ```

Edit these lines to point to the UI directory:
     ```# Get path to UI file which is a sibling of this file   
        # put your package name in the argument:     
        pkg_dir = roslib.packages.get_pkg_dir('example_gui2')
        #put the user-interface file name in the argument below
        ui_file_path = os.path.join(pkg_dir, 'ui/example_gui2.ui') ```

optionally, change name in this line:
     ```# Give QObjects reasonable names
        self._widget.setObjectName('ExampleGuiUi')```

Now, refer to the name(s) assigned to GUI objects, as per the *.ui file: btn_ok in this case
    ```    # Now Set up our own interface:
        # ==> Connect the button to a functions
        #for a different widget name than "btn_ok", change this name below;
        # specify the name of the function to be written as the callback--in this case, btn_ok_clicked
        self._widget.btn_ok.clicked.connect(self.btn_ok_clicked)```

 this links the widget "btn_ok" to a callback function we will write, in this case called "btn_ok_clicked"

11) write the callback function called "btn_ok_clicked";  here is an example:
   ```def btn_ok_clicked(self):
        #print text in terminal
        print "Hello World"
        #printing text in the ui label box
        self._widget.StatusReturn.setText('Hello, World')```

  Here is a more complex example.  Upon click of the button, it publishes a message to the topic 
"multisense_sl/set_spindle_speed" with the argument 3.0 using message type: std_msgs/Float64.
(rqrs addl line at top: from std_msgs.msg import Float64)

   ```def btn_ok_clicked(self):
        #set the desired spindle-speed value in variable: spin_speed
        spin_speed = 3.0
        self._widget.StatusReturn.setText('set LIDAR speed to ' + str(spin_speed))
        #publish the data to multisense_sl
	#instantiate a publisher object in ROS, with specified topic and message type:        
        self.pub = rospy.Publisher('multisense_sl/set_spindle_speed', Float64, queue_size=10)  
        #use this publisher to send the desired message    
        self.pub.publish(spin_speed)```

12) RUN THE APPLICATION:
  in a terminal window, enter:
     `rqt --force-discover`
  (see: http://wiki.ros.org/rqt/UserGuide#Running_rqt for more details and options)
  a window will pop up 
  under the menu item "Plugins", select your new GUI name: Example Gui Hello
  click the graphical button in invoke the callback-function response
   









    
