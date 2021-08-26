#!/bin/python3
# @author Gurveer Singh (Github = Gurv33r)

from pathlib import Path #used to validate a filepath
import csv #csv file processing
import random #RNG 
from bs4 import BeautifulSoup #retrieves and searches within the HTML content of the target page
import requests #accesses the target page
# holds all constellation names retrieved from the link
constellations=[] 
url="https://www.iau.org/public/themes/constellations/" # the target link

def innerHTML(element):
    """Returns the inner HTML of an element as a string"""
    return element.encode_contents().decode("utf-8")

# Meat and Potatoes 
def main():
    #first check if the cache file exists via the filepath
    filepath = Path("./constellations.csv")
    #is_file() assures that the file exists and is a file
    if filepath.is_file(): # constellations.csv exists
        # read constellations.csv
        with open('constellations.csv', 'r') as file:
            # read the file
            reader = csv.reader(file, delimiter=',')
            # there's only one row in the file, but reader isn't subscriptable, so this is the next best solution
            for row in reader:
                # turn row into string with ",".join(row) and get the individual elements with .split(',')
                constellations = ",".join(row).split(',')
                # print a random constellation name
                print(random.choice(constellations))
    else: # cache file doesn't exist
        # create the cache file
        file = open('constellations.csv','w')
        # scrape https://www.iau.org/public/themes/constellations/
        page = requests.get(url) # send a request and get the page
        soup = BeautifulSoup(page.content,"html.parser")
        # info is arranged as table values
        table = soup.find('tbody') # tbody has all the names i'm looking for
        rows = table.find_all('tr')[1:] # first row is just column headers
        # for every row in the tbody
        for row in rows:
            # collect all the td tags into an array
            namecol = row.find_all('td')[0]
            # this site is mildly inconsistent with its display strcture
            # at some points, it wraps the constellation name in a p-tag and at some points it doesn't
            p = namecol.find_all('p')
            temp = [] # holds the components of the constellation name
            if p: # if there is a p tag, the first one will have the name
                temp = innerHTML(p[0]).split(" ") 
            else: # no p tag means you are already at the element you want
                temp = innerHTML(namecol).split(' ')
            # assemble the name given the size of temp
            if len(temp) > 3:
                name = temp[0]+" "+temp[1]
            else:
                name = temp[0]
            # some names were spaced inconsistently or had a comma, so the next 4 lines removes any byproducts of those    
            if name.endswith('<a'):
                name = name[:name.index('<')]
            elif name.endswith(','):
                name = name[:len(name)-1]
            # append it to constellations
            constellations.append(name)
        # initialize a csv.Writer() object for writing to the cache file
        writer = csv.writer(file)
        # write the names to the file
        writer.writerow(constellations)
        # close the cache file 
        file.close()
        # print a random element in constellations 
        print(random.choice(constellations)) 
main()       
