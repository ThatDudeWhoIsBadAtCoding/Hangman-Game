from math import ceil
from tkinter import Canvas, Tk, ALL, Entry, Button, END
from fetcher import get_words
from pyperclip import copy as pyperclipCopy
i = 0
entry = None
button = None
word = None
words = None


class Word:
    def __init__(self, word) -> None:
        self.content = word
        self.under = ["_" for _ in list(self.content)]
        self.und = lambda: " ".join(self.under)
        self.li = list(word)
        self.hints = []
        self.length = len(self.content)
        self.lives = ceil(self.length / 2) + 2

    def delete_word(self, canvas, tag):
        canvas.delete(tag)

    def add_text(self, canvas, x, y, font, text, fill, tag):
        canvas.create_text(x, y, font=font, text=text, fill=fill, tag=tag)


def start_game(canvas) -> None:
    global word
    global i
    global words
    i = 0
    words = get_words(url)[:7]
    canvas.delete(ALL)
    update_word(words)
    final = Entry(window, width=5)
    canvas.create_window(500, 450, window=final)
    entry = Entry(window)
    canvas.create_window(500, 100, window=entry)
    last = Button(window, text="Submit Answer",
                  command=lambda: check_word(entry.get(), word, words, entry))
    canvas.create_window(500, 130, window=last)
    button = Button(window, text="Search Letter",
                    command=lambda: search(word, final.get(), final))
    canvas.create_window(500, 480, window=button)


def update_word(words) -> None:
    global i
    global word
    global canvas
    if i >= len(words):
        game_end(canvas, word)
        return
    word = Word(words[i])
    pyperclipCopy(word.content)
    word.delete_word(canvas, "curr_word")
    word.delete_word(canvas, "footer")
    word.delete_word(canvas, "lives")
    word.add_text(canvas, 500, 250, ("Arial", 50), word.und(),
                  "#FFFFFF", "curr_word")
    word.add_text(canvas, 500, 320, ("Arial", 20), F"The Word is {word.length} letters long",
                  "#FFFFFF", "footer")
    word.add_text(canvas, 940, 25, ("Arial", 20),
                  f"Lives = {word.lives}", "#FFFFFF", "lives")


def search(word, letter, inp):
    inp.delete(0, END)
    if len(letter) <= 0:
        return
    if len(letter) > 1:
        letter = letter[0]
    if letter not in word.li:
        word.delete_word(canvas, "lives")
        word.lives -= 1
        if word.lives < 0:
            game_over(canvas, word)
            return
        elif word.lives == 0:
            word.add_text(canvas, 940, 25, ("Arial", 20),
                          "Last Shot!", "#FFFFFF", "lives")
            return
        word.add_text(canvas, 940, 25, ("Arial", 20),
                      F"Lives = {word.lives}", "#FFFFFF", "lives")
    else:
        for i in range(word.length):
            if (word.li[i] == letter) and i not in word.hints:
                word.under[i] = word.li[i]
                word.hints.append(i)
        word.delete_word(canvas, "curr_word")
        word.add_text(canvas, 500, 250, ("Arial", 50), word.und(),
                      "#FFFFFF", "curr_word")


def check_word(answer, word, words, inp) -> None:
    global canvas
    global i
    inp.delete(0, END)
    if len(answer) <= 0:
        return
    if word.content == answer:
        i += 1
        update_word(words)
        return
    game_over(canvas, word)


def game_over(canvas, word):
    canvas.delete(ALL)
    word.add_text(canvas, 500, 250, ("Arial", 50), f"           You Lost!\n   The word was {word.content}.\
    \n          Try again?",
                  "#FFFFFF", "game_over")
    button = Button(window, text="Try Again",
                    command=lambda: start_game(canvas))
    canvas.create_window(500, 480, window=button)


def game_end(canvas, word):
    canvas.delete(ALL)
    word.add_text(canvas, 500, 250, ("Arial", 50), f"   You Won!\n   Great Job!!.\
    \n  Play again?",
                  "#FFFFFF", "game_over")
    button = Button(window, text="Play Again",
                    command=lambda: start_game(canvas))
    canvas.create_window(500, 480, window=button)


url = "https://www.thefreedictionary.com/dictionary.htm"
window = Tk()
window.title = "Hangman!"
canvas = Canvas(window, bg="#000000", height=500, width=1000)
canvas.pack()
window.resizable(False, False)
start_game(canvas)
window.mainloop()
