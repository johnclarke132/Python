from tkinter import messagebox, Label, Entry, Button, StringVar, Tk
from csv import reader
from select_position import main


# checks login credentials against login_details.csv and if user has voted before
def login(username, password):
    with open("login_details.csv") as csvfile:
        csv_reader = reader(csvfile)
        next(csv_reader)
        for row in csv_reader:
            # if login details are correct open voting page3
            if voted(username, password):
                window.destroy()
                return main(username, password)
            # if login details are correct but they have already voted, raise error
            elif row[0] == username and row[1] == password:
                return messagebox.showerror(title="Login error", message="You have already voted.")
        # else return invalid login error
        return messagebox.showerror(title="Login error", message="Invalid login. Please try again.")


# checks if user has voted for every position already
def voted(username, password):
    with open("login_details.csv") as csvfile:
        next(csvfile)
        csv_reader = reader(csvfile)
        for line in csv_reader:
            # if positions still available to vote for: continue
            if line[0] == username and line[1] == password and ("false" in line[2::]):
                return True
    return False


if __name__ == "__main__":
    window = Tk()
    window.title("Login")
    window.geometry("450x200")

    username_label = Label(window, text="Username").grid(column=0, row=0)
    username = StringVar()
    username_entry = Entry(window, width=20, textvariable=username).grid(column=1, row=0)

    password_label = Label(window, text="Password").grid(column=0, row=1)
    password = StringVar()
    password_entry = Entry(window, width=20, textvariable=password, show="*").grid(column=1, row=1)

    login_btn = Button(window, text="Login", command=lambda: login(username.get(), password.get()))
    login_btn.grid(column=0, row=2)

    window.mainloop()
