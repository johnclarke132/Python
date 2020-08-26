from csv import reader
from tkinter import *
from tkinter import Tk, ttk
import individual_votes


# generates an ordered list of candidates from candidates.csv
def get_positions():
    positions = []
    with open("candidates.csv") as csvfile:
        next(csvfile)
        csv_reader = reader(csvfile)
        for item in csv_reader:
            if item[1].capitalize() not in positions:
                positions.append(item[1].capitalize())
    return positions


if __name__ == "__main__":
    window = Tk()
    window.title("Results")
    window.geometry("450x200")

    Label(window, text="Select the position you would like to view.").grid(column=0, row=0)
    position_var = StringVar()
    position_combobox = ttk.Combobox(window, textvariable=position_var, values=get_positions())
    position_combobox.current(0)
    position_combobox.grid(column=0, row=1)

    # opens page with breakdown of positions votes
    Button(window, text="Select", command=lambda: individual_votes.main(position_var.get())).grid(column=1, row=1)

    window.mainloop()
