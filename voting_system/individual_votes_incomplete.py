from tkinter import Tk
from tkinter import *
from csv import reader, writer
from operator import itemgetter


def find_candidates(position_var):

    # create list of candidates from selected position
    with open("candidates.csv") as csvfile:
        csv_reader = reader(csvfile)
        candidate_list = [name for name in csv_reader if name[-1] == position_var]
    return candidate_list


def count_votes(position_var):
    # creates csv file name
    file_name = position_var + ".csv"

    # count number of votes for each candidate using dictionary
    with open(file_name) as csvfile:
        csv_reader = list(reader(csvfile))

        # loops through each column, saving each column of votes to separate dicts
        results = []
        var_name = ['p1', 'p2', 'p3', 'p4']
        for index, position in enumerate(var_name):

            # creates new variable for each column
            position = {}
            for name in find_candidates(position_var):
                position[name[0]] = 0

            # calculates number of votes using counter and adds to dictionary
            for line in csv_reader:
                for name in position:
                    if name == line[index]:
                        position[name] += 1

            # saves each column to list
            results.append(position)

        return results


# visualises candidates and votes in table format
def visualise_results(results, window):

    # create column of names
    first_col = results[0]
    names = list(first_col.keys())
    for index, name in enumerate(names):
        Label(window, text=name).grid(column=0, row=index+1)

    # display results for each preference in separate columns
    for col_index, col in enumerate(results):
        for vote_index, name in enumerate(col):
            Label(window, text=col[name]).grid(column=col_index+1, row=vote_index+1)


# calculate winner
def winner(results, position_var):
    # create list of candidates
    names = [x[0] for x in find_candidates(position_var)]

    # check for tie
    highest_vote = max(results[0].values())
    vote_count = 0
    for candidate in results[0].values():
        if candidate == highest_vote:
            vote_count += 1
    if vote_count == 1:
        return max(results[0].items(), key=itemgetter(1))[0]

    # creates a list of duplicate votes for each preference
    duplicate_lst = []
    for preference in results:

        # reverses key,values in dict
        rev_preference = {}
        for key, value in preference.items():
            rev_preference.setdefault(value, set()).add(key)

        # creates list of keys with duplicate values
        duplicates = [key for key, values in rev_preference.items() if len(values) > 1]
        duplicate_lst.append(duplicates)

        # remove 0 from duplicates
        if 0 in duplicates:
            duplicates.remove(0)

    # finds candidates that are tied for first place
    tied_candidates = []
    for candidate, vote in results[0].items():
        if vote == duplicate_lst[0][0]:
            tied_candidates.append(candidate)

    # update results to only contain tied candidates
    for item in results:
        for name in item:
            if name not in tied_candidates:
                print(name)

    print(results)


def main(position_var):
    window = Tk()
    window.title(f"Results: {position_var}")
    window.geometry("450x200")

    position_var = position_var.lower()

    # collects all candidates from position variable and counts votes
    results_lst = count_votes(position_var)

    # show results in GUI
    visualise_results(results_lst, window)

    # calculate winner
    print(winner(results_lst, position_var))

    # displays axis for table
    Label(window, text="Candidates:").grid(column=0, row=0)
    for n in range(1, 5):
        Label(window, text=f"preference {n}").grid(column=n, row=0)

    # back button
    Button(window, text="Back", command=window.destroy).grid()

    window.mainloop()
