# gs_cited_artical_crawler

This Python-based web scraper is designed to retrieve citation information from Google Scholar for a specified article. It extracts details such as the title, authors, publication platform, and year of all citing documents.

## Features

- **Fetch Citation Details:** Automatically gathers comprehensive citation data from Google Scholar.

- **Easy to Use:** User-friendly command line interface.

- **Output Formatting:** Organizes citation information in a structured format for easy analysis.

## Requirements

- Python 3.9 or higher

- Platform:Windows

- [chromedriver](https://googlechromelabs.github.io/chrome-for-testing/)

- Google Chrome

## Installation

Clone the repository to your local machine:

```bash
git clone git@github.com:showlibia/gs_cited_artical_crawler.git
cd gs_cited_artical_crawler
```

Install the required Python libraries:

```bash
pip install -r requirements.txt
```

## Usage

Run the scraper using the following command:

```bash
python crawler.py "articalname"
```

## Output

The script will output a json file named `cited_articles.json` containing the following columns:

- **Title:** Title of the citing article.

- **Citation**:GB/T 7714 citation text

- **Authors:** List of authors.

- **Publication:** Platform or journal where the article is published.

- **Year:** Publication year