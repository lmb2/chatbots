# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 20:47:33 2023

@author: Fabian
"""

import customtkinter
from chatting_hope import get_bot_response

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("1080x750")

def send(event):
    send = "You ->" +e.get()
    txt.insert("end","\n"+send)
    
    user = e.get().lower()
    
    if(user=="hello"):
        txt.insert("end","\n"+"Bot -> Hi there")
    else:
        txt.insert("end","\n"+"Bot -> Sorry! Didnt't unterstand that")
    
    e.delete(0,"end")
    
def run(event):
    user_input = e.get()
    txt.insert("end","\n"+"Me: "+user_input)
    if user_input=="exit":
        root.destroy()
    else:
        bot_answer = get_bot_response(user_input)
        txt.insert("end","\n"+"Hope: "+bot_answer)
        e.delete(0,"end")
    
    
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Chat System")
label.pack(pady=12, padx=10)

txt = customtkinter.CTkTextbox(master=frame, width=800, height=450)
txt.pack(pady=12, padx=10)

e = customtkinter.CTkEntry(master=frame,placeholder_text="Message", width= 800)
e.pack(pady=12, padx= 10)
e.bind('<Return>', run)

root.mainloop()