import json
from customtkinter import *
from tkinter import *
from tkinter import messagebox
from PIL import Image
from random import *
import requests
import pyperclip

import nice as dt


# ---------------------------- CONSTANTS ------------------------------- #


SCREEN = (1000, 600)

FONT_NAME = "Arial bold"
BACKGROUND_COLOR = "#242424"
SB_COLOR = "#0f0f0f"
FG_COLOR = "#0070C1"
DELETE_COLOR = "#c4372d"
VIEW_FRAME_COLOR = "#2b2d30"
ADD_TAB_LPAD = 30
DEFAULT_API_URL = "https://api.sheety.co/44c6027c9dfe9437c9cacf91b8f03a8a/guiClg/sheet1"
DEFAULT_CHAR_COUNT = 8
DEFAULT_SYMBOL_COUNT = 2
DEFAULT_NUMBER_COUNT = 2

# ---------------------------- API ------------------------------- #

api_url = DEFAULT_API_URL

data = [{'website': 'youtube', 'email': 'k7@gmail.com', 'password': 'BeastingDuck', 'id': 2},
        {'website': 'tinder', 'email': 'k11@gst.com', 'password': 'vil*2mhE#Zf6', 'id': 3}]
# response = requests.get(api_url)
# data = response.json()["sheet1"]
headers = {
    'Content-Type': 'application/json'
}


# ---------------------------- FUNCTIONS ------------------------------- #

def open_add():
    tabs.set("add")


def open_view():
    tabs.set("view")


def open_setting():
    tabs.set("setting")


def reset_entry():
    add_web_entry.delete(0, "end")
    add_mail_entry.delete(0, "end")
    add_pass_entry.delete(0, "end")


def check_exist():
    unique_data = [f"{i["website"]},{i["email"]}" for i in data]
    entered_data = f"{add_web_entry.get()},{add_mail_entry.get()}"
    if entered_data in unique_data:
        print(data[unique_data.index(entered_data)])
        return unique_data.index(entered_data) + 2
    else:
        return 0

def add_data():
    global data
    if len(add_web_entry.get()) == 0 or len(add_mail_entry.get()) == 0 or len(add_pass_entry.get()) == 0:
        messagebox.showerror(title="Values Missing", message="Make sure all values are entered")
    elif check_exist() != 0:
        print("repeated entry")
        messagebox.showwarning(title="Duplicate values", message="password with same website and email/username exist!")
    else:
        body = {
            "sheet1": {
                "website": add_web_entry.get(),
                "email": add_mail_entry.get(),
                "password": add_pass_entry.get()
            }
        }
        json_body = json.dumps(body)
        response = requests.post(api_url, headers=headers, data=json_body)
        if response.status_code == 200:
            print("Google Sheet updated successfully.")
            messagebox.showinfo(title="Data saved", message="password has been saved successfully")
            data.append({'website': body["sheet1"]["website"], 'email': body["sheet1"]["email"],
                         'password': body["sheet1"]["password"], 'id': len(data)+2})
            print(data)
            add_frame(body["sheet1"]["website"], body["sheet1"]["email"], body["sheet1"]["password"], len(data)+1)
        else:
            messagebox.showerror(title="Error:", message=f"{response.status_code}\n{response.text}")


def default_setting():
    global api_url
    global char_count
    global symbol_count
    global number_count
    api_url = DEFAULT_API_URL
    char_count = DEFAULT_CHAR_COUNT
    symbol_count = DEFAULT_SYMBOL_COUNT
    number_count = DEFAULT_NUMBER_COUNT
    pass_gen_char.delete(0, "end")
    pass_gen_char.insert(0, f"{char_count}")
    pass_gen_symb.delete(0, "end")
    pass_gen_symb.insert(0, f"{symbol_count}")
    pass_gen_num.delete(0, "end")
    pass_gen_num.insert(0, f"{number_count}")
    api_entry.delete(0, "end")
    api_entry.insert(0, f"{api_url}")

def save_setting():
    global api_url
    global char_count
    global symbol_count
    global number_count
    api_url = api_entry.get()
    char_count = int(pass_gen_char.get())
    symbol_count = int(pass_gen_symb.get())
    number_count = int(pass_gen_num.get())

def make_view_tab():
    global data_frame_list
    for i in range(len(data)):
        add_frame(data[i]["website"], data[i]["email"], data[i]["password"], data[i]["id"])


frame_counter = 0

def add_frame(webn, mailn, passwn, id):
    global frame_counter
    frame = CTkFrame(master=view_scrollframe, width=710, height=200, fg_color=VIEW_FRAME_COLOR)
    frame.grid(column=0, row=frame_counter, pady=10, padx=20)
    frame_counter += 1

    CTkLabel(frame, text="Website").grid(column=0, row=0, padx=(20, 600), pady=(10, 0), sticky="w", columnspan=5)
    CTkLabel(frame, text="Email/Username").grid(column=0, row=1, padx=(20, 20), pady=(10, 0), sticky="w")
    CTkLabel(frame, text="Password").grid(column=0, row=2, padx=(20, 0), pady=(10, 7), sticky="w")

    web = CTkEntry(frame, width=350)
    web.insert(0, webn)
    web.configure(state="readonly")
    web.grid(column=1, row=0, sticky="ew")

    mail = CTkEntry(frame)
    mail.insert(0, mailn)
    mail.configure(state="readonly")
    mail.grid(column=1, row=1, sticky="ew")

    passw = CTkEntry(frame)
    passw.insert(0, passwn)
    passw.configure(state="readonly")
    passw.grid(column=1, row=2, sticky="ew")

    CTkButton(frame, text="copy", command= lambda :clipboard(id, False), image=clipboard_img, width=15).grid(column=3, row=1, sticky="ew")
    CTkButton(frame, text="copy", command= lambda :clipboard(id, True), image=clipboard_img, width=15).grid(column=3, row=2, sticky="ew")
    # CTkButton(frame, text="delete", width=70, hover_color=DELETE_COLOR).grid(column=4, row=0, rowspan=3, sticky="nse")

    data_frame_list.append(frame)

def clipboard(id, passw):
    for i in range(len(data)):
        if data[i]["id"] == id:
            if passw:
                print(f"password : {data[i]["password"]}")
                pyperclip.copy(data[i]["password"])
            else:
                print(f"email : {data[i]["email"]}")
                pyperclip.copy(data[i]["email"])

# def delete(id):
#     res = messagebox.askyesno(title="Delete?", message="Are you sure you want to delete?")
#     # response = requests.delete(f"{api_url}/{id}")
#     # if response.status_code == 200:
#     if True:
#         messagebox.showinfo(title="Deleted", message="Password detail has been deleted successfully")
#     else:
#         messagebox.showerror(title="Delete Failed", message="Password detail was not deleted")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

char_count = 8
symbol_count = 2
number_count = 2

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(char_count)]
    password_symbols = [choice(symbols) for _ in range(symbol_count)]
    password_numbers = [choice(numbers) for _ in range(number_count)]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    add_pass_entry.delete(0, "end")
    add_pass_entry.insert(0, password)
    print("pass Gen")


# ---------------------------- UI SETUP ------------------------------- #


window = CTk()

window.title("Password Generator")
window.geometry(f"{SCREEN[0]}x{SCREEN[1]}")
window.resizable(False, False)

#   SIDE BAR

lock_img = CTkImage(light_image=Image.open("remind.png"), size=(150, 150))
setting_img = CTkImage(light_image=Image.open("settings_icon.png"))
plus_img = CTkImage(light_image=Image.open("plus_icon.png"))
triple_img = CTkImage(light_image=Image.open("triple_line_icon.png"))
clipboard_img = CTkImage(light_image=Image.open("Clipboard.png"))

side_bar = CTkFrame(master=window, fg_color=SB_COLOR, width=250, height=SCREEN[1])
side_bar.pack(fill="y", anchor="w", side="left")

label = CTkLabel(master=side_bar, image=lock_img, text="", width=250, height=250, bg_color=SB_COLOR)
label.pack()

add_tab_but = CTkButton(master=side_bar, text="Add Password", width=250, height=50, corner_radius=0,
                        fg_color=SB_COLOR, hover_color=FG_COLOR, font=("arial", 20), image=plus_img,
                        command=open_add)
add_tab_but.pack()

view_tab_but = CTkButton(master=side_bar, text="View Password", width=250, height=50, fg_color=SB_COLOR,
                         corner_radius=0, hover_color=FG_COLOR, font=("arial", 20), image=triple_img,
                         command=open_view)
view_tab_but.pack()

setting_tab_but = CTkButton(master=side_bar, text="Settings", width=250, height=50, corner_radius=0,
                            fg_color=SB_COLOR, hover_color=FG_COLOR, font=("arial", 20), image=setting_img,
                            command=open_setting)
setting_tab_but.pack(side="bottom", ipady=10)

#   Tabs

tabs = CTkTabview(master=window, height=SCREEN[1], fg_color="transparent", state="disabled",
                               segmented_button_fg_color=BACKGROUND_COLOR, segmented_button_unselected_color=BACKGROUND_COLOR,
                               segmented_button_selected_color=BACKGROUND_COLOR, text_color_disabled=BACKGROUND_COLOR)
tabs.pack(fill="both", side="top", anchor=S)

add_tab = tabs.add("add")
view_tab = tabs.add("view")
setting_tab = tabs.add("setting")

#   Add Tabs

add_Label = CTkLabel(master=tabs.tab("add"), text="Add Password", font=(FONT_NAME, 50))
add_Label.grid(column=0, row=0, pady=(50, 0), padx=(ADD_TAB_LPAD, 0), sticky=W)

add_web_label = CTkLabel(master=tabs.tab("add"), text="Website", font=(FONT_NAME, 20))
add_web_label.grid(column=0, row=1, pady=(50, 0), padx=(ADD_TAB_LPAD, 0), sticky=W)
add_web_entry = CTkEntry(master=tabs.tab("add"))

add_web_entry.insert(0, dt.value)

add_web_entry.grid(column=0, row=2, padx=(ADD_TAB_LPAD, 0), sticky="ew", columnspan=2)

add_mail_label = CTkLabel(master=tabs.tab("add"), text="Email/Username", font=(FONT_NAME, 20))
add_mail_label.grid(column=0, row=3, pady=(30, 0), padx=(ADD_TAB_LPAD, 0), sticky=W)
add_mail_entry = CTkEntry(master=tabs.tab("add"))
add_mail_entry.grid(column=0, row=4, padx=(ADD_TAB_LPAD, 0), sticky="ew", columnspan=2)

add_pass_label = CTkLabel(master=tabs.tab("add"), text="Password", font=(FONT_NAME, 20))
add_pass_label.grid(column=0, row=5, pady=(30, 0), padx=(ADD_TAB_LPAD, 0), sticky=W)
add_pass_entry = CTkEntry(master=tabs.tab("add"), width=500)
add_pass_entry.grid(column=0, row=6, padx=(ADD_TAB_LPAD, 0), sticky="w", columnspan=2)

add_pass_gen = CTkButton(master=tabs.tab("add"), text="Generate", command=generate_password)
add_pass_gen.grid(column=1, row=6, sticky=E)

add_reset_but = CTkButton(master=tabs.tab("add"), text="Reset", font=(FONT_NAME, 20), border_color=FG_COLOR,
                          border_width=2, fg_color="transparent", command=reset_entry)
add_reset_but.grid(column=0, row=7, pady=(90, 0), ipadx=90)

add_save_but = CTkButton(master=tabs.tab("add"), text="Save", font=(FONT_NAME, 20), border_color=FG_COLOR,
                         border_width=2, fg_color="transparent", command=add_data)
add_save_but.grid(column=1, row=7, pady=(90, 0), ipadx=90)

#   setting Tabs

view_Label = CTkLabel(master=tabs.tab("setting"), text="Settings", font=(FONT_NAME, 50))
view_Label.grid(column=0, row=0, pady=(50, 0), padx=(ADD_TAB_LPAD, 0), sticky=W)

api_label = CTkLabel(master=tabs.tab("setting"), text="API URL", font=(FONT_NAME, 20))
api_label.grid(column=0, row=1, pady=(50, 0), padx=(ADD_TAB_LPAD, 0), sticky=W)
api_entry = CTkEntry(master=tabs.tab("setting"), width=670)
api_entry.grid(column=0, row=2, padx=(ADD_TAB_LPAD, 0), sticky="ew", columnspan=2)

pass_gen_label = CTkLabel(master=tabs.tab("setting"), text="Password Generator", font=(FONT_NAME, 20))
pass_gen_label.grid(column=0, row=3, pady=(10, 0), padx=(ADD_TAB_LPAD, 0), sticky=W)

pass_gen_frame = CTkFrame(master=tabs.tab("setting"))
pass_gen_frame.grid(column=0, row=4, columnspan=2, sticky="ew", padx=(30,0))

CTkLabel(master=pass_gen_frame, text="Characters", font=(FONT_NAME, 15)).grid(column=0, row=0, sticky="w", padx=(0, 60))
CTkLabel(master=pass_gen_frame, text="Symbols", font=(FONT_NAME, 15)).grid(column=0, row=1, sticky="w")
CTkLabel(master=pass_gen_frame, text="numbers", font=(FONT_NAME, 15)).grid(column=0, row=2, sticky="w")

pass_gen_char = CTkEntry(master=pass_gen_frame)
pass_gen_char.grid(column=1, row=0, pady=5)

pass_gen_symb = CTkEntry(master=pass_gen_frame)
pass_gen_symb.grid(column=1, row=1, pady=5)

pass_gen_num = CTkEntry(master=pass_gen_frame)
pass_gen_num.grid(column=1, row=2, pady=5)

default_setting()

set_reset_but = CTkButton(master=tabs.tab("setting"), text="Reset", font=(FONT_NAME, 20), border_color=FG_COLOR,
                          border_width=2, fg_color="transparent", command=default_setting)
set_reset_but.grid(column=0, row=7, pady=(90, 0), ipadx=90, padx=(20, 0))

set_save_but = CTkButton(master=tabs.tab("setting"), text="Save", font=(FONT_NAME, 20), border_color=FG_COLOR,
                         border_width=2, fg_color="transparent", command=save_setting)
set_save_but.grid(column=1, row=7, pady=(90, 0), ipadx=90, padx=(20, 0))

#   view tab

view_scrollframe = CTkScrollableFrame(master=tabs.tab("view"), orientation="vertical", width=600, height=750, fg_color="transparent")
view_scrollframe.pack(fill="both")


names = ["Alice", "Bob", "Charlie", "David", "Emma", "Frank"]
data_frame_list = []

make_view_tab()


window.mainloop()