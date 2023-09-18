from queue import Empty
import tkinter as tk
import subprocess
import sys
import os
import re
import threading

is_NL = False



 

def show_panelNoText():
    panel.place(x=0, y=0, relwidth=1, relheight=1)
    panel_label.config(text=f"Running pagecount")
    panel.lift()  # Bring the panel to the front

def show_panel(name):
    panel.place(x=0, y=0, relwidth=1, relheight=1)
    panel_label.config(text=f"Running pagecount for {name}")
    panel.lift()  # Bring the panel to the front

def hide_panel():
    panel.place_forget()  # Hide the panel

def checkbox_callback():
    if checkbox_var.get():
        checkLabel.config(text="It is on NL server")
        global is_NL
        is_NL = True
    else:
        checkLabel.config(text="It is not on NL server")
        is_NL = False

def show_COOKIE_tooltip(event):
    tooltip_COOKIE_label.place(x=event.x+100, y=event.y+100)
    tooltip_COOKIE_label.lift()
    
def hide_COOKIE_tooltip(event):
    tooltip_COOKIE_label.place_forget()

def show_TITLE_tooltip(event):
    tooltip_TITLE_label.place(x=event.x+30, y=event.y+30)
    tooltip_TITLE_label.lift()
    
def hide_TITLE_tooltip(event):
    tooltip_TITLE_label.place_forget()



def get_input():
    if(snapshotLink_entry.get() and cookie_entry.get()):
        file_name = file_name_entry.get()
        if(file_name):
            show_panel(file_name)
        else:
            show_panelNoText()
        # Retrieve the text entered in the input fields
        default_python_command = sys.executable
        python_filename = os.path.basename(default_python_command)

        snapshotLink = snapshotLink_entry.get()

        sidPattern = r"snapshot=(\d+)"
        match = re.search(sidPattern, snapshotLink)
        sid = match.group(1)

        

        cookie = cookie_entry.get()

    

        domain = domain_entry.get()
        if is_NL == True:
            server = "nl"
        else:
            server = snapshotLink[10:12]

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
root.title("Pagecount Tool")
root.geometry("500x500")


# Create a panel (a Frame) with some content
panel = tk.Frame(root, width=500, height=500, bg="lightgray")
panel_label = tk.Label(panel, text="Running pagecount for")
panel_label.pack(pady=10)
panel_button = tk.Button(panel, text="Hide Panel", command=hide_panel)
panel_button.pack()



# Create labels
title_label = tk.Label(root, text="Pagecount Tool", font=("Helvetica", 26))

file_name_label = tk.Label(root, text="File Name")
snapshotLink_label = tk.Label(root, text="Snaphot URL*")

cookie_label = tk.Label(root,text="JSESSIONID*")

domain_label = tk.Label(root, text="Filter by a domain")
checkLabel = tk.Label(root, text="Check if it is on NL server")

#define tooltips
tooltip_COOKIE_label = tk.Label(root, text="You can get it using F12 > Cookies", background="black", relief="solid", font=("Arial", 20))
tooltip_TITLE_label = tk.Label(root, text="In honor of Leo F, we will remember you", background="black", relief="solid", font=("Arial", 12))
#create toltips events



cookie_label.bind("<Enter>", show_COOKIE_tooltip)
cookie_label.bind("<Leave>", hide_COOKIE_tooltip)
title_label.bind("<Enter>",show_TITLE_tooltip)
title_label.bind("<Leave>",hide_TITLE_tooltip)
# Create input fields (Entry widgets)
file_name_entry = tk.Entry(root)
snapshotLink_entry = tk.Entry(root)

cookie_entry = tk.Entry(root)

domain_entry = tk.Entry(root)
checkbox_var = tk.BooleanVar()  # This variable will hold the checkbox state
checkbox = tk.Checkbutton(root, text="NL Server", variable=checkbox_var, command=checkbox_callback)
# Create a button to get input
submit_button = tk.Button(root, text="Submit", command=lambda: threading.Thread(target=get_input).start())



# Create a Checkbutton widget




# Use grid layout to arrange the widgets

title_label.grid(row=0, column=0, columnspan=10, padx=15, pady=10, sticky="nsew")

file_name_label.grid(row=1, column=0, padx=20, pady=20)
file_name_entry.grid(row=1, column=1, padx=20, pady=20)

snapshotLink_label.grid(row=2, column=0, padx=20, pady=20)
snapshotLink_entry.grid(row=2, column=1, padx=20, pady=20)

cookie_label.grid(row=3, column=0, padx=20, pady=20)
cookie_entry.grid(row=3, column=1, padx=20, pady=20)

domain_label.grid(row=4, column=0, padx=20, pady=20)
domain_entry.grid(row=4, column=1, padx=20, pady=20)

checkLabel.grid(row=5, column=0)
checkbox.grid(row=5,column=1)

submit_button.grid(row=10, column=0, columnspan=2, padx=5, pady=5)



hide_panel()

# Start the main event loop
root.mainloop()

# ... (rest of the UI code) ...
