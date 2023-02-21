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
    
def run(event):
    user_input = e.get()
    txt.configure(state="normal")
    txt.insert("end","Me: ","Underline")
    txt.insert("end",user_input+"\n")
    if user_input=="exit":
        root.destroy()
    else:
        bot_answer = get_bot_response(user_input)
        txt.insert("end","Hope: ","Underline")
        txt.insert("end", bot_answer+"\n")
        txt.configure(state="disabled")
        txt.see("end")
        e.delete(0,"end")
    
    
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Chat with Hope")
label.pack(pady=12, padx=10)

txt = customtkinter.CTkTextbox(master=frame, width=800, height=450)
txt.pack(pady=12, padx=10)
txt.configure(state="disabled")
txt.tag_config("Underline",underline=1)

scrollbar = customtkinter.CTkScrollbar(master=txt, command=txt.yview)
scrollbar.grid(row=0, column=1, sticky="ns")

txt.configure(yscrollcommand=scrollbar.set)

e = customtkinter.CTkEntry(master=frame,placeholder_text="Enter you message", width= 800)
e.pack(pady=12, padx= 10)
e.bind('<Return>', run)

label2 = customtkinter.CTkLabel(master=frame,text='Type "exit" to Close', text_color="orange")
label2.pack(pady=12, padx=10)

root.mainloop()