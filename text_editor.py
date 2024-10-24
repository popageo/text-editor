import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import simpledialog

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
    # If no filepath is set, prompt the user to choose one
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

def find_text(query, text_edit):
    text_edit.tag_remove("highlight", "1.0", tk.END)  # Clear existing highlights
    if query:  # If there is a query
        start_pos = "1.0"  # Start searching from the beginning
        while True:
            # Search for the query string within the text
            start_pos = text_edit.search(query, start_pos, stopindex=tk.END, nocase=True)  
            if not start_pos:  # If no more occurrences are found, break the loop
                break   
            end_pos = f"{start_pos}+{len(query)}c"  # Determine the end position of the text found
            text_edit.tag_add("highlight", start_pos, end_pos)  # Highlight the text found
            start_pos = end_pos  # Move past the current found text for the next search
        # Set the highlighting style
        text_edit.tag_config("highlight", background="yellow", foreground="black")

def prompt_find_text(text_edit):
    query = simpledialog.askstring("Find", "Enter text to find:")
    if query:
        find_text(query, text_edit)

def toggle_theme(text_edit):
    current_bg = text_edit.cget("bg")
    if current_bg == "white" or current_bg == "#ffffff":
        text_edit.config(bg="black", fg="white", insertbackground="white")
    else:
        text_edit.config(bg="white", fg="black", insertbackground="black")

def change_font(text_edit, font_family_var, font_size_var):
    new_font = (font_family_var.get(), font_size_var.get())
    text_edit.config(font=new_font)

def select_all_text(text_edit):
    # Select all text, ignoring trailing newlines
    text_edit.tag_add("sel", "1.0", "end-1c")
    return "break"  # Prevent default behavior

def perform_undo(text_edit):
    try:
        text_edit.edit_undo()
    except tk.TclError:
        pass  # Ignore error if there's nothing to undo

def perform_redo(text_edit):
    try:
        text_edit.edit_redo()
    except tk.TclError:
        pass  # Ignore error if there's nothing to redo

def update_status(text_edit, status_label):
    content = text_edit.get(1.0, tk.END)
    words = len(content.split())
    char_count = len(content) - 1  # Subtract 1 to exclude the final newline character
    row, col = text_edit.index(tk.INSERT).split(".")
    status_label.config(text=f"Line: {row}   Column: {col}   Words: {words}   Characters: {char_count}")

def main():
    window = tk.Tk()
    window.title("Text Editor")
    window.geometry("800x600")  # Set a fixed window size
    window.grid_columnconfigure(1, weight=1)  # Ensure column expands with the window
    window.grid_rowconfigure(1, weight=1)

    window.minsize(600, 400)

    file_path_var = tk.StringVar()  # Stores the current file path

    text_edit = tk.Text(window, font="Helvetica 18", bg="white", fg="black", insertbackground="black", undo=True)
    text_edit.grid(row=1, column=1, sticky="nsew")

    frame = tk.Frame(window, relief=tk.RAISED, bd=2)
    open_button = tk.Button(frame, text="Open", command=lambda: open_file(window, text_edit, file_path_var))
    save_button = tk.Button(frame, text="Save", command=lambda: save_file(window, text_edit, file_path_var))
    save_as_button = tk.Button(frame, text="Save As", command=lambda: save_as_file(window, text_edit, file_path_var))
    find_button = tk.Button(frame, text="Find", command=lambda: prompt_find_text(text_edit))
    toggle_button = tk.Button(frame, text="Toggle Theme", command=lambda: toggle_theme(text_edit))

    open_button.grid(row=0, column=0, padx=5, pady=5)
    save_button.grid(row=0, column=1, padx=5, pady=5)
    save_as_button.grid(row=0, column=2, padx=5, pady=5)
    find_button.grid(row=0, column=3, padx=5, pady=5)
    toggle_button.grid(row=0, column=4, padx=5, pady=5)

    # Font customization dropdown menus
    font_family_var = tk.StringVar(value="Helvetica")
    font_size_var = tk.IntVar(value=18)

    font_families = ["Helvetica", "Arial", "Courier", "Times New Roman", "Verdana"]
    font_sizes = [10, 12, 14, 16, 18, 20, 24, 28, 32]

    font_family_menu = tk.OptionMenu(frame, font_family_var, *font_families, command=lambda _: change_font(text_edit, font_family_var, font_size_var))
    font_family_menu.grid(row=0, column=5, padx=0, pady=0)
    font_size_menu = tk.OptionMenu(frame, font_size_var, *font_sizes, command=lambda _: change_font(text_edit, font_family_var, font_size_var))
    font_size_menu.grid(row=0, column=6, padx=0, pady=0)

    frame.grid(row=0, column=0, columnspan=2, sticky="ew")  # Make the frame expand horizontally

    window.bind("<Control-o>", lambda _: open_file(window, text_edit, file_path_var))
    window.bind("<Control-s>", lambda _: save_file(window, text_edit, file_path_var))
    window.bind("<Control-S>", lambda _: save_as_file(window, text_edit, file_path_var)) # Control+Shift+s is interpreted as Control+S
    window.bind("<Control-f>", lambda _: prompt_find_text(text_edit))

    # Bind Undo and Redo shortcuts
    window.bind("<Control-z>", lambda _: perform_undo(text_edit))
    window.bind("<Control-y>", lambda _: perform_redo(text_edit))

    text_edit.bind("<Control-a>", lambda _: select_all_text(text_edit))
    text_edit.bind("<KeyRelease>", lambda _: update_status(text_edit, status_label))

    status_label = tk.Label(window, text="Line: 1   Column: 1   Words: 0   Characters: 0", anchor="w")
    status_label.grid(row=2, column=0, columnspan=2, sticky="ew")

    window.mainloop()

if __name__ == "__main__":
    main()
