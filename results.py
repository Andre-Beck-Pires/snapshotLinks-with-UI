import sys
import tkinter as tk

root = tk.Tk()
root.title("Total")

links = sys.argv[1]

links_label = tk.Label(root, text=links)

links_label.grid(row=0, column=0, padx=5, pady=5)
root.mainloop()