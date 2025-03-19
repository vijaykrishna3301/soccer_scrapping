## Soccer Team Scraper

This project is a Scrapy-based web scraper that collects soccer team data from various official club websites. Since each website has different structures, the scraper is designed to handle multiple formats efficiently.

### Installation

1. Clone the Repository

```
git clone https://github.com/yourusername/soccer-scraper.git
cd soccer-scraper
```

2. Create a Virtual Environment (Optional but Recommended)
```
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install Dependencies
```
pip3 install scrapy
```
### Usage

1. Run a Scrapy Spider

To crawl a specific soccer website:
```
scrapy crawl ymssoccer -o players.json
```
This will save the extracted player data into players.json.
