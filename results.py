import sys
import tkinter as tk

def close_window():
    root.destroy()

root = tk.Tk()
root.title("Total")

links = sys.argv[1]

links_label = tk.Label(root, text=links)
links_label.grid(row=0, column=0, padx=5, pady=5)
close_button = tk.Button(root, text="Close", command=close_window)
close_button.grid(row=1, column=0, padx=5, pady=5)

root.mainloop()