# Step 1: Data Preprocessing
import re  # regular expression
from collections import Counter
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import messagebox

# Implement the function process_data which
# 1) Reads in a corpus
# #2) Changes everything to lowercase
# 3) Returns a list of words.


w = []  # words
with open('sample.txt', 'r', encoding="utf8") as f:
    file_name_data = f.read()
    file_name_data = file_name_data.lower()
    w = re.findall('\w+', file_name_data)

v = set(w)  # vocabulary


# a get_count function that returns a dictionary of word vs frequency
def get_count(words):
    word_count = {}
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count


word_count = get_count(w)

# implement get_probs function
# to calculate the probability that any word will appear if randomly selected from the dictionary

def get_probs(word_count_dict):
    probs = {}
    m = sum(word_count_dict.values())
    for key in word_count_dict.keys():
        probs[key] = word_count_dict[key] / m
    return probs


# Now we implement 4 edit word functions

# DeleteLetter:removes a letter from a given word
def DeleteLetter(word):
    delete_list = []
    split_list = []
    for i in range(len(word)):
        split_list.append((word[0:i], word[i:]))
    for a, b in split_list:
        delete_list.append(a + b[1:])
    return delete_list


delete_word_l = DeleteLetter(word="cans")


# SwitchLetter:swap two adjacent letters
def SwitchLetter(word):
    split_l = []
    switch_l = []
    for i in range(len(word)):
        split_l.append((word[0:i], word[i:]))
    switch_l = [a + b[1] + b[0] + b[2:] for a, b in split_l if len(b) >= 2]
    return switch_l


switch_word_l = SwitchLetter(word="eta")


# replace_letter: changes one letter to another
def replace_letter(word):
    split_l = []
    replace_list = []
    for i in range(len(word)):
        split_l.append((word[0:i], word[i:]))
    alphabets = 'abcdefghijklmnopqrstuvwxyz'
    replace_list = [a + l + (b[1:] if len(b) > 1 else '') for a, b in split_l if b for l in alphabets]
    return replace_list


replace_l = replace_letter(word='can')


# insert_letter: adds additional characters
def insert_letter(word):
    split_l = []
    insert_list = []
    for i in range(len(word) + 1):
        split_l.append((word[0:i], word[i:]))
    letters = 'abcdefghijklmnopqrstuvwxyz'
    insert_list = [a + l + b for a, b in split_l for l in letters]
    # print(split_l)
    return insert_list


# combining the edits
# switch operation optional
def edit_one_letter(word, allow_switches=True):
    edit_set1 = set()
    edit_set1.update(DeleteLetter(word))
    if allow_switches:
        edit_set1.update(SwitchLetter(word))
    edit_set1.update(replace_letter(word))
    edit_set1.update(insert_letter(word))
    return edit_set1


# edit two letters
def edit_two_letters(word, allow_switches=True):
    edit_set2 = set()
    edit_one = edit_one_letter(word, allow_switches=allow_switches)
    for w in edit_one:
        if w:
            edit_two = edit_one_letter(w, allow_switches=allow_switches)
            edit_set2.update(edit_two)
    return edit_set2


# get corrected word
def get_corrections(word, probs, vocab, n=2):
    suggested_word = []
    best_suggestion = []
    suggested_word = list(
        (word in vocab and word) or edit_one_letter(word).intersection(vocab) or edit_two_letters(word).intersection(
            vocab))
    best_suggestion = [[s, probs[s]] for s in list(reversed(suggested_word))]
    return best_suggestion


# Color Palette
BACKGROUND_COLOR = "#393E46"
BUTTON_COLOR = "#3282B8"
TEXT_COLOR = "#EEEEEE"
ENTRY_COLOR = "#222831"

# Load the wordlist
with open("sample.txt", "r", encoding="utf8") as file:
    file_name_data = file.read().lower()
    word_list = re.findall('\w+', file_name_data)
    vocabulary = set(word_list)


def correct_text():
    my_word = text_entry.get("1.0", tk.END).strip()
    probs = get_probs(word_count)
    tmp_corrections = get_corrections(my_word, probs, v, 2)
    for i, word_prob in enumerate(tmp_corrections):
        print(f"word {i}: {word_prob[0]}, probability {word_prob[1]:.6f}")

    text = text_entry.get("1.0", tk.END).strip()
    corrections = get_corrections(text, probs, vocabulary, 2)
    corrected_text = corrections[0][0] if corrections else "No suggestions found."
    corrected_entry.delete("1.0", tk.END)
    corrected_entry.insert(tk.END, corrected_text)


def clear_text():
    text_entry.delete("1.0", tk.END)
    corrected_entry.delete("1.0", tk.END)


def show_about():
    messagebox.showinfo("About", "This is a simple auto-correct GUI application based on wordlist.txt.")


# Create the main window
window = tk.Tk()
window.title("Auto-Correct Application")
window.configure(bg=BACKGROUND_COLOR)

# Create and position the widgets
text_label = tk.Label(window, text="Enter Text:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
text_label.pack()

text_entry = tk.Text(window, height=10, width=50, bg=ENTRY_COLOR, fg=TEXT_COLOR)
text_entry.pack()

correct_button = tk.Button(window, text="Correct", command=correct_text, bg=BUTTON_COLOR, fg=BACKGROUND_COLOR)
correct_button.pack()

clear_button = tk.Button(window, text="Clear", command=clear_text, bg=BUTTON_COLOR, fg=BACKGROUND_COLOR)
clear_button.pack()

corrected_label = tk.Label(window, text="Corrected Text:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
corrected_label.pack()

corrected_entry = tk.Text(window, height=10, width=50, bg=ENTRY_COLOR, fg=TEXT_COLOR)
corrected_entry.pack()

menu_bar = tk.Menu(window)
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menu_bar.add_cascade(label="Help", menu=help_menu)
window.config(menu=menu_bar)

# Start the main loop
window.mainloop()
