# Phishing Website Preporting Assistant

A tool to help with reporting phishing websites to the domain seller and several security flagging databases.

This tool was designed to go with, and has a list of websites from, this video by ThioJoe on YouTube https://www.youtube.com/watch?v=0fIUiv9-UFk
Hope it helps! TYJ, I learned how to do proper tkinter resizing while writing this :-D

# What it does
The program is simple: Open a browser to several online security service report pages, and give the user an easy way to copy-paste the same report information to each of them. It has buttons to read the user's name and email from a config file and copy them to the clipboard (required for some reports), an entry field for the phishing URL itself with a copy button, and a large text field for a description of the malicious site also with a copy button.



This program expects firefox to be in PATH in the command to open the browser (will be the case if you are using system-package firefox on Linux), but you can edit this. I intend to incorporate strong Windows compatibility soon with webbrowser or another library, but right now it's helpful that the sites are loaded in order.

Change info in the config/log file as desired.

# How to use
1. Have the url of the phishing site on the clipboard, and save a screenshot of the site itself, showing the most self-incriminating part. WARNING: Some malicious sites have been known to be very agressive. Do not open a link you believe could be an advanced cyberattack, even in a private browsing window with a VPN to hide your location.
2. Run this program. Firefox will open with tabs to various reporting websites (plus a whois lookup so you can contact the host company and report the site there).
3. Paste the phishing site url in my program's field for such, and type out a description of what the site seems to be doing, along eith any details that might help convict it.
4. If your desktop supports window tiling, I like to tile the my program on the left side of the screen, and Firefox on the right. You can move the halfway point between windows after tiling in most desktops.
5. Go through each Firefox tab, and follow the steps to report (or lookup then report) the phishing site to each company.
6. Check your email. Currently, TrendMicro requires email confirmation before they will review the report. Also, you will receive emails from the companies notifying you of the report status. Some companies may require resubmission before a human will review the site. You can check my program's log for the description you previously wrote for the site.

S.D.G.
