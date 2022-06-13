# a notepad clone that saves in a GUI interface (with tkinter)
import datetime
import os # for checking if the plugins folder is downloaded
import tkinter as tk # everything related to the GUI
import tkinter.filedialog # for running the program
import tkinter.messagebox # for displaying a message box
import time
import webbrowser # for opening URLs and for the search bar

# the time the file was last saved
last_save = time.time()

def save_file(text_box):
    # call the file save dialog
    file_name = tk.filedialog.asksaveasfile(mode='w', defaultextension='.txt')
    # if the user didn't cancel the save dialog
    if file_name is not None:
        # write the contents of the text box to the file
        file_name.write(text_box.get('1.0', 'end-1c'))
        # close the file
        file_name.close()
        # update the last save time
        global last_save
        last_save = time.time()

def load_file(text_box):
    # call the file load dialog
    file_name = tk.filedialog.askopenfile(mode='r')
    # if the user didn't cancel the load dialog
    if file_name is not None:
        # read the contents of the file into the text box
        text_box.insert('1.0', file_name.read())
        # close the file
        file_name.close()

def exit_program(window, text_box):
    # if the file has been saved in the last 5 minutes or the file is blank
    if time.time() - last_save < 300 or text_box.get('1.0', 'end-1c') == '':
        # just close the window
        window.destroy()
    # if the file has not been saved in the last 5 minutes, ask if they want to save the file
    elif tk.messagebox.askyesno('Save', 'Do you want to save the file?'):
        # if they do, save the file
        save_file(window) 
        # then close the window
        window.destroy()

def find_substring_helper(text_box, substring_box, window2):
    # get the substring from the text box
    substring = substring_box.get()
    # get the contents of the text box
    contents = text_box.get('1.0', 'end-1c')
    # if the substring is in the contents
    if substring in contents:
        # find the index of the substring in the contents
        index = contents.index(substring)
        # set the cursor to the index of the substring
        text_box.icursor(index)
        # display a message box saying "Substring found at [index]"
        tk.messagebox.showinfo('Substring found at' , index)
    # if the substring is not in the contents
    else:
        # display a message box
        tk.messagebox.showinfo('Find', 'Substring not found')
    # close the window
    window2.destroy()


def find_substring(text_box):
    # create a window
    window2 = tk.Tk()
    # set the window title
    window2.title('Find - N0tep4d')
    window2.iconbitmap('n0tep4d.ico')
    # create a text box labeled "Substring"
    substring_box = tk.Entry(window2)
    # create a button labeled "Find" below the text box
    find_button = tk.Button(window2, text='Find', command=lambda: find_substring_helper(text_box, substring_box, window2))
    # pack the text box and button
    substring_box.pack()
    find_button.pack()

def url_helper(text):
    # if the text is a valid URL
    if 'http://' in text:
        # add a warning message
        tk.messagebox.showwarning('Unsafe URL', 'As HTTP is not secure, you should not use it unless you trust the source of the URL. However, most websites and browsers automatically redirect to HTTPS, so you should not worry about it if you are using a secure connection.')
        # if the user wants to open the URL
        if tk.messagebox.askyesno('Open', 'Do you still want to open the URL?'):
            # open the URL
            webbrowser.open(text)
    elif 'https://' in text:
        # open the URL
        webbrowser.open(text)

def custom_search(text):
    # open up a new window
    window3 = tk.Tk()
    # set the window title
    window3.title('Search (custom) - N0tep4d')
    window3.iconbitmap('n0tep4d.ico')
    # create a text box labeled "Search"
    search_box = tk.Entry(window3)
    # put the text in the text box
    search_box.insert(0, text)
    # create another text box labeled "URL" below the search box
    url_box = tk.Entry(window3)
    # by default, put the example.com URL in the text box
    url_box.insert(0, 'https://example.com/search?q=')
    # if the url is a HTTP URL, show an error message
    if 'http://' in text:
        tk.messagebox.showerror('Error', 'HTTP is not secure, you should not use it unless you trust the source of the URL. However, most websites and browsers automatically redirect to HTTPS, so you should not worry about it if you are using a secure connection.')
    # create a button labeled "Search" below the text box
    search_button = tk.Button(window3, text='Search', command=lambda: url_helper(search_box.get() + url_box.get()))
    # pack the text box and button
    search_box.pack()
    url_box.pack()
    search_button.pack()
    
def notepad_gui():
    # create a window
    window = tk.Tk()
    # make it so that any instalce of window.destroy calls exit_program
    window.protocol('WM_DELETE_WINDOW', lambda: exit_program(window, text_box))
    # set the window title
    window.title('N0tep4d')
    window.iconbitmap('n0tep4d.ico')
    # create a text box
    text_box = tk.Text(window)
    # bind the save function to CTRL+S
    text_box.bind('<Control-s>', lambda event: save_file(text_box))
    # bind the load function to CTRL+O
    text_box.bind('<Control-o>', lambda event: load_file(text_box))
    # bind the exit function to CTRL+Q
    text_box.bind('<Control-q>', lambda event: exit_program(window, text_box))
    # bind CTRL+C to an error message
    text_box.bind('<Control-c>', lambda event: tk.messagebox.showerror('Error', 'You cannot copy from n0tep4d yet'))
    # when right-clicking on the text box, minimize the window
    text_box.bind('<Button-3>', lambda event: window.iconify())
    # when highlighting text and pressing CTRL+1, open the number of characters selected in a new window and in human-readable format
    text_box.bind('<Control-Delete>', lambda event: tk.messagebox.showinfo('Selected text', text_box.selection_get()))
    # when highlighting a URL and pressing CTRL+ALT+U, open the URL in a new window
    text_box.bind('<Control-Alt-u>', lambda event: url_helper(text_box.selection_get()))
    # set the text box to be the size of the window
    text_box.pack(expand=True, fill='both')
    # create a menu bar at the bottom of the screen
    menu_bar = tk.Menu(window)
    # locate it at the bottom of the screen
    window.config(menu=menu_bar)
    # create a file menu
    file_menu = tk.Menu(menu_bar)
    # add the file menu to the menu bar
    menu_bar.add_cascade(label='File', menu=file_menu)
    file_menu.add_command(label='Save', command=lambda: save_file(text_box))
    file_menu.add_command(label='Load', command=lambda: load_file(text_box))
    file_menu.add_separator()
    file_menu.add_command(label='Exit', command=lambda: exit_program(text_box, window))
    # create a help menu
    help_menu = tk.Menu(menu_bar)
    # add the help menu to the menu bar
    menu_bar.add_cascade(label='Help', menu=help_menu)
    help_menu.add_command(label='About', command=lambda: tk.messagebox.showinfo('About', 'N0tep4d is a notepad clone that saves in a GUI interface (with tkinter).'))
    help_menu.add_command(label='License', command=lambda: tk.messagebox.showinfo('License', 'N0tep4d is licensed under the GNU-GPL license.'))
    # make a submenu in the help menu
    help_menu.add_cascade(label='Documentation', menu=tk.Menu(help_menu))
    help_menu.add_cascade(label='Report a bug', command=lambda: webbrowser.open('https://github.com/UniqueName12345/n0tep4d/issues'))
    help_menu.add_cascade(label='View source code', command=lambda: webbrowser.open('https://github.com/UniqueName12345/n0tep4d/'))
    # create a edit menu
    edit_menu = tk.Menu(menu_bar)
    # add the edit menu to the menu bar
    menu_bar.add_cascade(label='Edit', menu=edit_menu)
    edit_menu.add_command(label='Cut', command=lambda: text_box.clipboard_clear())
    edit_menu.add_command(label='Copy', command=lambda: text_box.clipboard_append(text_box.selection_get()))
    edit_menu.add_command(label='Paste', command=lambda: text_box.insert('insert', text_box.clipboard_get()))
    edit_menu.add_separator()
    edit_menu.add_command(label='Settings', command=lambda: tk.messagebox.showerror('Settings', 'Settings not implemented yet.'))
    # remove the grey bar on top of the edit and file menus
    file_menu.config(tearoff=0)
    edit_menu.config(tearoff=0)
    help_menu.config(tearoff=0)
    search_menu = tk.Menu(menu_bar)
    # add the search menu to the menu bar
    menu_bar.add_cascade(label='Search', menu=search_menu)
    search_menu.add_command(label='Find', command=lambda: find_substring(text_box))
    search_menu.add_command(label='Search on the web (Google)', command=lambda: webbrowser.open('https://www.google.com/search?q=' + text_box.selection_get()))
    search_menu.add_command(label='Search on the web (Bing)', command=lambda: webbrowser.open('https://www.bing.com/search?q=' + text_box.selection_get()))
    search_menu.add_command(label='Search on the web (Yahoo)', command=lambda: webbrowser.open('https://search.yahoo.com/search?p=' + text_box.selection_get()))
    search_menu.add_command(label='Search on the web (Ask)', command=lambda: webbrowser.open('https://www.ask.com/web?q=' + text_box.selection_get()))
    search_menu.add_command(label='Search on the web (Wikipedia)', command=lambda: webbrowser.open('https://en.wikipedia.org/wiki/Special:Search?search=' + text_box.selection_get()))
    search_menu.add_command(label='Search on the web (Qwant)', command=lambda: webbrowser.open('https://www.qwant.com/?q=' + text_box.selection_get()))
    search_menu.add_command(label='Search on the web (DuckDuckGo)', command=lambda: webbrowser.open('https://duckduckgo.com/?q=' + text_box.selection_get()))
    search_menu.add_command(label='Search on the web (Yandex)', command=lambda: webbrowser.open('https://yandex.ru/search/?text=' + text_box.selection_get()))
    search_menu.add_command(label='Search on the web (Baidu)', command=lambda: webbrowser.open('https://www.baidu.com/s?wd=' + text_box.selection_get()))
    search_menu.add_command(label='Search on the web (360)', command=lambda: webbrowser.open('https://www.so.com/s?ie=utf-8&q=' + text_box.selection_get()))
    search_menu.config(tearoff=0)
    # make a maths menu
    maths_menu = tk.Menu(menu_bar)
    # add the maths menu to the menu bar
    menu_bar.add_cascade(label='Maths', menu=maths_menu)
    maths_menu.add_command(label='Calculate (Wolfram|Alpha)', command=lambda: webbrowser.open('https://www.wolframalpha.com/input/?i=' + text_box.selection_get()))
    maths_menu.add_command(label='Calculate (Google)', command=lambda: webbrowser.open('https://www.google.com/search?q=' + text_box.selection_get()))
    maths_menu.add_command(label='Calculate (Built-in)', command=lambda: tk.messagebox.showinfo('Calculate', 'The result of ' + text_box.selection_get() + ' is ' + str(eval(text_box.selection_get()))))
    maths_menu.config(tearoff=0)
    # make a date and time menu
    date_time_menu = tk.Menu(menu_bar)
    # add the date and time menu to the menu bar
    menu_bar.add_cascade(label='Date and Time', menu=date_time_menu)
    date_time_menu.add_command(label='Get current date', command=lambda: text_box.insert('insert', datetime.datetime.now().strftime('%d/%m/%Y')))
    date_time_menu.add_command(label='Get current time', command=lambda: text_box.insert('insert', datetime.datetime.now().strftime('%H:%M:%S')))
    date_time_menu.config(tearoff=0)
    # run the main loop
    window.mainloop()

def run_program(plugins):
    # if plugins are not provided, load no plugins
    if plugins is None:
        plugins = []
    # run the main program
    notepad_gui()

def setup():
    # make a plugin directory if it doesn't exist
    print("Making plugin directory if it doesn't exist...")
    time.sleep(0.5)
    working_dir = os.path.dirname(os.path.realpath(__file__))
    if not os.path.exists(working_dir + '/plugins'):
        os.makedirs(working_dir + '/plugins')
    print_two_things_after_wait("Plugin directory made.", "Loading plugins...")
    # load plugins
    plugins = [file for file in os.listdir(working_dir + '/plugins') if file.endswith('.n0tep4d')]

    print_two_things_after_wait("Plugins loaded.", "Running program...")
    # run the program
    run_program(plugins)


def main():
    # run the setup
    setup()

def print_two_things_after_wait(arg0, arg1):
    print(arg0)
    time.sleep(1)
    print(arg1)

if __name__ == '__main__':
    main()