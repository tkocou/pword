#1 /bin/python

## Copyright 2026 Thomas Kocourek
##
## ChangeLog
##
## 25jan2026 - initial upload
## 26jan2026 - added more extensive error checking
## 08feb2026 - Got pword working on Windows 11. Executable available for download.

## password generator using normal words randomly selected
## to create a long, easier to remember password phrase
##
## written for Linux users. Other platforms will need to update the various variables
##
## requires app 'shuf' (or its equivalent) to be installed and
## a word list being installed (like wamerican as an example)
##
## the default number of words to be generated is set to 4 words
##

import os
import sys
import random
import argparse
import platform
import fileinput

## add in GUI support
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import tkinter.font as tkFont


command = ""

current_os = platform.system()
current_os_flag = True
if current_os == "Linux":
    ## depending on your OS file structure, you may need to update the next two lines
    shuf_command = "/usr/bin/shuf"
    word_library = "/usr/share/dict/words"
elif current_os == "Darwin": ## MacOS
    ## warning!
    ## the prerequisite is the installed coreutils, use command >>> "brew install coreutils"
    ##
    shuf_command = "/usr/local/bin/gshuf"
    word_library = "/usr/share/dict/words"
elif current_os == "Windows": ## MS Windows
    current_os_flag = False
    home_dir = os.path.expanduser('~')
    ## the words list should be in the user's Documents directory
    wl = os.path.join(home_dir,"Documents")
    word_library = os.path.join(wl,"words.txt")

program_name =  "pword"

default_number_of_words = '4' ## a string representation of an positive Integer
minimum_words = '3' ## ditto
maximum_words = '6' ## ditto

def win_shuf(word_file):
    lines=[line for line in fileinput.input(word_file)]
    random.shuffle(lines)
    return lines ## return a list of randomly shuffled strings


def create_pw(number_of_words):
    if current_os_flag:
        ## Linux or MacOS version
        ##
        ## Let's see if there are missing files
        flag = False
        if not os.path.isfile(word_library):
            flag = True
        if not os.access(shuf_command,os.X_OK):
            flag = True

        ## check if either file is missing
        if flag:
            mb.showwarning("Warning","'shuf' and/or the 'words' list are missing.\n Please install the missing files.\n")
            sys.exit()

        try: 
            command = shuf_command+ " --random-source=/dev/urandom -n "+str(number_of_words)+" "+word_library+" > temp.txt"
            os.system(command)

        except Exception as es:
            mb.showwarning("Warning","Has 'shuf' or a 'words' list been installed?\n")
            sys.exit()
        
    else:
        ## windows version
        if not os.path.isfile(word_library):
            mb.showwarning("Warning","The 'words' list is missing.\n Please install the 'words.txt' file into your Documents directory.\n")
            sys.exit()
        index = 0
        with open("temp.txt",'w') as fd:
            rand_list = win_shuf(word_library)
            for sl in rand_list:
                fd.writelines(sl)
                index += 1
                if index == int(number_of_words):
                    break
    
    with open("temp.txt",'r') as fd:
        result = fd.readlines()
    os.remove("temp.txt")

    pw_text = ""
    special = ['_','-']
    for element in result:
        ## select a word separator
        s = special[random.randint(0,1)]
        ## remove the '\n' from each line
        e = element[:-1]
        ## concantanate the words into a phrase
        pw_text += e + s
    ## remove the last separator and return the phrase
    return pw_text[:-1]

## start of program
class App(tk.Tk):
    def __init__(self):
        #tk.Tk.__init__(self)

        self.window = tk.Tk()

        self.window.protocol("WM_DELETE_WINDOW",self.goodbye)
        ## set up window dimensions, title , etc.
        self.window.title(program_name)
        self.words_var = tk.StringVar()
        self.words_var.set(default_number_of_words)

        ## Let's start the window in the center of the desktop screen
        window_height = 400
        window_width = 1000
        screen_width = self.window.winfo_screenwidth()   ## from tkinter library
        #print("screen width: ",screen_width)
        screen_height = self.window.winfo_screenheight() ## ditto
        #print("screen height: ",screen_height)
        x_coordinate = int((screen_width/2) - (window_width/2))
        #print("x: ",x_coordinate)
        y_coordinate = int((screen_height/2) - (window_height/2))
        #print("y: ",y_coordinate)
        #print("setting geometry...")
        self.window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))

        #print("configuring column and row settings.")
        
        #print("setting style.")
        
        self.style = tk.ttk.Style(self.window)
        '''
        available_themes = self.style.theme_names()
        #print("Available themes:", available_themes)
        '''
        self.style.theme_use("clam")
        ## set all text color to black
        self.style.configure('TButton',foreground='blue',font=('Courier New',12,'bold'))
        self.style.configure('TLabel',foreground='purple',font=('Courier New',12,'bold'))
        self.style.configure('TEntry',foreground='black')
        self.style.configure('Help.TButton',foreground='green')
        self.style.configure('Quit.TButton',foreground='red')
        
        #print("setting col & row configurations")
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)
        self.window.columnconfigure(2, weight=1)
        self.window.columnconfigure(3, weight=1)
        self.window.rowconfigure(0,weight=1)
        self.window.rowconfigure(1,weight=1)
        self.window.rowconfigure(2,weight=1)
        self.window.rowconfigure(3,weight=1)
        self.window.rowconfigure(4,weight=1)

        #print("calling function set_gui()")

        ## Set up GUI
        self.set_gui(self.window)

        ## Create a Phrase
        self.update_phrase()
        
        self.window.update_idletasks()
        #print("Looping with mainloop...")

        #self.window.mainloop()


    def set_gui(self, window):

        #print("Setting up left Frame")
        self.left_frame = tk.Frame(self.window)
        self.left_frame.configure(bg='lightblue')
        self.left_frame.grid(column=0, row=0, columnspan=2, rowspan=20, sticky='nsew', padx=10, pady=(0,10))
        self.left_frame.columnconfigure(0,weight=1)

        #print("Setting up right Frame")
        self.right_frame = tk.Frame(self.window)
        self.right_frame.configure(bg='lightgreen')
        self.right_frame.grid(column=2, row=0, columnspan=2, rowspan=20, sticky='nsew', padx=10, pady=(0,10))
        self.right_frame.columnconfigure(2,weight=1)

        my_OS = platform.system()

        if my_OS == "Linux":
            #print("Setting up Text box")
            self.text_font = tkFont.Font(family="Arial", size=12, weight="bold")
            self.result_text = tk.Text(self.right_frame)
            self.result_text.grid(column=2, row=0, columnspan=2, pady=(15,15), padx=(30,30), sticky='nsew')
            self.result_text.configure(background="#d8f8d8", wrap="word", height=21, width=63,fg="#000077", font=self.text_font)
            self.result_text.delete(1.0,tk.END)
            self.text_scroll = ttk.Scrollbar(self.right_frame, orient=tk.VERTICAL, command=self.result_text.yview)
            self.text_scroll.grid(column=2, row=0, sticky='nse', rowspan=20, pady=4, padx=(20,20))
            self.result_text['yscrollcommand'] = self.text_scroll.set
            
            #print("Setting up pass btn")
            self.generate_button = ttk.Button(self.left_frame, text='New Pass Phrase.', command=self.update_phrase)
            self.generate_button.config(style='TButton')
            self.generate_button.grid(column=0, row=0, sticky='ne', padx=(5,5), pady=(5,5))
            #print("setting up #")
            self.set_words_button = ttk.Button(self.left_frame, text='Set new number of words: 3-6', command=self.set_words)
            self.set_words_button = self.set_words_button.grid(column=0,row=1, sticky="ne",padx=(10,10),pady=(10,10))
            #print("setting up entry label")
            self.entry_label = ttk.Label(self.left_frame, text="New Number ->")
            self.entry_label.config(style='TLabel')
            self.entry_label.grid(column=0, row=2, sticky='nes',padx=(80))
            #print("setting up entry box")
            self.words_entry = tk.Entry(self.left_frame, textvariable=self.words_var, width=8)
            self.words_entry.grid(column=0, row=2, sticky='nes', padx=(5,5), pady=(5,5))
            #print("setting up help btn")
            self.help_text = ttk.Button(self.left_frame, text="Help", command=self.help)
            self.help_text.config(style='Help.TButton')
            self.help_text.grid(column=0, row=3, sticky="nw",padx=(10,10), pady=(10,10))
            #print("setting up Quit btn")
            self.quit_app = ttk.Button(self.left_frame, text='Quit program', command=self.goodbye)
            self.quit_app.config(style='Quit.TButton')
            self.quit_app.grid(column=0, row=3, sticky="ne",padx=(10,10), pady=(10,10))
            #print("setting up exit btn")
            self.help_text = ttk.Button(self.left_frame, text="Exit Help", command=self.help_exit)
            self.help_text.config(style='Quit.TButton')
            self.help_text.grid(column=0, row=4, sticky="nw",padx=(10,10), pady=(10,10))
            #print("fini GUI setup")
        else:
            #print("Setting up Text box")
            self.result_text = tk.Text(self.right_frame)
            self.result_text.grid(column=2, row=0, columnspan=2, pady=(15,15), padx=(30,30), sticky='nsew')
            self.result_text.configure(background="#d8f8d8", wrap="word", height=21, width=63,fg="#000077")
            self.result_text.delete(1.0,tk.END)
            self.text_scroll = ttk.Scrollbar(self.right_frame, orient=tk.VERTICAL, command=self.result_text.yview)
            self.text_scroll.grid(column=2, row=0, sticky='nse', rowspan=20, pady=4, padx=(20,20))
            self.result_text['yscrollcommand'] = self.text_scroll.set
            
            #print("Setting up pass btn")
            self.generate_button = tk.Button(self.left_frame, text='New Pass Phrase.', command=self.update_phrase)
            self.generate_button.grid(column=0, row=0, sticky='ne', padx=(5,5), pady=(5,5))
            #print("setting up #")
            self.set_words_button = tk.Button(self.left_frame, text='Set new number of words: 3-6', command=self.set_words)
            self.set_words_button = self.set_words_button.grid(column=0,row=1, sticky="ne",padx=(10,10),pady=(10,10))
            #print("setting up entry label")
            self.entry_label = tk.Label(self.left_frame, text="New Number ->")
            self.entry_label.grid(column=0, row=2, sticky='nes',padx=(80))
            #print("setting up entry box")
            self.words_entry = tk.Entry(self.left_frame, textvariable=self.words_var, width=8)
            self.words_entry.grid(column=0, row=2, sticky='nes', padx=(5,5), pady=(5,5))
            #print("setting up help btn")
            self.help_text = tk.Button(self.left_frame, text="Help", command=self.help)
            self.help_text.grid(column=0, row=3, sticky="nw",padx=(10,10), pady=(10,10))
            #print("setting up Quit btn")
            self.quit_app = tk.Button(self.left_frame, text='Quit program', command=self.goodbye)
            self.quit_app.grid(column=0, row=3, sticky="ne",padx=(10,10), pady=(10,10))
            #print("setting up exit btn")
            self.help_text = tk.Button(self.left_frame, text="Exit Help", command=self.help_exit)
            self.help_text.grid(column=0, row=4, sticky="nw",padx=(10,10), pady=(10,10))
            #print("fini GUI setup")

    def goodbye(self):
        sys.exit()

    def update_phrase(self):
        #print("running update_phrase")
        #print("checking for string from 'words_var' ")
        if not isinstance(self.words_var,str):
            self.words_var = default_number_of_words
        #print("using func 'create_pw()' ")
        text = create_pw(self.words_var)
        #print("adding phrase to Text box")
        self.result_text.insert(tk.END,text)
        ##print("updating yview")
        #self.result_text.yview(tk.END)
        #print("adding dividor string")
        text = "\n------\n"
        self.result_text.insert(tk.END,text)
        #print("updating yview")
        self.result_text.yview(tk.END)
        #self.window.update_idletasks()
        #print("Finishing update_phrase")

    def set_words(self):
        try:
            self.words_var = self.words_entry.get()
            if not isinstance(self.words_var,str):
                self.words_var = default_number_of_words
            self.words_entry.delete(0, 'end')
        except Exception as es:
            self.words_var = default_number_of_words
        try:
            if int(self.words_var) < int(minimum_words):
                self.words_var = minimum_words
            elif int(self.words_var) > int(maximum_words):
                self.words_var = maximum_words
        except Exception as es:
            self.words_var = default_number_of_words
        self.update_phrase()

    def help(self):
        self.result_text.delete('1.0','end')
        text = '''  Default number of words used is 4.\n\n  The Entry box (New Number) can be used to set a different number of words to use. Use the Set button to enable the word count. Bad inputs will be ignored!\n\n  The New Pass Phrase button will generate a new phrase of words based on the current number of words\n\n  Each word of the phrase will be separated by either a dash or an underscore.\n\n  The Help button gives this explanation. Remember to click the OK button.'''
        self.result_text.insert(tk.END,text)
        self.result_text.yview(tk.END)

    def help_exit(self):
        self.result_text.delete('1.0','end')
        self.update_phrase()

def main():
    app = App()
    app.window.mainloop()
    
if __name__ == '__main__':
    main()
