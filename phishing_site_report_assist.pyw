#!/usr/bin/env python3
"""Fraud website reporting assistant

Opens a list of security vendor websites and provides convenient
fields for data about the website with copy-to-clipboard buttons.
S.D.G.
"""

#import all modules
from tkinter import *
import tkinter.messagebox as mb
import os #To launch browser
import tomllib
import sys

#All files we open and save use this encoding
ENCODING = "utf-8"

#Load config
CONFIG_FILE = "config.toml"
try:
    with open(CONFIG_FILE, encoding = ENCODING) as f:
        CONFIG = tomllib.loads(f.read())

except FileNotFoundError:
    mb.showerror("No config file", "Could not find " + CONFIG_FILE)
    sys.exit()

#Padding amount to use for big buttons
BIG_BUTTON_PADDING = 30

#Padding used normally
DEFAULT_PADDING = 5

def open_browser():
    """Command to launch browser with all security sites in separate tabs"""
    print("BROWSER OPEN DISABLED. Code must be changed. DO NOT COMMIT THIS.")
    #os.popen(CONFIG["browserPath"] + " " + " ".join(CONFIG["securitySites"]))

class Window(Tk):
    """The main Phishing site Report Assist window"""
    def __init__(self):
        """Report Assiatant GUI"""
        super().__init__() #Initialize Tk object

        self.title("Phishing Website Report Assistant")

        #Site URL and comment, used for log.
        self.reported_url = ""
        self.report_comment = ""

        self.build() #construct GUI
        self.mainloop() #start GUI

    def build(self):
        """Construct the GUI"""
        #List of buttons, for size configuration later
        self.buttons = []

        #Menubar
        self.menubar = Menu(self)
        self.config(menu = self.menubar)

        #View menu
        self.viewmenu = Menu(self.menubar)
        self.menubar.add_cascade(label = "View", menu = self.viewmenu)
        self.big_buttons_var = BooleanVar(self, value = False)
        self.viewmenu.add_checkbutton(label = "Big buttons (for touch screens)", variable = self.big_buttons_var, command = self.update_big_buttons)

        #Buttons for copying your ID info
        bn = Button(self, text = "Copy your name", command = self.copy_name)
        bn.grid(row = 0, sticky = E + W)
        self.buttons.append(bn)
        be = Button(self, text = "Copy your email", command = self.copy_email)
        be.grid(row = 1, sticky = E + W)
        self.buttons.append(be)

        #Subframe with entry field for malicious URL, and a button to copy it
        self.url_frame=Frame(self)
        self.url_frame.grid(row = 2, sticky=E+W)

        Label(self.url_frame, text = "Phishing URL:").grid(row = 0, column = 0, sticky = E)

        self.url_entry = Entry(self.url_frame)
        self.url_entry.grid(row = 0, column = 1, sticky = NSEW)

        bu = Button(self.url_frame, text = "Copy URL", command = self.copy_url)
        bu.grid(row=0, column=2)
        self.buttons.append(bu)

        self.url_frame.columnconfigure(1, weight = 1) #Set center column (the one with the field) to expand sideways)

        #Subframe for malicious site description comment area and a button to copy it
        self.desc_frame = Frame(self)
        self.desc_frame.grid(row = 3, sticky=N+S+E+W)

        Label(self.desc_frame, text = "Phishing description:").grid(row=0, sticky=E+W)

        bd = Button(self.desc_frame, text = "Copy description", command = self.copy_desc)
        bd.grid(row = 1, sticky = E + W)
        self.buttons.append(bd)

        self.desc_text = Text(self.desc_frame, width = 30, height = 20, wrap = "word")
        self.desc_text.grid(row = 2, sticky = NSEW)

        self.desc_frame.rowconfigure(2, weight = 1) #Set comment text area to expand vertically
        self.desc_frame.columnconfigure(0, weight = 1) #Comment frame is one column wide. Set to expand horizontally

        self.rowconfigure(3, weight = 1) #Comment frame is on row 3. Set to expand vertically.

        self.columnconfigure(0, weight = 1) #Root window is one column wide. Set to expand sideways.

    def update_big_buttons(self):
        """Update the GUI based on wether we are using big buttons"""
        val = (DEFAULT_PADDING, BIG_BUTTON_PADDING)[self.big_buttons_var.get()]
        for button in self.buttons:
            button.config(padx = val, pady = val)

    def copy_name(self):
        """Copy your name to the clipboard"""
        self.clipboard_clear()
        self.clipboard_append(CONFIG["name"])

    def copy_email(self):
        """Copy one of your emails to the clipboard"""
        self.clipboard_clear()
        self.clipboard_append(CONFIG["email"])

    def copy_url(self):
        """Copy the malicious URL to the clipboard, and write it to window memory"""
        self.reported_url = self.url_entry.get()
        self.clipboard_clear()
        self.clipboard_append(self.reported_url)

    def copy_desc(self):
        """Copy the malicious site description to the clipboard, and write it to window memory"""
        self.report_comment = self.desc_text.get(0.0, END).strip()
        self.clipboard_clear()
        self.clipboard_append(self.report_comment)

#Open browser to all security sites in separate tabs
open_browser()

window = Window() #Call main window

#After the window closes, try to save the URL and comment to the log.
try:
    if window.reported_url or window.report_comment: #If any information was written then copied, save it.
        with open(CONFIG["logFile"], "a", encoding = ENCODING) as f:
            f.write(window.reported_url + "\n" + window.report_comment + "\n\n")

except Exception as ex: #A save error occured. Notify the user.
    text = str(ex)
    if hasattr(ex, "message"):
        text += " " + ex.message
    mb.showerror(title = "Save error", message = text)
