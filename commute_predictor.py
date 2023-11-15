import pickle
import pandas as pd
from bs4 import BeautifulSoup
import requests
import tkinter as tk

# Global variables
grid_depth = 0
labels = ['Commute Direction',
        'Max Temp (°C)',
        'Min Temp (°C)',
        'Mean Temp (°C)',
        'Total Rain (mm)',
        'Total Snow (cm)',
        'Total Precip (mm)',
        'Snow on Grnd (cm)',
        'Wind Direction',
        'Wind Speed (km/h)']

# Loading ColumnTransformer and ML Model
model_filename = 'commute_estimator_model.pkl'
with open(model_filename, 'rb') as file:
    model = pickle.load(file)

ct_filename = 'commute_estimator_ct.pkl'
with open(ct_filename, 'rb') as file:
    ct = pickle.load(file)   

# Funciton to run model and print result in GUI
def run_model(inputs): 
    wind_dir_dict = {'N':0, 'NE': 4.5, 'E':9, 'SE':14.5, 'S':18, 'SW':22.5, 'W':27, 'NW':31.5} 

    direction = 'northbound' if inputs[0].get() else 'southbound'
    max_temp = float(inputs[1].get())
    min_temp = float(inputs[2].get())
    mean_temp = float(inputs[3].get())
    total_rain = float(inputs[4].get())
    total_snow = float(inputs[5].get())
    total_precip = float(inputs[6].get())
    snow_on_grnd = float(inputs[7].get())
    wind_dir = wind_dir_dict[inputs[8].get()]
    wind_speed = float(inputs[16].get())

    new_data = pd.DataFrame({
        'direction': [direction],
        'Max Temp (°C)': [max_temp],
        'Min Temp (°C)': [min_temp],
        'Mean Temp (°C)': [mean_temp],
        'Total Rain (mm)': [total_rain],
        'Total Snow (cm)': [total_snow],
        'Total Precip (mm)': [total_precip],
        'Snow on Grnd (cm)': [snow_on_grnd],
        'Dir of Max Gust (10s deg)': [wind_dir],
        'Spd of Max Gust (km/h)': [wind_speed]
    })
    
    transformed_new_data = ct.transform(new_data)
    prediction = model.predict(transformed_new_data)

    if direction == 'northbound':
        text = f"It will take {int(prediction//60)}min, {int(prediction%60)}sec to get to school."
    else: 
        text = f"It will take {int(prediction//60)}min, {int(prediction%60)}sec to get home."

    output = tk.Label(root, text=text)
    global grid_depth
    grid_depth += 1
    output.grid(row=grid_depth, column=0, columnspan=3, pady=10)

# Initializing window
root = tk.Tk()
root.title("Commute Predictor")

entries = []

# Initializing user input variables
commute_direction_var = tk.IntVar()
selected_wind_direction = tk.StringVar()
input_vars = []

# Setting up grid in GUI 
for label_text in labels:
    label = tk.Label(root, text=label_text)
    label.grid(row=grid_depth, column=0, padx=5, pady=5)

    if label_text == 'Commute Direction':
        northbound_checkbox = tk.Checkbutton(root, text='Northbound', variable=commute_direction_var, onvalue=1, offvalue=0)
        southbound_checkbox = tk.Checkbutton(root, text='Southbound', variable=commute_direction_var, onvalue=0, offvalue=1)

        northbound_checkbox.grid(row=grid_depth, column=1, padx=5, pady=5, sticky="w")
        grid_depth += 1
        southbound_checkbox.grid(row=grid_depth, column=1, padx=5, pady=5, sticky="w")

        input_vars.append(commute_direction_var)

    elif label_text == 'Wind Direction':
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        checkboxes_per_row = 2
        for j, direction in enumerate(directions):
            radiobutton = tk.Radiobutton(root, text=direction, variable=selected_wind_direction, value=direction)
            row_value = grid_depth + j // checkboxes_per_row
            col_value = 1 + j % checkboxes_per_row
            radiobutton.grid(row=row_value, column=col_value, padx=1, pady=5, sticky="w")
            input_vars.append(selected_wind_direction)

        grid_depth += (len(directions) + checkboxes_per_row - 1) // checkboxes_per_row

    else:
        entry = tk.Entry(root)
        entry.grid(row=grid_depth, column=1, columnspan=2, padx=5, pady=5)
        entries.append(entry)

        input_vars.append(entry)

    grid_depth += 1

# Button which calls run_model()
calc_button = tk.Button(root, text="Calculate Commute", command=lambda: run_model(input_vars))
calc_button.grid(row=grid_depth, column=0, columnspan=3, pady=10)

# fit window to contents
root.update_idletasks()

root.mainloop()
