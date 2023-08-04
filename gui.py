from queue import Empty
import tkinter as tk
import subprocess

def get_input():
    # Retrieve the text entered in the input fields
    sid = sid_entry.get()
    server = server_entry.get()
    cookie = cookie_entry.get()
    file_name = file_name_entry.get()
    domain = domain_entry.get()

    
    # Build the command to run the getLinks.py script with the provided arguments
    if(file_name):
        command = f"py getLinks.py -s {sid} -w {server} -c {cookie} -f true -o {file_name}"
    else:
        command = f"py getLinks.py -s {sid} -w {server} -c {cookie} -f true"
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

# Create labels
sid_label = tk.Label(root, text="SID:*")
server_label = tk.Label(root, text="Server:*")
cookie_label = tk.Label(root,text="JSESSIONID*")
file_name_label = tk.Label(root, text="File Name")
domain_label = tk.Label(root, text="Filter by a domain")


# Create input fields (Entry widgets)
sid_entry = tk.Entry(root)
server_entry = tk.Entry(root)
cookie_entry = tk.Entry(root)
file_name_entry = tk.Entry(root)
domain_entry = tk.Entry(root)

# Create a button to get input
submit_button = tk.Button(root, text="Submit", command=get_input)
# Use grid layout to arrange the widgets
file_name_label.grid(row=0, column=0, padx=5, pady=5)
file_name_entry.grid(row=0, column=1, padx=5, pady=5)
sid_label.grid(row=1, column=0, padx=5, pady=5)
sid_entry.grid(row=1, column=1, padx=5, pady=5)
server_label.grid(row=2, column=0, padx=5, pady=5)
server_entry.grid(row=2, column=1, padx=5, pady=5)
cookie_label.grid(row=3, column=0, padx=5, pady=5)
cookie_entry.grid(row=3, column=1, padx=5, pady=5)
domain_label.grid(row=4, column=0, padx=5, pady=5)
domain_entry.grid(row=4, column=1, padx=5, pady=5)
submit_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Start the main event loop
root.mainloop()

# ... (rest of the UI code) ...
