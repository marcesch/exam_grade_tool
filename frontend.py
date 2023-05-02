"""
Not sure how to best approach this --  use https://wiki.python.org/moin/TkInter for GUI. Postpone for now


Only a small test so far, but it's nice that I can input data more or less reasonably

"""

import tkinter as tk


class TableInput(tk.Frame):
    def __init__(self, parent, rows, columns):
        super().__init__(parent)
        self.rows = rows
        self.columns = columns

        # Create a Text widget to display the table
        self.table = tk.Text(self, height=rows + 1, width=30 * (columns + 1))
        self.table.pack(side="left", fill="both", expand=True)

        # Add column headers to the table
        self.table.insert("end", f"{'Nachname':<20} {'Vorname':>10}\n")

        # Add rows to the table
        for i in range(rows):
            self.table.insert("end", f"{'':<20} {'':>10}\n")

    def get_data(self):
        # Get the data from the table
        data = []
        lines = self.table.get("1.0", "end").split("\n")
        for line in lines:
            if line.strip():
                surname, firstname = line.split()
                if surname == "Nachname":
                    print("Skipping first row...")
                    continue
                data.append({"lastname" : surname.strip(), "firstname": firstname.strip()})
                # data.append((surname.strip(), firstname.strip()))
        return data


"""



# Create a new Tkinter window
root = tk.Tk()

# Create a new TableInput widget with 5 rows and 2 columns
table_input = TableInput(root, rows=5, columns=2)
table_input.pack(side="top", fill="both", expand=True)

# Create a button to get the data from the table
button = tk.Button(root, text="Get Data", command=lambda: print(table_input.get_data()))
button.pack(side="bottom")

# Run the main event loop
root.mainloop()

"""