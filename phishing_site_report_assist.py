#!/usr/bin/env python3
#Fraud website reporting assistant v1.0
#S.D.G.

#import all modules
from tkinter import *
import tkinter.messagebox as mb
import os #To launch browser

REPORT_FILE="./phishing_reports.txt" #config and logs are stored here

#Load config
try:
    f=open(REPORT_FILE)
except FileNotFoundError:
    mb.showerror(title="No congif/records file", message=REPORT_FILE+" does not exist. Please create with config.")
    quit()

try:
    NAME = f.readline().strip()
    SHIELD_EMAIL = f.readline().strip()
    ACTUAL_EMAIL = f.readline().strip()
    EMAILS = (SHIELD_EMAIL, ACTUAL_EMAIL)
    MAIL_SITE=f.readline().strip()
    f.close()
    if not ("@" in SHIELD_EMAIL and "@" in ACTUAL_EMAIL and "mail" in MAIL_SITE): #rudimentary checks that the config data is actually config data
        raise EOFError

except EOFError:
    mb.showerror(title="Incomplete congif/records file", message=REPORT_FILE+" did not contain config. Please create with config.")
    quit()


SECURITY_SITES = ( #List of sites to open
"https://whois.com/whois",
MAIL_SITE,
"https://safebrowsing.google.com/safebrowsing/report_phish/",
"https://www.microsoft.com/en-us/wdsi/support/report-unsafe-site",
"https://www.fortiguard.com/webfilter",
"https://www.brightcloud.com/tools/url-ip-lookup.php",
"https://threatcenter.crdf.fr/submit_url.html",
"https://report.netcraft.com/report",
"https://urlfiltering.paloaltonetworks.com/",
"https://phishing.eset.com/en-us/report",
"https://global.sitesafety.trendmicro.com/index.php",
"https://www.bitdefender.com/consumer/support/answer/29358/",
"https://sitelookup.mcafee.com/",
"https://csi.forcepoint.com/",
"https://sitereview.symantec.com/#/",
"https://www.spam404.com/report.html",
"https://opentip.kaspersky.com/",
"https://talosintelligence.com/reputation_center"
)

def open_browser():
    """Command to launch browser with all security sites in separate tabs"""
    os.popen("firefox " + " ".join(SECURITY_SITES)) #Command to launch browser with all security sites in different tabs

class Window(Tk):
    def __init__(self):
        """Report Assiatant GUI"""
        super(Window, self).__init__() #Initialize Tk object

        self.title("Phishing Website Report Assistant")

        #Site URL and comment, used for log.
        self.reported_url=""
        self.report_comment=""

        self.build() #construct GUI
        self.mainloop() #start GUI

    def build(self):
        """Construct the GUI"""

        #Buttons for copying your ID info
        Button(self, text="Copy name", command=self.copy_name).grid(row=0, sticky=E+W)
        Button(self, text="Copy shielded email", command=lambda: self.copy_email(0)).grid(row=1, sticky=E+W)
        Button(self, text="Copy actual email", command=lambda: self.copy_email(1)).grid(row=2, sticky=E+W)

        #Subframe with entry field for malicious URL, and a button to copy it
        self.url_frame=Frame(self)
        self.url_frame.grid(row=3, sticky=E+W)

        Label(self.url_frame, text="Phishing URL:").grid(row=0, column=0, sticky=E)

        self.url_entry=Entry(self.url_frame)
        self.url_entry.grid(row=0, column=1, sticky=N+S+E+W)

        Button(self.url_frame, text="Copy URL", command=self.copy_url).grid(row=0, column=2)

        self.url_frame.columnconfigure(1, weight=1) #Set center column (the one with the field) to expand sideways)

        #Subframe for malicious site description comment area and a button to copy it
        self.desc_frame=Frame(self)
        self.desc_frame.grid(row=4, sticky=N+S+E+W)

        Label(self.desc_frame, text="Phishing description:").grid(row=0, sticky=N+E+W)

        self.desc_text=Text(self.desc_frame, width=30, height=20, wrap="word")
        self.desc_text.grid(row=1, sticky=N+S+E+W)

        Button(self.desc_frame, text="Copy description", command=self.copy_desc).grid(row=2, sticky=E+W+S)

        self.desc_frame.rowconfigure(1, weight=1) #Set comment text area to expand vertically
        self.desc_frame.columnconfigure(0, weight=1) #Comment frame is one column wide. Set to expand horizontally

        self.rowconfigure(4, weight=1) #Comment frame is on row 4. Set to expand vertically.

        self.columnconfigure(0, weight=1) #Root window is one column wide. Set to expand sideways.

    def copy_name(self):
        """Copy your name to the clipboard"""
        self.clipboard_clear()
        self.clipboard_append(NAME)

    def copy_email(self, email_index):
        """Copy one of your emails to the clipboard"""
        self.clipboard_clear()
        self.clipboard_append(EMAILS[email_index])

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
        f = open(REPORT_FILE, "a")
        f.write("\n\n"+window.reported_url+"\n"+window.report_comment)
        f.close()
except Exception as ex: #A save error occured. Notify the user.
    text=str(ex)
    if hasattr(ex, "message"):
        text+=" "+ex.message
    mb.showerror(title="Save error", message=text)
