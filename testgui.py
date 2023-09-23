'''import tkinter as tk
import tkinter.ttk as ttk


class CellSelectionFrame(ttk.Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid()

        self.cellvar = tk.StringVar()

        self.make_widgets()

    def make_widgets(self):
        self.country = ttk.Entry(self, textvariable=self.cellvar)
        self.country.grid()

        ttk.Button(self, text="Start Test", command=self.start_test).grid()

    def start_test(self):
        print(self.cellvar.get())
        
        

root = tk.Tk()
input = CellSelectionFrame(root)

cell = input.start_test()

print(cell)

root.mainloop()'''

import tkinter as tk
import tkinter.ttk as ttk

class CellSelectionFrame(ttk.Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid()

        self.cellvar = tk.StringVar()

        self.make_widgets()

    def make_widgets(self):
        self.country = ttk.Entry(self, textvariable=self.cellvar)
        self.country.grid()

        ttk.Button(self, text="Start Test", command=self.start_test).grid()

    def start_test(self):
        self.cell_value = self.cellvar.get()  # Store the value in an instance variable
        self.master.quit()  # This will exit the GUI

    def get_cell_value(self):
        return self.cell_value

root = tk.Tk()
input = CellSelectionFrame(root)

root.mainloop()  # This starts the GUI event loop, which will exit when you call self.master.quit() in the start_test method

# Now, you can access the cell value outside the class using the get_cell_value method:
cell_value = input.get_cell_value()
print(type(cell_value))

parts = cell_value.split('-')  
last_part = parts[-1]  
print(last_part)

# You can use cell_value for calculations outside the class.