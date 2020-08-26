from tkinter import *
from tkinter import ttk, messagebox
from csv import writer, reader
# from login import username, password
import select_position


# reads candidate names from csv file and returns as a list
def candidate_names(position):
    with open("candidates.csv") as csvfile:
        candidates = []
        next(csvfile)
        csv_reader = reader(csvfile)
        for row in csv_reader:
            if row[1] == position.lower():
                candidates.append(row[0])
        return candidates


def vote(selection1, selection2, selection3, selection4, window, username, password, position):
    order_preference = [selection1, selection2, selection3, selection4]

    # ensures at lease one selection is made
    if not selection1:
        return messagebox.showerror(title="Invalid vote", message="You must choose a first preference.")

    # ensures selections are consecutive and removes empty selections from order_preference
    if selection1 and selection2 and selection3 and selection4:
        candidate_preference = order_preference
        valid = True
    elif selection1 and selection2 and selection3 and not selection4:
        candidate_preference = [selection1, selection2, selection3]
        order_preference = [selection1, selection2, selection3, None]
        valid = True
    elif selection1 and selection2 and not (selection3 or selection4):
        candidate_preference = [selection1, selection2]
        order_preference = [selection1, selection2, None, None]
        valid = True
    elif selection1 and not (selection2 or selection3 or selection4):
        candidate_preference = [selection1]
        order_preference = [selection1, None, None, None]
        valid = True
    else:
        return messagebox.showerror(title="Invalid vote", message="Selections must be consecutive.")

    # looks for duplicate preferences
    if len(set(candidate_preference)) == len(candidate_preference):
        unique = True
    else:
        return messagebox.showerror(title="Invalid vote", message="You can only select the same candidate once.")

    # appends vote to csv file
    if valid and unique:
        # creates a csv file of candidate names
        file_name = position.lower() + ".csv"
        with open(str(file_name), "a", newline="") as csvnames:
            csv_writer = writer(csvnames)
            csv_writer.writerow(order_preference)

        voted(username, position)

        messagebox.showinfo(title="Complete",
                            message="Thank you for your vote. You will be redirected to the start page.")
        previous_page(window, username, password)
        return


# after user has voted login_details.csv column for candidate position changed to true so user cannot vote again
def voted(username, position):
    with open('login_details.csv') as details_in:
        details_reader = reader(details_in.readlines())

    with open('login_details.csv', 'w', newline="") as details_out:
        details_writer = writer(details_out)

        # header
        details_writer.writerow(["username", "password", "president", "officer1", "officer2", "officer3", "faculty1",
                                 "faculty2", "faculty3", "faculty4"])

        # find index of position
        header = next(details_reader)
        for header_index, val in enumerate(header):
            if val == position.lower():
                position_index = header_index

        # find user and replace line with "true"
        for line in details_reader:
            if line[0] == username:
                line[position_index] = "true"
                details_writer.writerow(line)
            else:
                details_writer.writerow(line)


# moves back to previous page without casting vote
def previous_page(window, username, password):
    window.destroy()
    select_position.main(username, password)


# window initialisation
def main(position, username, password):
    window = Tk()
    window.title(f"Selection: {position}")
    window.geometry("450x200")
    selection_dict = {}
    Label(window, text=f"Rank {position.lower()} candidates in order of preference.").grid(column=0, row=0)

    # creates multiple combobox's with candidates names
    for n in range(1, 5):
        Label(window, text=f"Preference {n}").grid(column=0, row=n)
        selection_dict[n - 1] = StringVar()
        candidate_combobox = ttk.Combobox(window, textvariable=selection_dict[n - 1], values=candidate_names(position))
        candidate_combobox.grid(column=1, row=n)

    Button(window, text="Confirm", command=lambda: vote(selection_dict[0].get(), selection_dict[1].get(),
                                                        selection_dict[2].get(), selection_dict[3].get(), window,
                                                        username, password, position)).grid()
    Button(window, text="Back", command=lambda: previous_page(window, username, password)).grid()

    window.mainloop()
