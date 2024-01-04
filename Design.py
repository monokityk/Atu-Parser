# gui_script.py

import tkinter as tk
import subprocess

def update_url():
    new_url = url_entry.get()
    
    # Ensure the URL is not empty before running the script
    if new_url:
        # Replace the path with the correct path to your script
        script_path = "OneDrive/Документы/Atu-Parser 2.0.py"
        command = ["python", script_path, new_url]
        print(f"Running command: {' '.join(command)}")
        subprocess.run(command)
        
        # Update the config.ini file with the new URL
        with open("config.ini", "w") as config_file:
            config_file.write(f"[Settings]\nurl = {new_url}")
        
        print(f"Updated config.ini with URL: {new_url}")
    else:
        print("URL is empty. Please enter a valid URL.")

# Create the main window
root = tk.Tk()
root.title("URL Replacer")

# Create and place widgets
url_label = tk.Label(root, text="Enter new URL:")
url_label.pack(pady=10)

url_entry = tk.Entry(root, width=40)
url_entry.pack(pady=10)

update_button = tk.Button(root, text="Update URL", command=update_url)
update_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
