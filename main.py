from tkinter import *
import customtkinter
from PIL import Image
import random
import pandas
import time
import pygame


app = customtkinter.CTk()
pygame.mixer.init()
# ---------------------------- CONSTANTS ------------------------------- #
GREEN = "#98D8AA"
WHITE = "#F9F5F6"










# ---------------------------- READ FROM CSV FILE ------------------------------- #
current_card = {}
to_learn = {}
# catch filenotfound error and direct it to create a new csv file with the words that need to be learnt.
try:

    data = pandas.read_csv("words-to-learn.csv")
except FileNotFoundError:
    original_data =pandas.read_csv("ita-to-en.csv")
    to_learn = original_data.to_dict(orient="records")
else: 
    to_learn = data.to_dict(orient="records")






# ---------------------------- MOVE ONTO NEXT CARD ------------------------------- #

def next_card():
# added flip timer to global to prevent bug of flipping no matter how many cards you skip
# added global so that I can use it in multiple functions, but before it has to be a varaible assigned to a dictionary 
    global current_card, flip_timer
    app.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_language,text="Italian", fill="black")
    canvas.itemconfig(card_word, text=current_card["Italian"], fill="black")
    canvas.itemconfig(card_backgorund, image=cardfront_img)
    
    wrong_answer = ("wrong_answer.mp3")

    pygame.mixer.music.load(wrong_answer)
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.008)
    flip_timer = app.after(3000, func=flip_card)



def flip_card():
    # itemconfig give ability to change the elements in a canvas
    canvas.itemconfig(card_language, text="English", fill=WHITE)
    canvas.itemconfig(card_word, text=current_card["English"], fill=WHITE)
    canvas.itemconfig(card_backgorund, image=cardback_img)
# play sound when it shows the correct answer
    correct_answer = ("correct_answer.mp3")
    pygame.mixer.music.load(correct_answer)
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.008)


def is_known():
    
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("words-to-learn.csv", index=False)
  
    next_card()


# ---------------------------- UI SETUP ------------------------------- #

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


app.title("Languages Flashcard")
app.config(padx=50, pady=50, bg=GREEN)



# images 
cardback_img = PhotoImage(file="card_back.png")
cardfront_img = PhotoImage(file="card_front.png") 


# to time the flip of the card
flip_timer = app.after(3000, func=flip_card)


# canvas
canvas = Canvas(width=800, height=526)
card_backgorund = canvas.create_image(400, 263, image=cardfront_img)
card_language = canvas.create_text(400, 150, text="", font=("Roboto", 40,"italic"))
card_word = canvas.create_text(400, 263, text="", font=("Roboto", 50,"bold"))
canvas.grid(row=0,column=0,columnspan=2)
canvas.config(bg=GREEN, highlightthickness=0,)



# buttons
right_img = customtkinter.CTkImage(light_image=Image.open("right.png"), dark_image=Image.open("right.png"), size=(72,72))
right_button = customtkinter.CTkButton(app, bg_color=GREEN, image=right_img, text=None, cursor="hand2",fg_color=GREEN, hover=False, command=is_known)
right_button.grid(row=1, column=1,pady=20)

wrong_img = customtkinter.CTkImage(light_image=Image.open("wrong.png"), dark_image=Image.open("wrong.png"), size=(90,90))
wrong_button = customtkinter.CTkButton(app,bg_color=GREEN, image=wrong_img, text=None,cursor="hand2", fg_color=GREEN, hover=False,command=next_card)
wrong_button.grid(row=1, column=0,pady=20)





next_card()





app.mainloop()