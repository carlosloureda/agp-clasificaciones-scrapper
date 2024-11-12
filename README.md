# AGPool Scraper

This project is a web scraper designed to extract data from the AGPool website. The scraper collects league information and generates JSON files, which are then made available through GitHub Pages. These JSON files are later consumed by a frontend application hosted in a separate repository.

## Features

- Scrapes league selection information from AGPool.
- Uses a headless browser for operations to support execution on servers without a GUI.
- Automatically triggered with GitHub Actions.
- Outputs JSON data files hosted on GitHub Pages.

## Setup and Usage

### Prerequisites

- [Python 3.x](https://www.python.org/)
- [Selenium](https://www.selenium.dev/) with ChromeDriver installed.

### Running Locally

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/carlosloureda/agpool-scraper.git
   cd agpool-scraper

   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Scraper**:

   Execute the scraper using Python's module system:

   ```bash
   python -m app.main
   ```

   This will run the scraper and generate the JSON files in the data directory.

## Deployment

The scraping process is automated through GitHub Actions, which runs the scraper and updates the JSON files on GitHub Pages. Ensure the GitHub Action workflow is correctly configured in the .github/workflows directory.

## Frontend Integration

The frontend application, which utilizes the generated JSON data, is hosted in a separate repository. You can find the frontend code and further details here: [Frontend Repository](https://github.com/carlosloureda/agp-clasificaciones).

## License

This project is licensed under the MIT License. See the LICENSE file for details.
