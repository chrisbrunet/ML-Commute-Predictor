import pickle
import pandas as pd
from bs4 import BeautifulSoup
import requests
import tkinter as tk

# Loading ColumnTransformer and ML Model
model_filename = 'commute_estimator_model.pkl'
with open(model_filename, 'rb') as file:
    model = pickle.load(file)

ct_filename = 'commute_estimator_ct.pkl'
with open(ct_filename, 'rb') as file:
    ct = pickle.load(file)

def run_model(r):
    direction = 'northbound' 
    max_temp = 10
    min_temp = 0
    mean_temp = 5
    total_rain = 0
    total_snow = 0
    total_precip = 0 
    snow_on_grnd = 0
    wind_dir = 28
    wind_speed = 40

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

    text = f"It will take approximately {int(prediction//60)} mintues and {int(prediction%60)} seconds to get to school."

    output = tk.Label(r, text=text)
    output.pack(padx=20, pady=5)

## Try web scraping
# url = '<a href="https://www.timeanddate.com/weather/canada/calgary">https://www.timeanddate.com/weather/canada/calgary</a>'  # Replace this with the URL of the website you want to scrape
# response = requests.get(url)

# if response.status_code == 200:
#     html_content = response.content
# else:
#     print("Failed to fetch the website.")
#     exit()

root = tk.Tk()
root.title("Commute Predictor")
root.geometry("600x400")

txt1 = tk.Entry().pack(padx=1, pady=1)
calc_button = tk.Button(text="Calculate Commute", command=lambda: run_model(root)).pack(padx=5, pady=20)

root.mainloop()
