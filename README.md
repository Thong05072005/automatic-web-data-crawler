# Automatic Web Data Crawler

A Python-based automation tool for crawling product data from e-commerce websites and exporting the results to Excel files.  
This project focuses on web automation, data extraction, and handling dynamic web content.

---

## Features
- Automatically crawl product information from web pages
- Extract data such as product name, price, specifications, and category
- Handle dynamic content (e.g. "Load more" button)
- Export collected data to Excel (.xlsx)
- Support scheduled or repeated crawling runs

---

## Technologies Used
- Python
- Selenium
- BeautifulSoup
- Pandas
- Chrome WebDriver

---

## Data Source
- Target website: Thegioididong.com (for learning purposes)
- Data includes publicly available product information

> **Note:** This project is for educational purposes only.

---

## How It Works
1. Selenium opens the browser and navigates to the target page
2. Dynamic content is loaded automatically
3. BeautifulSoup parses the HTML content
4. Extracted data is processed using Pandas
5. Final results are exported to an Excel file

---

## Output
- Excel file containing structured product data
- Columns: product name, price, specifications, category, etc.

---

## Project Purpose
- Practice web automation with Selenium
- Learn web scraping workflows
- Improve data processing and export using Pandas

---

## Notes
- Crawling speed depends on network and website response
- WebDriver version must match the installed browser version
