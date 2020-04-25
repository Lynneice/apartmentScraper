"""
This is a work-in=progress. It currently works in the console, but I am working on expanding it.
"""
import requests
from bs4 import BeautifulSoup
from string import ascii_lowercase


correct_search = True
while correct_search is True:
    
    #accepted answers for 'state'
    states = ['alabama', 'alaska', 'arizona', 'Arkansas', 'California', 'Colorado',
    'Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa',
    'Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota',
    'Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico',
    'New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania',
    'Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont',
    'Virginia','Washington','West Virginia','Wisconsin','Wyoming']
    
	#take user input and place it in URL placeholder
    state = input("Please type your state:").lower().strip()
	
    #do not allow entry other than accepted spelling in lowercase
    if state.lower() not in states:
         state = input("That is not a valid state. Please try again by typing it out entirely:").lower()
    else:
         print()


    city = input( "Please type your city:").strip()
    city = city.replace(" ","-")
    
    #trying not to break the URL
    num_bedrooms = input("Number of bedrooms desired:").strip()
    if num_bedrooms not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'studio']:
        num_bedrooms = input("Please enter the number of bedrooms desired.")
    price = input("Max price:").strip()
    break
    
URL = 'https://www.rent.com/{}/{}/apartments_condos_houses_townhouses_{}-bedroom_max-price-{}'.format(state, city, num_bedrooms, price)
page = requests.get(URL)

#create soup
soup = BeautifulSoup(page.content, 'lxml')

#first 30 listings card
results = soup.find(class_='_2TvbS')

 #individual apts cards 
apts = results.find_all('div', class_ ='_1bA6B _3wWhv')


#see the number of listings available with usesr input criteria
print("There are " + str(len(apts)) + " listings available!")

#iterate through first 30 listings and return the results.
for i in apts:
    price = i.find('div', class_='_1r1Nq')
    location = i.find('a', class_='_1Fv8S _3DZdx')
    bedBath = i.find('div', class_='_2qk16')
    print(price.text)
    print(location.text)
    print(bedBath.text)
    
    print('\n')

     
