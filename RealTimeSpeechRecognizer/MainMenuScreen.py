import tkinter as tk
from RealTimeSpeechRecognizer.AudioStreamReceiver.BaseAudioStreamReceiver import BaseAudioStreamReceiver

root = tk.Tk()
root.geometry("700x600")
root.title("Translation")
root.configure(bg="white")

block1 = None
block2 = None

# FIelds
isButtonClicked = False

# Первая часть
block1 = tk.Frame(root, bg="red")
block1.pack(side=tk.TOP, padx=20, pady=10, anchor=tk.W)

button = tk.Button(root, text="Paused", command=lambda: doOnBtnClicked())
button.pack(anchor=tk.NE)

label1 = tk.Label(block1, text="Choose the language to translate")
label1.pack(anchor="w", side=tk.TOP, padx=10, pady=10)

OPTIONS = ["English", "Russian"]
variable = tk.StringVar(root)
variable.set(OPTIONS[0]) # default value
option_menu = tk.OptionMenu(block1, variable, *OPTIONS)
option_menu.pack(anchor="w", side=tk.TOP, padx=10, pady=10)

block2 = tk.Frame(root, bg="red")
block2.pack(side=tk.TOP, padx=20, pady=10, anchor=tk.W)

label2 = tk.Label(block2, text="Translation result")
label2.pack(anchor="w", side=tk.TOP, padx=10, pady=10)

text_field = tk.Text(block2, height=15, bg="gray")
text_field.pack(anchor="w", fill=tk.BOTH, expand=True, padx=10, pady=10)

# Вторая часть
block3 = tk.Frame(root, bg="red")
block3.pack(side=tk.TOP, padx=20, pady=10, anchor=tk.W)

label3 = tk.Label(block3, text="Interface language")
label3.pack(anchor="w", side=tk.TOP, padx=10, pady=10)

OPTIONS = ["English", "Russian"]
variable = tk.StringVar(root)
variable.set(OPTIONS[0]) # default value
option_menu = tk.OptionMenu(block3, variable, *OPTIONS)
option_menu.pack(anchor="w", side=tk.TOP, padx=10, pady=10)

block4 = tk.Frame(root, bg="red")
block4.pack(side=tk.TOP, padx=20, pady=10, anchor=tk.W)

label4 = tk.Label(block4, text="Theme")
label4.pack(anchor="w", side=tk.TOP, padx=10, pady=10)

OPTIONS = ["Light", "Night"]
variable = tk.StringVar(root)
variable.set(OPTIONS[0]) # default value
option_menu = tk.OptionMenu(block4, variable, *OPTIONS)
option_menu.pack(anchor="w", side=tk.TOP, padx=10, pady=10)

block5 = tk.Frame(root, bg="red")
block5.pack(side=tk.TOP, padx=20, pady=10, anchor=tk.W)

label5 = tk.Label(block5, text="Type of translation display")
label5.pack(anchor="w", side=tk.TOP, padx=10, pady=10)

OPTIONS = ["In a separator window", "In the program"]
variable = tk.StringVar(root)
variable.set(OPTIONS[0]) # default value
option_menu = tk.OptionMenu(block5, variable, *OPTIONS)
option_menu.pack(anchor="w", side=tk.TOP, padx=10, pady=10)

# Третья часть
block6 = tk.Frame(root, bg="red")
block6.pack(side=tk.TOP, padx=20, pady=10, anchor=tk.W)

label6 = tk.Label(block6, text="List of translates")
label6.pack(anchor="w", side=tk.TOP, padx=10, pady=10)

label7 = tk.Label(block6, text="First translate.txt")
label7.pack(anchor="w", side=tk.TOP, padx=10, pady=10)

label8 = tk.Label(block6, text="Second translate.txt")
label8.pack(anchor="w", side=tk.TOP, padx=10, pady=10)

block8 = tk.Frame(root, bg="red")
block8.pack(side=tk.TOP, padx=20, pady=10, anchor=tk.W)

label9 = tk.Label(block8, text="Sorting")
label9.pack(anchor="w", side=tk.TOP, padx=10, pady=10)

OPTIONS = ["By date", "By alphabet"]
variable = tk.StringVar(root)
variable.set(OPTIONS[0]) # default value
option_menu = tk.OptionMenu(block8, variable, *OPTIONS)
option_menu.pack(anchor="w", side=tk.TOP, padx=10, pady=10)

# Отображение кнопок
frame = tk.Frame(root)
frame.pack(side=tk.BOTTOM, pady=20)

home_button = tk.Button(frame, text="Home")
home_button.pack(anchor="w", side=tk.LEFT, padx=10)

settings_button = tk.Button(frame, text="Settings")
settings_button.pack(anchor="w", side=tk.LEFT, padx=10)

translates_button = tk.Button(frame, text="Translates")
translates_button.pack(anchor="w", side=tk.LEFT, padx=10)

# Функции для кнопок
def show_first_part():
    block3.pack_forget()
    block4.pack_forget()
    block5.pack_forget()
    block6.pack_forget()
    block8.pack_forget()
    settings_button.configure(bg="white")
    translates_button.configure(bg="white")
    home_button.configure(bg="blue")
    block1.pack(side=tk.TOP, padx=20, pady=10, anchor=tk.W)
    block2.pack(side=tk.TOP, padx=20, pady=10, anchor=tk.W)

def show_second_part():
    block1.pack_forget()
    block2.pack_forget()
    block6.pack_forget()
    block8.pack_forget()
    home_button.configure(bg="white")
    translates_button.configure(bg="white")
    settings_button.configure(bg="blue")
    block3.pack(side=tk.TOP, padx=20, pady=10, anchor=tk.W)
    block4.pack(side=tk.TOP, padx=20, pady=10, anchor=tk.W)
    block5.pack(side=tk.TOP, padx=20, pady=10, anchor=tk.W)

def show_third_part():
    block1.pack_forget()
    block2.pack_forget()
    block3.pack_forget()
    block4.pack_forget()
    block5.pack_forget()
    home_button.configure(bg="white")
    settings_button.configure(bg="white")
    translates_button.configure(bg="blue")
    block6.pack(side=tk.TOP, padx=20, pady=10, anchor=tk.W)
    block8.pack(side=tk.TOP, padx=20, pady=10, anchor=tk.W)

def doOnBtnClicked():
    global isButtonClicked
    if isButtonClicked == True:
        button.configure(text="Paused")
        isButtonClicked = False
        text_field.insert(tk.END, "Unclicked")
    else:
        button.configure(text="Running")
        isButtonClicked = True
        text_field.insert(tk.END, "Clicked")

# Привязка функций к кнопкам
home_button.configure(command=show_first_part)
settings_button.configure(command=show_second_part)
translates_button.configure(command=show_third_part)

# Отображение первой части и кнопок
show_first_part()

root.mainloop()