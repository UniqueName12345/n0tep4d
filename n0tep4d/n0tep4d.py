# a notepad clone that saves in a GUI interface (with tkinter)
import datetime
import os
from tkinter import filedialog
import tkinter as tk # everything related to the GUI
import tkinter.filedialog # for running the program
import tkinter.messagebox # for displaying a message box
import time
import webbrowser # for opening URLs and for the search bar
import pyperclip
# the time the file was last saved
last_save = time.time()

def save_file(text_box):
    

    # call the file save dialog
    file_name = filedialog.asksaveasfile(mode='w', defaultextension='.txt', filetypes=[('Text Files', '*.txt')])
    
    # if the user didn't cancel the save dialog
    if file_name:
        # write the contents of the text box to the file
        with open(file_name.name, 'w') as file:
            file.write(text_box.get('1.0', 'end-1c'))
        
        # update the last save time
        global last_save
        last_save = time.time()

def load_file(text_box):
    # create a file dialog
    file_dialog = filedialog.askopenfile(mode='r')

    # if the user selected a file
    if file_dialog:
        # read the contents of the file
        file_contents = file_dialog.read()

        # insert the contents into the text box
        text_box.insert('1.0', file_contents)

        # close the file
        file_dialog.close()

def exit_program(window, text_box):
    if (time.time() - last_save < 300) or (text_box.get('1.0', 'end-1c') == ''):
        text_box.destroy()
        window.destroy()
    elif tk.messagebox.askyesno('Save', 'Do you want to save the file?'):
        save_file(window)
        window.destroy()

def find_substring_helper(text_box, substring_box, window2):
    # Get the substring from the text box
    substring = substring_box.get()

    # Get the contents of the text box
    contents = text_box.get('1.0', 'end-1c')

    # Check if the substring is in the contents
    if substring in contents:
        # Find the index of the substring in the contents
        index = contents.index(substring)

        # Set the cursor to the index of the substring
        text_box.icursor(index)

        # Display a message box with the index of the substring
        tk.messagebox.showinfo('Substring found at', index)
    else:
        # Display a message box indicating the substring was not found
        tk.messagebox.showinfo('Find', 'Substring not found')

    # Close the window
    window2.destroy()


def find_substring(text_box):
    # create a window
    window2 = tk.Tk()
    # set the window title
    window2.title('Find - N0tep4d')
    window2.iconbitmap('n0tep4d/n0tep4d.ico')
    # create a text box labeled "Substring"
    substring_box = tk.Entry(window2)
    # create a button labeled "Find" below the text box
    find_button = tk.Button(window2, text='Find', command=lambda: find_substring_helper(text_box, substring_box, window2))
    # pack the text box and button
    substring_box.pack()
    find_button.pack()

import tkinter as tk
import webbrowser

def url_helper(text):
    if text.startswith('http://'):
        tk.messagebox.showwarning('Unsafe URL', 'As HTTP is not secure, you should not use it unless you trust the source of the URL. However, most websites and browsers automatically redirect to HTTPS, so you should not worry about it if you are using a secure connection.')
        if tk.messagebox.askyesno('Open', 'Do you still want to open the URL?'):
            webbrowser.open(text)
    elif text.startswith('https://'):
        webbrowser.open(text)

def custom_search(text):
    # Create the main window
    window3 = tk.Tk()
    window3.title('Search (custom) - N0tep4d')
    window3.iconbitmap('n0tep4d/n0tep4d.ico')

    # Create the search box
    search_box = tk.Entry(window3)
    search_box.insert(0, text)
    search_box.pack()

    # Create the URL box
    url_box = tk.Entry(window3)
    url_box.insert(0, 'https://example.com/search?q=')
    url_box.pack()

    # Create the search button
    def search():
        search_text = search_box.get()
        url_text = url_box.get()
        url_helper(search_text + url_text)

    search_button = tk.Button(window3, text='Search', command=search)
    search_button.pack()

    # Show error message if HTTP URL
    if 'http://' in text:
        tkinter.messagebox.messagebox.showerror('Error', 'HTTP is not secure, you should not use it unless you trust the source of the URL. However, most websites and browsers automatically redirect to HTTPS, so you should not worry about it if you are using a secure connection.')
    
def notepad_gui():
    # create a window
    window = tk.Tk()
    window.title('N0tep4d')
    window.iconbitmap('n0tep4d/n0tep4d.ico')

    # make it so that any instance of window.destroy calls exit_program
    window.protocol('WM_DELETE_WINDOW', lambda: exit_program(window, text_box))

    # create a text box
    text_box = tk.Text(window)
    text_box.pack(expand=True, fill='both')

    # bind the save function to CTRL+S
    text_box.bind('<Control-s>', lambda event: save_file(text_box))
    # bind the load function to CTRL+O
    text_box.bind('<Control-o>', lambda event: load_file(text_box))
    # bind the exit function to CTRL+Q
    text_box.bind('<Control-q>', lambda event: exit_program(window, text_box))
    # bind CTRL+C to copy the selected text
    text_box.bind('<Control-c>', lambda event: pyperclip.copy(text_box.selection_get()))
    # bind CTRL+V to paste the last thing from the clipboard, excluding the first few garbage characters
    text_box.bind('<Control-v>', lambda event: text_box.insert(text_box.index('insert'), pyperclip.paste()[3:]))
    # when right-clicking on the text box, minimize the window
    text_box.bind('<Button-3>', lambda event: window.iconify())
    # when highlighting text and pressing CTRL+1, open the number of characters selected in a new window and in human-readable format
    text_box.bind('<Control-Delete>', lambda event: tk.messagebox.showinfo('Selected text', text_box.selection_get()))
    # when highlighting a URL and pressing CTRL+ALT+U, open the URL in a new window
    text_box.bind('<Control-Alt-u>', lambda event: url_helper(text_box.selection_get()))
    # when the textbox is deleted, destroy the window
    text_box.bind('<Delete>', lambda event: window.destroy())

    # create a menu bar at the bottom of the screen
    menu_bar = tk.Menu(window)
    window.config(menu=menu_bar)

    # create a file menu
    file_menu = tk.Menu(menu_bar)
    menu_bar.add_cascade(label='File', menu=file_menu)
    file_menu.add_command(label='Save', command=lambda: save_file(text_box))
    file_menu.add_command(label='Load', command=lambda: load_file(text_box))
    file_menu.add_separator()
    file_menu.add_command(label='Exit', command=lambda: exit_program(text_box, window))

    # create a help menu
    help_menu = tk.Menu(menu_bar)
    menu_bar.add_cascade(label='Help', menu=help_menu)
    help_menu.add_command(label='About', command=lambda: tk.messagebox.showinfo('About', 'N0tep4d is a notepad clone that saves in a GUI interface (with tkinter).'))
    help_menu.add_command(label='License', command=lambda: tk.messagebox.showinfo('License', 'N0tep4d is licensed under the GNU-GPL license.'))

def run_program():
    notepad_gui()

def setup():
    # Silently delete the plugins directory if it exists
    if os.path.exists('plugins'):
        os.remove('plugins')
    
    # Run the program
    run_program()


def main():
    # run the setup
    setup()

def print_two_things(arg0, arg1):
    print(arg0)
    print(arg1)

if __name__ == '__main__':
    main()