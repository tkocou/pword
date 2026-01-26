#1 /bin/python

## Copyright 2026 Thomas Kocourek
##
## ChangeLog
##
## 25jan2026 - initial upload
## 26jan2026 - added more extensive error checking

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

## add in GUI support
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb


command = ""

## depending on your OS file structure, you may need to update the next two lines
shuf_command = "/usr/bin/shuf"
word_library = "/usr/share/dict/words"

program_name =  "pword"

default_number_of_words = '4' ## a string representation of an positive Integer
minimum_words = '3' ## ditto
maximum_words = '6' ## ditto

def create_pw(number_of_words):
    ## Let's see if there are missing files
    flag = False
    if not os.path.isfile(word_library):
        flag = True
    if not os.access(shuf_command,os.X_OK):
        flag = True

    ## check if either file is missing
    if flag:
        mb.showwarning("Warning","'shuf' and/or the 'word' list are missing.\n Please install the missing files.\n")
        sys.exit()

    try: 
        command = shuf_command+ " --random-source=/dev/urandom -n "+str(number_of_words)+" "+word_library+" > temp.txt"
        os.system(command)

    except Exception as es:
        mb.showwarning("Warning","Has 'shuf' or a 'word' list been installed?\n")
        sys.exit()

    with open("temp.txt") as fd:
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
        super().__init__()

        
        self.words_var = tk.StringVar()

        self.protocol("WM_DELETE_WINDOW",self.goodbye)
        ## set up window dimensions, title , etc.
        self.title(program_name)

        ## Let's start the window in the center of the desktop screen
        window_height = 400
        window_width = 1000
        screen_width = self.winfo_screenwidth()   ## from tkinter library
        screen_height = self.winfo_screenheight() ## ditto
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        self.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=10)
        self.columnconfigure(2, weight=40)
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight=1)
        self.rowconfigure(3,weight=1)
        ## Set up GUI
        self.set_gui()
        self.update_phrase()


    def set_gui(self):

        self.result_text = tk.Text(self)
        self.result_text.grid(column=2, row=0, pady=(10,10), padx=(20,30), sticky='nes')
        self.result_text.configure(background="#d8f8d8", wrap="word", height=38, width=90,fg="#000000")
        self.result_text.delete(1.0,tk.END)
        self.text_scroll = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.result_text.yview)
        self.text_scroll.grid(column=2, row=0, sticky='nse', rowspan=20, pady=4, padx=(10,10))
        self.result_text['yscrollcommand'] = self.text_scroll.set

        self.urframe = tk.Frame(self)
        self.urframe.grid(column=0, row=0, columnspan=2, rowspan=20, sticky='nsew', padx=10, pady=(0,10))
        self.urframe.columnconfigure(0,weight=5)

        self.generate_button = tk.Button(self.urframe, text='New Pass Phrase. Default = 4', command=self.update_phrase)
        self.generate_button.grid(column=0, row=0, sticky='ne', padx=(5,5), pady=(5,5))

        self.set_words_button = tk.Button(self.urframe, text='Set new number of words (3-6)', command=self.set_words)
        self.set_words_button = self.set_words_button.grid(column=0,row=1, sticky="ne",padx=(10,10),pady=(10,10))

        self.entry_label = tk.Label(self.urframe, text="New Number ->")
        self.entry_label.grid(column=0, row=2, sticky='nws')

        self.words_entry = tk.Entry(self.urframe, textvariable=self.words_var, width=10)
        self.words_entry.grid(column=0, row=2, sticky='nes', padx=(5,5), pady=(5,5))

        self.help_text = tk.Button(self.urframe, text="Help", command=self.help)
        self.help_text.grid(column=0, row=3, sticky="nw",padx=(10,10), pady=(10,10))

        self.quit_app = tk.Button(self.urframe, text='Quit program', command=self.goodbye)
        self.quit_app.grid(column=0, row=3, sticky="ne",padx=(10,10), pady=(10,10))


    def goodbye(self):
        sys.exit()

    def update_phrase(self):
        
        if not isinstance(self.words_var,str):
            self.words_var = default_number_of_words
        text = create_pw(self.words_var)
        self.result_text.insert(tk.END,text)
        self.result_text.yview(tk.END)
        text = "\n------\n"
        self.result_text.insert(tk.END,text)
        self.result_text.yview(tk.END)
        self.update_idletasks()

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
        self.update_idletasks()
        mb.showinfo("Help","Move me as needed & Click OK when ready.\n")
        self.result_text.delete('1.0','end')
        self.update_phrase()


def main():
    app = App()
    app.mainloop()
    
if __name__ == '__main__':
    main()
