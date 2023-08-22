import csv
import math
import statistics
import tkinter as tk
from tkinter import filedialog, ttk

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

# create app
app = tk.Tk()
app.title("Jinx's Data Analysis")

numbers = [] # create empty numbers list
data_analysed = False # global variable for functions that will only run if data has been analysed


def append_to_output(text): # every time text is inserted into output window, it will enable, insert text, then disable, making output window read only
    output_text.config(state=tk.NORMAL) # enable the output widget
    output_text.insert(tk.END, text) # print text
    output_text.config(state=tk.DISABLED) # disable the  output widget


# function for clear button
def clear_data(): # function to clear input and output data
    global numbers, data_analysed
    data_analysed = False
    numbers = [] # clear numbers list
    entry.delete("1.0", tk.END)
    output_text.config(state=tk.NORMAL) # enable the output widget
    output_text.delete(1.0, tk.END) # clear output data
    output_text.config(state=tk.DISABLED) # disable the  output widget


# function for save button
def save_results():
    if not data_analysed:
        tk.messagebox.showwarning("Warning", "No data available to save. Please enter and analyse data first.")
        return
    file_path = tk.filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as file:
            content = output_text.get(1.0, tk.END)
            file.write(content)
        append_to_output("Results saved successfully!\n" + "\n")


# create plots
def create_plot(x, y, plot_type, xlabel, ylabel, title):
    plt.figure()
    if plot_type == 'histogram':
            plt.hist(y, bins=30, edgecolor='black')
    elif plot_type == 'line':
            plt.plot(x, y, color='blue', marker='o', linestyle='-', linewidth='2')
    elif plot_type == 'scatter':
            plt.scatter(x, y, color='blue', marker='o')
    elif plot_type == 'box':
            plt.boxplot(y, vert=False)
            q1 = np.percentile(y, 25)
            q3 = np.percentile(y, 75)
            median = calculate_median(y)
    
            plt.annotate(f"Q1: {q1:.2f}", xy=(q1, 1.1), xytext=(q1, 1.4), arrowprops=dict(facecolor='black', arrowstyle="->"), ha='center')
            plt.annotate(f"Median: {median:.2f}", xy=(median, 1.1), xytext=(median, 1.2), arrowprops=dict(facecolor='black', arrowstyle="->"), ha='center')
            plt.annotate(f"Q3: {q3:.2f}", xy=(q3, 1.1), xytext=(q3, 1.3), arrowprops=dict(facecolor='black', arrowstyle="->"), ha='center')
    else:
        raise ValueError("Invalid Plot Type")

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)


# functions to display plots
def show_histogram():
    if not data_analysed:
        tk.messagebox.showwarning("Warning", "No data available to plot. Please enter and analyse data first!")
        return
    create_plot(None, numbers, 'histogram', 'Value', 'Frequency', 'Histogram of input values')
    plt.show()


def show_line_plot():
    if not data_analysed:
        tk.messagebox.showwarning("Warning", "No data available to plot. Please enter and analyse data first!")
        return
    
    q1 = np.percentile(numbers, 25)
    q3 = np.percentile(numbers, 75)
    median = calculate_median(numbers)
    
    create_plot(list(range(len(numbers))), numbers, 'line', 'Index', 'Value', 'Line plot of input values')
    
    # add vertical lines and text for quartiles and median
    plt.axvline(x=len(numbers) * 0.25, color='r', linestyle='--', label='Q1')
    plt.text(len(numbers) * 0.25, max(numbers), f'Q1: {q1}', color='red', ha='center', va='bottom')
    plt.axvline(x=len(numbers) * 0.75, color='g', linestyle='--', label='Q3')
    plt.text(len(numbers) * 0.75, max(numbers), f'Q3: {q3}', color='green', ha='center', va='bottom')
    plt.axvline(x=len(numbers) * 0.5, color='orange', linestyle='--', label='Median')
    plt.text(len(numbers) * 0.5, max(numbers), f'Median: {median}', color='orange', ha='center', va='bottom')

    plt.legend()
    plt.show()


def show_scatter_plot():
    if not data_analysed:
        tk.messagebox.showwarning("Warning", "No data available to plot. Please enter and analyse data first!")
        return
    create_plot(range(len(numbers)), numbers, 'scatter', 'Index', 'Value', 'Scatter plot of unsorted input values')
    plt.show()


def show_box_plot():
    if not data_analysed:
        tk.messagebox.showwarning("Warning", "No data available to plot. Please enter and analyse data first!")
        return
    create_plot(None, numbers, 'box', None, None, 'Box plot of input values')
    plt.show()


# create bell curve
def show_bell_curve():
    if not data_analysed:
        tk.messagebox.showwarning("Warning", "No data available to plot. Please enter and analyse data first!")
        return

    mean = calculate_mean(numbers)
    std = calculate_standard_deviation(numbers)

    plt.hist(numbers, bins=30, density=True, alpha=0.5, color='g', edgecolor='black')

    x = np.linspace(min(numbers), max(numbers), 100)
    y = norm.pdf(x, mean, std)
    plt.plot(x, y, color='blue')

    for i in range(-3, 4):
        plt.axvline(mean + i * std, alpha=0.6, color='red', linestyle='--')

        if i != 0:
            plt.text(mean + i * std, max(y)/10, f'Z={i}', color='red', ha='center', va='bottom')

    plt.title('Bell Curve (Normal Distribution)')
    plt.xlabel('Value')
    plt.ylabel('Density')
    plt.show()


# calculate mean of list
def calculate_mean(numbers):
    total = sum(numbers)
    count = len(numbers)
    mean = total / count
    return mean


# calculate median of list
def calculate_median(numbers):
    sorted_numbers = sorted(numbers)
    length = len(sorted_numbers)

    if length % 2 == 1:
        median = sorted_numbers[length // 2]
    else:
        middle_right = length // 2
        middle_left = middle_right - 1
        median = (sorted_numbers[middle_left] + sorted_numbers[middle_right]) / 2
    return median


# calculate range of list
def calculate_range(numbers):
    list_range = max(numbers) - min(numbers)
    return list_range


# calculate standard deviation of list
def calculate_standard_deviation(numbers):
    mean = calculate_mean(numbers)
    squared_diff_sum = sum((x - mean) ** 2 for x in numbers)
    variance = squared_diff_sum / len(numbers)
    standard_deviation = math.sqrt(variance)
    return standard_deviation


# calculate z scores
def calculate_z_scores():
    mean = calculate_mean(numbers)
    std = calculate_standard_deviation(numbers)
    z_scores = [(x - mean) / std for x in numbers]
    return z_scores


# function for finding z score of specific value
def find_z_score():
    if not data_analysed:
        tk.messagebox.showwarning("Warning", "No data available. Please enter and analyse data first!")
        return

    value_to_find_str = z_search_entry.get().strip()
    
    if not value_to_find_str:
        tk.messagebox.showwarning("Warning", "Please enter a value to find its Z-score!")
        return

    try:
        value_to_find = float(value_to_find_str)
    except ValueError:
        tk.messagebox.showwarning("Warning", "Invalid input! Please enter a numerical value to find its Z-score.")
        return
    
    mean = calculate_mean(numbers)
    std = calculate_standard_deviation(numbers)
    z_score = (value_to_find - mean) / std

    if value_to_find in numbers:
        append_to_output("Z-score of {}: {:.2f}\n".format(value_to_find, z_score) + "\n")
    else:
        append_to_output("Z-score of {}: {:.2f}".format(value_to_find, z_score) + "\n" + "Note: The value {} was not found in your dataset and may not be applicable.\n".format(value_to_find) + "\n")


# importing csv files
def load_csv():
    global numbers
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return
    
    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.config(state=tk.DISABLED)

    entry.delete("1.0", tk.END)
    numbers = []

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for item in row:
                try:
                    number = int(item)
                    numbers.append(number)
                    entry.insert(tk.END, str(number) + " ")
                except ValueError:
                    continue


# global application theme
theme_var = tk.StringVar(value='light')

# define colours for widgets in each app theme
themes = {
    "dark": {
        "app_bg_colour": "#1a1a1a",
        "entry_output_bg": "#3b3b3b",
        "fg_colour": "white",
        "btn_colour": "#333333",
        "ttk_bg": "#333333",
        "ttk_fg": "white",
        "ttk_border": "#666565",
        "ttk_bg_deselected": "#2a2a2a",
        "ttk_fg_deselected": "#aaaaaa",
    },
    "light": {
        "app_bg_colour": "#f0f0f0",
        "entry_output_bg": "white",
        "fg_colour": "black",
        "btn_colour": "white",
        "ttk_bg": "white",
        "ttk_fg": "black",
        "ttk_border": "#c9c7c7",
        "ttk_bg_deselected": "#e0e0e0",
        "ttk_fg_deselected": "#7a7a7a",
    }
}

# set gui style
style = ttk.Style()
style.theme_use('clam')


# apply theme to standard tk widgets
def apply_theme_to_widget(widget, theme_dict):
    try:
        if isinstance(widget, tk.Label):
            widget.configure(bg=theme_dict["app_bg_colour"], fg=theme_dict["fg_colour"])
        elif isinstance(widget, (tk.Toplevel, tk.Frame)):
            widget.configure(bg=theme_dict["app_bg_colour"])
        elif isinstance(widget, tk.Button):
            widget.configure(bg=theme_dict["btn_colour"], fg=theme_dict["fg_colour"])
        elif isinstance(widget, tk.Entry):
            widget.configure(bg=theme_dict["entry_output_bg"], fg=theme_dict["fg_colour"])
        elif isinstance(widget, tk.Text):
            widget.configure(bg=theme_dict["entry_output_bg"], fg=theme_dict["fg_colour"])
    except tk.TclError:
        pass

    for child in widget.winfo_children():
        apply_theme_to_widget(child, theme_dict)


# apply theme to tkk widgets
def apply_theme_to_ttk_widgets(theme_dict):
    style = ttk.Style()

    style.configure('TFrame', background=theme_dict["app_bg_colour"])
    style.configure('TLabel', background=theme_dict["app_bg_colour"], foreground=theme_dict["fg_colour"])
    style.configure('TEntry', fieldbackground=theme_dict["entry_output_bg"], foreground=theme_dict["fg_colour"])
    style.configure('TButton', background=theme_dict["ttk_bg"], foreground=theme_dict["ttk_fg"])
    style.map('TButton',
              background=[('active', theme_dict["ttk_border"])],
              foreground=[('active', theme_dict["ttk_fg"])]
             )
    style.configure('TMenubutton', background=theme_dict["ttk_bg"], foreground=theme_dict["ttk_fg"])
    style.map('TMenubutton',
              background=[('active', theme_dict["ttk_border"])],
              foreground=[('active', theme_dict["ttk_fg"])]
             )
    style.configure('TSpinbox', fieldbackground=theme_dict["entry_output_bg"], foreground=theme_dict["fg_colour"])
    style.map('TSpinbox',
              fieldbackground=[('readonly', theme_dict["btn_colour"])],
              foreground=[('readonly', theme_dict["fg_colour"])]
             )
    style.configure('TNotebook', background=theme_dict["ttk_bg"])
    style.map('TNotebook.Tab',
              background=[('selected', theme_dict["ttk_bg"]), ('!selected', theme_dict["ttk_bg_deselected"])],
              foreground=[('selected', theme_dict["ttk_fg"]), ('!selected', theme_dict["ttk_fg_deselected"])])
    style.configure('TNotebook.Tab', padding=[5, 2])
    style.configure('TCombobox', 
                    background=theme_dict["ttk_bg"], 
                    foreground=theme_dict["ttk_fg"], 
                    fieldbackground=theme_dict["entry_output_bg"])
    style.map('TCombobox',
              background=[('readonly', theme_dict["ttk_bg"])],
              foreground=[('readonly', theme_dict["ttk_fg"])])
    style.configure('TScrollbar', 
                background=theme_dict["ttk_bg"], 
                troughcolor=theme_dict["app_bg_colour"], 
                width=12)
    style.map('TScrollbar', 
          background=[('active', theme_dict["ttk_border"]), ('pressed', theme_dict["ttk_fg"])])


# apply appearance settings
def apply_appearance(theme):
    global theme_var

    theme_var.set(theme)
    theme_dict = themes[theme]

    apply_theme_to_ttk_widgets(theme_dict)
    apply_theme_to_widget(app, theme_dict)


# appearance settings for sorted values window
def apply_sorted_window_appearance(window, text_widget):
    theme = theme_var.get()
    theme_dict = themes[theme]

    window.configure(bg=theme_dict["app_bg_colour"])
    text_widget.configure(fg=theme_dict["fg_colour"], bg=theme_dict["app_bg_colour"])

    apply_theme_to_widget(window, theme_dict)


def show_settings():
    format_window = tk.Toplevel()
    format_window.title("Format Settings")

    label = tk.Label(format_window, text="Number of Decimal Places:")
    label.pack()

    decimal_places_var = tk.IntVar(value=1)
    spinbox = ttk.Spinbox(format_window, from_=0, to=10, textvariable=decimal_places_var)
    spinbox.pack()

    apply_button = ttk.Button(format_window, text="Apply", command=lambda: apply_settings(decimal_places_var.get()))
    apply_button.pack()


default_font = "TkDefaultFont"

current_theme = 'light'
apply_appearance(current_theme)
selected_decimal_places = 0  # default value
current_font_size = 12 # default font size


def format_number(number, decimal_places):
    return f"{number:.{decimal_places}f}"


# when apply button is pressed
def apply_settings(size, decimal_places, theme):
    global selected_decimal_places, current_font_size, current_theme
    selected_decimal_places = decimal_places
    current_theme = theme
    current_font_size = size
    
    font_tuple = ("TkDefaultFont", size)
    entry.configure(font=font_tuple)
    output_text.configure(font=font_tuple)

    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.config(state=tk.DISABLED)

    if data_analysed == True:
      get_input()

    apply_appearance(theme)


# when ok button is pressed
def apply_and_close_settings(window, size, decimal_places, theme):
    apply_settings(size, decimal_places, theme)
    window.destroy()


# settings window
def settings():
    global format_frame, appearance_frame, spacer

    theme = theme_var.get()
    theme_dict = themes[theme]
    
    settings_window = tk.Toplevel(app)
    settings_window.title("Settings")
    settings_window.geometry('250x300')
    
    # apply theme
    apply_theme_to_widget(settings_window, theme_dict)
    
    # create notebook
    notebook = ttk.Notebook(settings_window)
    notebook.pack(fill=tk.BOTH, expand=True)
    
    format_frame = ttk.Frame(notebook)

    spacer_2 = ttk.Frame(format_frame, height=5)
    spacer_2.pack(fill=tk.X)

    font_size_label = ttk.Label(format_frame, text="Font Size:")
    font_size_label.pack(anchor=tk.W, padx=10)
    font_size_var = tk.IntVar(value=12)
    font_size_spinbox = ttk.Spinbox(format_frame, from_=8, to=24, textvariable=font_size_var, state='readonly')
    font_size_spinbox.pack(anchor=tk.W, padx=10)

    spacer = ttk.Frame(format_frame, height=20)
    spacer.pack(fill=tk.X)

    label = ttk.Label(format_frame, text="Number of Decimal Places:")
    label.pack(anchor=tk.W, padx=10)
    decimal_places_var = tk.IntVar(value=2)
    decimal_places_spinbox = ttk.Spinbox(format_frame, from_=0, to=10, textvariable=decimal_places_var, state='readonly')
    decimal_places_spinbox.pack(anchor=tk.W, padx=10)

    notebook.add(format_frame, text="Format Settings")
    
    # appearance settings tab
    appearance_frame = ttk.Frame(notebook)
    
    # change app theme
    label = ttk.Label(appearance_frame, text="Application Theme:")
    label.pack(anchor=tk.W, padx=10, pady=5)

    theme_options = ["light", "dark"]
    theme_dropdown = ttk.OptionMenu(appearance_frame, theme_var, *theme_options)
    theme_dropdown.pack(anchor=tk.W, padx=10)
    menu = theme_dropdown["menu"]
    menu.delete(0, "end")
    for option in theme_options:
        menu.add_command(label=option, command=lambda choice=option: theme_var.set(choice))
    
    notebook.add(appearance_frame, text="Appearance Settings")

    # buttons at the bottom
    button_frame = ttk.Frame(settings_window)
    button_frame.pack(pady=10, fill=tk.X)

    ok_button = ttk.Button(button_frame, text="OK", command=lambda: apply_and_close_settings(settings_window, font_size_var.get(), decimal_places_var.get(), theme_var.get()))
    ok_button.pack(side=tk.LEFT, padx=5)

    apply_button = ttk.Button(button_frame, text="Apply", command=lambda: apply_settings(font_size_var.get(), decimal_places_var.get(), theme_var.get()))
    apply_button.pack(side=tk.LEFT, padx=5)

    cancel_button = ttk.Button(button_frame, text="Cancel", command=settings_window.destroy)
    cancel_button.pack(side=tk.LEFT, padx=5)

    font_size_var.set(current_font_size)
    decimal_places_var.set(selected_decimal_places)
    theme_var.set(current_theme)

    settings_window.update()


def open_format_settings():
    appearance_frame.pack_forget()
    format_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)


def open_appearance_settings():
    format_frame.pack_forget()
    appearance_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)


# function to show sorted values in separate window
def show_sorted_values():
    global data_analysed, apply_appearance, current_font_size

    if not data_analysed:
        tk.messagebox.showwarning("Warning", "No data available. Please enter and analyse data first!")
        return

    sorted_window = tk.Toplevel()
    sorted_window.title("Sorted Values")
    sorted_window.columnconfigure(0, weight=1)
    sorted_window.rowconfigure(0, weight=1)

    sorted_text = tk.Text(sorted_window, wrap=tk.WORD, height=20, width=50)
    sorted_text_scrollbar = ttk.Scrollbar(sorted_window, orient="vertical", command=sorted_text.yview)
    sorted_text.config(yscrollcommand=sorted_text_scrollbar.set)
    sorted_text.configure(font=(default_font, current_font_size))

    sorted_text.grid(row=0, column=0, sticky='nsew')
    sorted_text_scrollbar.grid(row=0, column=1, sticky='ns')

    sorted_values_str = ' '.join(format_number(number, selected_decimal_places) for number in sorted(numbers))

    sorted_text.insert(tk.END, "Sorted Values:\n" + sorted_values_str)
    sorted_text.config(state=tk.DISABLED)

    apply_sorted_window_appearance(sorted_window, sorted_text)


# when analyse button is pressed
def get_input():
    global numbers, create_plot, data_analysed, selected_decimal_places

    # clear output window
    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.config(state=tk.DISABLED)

    numbers_input = entry.get("1.0", tk.END).strip()

    # take input values and split them
    number_strings = numbers_input.split()

    # clear numbers list to append input values to
    numbers = []

    # define a flag to track if any valid numbers were found
    valid_numbers_found = False
    for number_string in number_strings:
        try:
            if "." in number_string:
                numbers.append(float(number_string))
                valid_numbers_found = True
            else:
                numbers.append(int(number_string))
                valid_numbers_found = True
        except ValueError:
            pass

    if valid_numbers_found:
        data_analysed = True
        if len(numbers) < len(number_strings):
            append_to_output("Invalid input/s found. Analysing valid values input...\n")
    else:
        tk.messagebox.showwarning("Warning", "No numerical data available. Please enter data first!")
        return

    # print attributes of list
    if numbers:
        append_to_output("Values count: " + format_number(len(numbers), selected_decimal_places) + "\n")
        append_to_output("Sum of values: " + format_number(sum(numbers), selected_decimal_places) + "\n")
        append_to_output("Highest value: " + format_number(max(numbers), selected_decimal_places) + "\n")
        append_to_output("Lowest value: " + format_number(min(numbers), selected_decimal_places) + "\n")
        mean_result = calculate_mean(numbers)
        append_to_output("Mean: " + format_number(mean_result, selected_decimal_places) + "\n")
        median_result = calculate_median(numbers)
        append_to_output("Median: " + format_number((median_result), selected_decimal_places) + "\n")

        # calculate quartiles and IQR
        q1 = np.percentile(numbers, 25)
        q3 = np.percentile(numbers, 75)
        iqr = q3 - q1

        # calculate mode
        count_dict = {}
        for num in numbers:
            count_dict[num] = count_dict.get(num, 0) + 1

        max_count = max(count_dict.values())
        modes = [format_number(num, selected_decimal_places) for num, count in count_dict.items() if count == max_count]

        if len(modes) > 1:
            append_to_output("Modes: " + ", ".join(str(mode) for mode in modes) + "\n")
        elif len(modes) == 1:
            append_to_output("Mode: " + str(modes[0]) + "\n")
        else:
            append_to_output("No unique mode found.\n")

        range_result = calculate_range(numbers)
        append_to_output("Range: " + format_number((range_result), selected_decimal_places) + "\n")
        append_to_output("Standard Deviation: " + format_number(calculate_standard_deviation(numbers), selected_decimal_places) + "\n")

        # print quartiles and IQR
        append_to_output("First Quartile (Q1): " + format_number((q1), selected_decimal_places) + "\n")
        append_to_output("Third Quartile (Q3): " + format_number((q3), selected_decimal_places) + "\n")
        append_to_output("IQR: " + format_number((iqr), selected_decimal_places) + "\n" + "\n")

        # calculate z score statistics
        def z_score_statistics():
            z_scores = calculate_z_scores()
            within_quarter_std = sum(1 for z in z_scores if -0.25 <= z <= 0.25)
            within_half_std = sum(1 for z in z_scores if -0.5 <= z <= 0.5)
            within_one_std = sum(1 for z in z_scores if -1 <= z <= 1)
            within_two_std = sum(1 for z in z_scores if -2 <= z <= 2)
            within_three_std = sum(1 for z in z_scores if -3 <= z <= 3)

            append_to_output("{}% of values are within 0.25 standard deviations of the mean\n".format(format_number(within_quarter_std / len(numbers) * 100, selected_decimal_places)))
            append_to_output("{}% of values are within 0.5 standard deviations of the mean\n".format(format_number(within_half_std / len(numbers) * 100, selected_decimal_places)))
            append_to_output("{}% of values are within 1 standard deviation of the mean\n".format(format_number(within_one_std / len(numbers) * 100, selected_decimal_places)))
            append_to_output("{}% of values are within 2 standard deviations of the mean\n".format(format_number(within_two_std / len(numbers) * 100, selected_decimal_places)))
            append_to_output("{}% of values are within 3 standard deviations of the mean\n".format(format_number(within_three_std / len(numbers) * 100, selected_decimal_places)) + "\n")
        z_score_statistics()

    else:
        append_to_output("No numerical values were provided.\n")


# create menu bar
def create_menu():
    menu_bar = tk.Menu(app)

    # create a file menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Load CSV", command=load_csv)
    file_menu.add_command(label="Save Results", command=save_results)
    file_menu.add_command(label="Settings", command=settings)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=app.quit)
    menu_bar.add_cascade(label="File", menu=file_menu)

    # create a plot menu
    plot_menu = tk.Menu(menu_bar, tearoff=0)
    plot_menu.add_command(label="Show Histogram", command=show_histogram)
    plot_menu.add_command(label="Show Line Plot", command=show_line_plot)
    plot_menu.add_command(label="Show Scatter Plot", command=show_scatter_plot)
    plot_menu.add_command(label="Show Box Plot", command=show_box_plot)
    plot_menu.add_command(label="Show Bell Curve", command=show_bell_curve)
    menu_bar.add_cascade(label="Plot", menu=plot_menu)

    app.config(menu=menu_bar)
create_menu()


# create frame to hold all the buttons
frame = tk.Frame(app, padx=10, pady=10)
frame.columnconfigure(0, weight=1, minsize=200)
frame.columnconfigure(1, weight=1, minsize=200)
frame.pack()

label = tk.Label(frame, text="Please enter a series of numbers separated by spaces or load a .CSV file:")
entry = tk.Text(frame, wrap=tk.WORD, height=5, width=50, font=(default_font, current_font_size))
output_text = tk.Text(frame, wrap=tk.WORD, height=25, width=50, font=(default_font, current_font_size))
output_text.config(state=tk.DISABLED)

# input entry and label
label.grid(row=0, column=0, columnspan=2, pady=5) # padding to add some space between buttons
entry.grid(row=1, column=0, columnspan=2, pady=5)
output_text.grid(row=2, column=0, columnspan=2, pady=5)

# z score search
search_label = tk.Label(frame, text="Enter value from list to find Z-score:")
search_label.grid(row=5, column=0)

z_search_entry = tk.Entry(frame)
z_search_entry.grid(row=5, column=1)

button_z_score_search = ttk.Button(frame, text='Search', command=find_z_score)
button_z_score_search.grid(row=6, column=1, pady=5)

# analyse and clear buttons on the first row
button_analyse = ttk.Button(frame, text="Analyse", command=get_input)
button_analyse.grid(row=3, column=0, pady=10, sticky='ew')

button_clear = ttk.Button(frame, text="Clear", command=clear_data)
button_clear.grid(row=3, column=1, pady=10, sticky='ew')

# show sorted values button
button_show_sorted = ttk.Button(frame, text="Show Sorted Values", command=show_sorted_values)
button_show_sorted.grid(row=4, column=0, columnspan=2, pady=10, sticky='ew')

# scrollbar for input and output windows
input_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=entry.yview)
input_scrollbar.grid(row=1, column=2, sticky='ns')
entry.config(yscrollcommand=input_scrollbar.set)

output_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=output_text.yview)
output_scrollbar.grid(row=2, column=2, sticky='ns')
output_text.config(yscrollcommand=output_scrollbar.set)

app.mainloop()
