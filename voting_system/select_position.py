from tkinter import *
from tkinter import ttk, messagebox
from csv import reader
import selection_page


# create list of candidate positions
def create_positions():
    positions = []
    with open("candidates.csv") as csvfile:
        csv_reader = reader(csvfile)
        next(csv_reader)
        for item in csv_reader:
            position = item[1].capitalize()
            if position not in positions:
                positions.append(position)
    return positions


# opens selection_page.py with correct position passed through
def open_page(window, position, username, password):
    # check if user has voted for current position
    if check_voted(position, username, password):
        window.destroy()
        selection_page.main(position, username, password)
    else:
        return messagebox.showerror(title="Voting error", message=f"You have already voted for {position}.")


# checks if user has voted for position selected
def check_voted(position, username, password):
    with open("login_details.csv") as csvfile:
        csv_reader = reader(csvfile)
        header = next(csv_reader)
        # finds index of column with selected position
        for header_index, val in enumerate(header):
            if val == position.lower():
                index = header_index

        # checks if position column for user is set to false
        for line in csv_reader:
            if line[0] == username and line[1] == password and line[index] == "false":
                return True
        return False


def main(username, password):
    window = Tk()
    window.title("Select Position")
    window.geometry("450x200")

    Label(window, text="Select the position you would like to vote for.").grid(column=0, row=0)
    position_var = StringVar()
    position_combobox = ttk.Combobox(window, textvariable=position_var, values=create_positions())
    position_combobox.grid(column=0, row=1)
    position_combobox.current(0)
    confirm_btn = Button(window, text="Confirm",
                         command=lambda: open_page(window, position_var.get(), username, password))
    confirm_btn.grid(column=1, row=1)

    window.mainloop()
