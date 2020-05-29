
#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#    Student no: n10336516
#    Student name: Max O'Dell
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  Submitted files will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Assignment Description-----------------------------------------#
#
#  The Best, Then and Now
#
#  In this assignment you will combine your knowledge of HTMl/XML
#  mark-up languages with your skills in Python scripting, pattern
#  matching, and Graphical User Interface design to produce a useful
#  application that allows the user to preview and print lists of
#  top-ten rankings.  See the instruction sheet accompanying this
#  file for full details.
#
#--------------------------------------------------------------------#



#-----Imported Functions---------------------------------------------#
#
# Below are various import statements for helpful functions.  You
# should be able to complete this assignment using these
# functions only.  Note that not all of these functions are
# needed to successfully complete this assignment.  YOU MAY NOT USE
# ANY NON-STANDARD MODULES SUCH AS 'Beautiful Soup' OR 'Pillow'.  ONLY
# MODULES THAT COME WITH A STANDARD PYTHON 3 INSTALLATION MAY BE
# USED.

# The function for opening a web document given its URL.
# (You WILL need to use this function in your solution,
# either directly or via our "download" function.)
from urllib.request import urlopen

# Import the standard Tkinter functions. (You WILL need to use
# these functions in your solution.)
from tkinter import *

# Functions for finding all occurrences of a pattern
# defined via a regular expression, as well as
# the "multiline" and "dotall" flags.  (You do NOT need to
# use these functions in your solution, because the problem
# can be solved with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.)
from re import findall, finditer, MULTILINE, DOTALL, sub

# Import the standard SQLite functions (just in case they're
# needed).
from sqlite3 import *

#
#--------------------------------------------------------------------#



#-----Downloader Function--------------------------------------------#
#
# This is our function for downloading a web page's content and both
# saving it on a local file and returning its source code
# as a Unicode string. The function tries to produce a
# meaningful error message if the attempt fails.  WARNING: This
# function will silently overwrite the target file if it
# already exists!  NB: You should change the filename extension to
# "xhtml" when downloading an XML document.  (You do NOT need to use
# this function in your solution if you choose to call "urlopen"
# directly, but it is provided for your convenience.)
#
def download(url = 'http://www.wikipedia.org/',
             target_filename = 'download',
             filename_extension = 'html'):

    # Import an exception raised when a web server denies access
    # to a document
    from urllib.error import HTTPError

    # Open the web document for reading
    try:
        web_page = urlopen(url)
    except ValueError:
        raise Exception("Download error - Cannot find document at URL '" + url + "'")
    except HTTPError:
        raise Exception("Download error - Access denied to document at URL '" + url + "'")
    except:
        raise Exception("Download error - Something went wrong when trying to download " + \
                        "the document at URL '" + url + "'")

    # Read its contents as a Unicode string
    try:
        web_page_contents = web_page.read().decode('UTF-8')
    except UnicodeDecodeError:
        raise Exception("Download error - Unable to decode document at URL '" + \
                        url + "' as Unicode text")

    # Write the contents to a local text file as Unicode
    # characters (overwriting the file if it
    # already exists!)
    try:
        text_file = open(target_filename + '.' + filename_extension,
                         'w', encoding = 'UTF-8')
        text_file.write(web_page_contents)
        text_file.close()
    except:
        raise Exception("Download error - Unable to write to file '" + \
                        target_file + "'")

    # Return the downloaded document to the caller
    return web_page_contents

#
#--------------------------------------------------------------------#



#-----Student's Solution---------------------------------------------#

#
# Put your solution at the end of this file.
#

# Import libraries needed for use with opening HTML files SQLite
import webbrowser as wb
from sqlite3 import *

# Initiate the 'landing' screen with a title and background colour
window1 = Tk()
window1.title('The Best... Then and Now')
window1.configure(bg = "white")

# Store a few font configurations in variables for ease of use throughout
labelfont = ('Arial', 18, 'bold')
buttonfont = ('Arial', 16)
previewfont = ('Arial', 12)

# Initiate the screen for previewing lists with a title and size dimensions, then hide it until it is used later
previewscreen = Toplevel()
previewscreen.title('Previewed List')
previewscreen.configure(width=650, height=350, bg='white')
previewscreen.withdraw()

# Store the links to the websites containing the three lists used, to be used as a form of referencing the source of information
website1 = 'https://www.ariacharts.com.au/charts/albums-chart'
website2 = 'https://coinmarketcap.com/all/views/all/'
website3 = 'https://www.betterreading.com.au/book_list/the-weekly-top-10-non-fiction-bestseller-list/'

# Store the links to the images to display on the exported HTML file
exportimage1 = 'https://ichef.bbci.co.uk/images/ic/640xn/p04l2y11.jpg'
exportimage2 = 'https://cdn.images.express.co.uk/img/dynamic/22/590x/cryptocurrency-predictions-2018-914087.jpg'
exportimage3 = 'https://cdn5.teebooks.com/243-large_default/bookshelf-45-cm.jpg'

# Open and read the HTML files from both the website urls and the previously downloaded files
dl1 = download(url=website1, target_filename='list1')
dl2 = download(url=website2, target_filename='list2')
dl3 = download(url=website3, target_filename='list3')
list1 = open('Old Lists/Albums - Australia.html').read()
list2 = open('Old Lists/Cryptocurrencies.html', encoding="utf8").read()
list3 = open('Old Lists/Non-Fiction Bestsellers.html').read()

# Store these strings in a list, for the purpose of seamlessly matching their index position with the variable of the radio button selected
lists = [list1, list2, list3, dl1, dl2, dl3]

# Open the template HTML file to replace with the list item data
template = open('toptentemplate.html').read()

# Initiate the variable which stores the radio button currently selected, as well as a couple other variables for use in loops
v = IntVar()
v.set(0)
r1 = 1
r2 = 1

# Create three labels with the names of the top 10 lists
listlabel1 = Label(window1, text = 'Top 10 Albums', font = labelfont, bg='white', padx = 0).grid(row=0,column=1,sticky='W',columnspan=2)
listlabel2 = Label(window1, text = 'Top 10 Cryptocurrencies', font = labelfont, bg='white', padx = 0).grid(row=2,column=1,sticky='W',columnspan=2)
listlabel3 = Label(window1, text = 'Top 10 Non-Fiction Bestsellers', font = labelfont, bg='white', padx = 0).grid(row=4,column=1,sticky='W',columnspan=2)

# Create the radio buttons and increment the variable storing which row to place them in
for i in range(3):
    previousradio = Radiobutton(window1, text = 'Previous', font = buttonfont, variable = v, value = i, bg='white').grid(row=r1,column=1,sticky='W')
    r1 += 2

for i in range(3, 6):
    currentradio = Radiobutton(window1, text = 'Current', font = buttonfont, variable = v, value = i, bg='white').grid(row=r2,column=2,sticky='W')
    r2 += 2

# Create the three buttons and pass the selected radio button in the form of a variable
previewbutton = Button(window1, text = 'Preview', font = buttonfont, command = lambda : Preview(v.get()), bg='white').grid(row=6,column=1, sticky='W')
exportbutton = Button(window1, text = 'Export', font = buttonfont, command = lambda : Export(v.get()), bg='white').grid(row=6,column=1,columnspan=2)
savebutton = Button(window1, text = 'Save', font = buttonfont, command = lambda : Save(v.get()), bg='white').grid(row=6,column=2,sticky='E')

# Initiate the logo variable with reference to the local file and display it in the window within a label widget
logo = PhotoImage(file="top-10.gif")
logolabel = Label(window1, image=logo,borderwidth=0,highlightthickness=0).grid(column=0, row=0, rowspan=7)

# Function for previewing the selected list in the GUI
def Preview(sel):
    # Store variables for the title text in the preview window
    title1 = 'Top 10 Albums'
    title2 = 'Top 10 Cryptocurrencies'
    title3 = 'Top 10 Non-Fiction Bestsellers'

    # Check if there is already a previewed list in the window and delete the elements if so
    if len(previewscreen.winfo_children()) > 10:
        for widget in previewscreen.winfo_children():
            widget.destroy()

    # Hide the main screen and show the preview screen
    window1.withdraw()
    previewscreen.deiconify()

    # Check which radio button was selected when the 'Preview' button is pressed
    if sel == 0 or sel == 3:
        # Set the local list variable to the return value from the regular expression function, passing it the correct string from the list of HTML files
        list = List1(lists[sel])
        # Set the image variable to display the local file applicable to the selected list
        img = PhotoImage(file="listimg1.gif")
        # Set the title text of the preview screen, depending on if it's current or previous
        if sel == 0:
           titletext = 'Previous ' + title1
        elif sel == 3:
            titletext = 'Current ' + title1

    elif sel == 1 or sel == 4:
        list = List2(lists[sel])
        img = PhotoImage(file="listimg2.gif")
        if sel == 1:
           titletext = 'Previous ' + title2
        elif sel == 4:
            titletext = 'Current ' + title2

    elif sel == 2 or sel == 5:
        list = List3(lists[sel])
        img = PhotoImage(file="listimg3.gif")
        if sel == 2:
           titletext = 'Previous ' + title3
        elif sel == 5:
            titletext = 'Current ' + title3

    # Create the preview by creating labels displaying each element one after the other
    for i in range(10):
        Label(previewscreen, text='[' + str(i + 1) + '] ' + (list[i]), font=previewfont, bg='white').grid(row=i+1,column=1,sticky='W')

    # Create supporting widgets
    Button(previewscreen, text = 'Back', font = buttonfont, command = Back, bg='white').grid(column=1)
    titlelabel = Label(previewscreen, text=titletext, font =('Arial', 12, 'bold'), bg='white').grid(column=1,row=0)
    previewimg = Label(previewscreen, image=img,borderwidth=0,highlightthickness=0).grid(column=0,row=0,rowspan=11)
    previewscreen.mainloop()

# Function for exporting the list into a HTML document and opening in a web browser
def Export(sel):
    # Create an empty list to store the HTML code in
    exp = []

    # Check which radio button was selected when the 'Export' button is pressed
    if sel == 0 or sel == 3:
        # Use a regular expression to find the date of the webpage
        date = findall('"date-display">(.*)<', lists[sel])
        # Set the local list variable to the return value from the regular expression function, passing it the correct string from the list of HTML files
        list = List1(lists[sel])
        # Enter into the empty list a new string with updated attributes pertaining to the selected list
        exp.append(template.replace('ItemName', 'Albums').replace('ItemAttribute', 'Artwork').replace('listtitle', 'Top 10 Albums')
                   .replace('date', date[0]).replace('headerimage', exportimage1).replace('website0', website1))
        # Set the local attr variable to the return value from the regular expression function, passing it the correct string from the list of HTML files
        attr = List1Attributes(lists[sel])

    elif sel == 1 or sel == 4:
        date = findall('Last updated: (.*)\n', lists[sel])
        list = List2(lists[sel])
        exp.append(template.replace('ItemName', 'Cryptocurrency').replace('ItemAttribute', 'Market Cap').replace('listtitle', 'Top 10 Cryptocurrencies')
                   .replace('date', 'As of ' + date[0]).replace('headerimage', exportimage2).replace('website0', website2))
        attr = List2Attributes(lists[sel])

    elif sel == 2 or sel == 5:
        date = findall('(Week Ending.*)<', lists[sel])
        list = List3(lists[sel])
        exp.append(template.replace('ItemName', 'Book Title').replace('ItemAttribute', 'Cover').replace('listtitle', 'Top 10 Non-Fiction Bestsellers')
                   .replace('date', date[0]).replace('headerimage', exportimage3).replace('website0', website3))
        attr = List3Attributes(lists[sel])

    # Replace the previous item in the list with an updated string with the next list item added to it
    for item in range(10):
        exp.append(exp[item].replace('item' + str((item + 1)) + '.', list[item]))

    # Replace the previous string again, but for attributes - adding the correct image syntax is the attribute is a displayed image
    for att in range(10):
        if sel == 0 or sel == 3 or sel == 2 or sel == 5:
            exp.append(exp[(att + 10)].replace('attribute' + str((att + 1)) + '.', '<img src=' + attr[att] + ' alt=not found>'))
        elif sel == 1 or sel == 4:
            exp.append(exp[(att + 10)].replace('attribute' + str((att + 1)) + '.', attr[att]))

    # Write this updated HTML file into a new file in the folder and open it in the browser
    export = open('exported.html', 'w')
    export.write(exp[20])
    export.close()
    wb.open_new_tab('exported.html')

# Function for saving the selected list into the accompanying database
def Save(sel):
    # Establish the connection to the database
    connection = connect(database='top_ten.db')
    top10db = connection.cursor()

    # Check which radio button was selected when the 'Save' button is pressed
    if sel == 0 or sel == 3:
        # Set the local list variable to the return value from the regular expression function, passing it the correct string from the list of HTML files
        list = List1(lists[sel])
        # Set the local attr variable to the return value from the regular expression function, passing it the correct string from the list of HTML files
        attribute = List1Attributes(lists[sel])
        # Use a regular expression to find the date of the webpage
        date = findall('"date-display">(.*)<', lists[sel])
    elif sel == 1 or sel == 4:
        list = List2(lists[sel])
        attribute = List2Attributes(lists[sel])
        date = findall('Last updated: (.*)\n', lists[sel])
    elif sel == 2 or sel == 5:
        list = List3(lists[sel])
        attribute = List3Attributes(lists[sel])
        date = findall('(Week Ending.*)<', lists[sel])

    # Add every list item, rank, date and attribute into the database and commit the changes
    for i in range(10):
        exe = (date[0], i + 1, list[i], attribute[i])
        top10db.execute('INSERT INTO top_ten VALUES ' + str(exe))
        connection.commit()

# Function to change between windows when the 'Back' button is pressed
def Back():
    previewscreen.withdraw()
    window1.deiconify()

# Function to use regular expressions to find the album names and the artist names and add them together, returning that list
def List1(selection):
    artistnames = findall('"artist-name">(.*)<', selection)
    albumnames = findall('"item-title">(.*)<', selection)
    albumlist = []
    for i in range(10):
        album = artistnames[i] + ' - ' + albumnames[i]
        albumlist.append(album)
    return albumlist

# Function to use regular expressions to find the cryptocurrency names, reduce the list to ten items and return it
def List2(selection):
    cryptolist = findall('"currency-name-container link-secondary".*">(.*)</a>', selection)
    del(cryptolist[10:])
    return cryptolist

# Function to use regular expressions to find the book names and return the list
def List3(selection):
    booklist = findall('/">(.*)</a>.*by', selection)
    return booklist

# Functions to find the unique attributes for the lists and return them
def List1Attributes(selection):
    artwork = findall('"(.*/coverart.*)".+alt', selection)
    return artwork

def List2Attributes(selection):
    marketcap = findall('">\n(\$.*)', selection)
    return marketcap

def List3Attributes(selection):
    cover = findall('class.*data-src="(.*)" alt', selection)
    return cover

mainloop()

pass