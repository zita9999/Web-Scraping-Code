# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys
 

###INPUT THE LOCATION YOU WANT WITH STAYS AT THE END######################
n= 1
city = 'italy, rome'
class AirSpider(scrapy.Spider):
    name = 'air'
    #allowed_domains = ['www.airbnb.ca']
    
    #get the webpage
    def start_requests(self):
        global city
        yield SeleniumRequest(url = "https://www.airbnb.ca/s/"+city+"/homes?refinement_paths%5B%5D=%2Ffor_you&search_type=search_query",
                              wait_time = 1, 
                              callback = self.parse)

   #send the name of the city you inputted into the search box on the website 
    def parse(self, response):
        global n
        global city
        #response.setHeader("Set-Cookie", "HttpOnly;Secure;SameSite=Strict")
        driver = response.meta['driver']
        search_input = driver.find_element_by_xpath("//input[@aria-label]")
        
        search_input.send_keys('')
        search_input.send_keys(Keys.ENTER)
        
        driver.save_screenshot('after_filling_input.png')
       
       
        html = driver.page_source
        response_obj = Selector(text = html)
       
    
        house = response_obj.xpath("//div[@itemprop = 'itemListElement']/div/div[@class]")
        i=2
        ii = str(i)
        
        #loop through all the listings collecting data     
        for houses in house:
            name = houses.xpath(".//a/@aria-label").get()
            link = houses.xpath(".//a/@href").get()
            rating = houses.xpath("(((//div[@itemprop = 'itemListElement']/div/div[@class]/div[@class])["+ii+"]/div/span)[2]/span/span[@class])[3]/text()").get()
            guests = houses.xpath("((//div[@itemprop = 'itemListElement']/div/div[@class]/div[@class])["+ii+"]/div[@class])[3]/text()").get()
            bedrooms = houses.xpath("(((//div[@itemprop = 'itemListElement']/div/div[@class]/div[@class])["+ii+"]/div[@class])[3]/text())[3]").get()
            beds = houses.xpath("(((//div[@itemprop = 'itemListElement']/div/div[@class]/div[@class])["+ii+"]/div[@class])[3]/text())[5]").get()
            baths = houses.xpath("(((//div[@itemprop = 'itemListElement']/div/div[@class]/div[@class])["+ii+"]/div[@class])[3]/text())[7]").get()
            price = houses.xpath("((//div[@itemprop = 'itemListElement']/div/div[@class]/div[@class])["+ii+"]/div[@class])[5]/div/div/span/span[@class]/text()").get()
            i = i+2
            ii = str(i)
            if link:
                yield{'link': 'https://airbnb.ca'+link, 'name': name, 'rating':rating, 'guests': guests,
                      'bedrooms': bedrooms, 'beds': beds, 'baths': baths, 'price':price}
        
        if n <6:
            n += 1
            if n ==3:
                n = 4
            nn = str(n)
        else:
            n =6
        nn = str(n)
        print(n)
        
        #if at end of page will go to the next available page
        next_page = response.xpath("(//nav/ul/li)["+nn+"]/a/@href").get()
        if next_page:
            yield SeleniumRequest(url = 'https://www.airbnb.ca'+next_page, callback = self.parse, wait_time =3)
            
