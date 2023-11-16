import pickle
import pandas as pd
from bs4 import BeautifulSoup
import requests
import html5lib
import tkinter as tk

# Global variables
grid_depth = 0

# Functions
def load_model():
    model_filename = 'commute_estimator_model.pkl'
    with open(model_filename, 'rb') as file:
        model = pickle.load(file)
    return model

def load_ct():
    ct_filename = 'commute_estimator_ct.pkl'
    with open(ct_filename, 'rb') as file:
        ct = pickle.load(file)
    return ct

def get_current_weather():
    URL = "https://www.timeanddate.com/weather/canada/calgary"
    r = requests.get(URL) 

    soup = BeautifulSoup(r.content, 'html5lib')
    qlook = soup.find('div', attrs={'id': 'qlook'})
    text = qlook.find_all('p')[1].text
    weather = text.split()
    hi = weather[4]
    lo = weather[6]
    mean = (int(hi) + int(lo)) / 2
    wind_s = weather[8]

    default_values = {
        'Max Temp (°C)': hi,
        'Min Temp (°C)': lo,
        'Mean Temp (°C)': mean,
        'Wind Speed (km/h)': wind_s,
    }

    return default_values

def get_current_weather_and_set_defaults():
    default_values = get_current_weather()
    max_temp_entry.delete(0, tk.END) 
    max_temp_entry.insert(0, default_values['Max Temp (°C)'])
    min_temp_entry.delete(0, tk.END) 
    min_temp_entry.insert(0, default_values['Min Temp (°C)'])
    mean_temp_entry.delete(0, tk.END) 
    mean_temp_entry.insert(0, default_values['Mean Temp (°C)'])
    wind_spd_entry.delete(0, tk.END) 
    wind_spd_entry.insert(0, default_values['Wind Speed (km/h)'])

def run_model(): 
    model = load_model()
    ct = load_ct()

    wind_dir_dict = {'N':0, 'NE': 4.5, 'E':9, 'SE':14.5, 'S':18, 'SW':22.5, 'W':27, 'NW':31.5} 
    commute_dir = 'northbound' if commute_dir_var.get() else 'southbound'
    max_temp = max_temp_entry.get()
    min_temp = min_temp_entry.get()
    mean_temp = mean_temp_entry.get()
    rain = rain_entry.get()
    snow = snow_entry.get()
    precip = precip_entry.get()
    snowg = snow_on_gnd_entry.get()
    wind_dir = selected_wind_direction.get()
    wind_spd = wind_spd_entry.get()
    
    new_data = pd.DataFrame({
        'direction': [commute_dir],
        'Max Temp (°C)': [float(max_temp)],
        'Min Temp (°C)': [float(min_temp)],
        'Mean Temp (°C)': [float(mean_temp)],
        'Total Rain (mm)': [float(rain)],
        'Total Snow (cm)': [float(snow)],
        'Total Precip (mm)': [float(precip)],
        'Snow on Grnd (cm)': [float(snowg)],
        'Dir of Max Gust (10s deg)': [wind_dir_dict[wind_dir]],
        'Spd of Max Gust (km/h)': [float(wind_spd)]
    })

    transformed_new_data = ct.transform(new_data)
    prediction = model.predict(transformed_new_data)

    if new_data['direction'].equals('northbound'):
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

# Checkbox variables
commute_dir_var = tk.IntVar()
selected_wind_direction = tk.StringVar()

# Setting up grid in GUI 
commute_dir_label = tk.Label(root, text='Commute Direction').grid(row=grid_depth, column=0, padx=5, pady=5)
northbound_checkbox = tk.Checkbutton(root, text='Northbound', variable=commute_dir_var, onvalue=1, offvalue=0)
southbound_checkbox = tk.Checkbutton(root, text='Southbound', variable=commute_dir_var, onvalue=0, offvalue=1)
northbound_checkbox.grid(row=grid_depth, column=1, padx=5, pady=5, sticky="w")
grid_depth += 1
southbound_checkbox.grid(row=grid_depth, column=1, padx=5, pady=5, sticky="w")
grid_depth += 1

get_weather_button = tk.Button(root, text="Get Current Weather", command=get_current_weather_and_set_defaults)
get_weather_button.grid(row=grid_depth, column=0, columnspan=3, pady=10)
grid_depth += 1

max_temp_label = tk.Label(root, text='Max Temp (°C)').grid(row=grid_depth, column=0, padx=5, pady=5)
max_temp_entry = tk.Entry(root)
max_temp_entry.grid(row=grid_depth, column=1, columnspan=2, padx=5, pady=5, sticky="w")
grid_depth += 1

min_temp_label = tk.Label(root, text='Min Temp (°C)').grid(row=grid_depth, column=0, padx=5, pady=5)
min_temp_entry = tk.Entry(root)
min_temp_entry.grid(row=grid_depth, column=1, columnspan=2, padx=5, pady=5, sticky="w")
grid_depth += 1

mean_temp_label = tk.Label(root, text='Mean Temp (°C)').grid(row=grid_depth, column=0, padx=5, pady=5)
mean_temp_entry = tk.Entry(root)
mean_temp_entry.grid(row=grid_depth, column=1, columnspan=2, padx=5, pady=5, sticky="w")
grid_depth += 1

rain_label = tk.Label(root, text='Total Rain (mm)').grid(row=grid_depth, column=0, padx=5, pady=5)
rain_entry = tk.Entry(root)
rain_entry.grid(row=grid_depth, column=1, columnspan=2, padx=5, pady=5, sticky="w")
grid_depth += 1

snow_label = tk.Label(root, text='Total Snow (cm)').grid(row=grid_depth, column=0, padx=5, pady=5)
snow_entry = tk.Entry(root)
snow_entry.grid(row=grid_depth, column=1, columnspan=2, padx=5, pady=5, sticky="w")
grid_depth += 1

precip_label = tk.Label(root, text='Total Precip (mm)').grid(row=grid_depth, column=0, padx=5, pady=5)
precip_entry = tk.Entry(root)
precip_entry.grid(row=grid_depth, column=1, columnspan=2, padx=5, pady=5, sticky="w")
grid_depth += 1

snow_on_gnd_label = tk.Label(root, text='Snow on Ground (cm)').grid(row=grid_depth, column=0, padx=5, pady=5)
snow_on_gnd_entry = tk.Entry(root)
snow_on_gnd_entry.grid(row=grid_depth, column=1, columnspan=2, padx=5, pady=5, sticky="w")
grid_depth += 1

wind_spd_label = tk.Label(root, text='Wind Speed (km/h)').grid(row=grid_depth, column=0, padx=5, pady=5)
wind_spd_entry = tk.Entry(root)
wind_spd_entry.grid(row=grid_depth, column=1, columnspan=2, padx=5, pady=5, sticky="w")
grid_depth += 1

wind_dir_label = tk.Label(root, text='Wind Direction').grid(row=grid_depth, column=0, padx=5, pady=5)
N_button = tk.Radiobutton(root, text='N', variable=selected_wind_direction, value='N').grid(row=grid_depth, column=1, padx=1, pady=5, sticky="w")
NE_button = tk.Radiobutton(root, text='NE', variable=selected_wind_direction, value='NE').grid(row=grid_depth, column=2, padx=1, pady=5, sticky="w")
grid_depth += 1
E_button = tk.Radiobutton(root, text='E', variable=selected_wind_direction, value='E').grid(row=grid_depth, column=1, padx=1, pady=5, sticky="w")
SE_button = tk.Radiobutton(root, text='SE', variable=selected_wind_direction, value='SE').grid(row=grid_depth, column=2, padx=1, pady=5, sticky="w")
grid_depth += 1
S_button = tk.Radiobutton(root, text='S', variable=selected_wind_direction, value='S').grid(row=grid_depth, column=1, padx=1, pady=5, sticky="w")
SW_button = tk.Radiobutton(root, text='SW', variable=selected_wind_direction, value='SW').grid(row=grid_depth, column=2, padx=1, pady=5, sticky="w")
grid_depth += 1
W_button = tk.Radiobutton(root, text='W', variable=selected_wind_direction, value='W').grid(row=grid_depth, column=1, padx=1, pady=5, sticky="w")
NW_button = tk.Radiobutton(root, text='NW', variable=selected_wind_direction, value='NW').grid(row=grid_depth, column=2, padx=1, pady=5, sticky="w")
grid_depth += 1

# Button which calls run_model()
calc_button = tk.Button(root, text="Calculate Commute", command=lambda: run_model())
calc_button.grid(row=grid_depth, column=0, columnspan=3, pady=10)

# fit window to contents
root.update_idletasks()

root.mainloop()