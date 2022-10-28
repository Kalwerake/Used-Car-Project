# packages
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re

class car_thief:
    '''car_thief() will output a pandas dataframe containing data on used cars, from https://www.cazoo.co.uk/.
            - use method fetch_links() for getting links to all car adverts on the website.
    '''
    def __init__(self):
        
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        self.results_price = []
        self.all_links = []
        self.soup_menu = []
        
        self.price = []
        self.name = []
        self.year = []
        self.transmission = []
        self.mileage = []
        self.seats = []
        self.engine = []
        self.body = []
        self.colour = []
        self.drive = []
        self.registration = []
        self.previous_owners = []
        self.keys = []
        self.emissions = []
        self.ulez = []
        self.top_speed= []
        self.accelaration_0_62 = []
        self.power = []
        self.tax = []
        self.insurance = []
        self.mpg = []
        self.service_record = []
        
    def fetch_links(self, pages):
        ''' fetch_links will creat list containing links to all car adverts and store in object,
            - function argument is number of pages on website.
            - use method soup_chef() next, to scrape data from each link .'''
        
        hrefs = []
        prices = []
        for i in range(1,pages):
            url = 'https://www.cazoo.co.uk/cars/?page='+ str(i)

            response = requests.get(url, headers = self.headers)

            soup = BeautifulSoup(response.content, 'html.parser')
            
            link = soup.find_all('a', {'class' : "vehicle-cardstyles__LinkWrap-sc-1bxv5iu-4 dLzowz"})
            price = soup.find_all('div', {'class':"pricingstyles__Wrap-rs9839-0 ckMUIu"})
            
            links.append(link)
            results_price.append(price)
        
        clean_hrefs = []
        for i in hrefs:
            for j in i:
                car = j.get("href")
                clean_hrefs.append(car)
        
        for i in range(len(clean_hrefs)):
            clean_hrefs[i] = "https://www.cazoo.co.uk" + clean_hrefs[i]
        
        self.all_links.append(clean_hrefs)
        self.results_price.append(prices)
        
    def soup_chef(self):
        ''' 
                        ~~~~~~~~~~~~~ THIS WILL TAKE A WHILE!!~~~~~~~~~~~~~~~~
            soup_chef() will parse all the car advert htmls, and make soup objects to be parsed later for all data, 
            the output will stored in object.
            - use soup_critic() to parse soup objects and extract all data which will be stored in object'''
        
        car_soups = []
        for i in all_links:
            response = requests.get(i, headers = self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            car_soups.append(soup)
        
        
        self.soup_menu.append(car_soups)
        
    def soup_critic(self):
        '''soup_critic() will parse all soup objects and extract data on used cars.All data will be stored in object.
           -  use panda_tamer() next to make a pandas dataframe containing all data'''
            
        for l,page in enumerate(self.results_price):
            for k,i in enumerate(page):
                p = i.find('p', {'class': 'full-pricestyles__Price-sc-12l0fhp-0 kZsXtM','data-test-id':"card-pricing-full-price-gb"})
                
                if p != None:
                    self.price.append(p.get_text())
        
                elif p == None:
                    clean = results_price[l][k].get_text() #get all text from each div section
                    value = re.findall('(£\d+(\,)?\d+\d){2}',clean)[0][0]# will return the second pattern match, the current price
                    self.price.append(value)
                
        
        for soup in car_soups:
            car = soup.find("h1",{"class":"sc-yrk414-0 Abyeg"}).get_text()
            name.append(car)
            specs =["registrationDate","gearbox","odometerReading","numSeats","engineSize","bodyType","exteriorColour","driveType","vrm","numberOfPreviousOwners","numberOfFunctioningKeys","emissions","ulezChargeExempt","topSpeedMph","from0to62milesAccelerationInSec","enginePowerBhp","vehicleTaxPerYear","insurance","fuelConsumption"]
            
            details = []
            
            for spec in specs:
                indv = soup.find("div",{"class": "flex flex-wrap gap-x-xs py-s","data-test-id": spec})
                
                if indv != None:
                    details.append(indv.find("dd",{"class": "font-semibold"}).get_text())
                else:
                    details.append(np.NaN)
    
            self.year.append(details[0])
            self.transmission.append(details[1])
            self.mileage.append(details[2])
            self.seats.append(details[3])
            self.engine.append(details[4])
            self.body.append(details[5])
            self.colour.append(details[6])
            self.drive.append(details[7])
            self.registration.append(details[8])
            self.previous_owners.append(details[9])
            self.keys.append(details[10])
            self.emissions.append(details[11])
            self.ulez.append(details[12])
            self.top_speed.append(details[13])
            self.accelaration_0_62.append(details[14])
            self.power.append(details[15])
            self.tax.append(details[16])
            self.insurance.append(details[17])
            self.mpg.append(details[18])
    
            service = soup.find("section",{"class":"px-s md:px-l self-center w-full max-w-base","id": "service-history"})
            if service != None:
                number = service.find_all("article",{"class":"AccordionItemstyles__Wrap-sc-1i7ks8d-0 erdWGR"})
                self.service_record.append(len(number))
            else:
                self.service_record.append(0)
                
    def panda_tamer(self):
        ''' panda tamer will output all car data in pandas DataFrame form. save output onto a variable'''
        
        df = pd.DataFrame({'Name': name,'Year': year, 'Mileage': mileage, 'Engine_Size': engine, 
                           'Transmission': transmission, 'Seats': seats , 'Body_Type': body, "Colour": colour, 'Drive_Type': drive,
                           'Registration': registration, 'Previous_Owners': previous_owners, 'Keys': keys, 'Emissions':emissions, 
                           'ULEZ_Exempt':ulez,'Top_speed':top_speed, 'Accelaration_0_62': accelaration_0_62, 'Power':power, 'Tax': tax,
                           'Insurance': insurance, 'Mpg': mpg, 'Service_record' : service_record,'Price': cost})
        
        '''There will be cars that were sold while the scraper was running'''
        missing_col = df.drop(columns = ['Service_record','Price','Name']) # dataframe with columns containing no Nan
        all_NaN = missing_col.isnull().all(1) #row indexes where all columns in missing_col contain NaN
        name_Nans = cazoo_cars.loc[all_NaN, "Name"] # name values for rows with all NaN
        missing_col[all_NaN].join(name_Nans).head()
        
        df.drop(cazoo_cars[all_NaN].index, inplace = True)
        df.reset_index(drop = True, inplace = True)
        
        return df
