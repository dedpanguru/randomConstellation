#!/bin/python3
# @author Gurveer Singh
# Web-scraping practice:
# check if constellations.csv exists
# if it does, 
#   separate by comma and print an element at a random index
# else 
#   https://www.iau.org/public/themes/constellations/ for all the constellation names
#   cache the names into a file called constellations.csv and print a random constellation 

# file existence check
from pathlib import Path #used to validate a filepath
import csv #csv file processing
import random #RNG 
from bs4 import BeautifulSoup
import requests

constellations=[]
url="https://www.iau.org/public/themes/constellations/"

def innerHTML(element):
    """Returns the inner HTML of an element as a UTF-8 encoded bytestring"""
    return element.encode_contents().decode("utf-8")

def main():
    filepath = Path("./constellations.csv")
    #is_file() assures that the file exists and is a file
    if filepath.is_file(): # constellations.csv exists
        #read constellations.csv
        with open('constellations.csv', 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                print(random.choice(",".join(row).split(',')))
    else:
        file = open('constellations.csv','w')
        # scrape https://www.iau.org/public/themes/constellations/
        page = requests.get(url)
        soup = BeautifulSoup(page.content,"html.parser")
        # info is arranged as table values
        table = soup.find('tbody')
        rows = table.find_all('tr')
        rows = rows[1:len(rows)-1]
        # for every row
        for row in rows:
            # collect all the td tags into an array
            namecol = row.find_all('td')[0]
            # name should be at first td's first p, has a-tag, so print to check
            p = namecol.find_all('p')
            temp = []
            if p:
                temp = innerHTML(p[0]).split(" ")
            else:
                temp = innerHTML(namecol).split(' ')
            
            if len(temp) > 3:
                name = temp[0]+" "+temp[1]
            else:
                name = temp[0]
                
            if name.endswith('<a'):
                name = name[:name.index('<')]
            elif name.endswith(','):
                name = name[:len(name)-1]
            # append it to constellations
            constellations.append(name)
        # initialize a csv.Writer() object write to constellations
        writer = csv.writer(file)
        # write constellations to the file
        writer.writerow(constellations)           
        # print a random element in constellations 
        print(random.choice(constellations)) 
main()       

