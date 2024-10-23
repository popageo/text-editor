import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

def open_file(window, text_edit, file_path_var):
    filepath = askopenfilename(filetypes=[("Text Files", "*.txt")])

    if not filepath:
        return
    
    text_edit.delete(1.0, tk.END)
    with open(filepath, "r") as f:
        content = f.read()
        text_edit.insert(tk.END, content)
    
    file_path_var.set(filepath)
    window.title(f"Open File: {filepath}")

def save_file(window, text_edit, file_path_var):
    filepath = file_path_var.get()
    # If no filepath is set, prompt the user to choose one (like Save As)
    if not filepath:
        save_as_file(window, text_edit, file_path_var)
    else:
        # Write the content to the existing filepath
        with open(filepath, "w") as f:
            content = text_edit.get(1.0, tk.END)
            f.write(content)
        window.title(f"Saved File: {filepath}")

def save_as_file(window, text_edit, file_path_var):
    filepath = asksaveasfilename(filetypes=[("Text Files", "*.txt")])

    if not filepath:
        return
    
    with open(filepath, "w") as f:
        content = text_edit.get(1.0, tk.END)
        f.write(content)

    file_path_var.set(filepath)
    window.title(f"Saved As: {filepath}")

def main():
    window = tk.Tk()
    window.title("Text Editor")
    window.rowconfigure(1, minsize=400)
    window.columnconfigure(1, minsize=400)

    file_path_var = tk.StringVar()  # Stores the current file path

    text_edit = tk.Text(window, font="Helvetica 18")
    text_edit.grid(row=1, column=1)

    frame = tk.Frame(window, relief=tk.RAISED, bd=2)
    open_button = tk.Button(frame, text="Open", command=lambda: open_file(window, text_edit, file_path_var))
    save_button = tk.Button(frame, text="Save", command=lambda: save_file(window, text_edit, file_path_var))
    save_as_button = tk.Button(frame, text="Save As", command=lambda: save_as_file(window, text_edit, file_path_var))

    open_button.grid(row=0, column=0, padx=5, pady=5)
    save_button.grid(row=0, column=1, padx=5, pady=5)
    save_as_button.grid(row=0, column=2, padx=5, pady=5)
    frame.grid(row=0, column=1, sticky="ew")

    window.bind("<Control-o>", lambda x: open_file(window, text_edit, file_path_var))
    window.bind("<Control-s>", lambda x: save_file(window, text_edit, file_path_var))
    window.bind("<Control-S>", lambda x: save_as_file(window, text_edit, file_path_var)) # Control+Shift+s is interpreted as Control+S

    window.mainloop()

main()