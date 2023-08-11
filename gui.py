from queue import Empty
import tkinter as tk
import subprocess
import sys
import os
import re

#tooltip methods
def show_SID_tooltip(event):
    tooltip_SID_label.place(x=event.x+100, y=event.y+100)
    tooltip_SID_label.lift()
    
def hide_SID_tooltip(event):
    tooltip_SID_label.place_forget()

def show_SERVER_tooltip(event):
    tooltip_SERVER_label.place(x=event.x+100, y=event.y+100)
    tooltip_SERVER_label.lift()
    
def hide_SERVER_tooltip(event):
    tooltip_SERVER_label.place_forget()

def show_COOKIE_tooltip(event):
    tooltip_COOKIE_label.place(x=event.x+100, y=event.y+100)
    tooltip_COOKIE_label.lift()
    
def hide_COOKIE_tooltip(event):
    tooltip_COOKIE_label.place_forget()



def get_input():
    # Retrieve the text entered in the input fields
    default_python_command = sys.executable
    python_filename = os.path.basename(default_python_command)

    snapshotLink = snapshotLink_entry.get()

    sidPattern = r"snapshot=(\d+)"
    match = re.search(sidPattern, snapshotLink)
    sid = match.group(1)

    server = snapshotLink[10:12]

    cookie = cookie_entry.get()

    file_name = file_name_entry.get()

    domain = domain_entry.get()

    
    # Build the command to run the getLinks.py script with the provided arguments
    if(file_name):
        command = f"{python_filename} getLinks.py -s {sid} -w {server} -c {cookie} -f true -o {file_name}"
    else:
        command = f"{python_filename} getLinks.py -s {sid} -w {server} -c {cookie} -f true"
    print(command)
    # Execute the command using subprocess
    try:
        subprocess.run(command, shell=True, check=True)
        print("Script executed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    
    # Add any additional actions you want after running the script.

# ... (rest of the UI code) ...
# Create the main window
root = tk.Tk()
root.title("Input Fields")
root.geometry("500x500")





# Create labels
snapshotLink_label = tk.Label(root, text="Snaphot URL")

cookie_label = tk.Label(root,text="JSESSIONID*")
file_name_label = tk.Label(root, text="File Name")
domain_label = tk.Label(root, text="Filter by a domain")

#define tooltips
tooltip_COOKIE_label = tk.Label(root, text="You can get it using F12 > Cookies", background="black", relief="solid", font=("Arial", 20))

#create toltips events



cookie_label.bind("<Enter>", show_COOKIE_tooltip)
cookie_label.bind("<Leave>", hide_COOKIE_tooltip)
# Create input fields (Entry widgets)

snapshotLink_entry = tk.Entry(root)

cookie_entry = tk.Entry(root)
file_name_entry = tk.Entry(root)
domain_entry = tk.Entry(root)

# Create a button to get input
submit_button = tk.Button(root, text="Submit", command=get_input)
# Use grid layout to arrange the widgets
file_name_label.grid(row=0, column=0, padx=20, pady=20)
file_name_entry.grid(row=0, column=1, padx=20, pady=20)

snapshotLink_label.grid(row=1, column=0, padx=20, pady=20)
snapshotLink_entry.grid(row=1, column=1, padx=20, pady=20)

cookie_label.grid(row=3, column=0, padx=20, pady=20)
cookie_entry.grid(row=3, column=1, padx=20, pady=20)

domain_label.grid(row=4, column=0, padx=20, pady=20)
domain_entry.grid(row=4, column=1, padx=20, pady=20)



submit_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

# Start the main event loop
root.mainloop()

# ... (rest of the UI code) ...
