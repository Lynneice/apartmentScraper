import tkinter as tk
from tkinter import font
import tkinter.scrolledtext as tkst
import requests

from bs4 import BeautifulSoup
from string import ascii_lowercase



#clear text entry before displaying new results
def clear_text():
    textbx.delete('1.0', '0.0')
    textbx.insert('0.0', "Fetching results..." )
    return

#format weather response using entry (city)
def display_weather(weather):
    try:
        name = weather['name']
        desc = weather['weather'][0]['description']
        temp = weather['main']['temp']
      
        #how to format the final display for the current conditions
        final_str = 'City: %s \nConditions: %s \nTemperature (F): %s' % (name, desc, temp)
    except:
        final_str = 'There was a problem retrieving that information.'
    return final_str



    
def start_program():
    #to start, clear the current data
    clear_text()
    
   
    #these are the entries we are getting from the user
    state = entryState.get().lower().strip()   
    city = entryCity.get().lower().strip()
    num_bedrooms = entryBeds.get().strip()
    price = entryPrice.get().strip()
   
   #the site we are scraping is rent.com
    URL = 'https://www.rent.com/{}/{}/apartments_condos_houses_townhouses_{}-bedroom_max-price-{}'.format(state, city, num_bedrooms, price)
    page = requests.get(URL)
    
    soup = BeautifulSoup(page.content, 'lxml')
    
    results = soup.find(class_='_2TvbS')
     
    try:
        apts = results.find_all('div', class_ ='_1bA6B _3wWhv')
    except AttributeError:
        textbx.insert('0.0', "Oops! Something went wrong.")
            
    weather_key= '2c3dac551108575d2ef561d56a8f345a'
    url='https://api.openweathermap.org/data/2.5/weather'
    params = {'APPID': weather_key, 'q': city, 'units': 'imperial'}
    response = requests.get(url,params=params)
    weather = response.json()
 
    #format weather for bottom frame
    print(weather['name'])
    print(weather['weather'][0]['description'])
    print(weather['main']['temp'])
    
    #display the result
    weatherbox['text'] = display_weather(weather)
    try:
        
        for i in apts:
                price = i.find('div', class_='_1r1Nq')
                location = i.find('a', class_='_1Fv8S _3DZdx')
                bedBath = i.find('div', class_='_2qk16')
                textbx.insert('1.0', price.text + '\n' + location.text + '\n' + bedBath.text + '\n\n' )
    except:
        textbx.insert('0.0', "There was a problem retrieving that information.")  
    return 

#Form the tkinter GUI 
WIDTH = 600
HEIGHT = 700

#The idea here is to provide a glance at the place the user is searching, 'rent is X, the weather is like X this time of year...'
root = tk.Tk()
root.title("Where should I live?")

#set the default dimensions
canvas = tk.Canvas(root, height = HEIGHT, width = WIDTH)
canvas.pack()

#Originally used a simple background image. may replace with textured background
# background_image = tk.PhotoImage(file='rocks.png')
background_label = tk.Label(root, bg = '#2d2d2d')
background_label.place(relwidth = 1, relheight = 1)

frame = tk.Frame(root, bg = '#2d2d2d', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.4, anchor='n')

#first of the entry boxes
entryState = tk.Entry(frame, font=40)
entryState.grid(row = 1, column = 2, sticky = 'e', padx = 5, pady = 5)

l1 = tk.Label(frame, font = 40, text = "State:")
l1.grid(row = 1, column = 1, sticky = 'se')

entryCity = tk.Entry(frame, font=40)
entryCity.grid(row = 2, column = 2, sticky = 'e', padx = 5, pady = 5)

l1 = tk.Label(frame, font = 40, text = "City:")
l1.grid(row = 2, column = 1, sticky = 'se')

entryBeds = tk.Entry(frame, font=40)
entryBeds.grid(row = 3, column= 2, sticky = 'e', padx = 5, pady = 5)

l1 = tk.Label(frame, font = 40, text = "Number of Bedrooms Desired:")
l1.grid(row = 3, column = 1, sticky = 'se')

entryPrice = tk.Entry(frame, font=40)
entryPrice.grid(row = 4, column = 2, sticky = 'e', padx = 5, pady = 5)

l1 = tk.Label(frame, font = 40, text = "Maximum Price:")
l1.grid(row = 4, column = 1, sticky = 'se')


#this button will initiate the search
button = tk.Button(frame, text = "🔎 Search", font=40, bg = '#8A9797', fg = '#ABC7DE', command=lambda: start_program())
button.grid(row =5, columnspan = 3, padx =10, pady = 10)


#this is where we'll display the weather conditions
lower_frame = tk.Frame(root, bg = '#ABDEDC', bd =  5)
lower_frame.place(relx = 0.5, rely = 0.8, relwidth = 0.75, relheight=0.4, anchor='s')

textbx = tk.Text(lower_frame, wrap = tk.WORD)
textbx.place(relwidth = 1, relheight = 1)

scroll = tk.Scrollbar(lower_frame)
scroll.pack(fill = tk.Y, side = tk.RIGHT)

scroll.config(command=textbx.yview)
textbx.config(yscrollcommand=scroll.set)


bottom_frame = tk.Frame(root, bg = '#ABDEDC', bd = 5)
bottom_frame.place(relx = 0.5, rely = 0.9, relwidth = 0.75, relheight = 0.09, anchor = 's')

weatherbox = tk.Label(bottom_frame)
weatherbox.place(relwidth = 1, relheight = 1)

root.mainloop()

