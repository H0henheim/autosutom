import sys
import re
import os.path
from tkinter import *
import tkinter.ttk


def clear_text():
    tex.delete(1.0,END)

def calculate():
    clear_text()
    input_word = var_word.get()
    input_length = 0
    if var_length.get():
        input_length = int(var_length.get())
    input_include = var_include.get()
    input_exclude = var_exclude.get()
    line = []
    excl_regex = ''
    incl_regex = ''
    beg_word_regex = input_word
    if input_exclude:
        excl_regex = "(?:(?!.*[{}]))".format(input_exclude)
    if input_include:
        inc = []
        incl_pattern = ''
        for i in input_include:
            inc.append(i)
        i=0
        for i in inc:
            incl_regex += "(?=.*" + i + ")"
    
    final_pattern = incl_regex + excl_regex + beg_word_regex
    final_regex = r"\b{}".format(final_pattern)
    #print(final_regex)

    with open('/usr/share/dict/french') as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    word_count = 0
    for word in lines:
        if re.search(final_regex, word):
            if input_length:
                if len(word) == input_length:
                    word_count +=1
                    tex.insert(END, word + "\n")   
            else:
                word_count +=1
                tex.insert(END, word + "\n") 
    file.close()
    tex.insert(END, "\n" + "Résultat : " + str(word_count) + " mots trouvés" + "\n")


window = Tk()
window.title("Auto Sutom")

window.grid_rowconfigure(0, weight=2)
window.grid_columnconfigure(0, weight=0)
window.grid_columnconfigure(1, weight=2)

froot = Frame(window)
froot.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")

f0 = Frame(froot, bd=1, relief="sunken")
f0.grid(row=0, column=0, sticky='we', rowspan=1, padx=5, pady=5)

f1 = Frame(froot, bd=1, relief="sunken")
f1.grid(row=1, column=0, sticky='we', rowspan=1, padx=5, pady=5)

f2 = Frame(window, bd=1, relief="sunken")
f2.grid(row=0, column=1, padx=5, pady=5, sticky="NSEW", rowspan=1)

message = Label(f0, text="Sutom automatique")
message.grid(row=0, column=2, padx=5, pady=5)

label_length = Label(f1, text="Nombre de lettres : ").grid(row=1, padx=5, pady=5)
var_length = StringVar()
line_length = Entry(f1, textvariable=var_length, width=30)
line_length.grid(row=1, column=1, padx=5, pady=5)
line_length.focus()

label_word = Label(f1, text="Taper les premières lettres : ").grid(row=2, padx=5, pady=5)
var_word = StringVar()
line_word = Entry(f1, textvariable=var_word, width=30)
line_word.grid(row=2, column=1, padx=5, pady=5)

label_include = Label(f1, text="Lettres à inclure (optionnel): ").grid(row=3, padx=5, pady=5)
var_include = StringVar()
line_include = Entry(f1, textvariable=var_include, width=30)
line_include.grid(row=3, column=1, padx=5, pady=5)

label_exclude = Label(f1, text="Lettres à exclure (optionnel): ").grid(row=4, padx=5, pady=5)
var_exclude = StringVar()
line_exclude = Entry(f1, textvariable=var_exclude, width=30)
line_exclude.grid(row=4, column=1, padx=5, pady=5)

tex = Text(master=f2)
scr=Scrollbar(f2, orient=VERTICAL, command=tex.yview)
scr.grid(row=0, column=1, sticky=NS)
tex.grid(row=0, column=0, sticky=NSEW, padx=5, pady=5)
tex.config(yscrollcommand=scr.set, font=('Arial', 10), width = 35, height = 20)

label_copyright = Label(f2, text="Copyleft Hohenheim 2022", font=('Arial', 7))
label_copyright.grid(row=1, column=0)

button_calc = Button(f1, text="Valider", fg="black", command=calculate)
button_calc.grid(row=5, column=0)
window.bind('<Return>', lambda e: calculate())

if os.path.isfile('icone.ico'):
    window.iconbitmap('icone.ico')
window.geometry("770x360")
window.mainloop()
