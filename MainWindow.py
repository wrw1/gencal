from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
import aboutDialog
from help import *
import globals as G

# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)
class Window(Frame):

    # Define settings upon initialization. Here you can specify
	def __init__(self, master=None):
		# parameters that you want to send through the Frame class.
		Frame.__init__(self, master)
		self.master = master
		self.init_window()
		self.about = aboutDialog
		self.gencalhelp = HelpWindow

	#Creation of init_window
	def init_window(self):

		# changing the title of our master widget
		self.master.title("Gencal " + G.Version)

		# allowing the widget to take the full space of the root window
		self.pack(fill=BOTH, expand=1)

		# creating a menu instance
		menu = Menu(self.master)
		self.master.config(menu=menu)

		# create the file pulldown menu
		filemenu = Menu(menu, tearoff=0)
		filemenu.add_command(label="Save As ...", underline=0, accelerator="Ctrl-s",
							 command=self.save_file)
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command=self.client_exit)
		menu.add_cascade(label="File", menu=filemenu)

		# create the help pulldown menu
		helpmenu = Menu(menu, tearoff=0)
		helpmenu.add_command(label="About Gencal", command=self.about_dialog)
		helpmenu.add_separator()
		helpmenu.add_command(label="Gencal Help", command=self.help_dialog)
		menu.add_cascade(label="Help", menu=helpmenu)

	def about_dialog(self):
		aboutDialog.show(self)

	def help_dialog(self):
		show_gencalhelp(self)

	def about(self):
		lines = 'Gencal\n' + '(Generate Calabration Gcode)\n' + 'Version 1.0'
		tkinter.messagebox.showinfo('About', lines)

	def save_file(self):
		global gcode
		options =  {}
		options['defaultextension'] = '.nc'
		options['filetypes'] = [('all files', '.*'), ('gcode files', '.nc'), ('gcode files', '.gcode')]
		options['initialfile'] = 'test.nc'
		options['title'] = 'Save Gcode as...'

		fn = tkinter.filedialog.asksaveasfilename(**options)
		if not fn:
			return
		try:
			UseFile = open(fn, 'w')
			for line in G.gcode:
				UseFile.write(line+'\n')
			UseFile.close()
		except:
			tkinter.messagebox.showinfo("Error", "Unable to open to write " + fn)

	def client_exit(self):
		exit()
