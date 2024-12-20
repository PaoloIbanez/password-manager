from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # Adjust these values to make passwords shorter or longer
    nr_letters = randint(8, 10)    # random count of letters
    nr_symbols = randint(2, 4)     # random count of symbols
    nr_numbers = randint(2, 4)     # random count of digits

    password_letters = [choice(letters) for _ in range(nr_letters)]
    password_symbols = [choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [choice(numbers) for _ in range(nr_numbers)]

    # Combine all chosen characters
    password_list = password_letters + password_symbols + password_numbers

    # Shuffle the resulting list to ensure randomness
    shuffle(password_list)

    # Join the characters to form the final password string
    password = "".join(password_list)

    # Clear the current password entry
    password_entry.delete(0, END)
    # Insert the newly generated password
    password_entry.insert(0, password)
    pyperclip.copy(password)







# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    # Check if any of the fields are empty
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showwarning(title="Oops!", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                # read old data
                data = json.load(data_file)
        except FileNotFoundError:
            # If no data file, we start a new dictionary
            data = {}

        # update old data with new data
        data.update(new_data)

        with open("data.json", "w") as data_file:
            # saving updated data
            json.dump(data, data_file, indent=4)

        # Clear the entries
        website_entry.delete(0, END)
        password_entry.delete(0, END)





# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
#         this is in case try is successful

        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message="No details for the website exists.")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)


canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# first we create the labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0, sticky="E")  # stick label to East (right) so it aligns nicely
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0, sticky="E")
password_label = Label(text="Password:")
password_label.grid(row=3, column=0, sticky="E")

# Entries (use consistent widths)
entry_width = 33
website_entry = Entry(width=entry_width)
website_entry.grid(row=1, column=1, sticky="W")
website_entry.focus()

email_entry = Entry(width=entry_width)
email_entry.grid(row=2, column=1, sticky="W")
email_entry.insert(0, "example@gmail.com")

password_entry = Entry(width=entry_width)
password_entry.grid(row=3, column=1, sticky="W")

# Buttons
search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(row=1, column=2, sticky="W")  # Keep it in the same row as website_entry

generate_password_button = Button(text="Generate Password", width=14, command=generate_password)
generate_password_button.grid(row=3, column=2, sticky="W")

add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)


window.mainloop()
