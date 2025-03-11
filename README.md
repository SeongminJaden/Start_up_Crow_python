# Qt-based Web Crawler GUI

This project provides a PyQt-based graphical user interface (GUI) for selecting and running web crawlers for various websites.

## Requirements

Ensure you have the following dependencies installed before running the script:

### System Requirements
- Python 3.x
- PyQt5 for the GUI

### Install Required Python Packages
```bash
pip install PyQt5
```

## Usage

Run the following command to execute the script:
```bash
python main.py
```

## How It Works
1. The application opens a PyQt-based GUI.
2. The user can select a website from a dropdown menu.
3. When the '크롤링!' button is clicked, the selected web scraper module runs.
4. The script prints the corresponding website link and starts the crawling process.
5. If '전체크롤링' is selected, all scrapers are executed sequentially.

## Features
- Select individual web crawlers for specific websites.
- Run all available crawlers at once.
- The script maintains a dictionary of available crawling modules.
- Crawled data is saved in `Output.txt` when '전체크롤링' is executed.

## Notes
- Ensure all required modules (`bizinfo`, `iitp`, `ip`, `kiat`, `kstartup`, `nipa`, `sba`, `smtech`, `startuppark`) are properly implemented.
- If a module is missing or not correctly imported, the script may not function as expected.

## License
This project is open-source and available under the MIT License.

