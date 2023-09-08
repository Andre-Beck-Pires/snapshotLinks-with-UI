import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Checkbox Example")

# Create a function to handle checkbox state changes
def checkbox_callback():
    if checkbox_var.get():
        label.config(text="Checkbox is checked")
    else:
        label.config(text="Checkbox is unchecked")

# Create a Checkbutton widget
checkbox_var = tk.BooleanVar()  # This variable will hold the checkbox state
checkbox = tk.Checkbutton(root, text="Check me", variable=checkbox_var, command=checkbox_callback)
checkbox.pack()

# Create a label to display checkbox state
label = tk.Label(root, text="Checkbox is unchecked")
label.pack()

# Start the main loop
root.mainloop()
