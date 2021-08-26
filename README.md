# Star Scraper
Prints random 1 name of the 88 constellations 
Scrapes https://www.iau.org/public/themes/constellations/[https://www.iau.org/public/themes/constellations/] for the constellation names when you first run it 
Caches the names into constellations.csv and then searches through the file, vastly improving performance
## How to use
    1. Download this repo to your computer, or just copy the 2 files
    2. This project depends on your device having these Python libraries:
        - BeautifulSoup 4
        - requests
        - pathlib