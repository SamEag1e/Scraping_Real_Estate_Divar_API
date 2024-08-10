# Scraping_Real_Estate_Divar_API
## Description
This project scrapes real estate ads from Divar’s API, focusing on large cities in Iran. By leveraging Divar’s backend API and some unique techniques, this tool retrieves comprehensive information about various real estate categories.

## Features
* **Categories**: Apartment, Villa, Land
* **Cities**: All 9 large cities of Iran
* **Data Retrieved**:
  * Title
  * Description
  * City
  * District
  * Price
  * Price per square meter
  * Details of the real estate property
  * Phone number of the ad maker
  * And more…
* **Error Handling**: General exception handling ensures the program continues running even with bad or unsuitable data, marking such data with a -404 value.
* **Model Module**: A tiny ORM to insert or read data to/from the database.
## Installation
1. Clone the repository:
```
git clone https://github.com/SamEag1e/Scraping_Real_Estate_Divar_API.git
```
2. Navigate to the project directory:
```
cd Scraping_Real_Estate_Divar_API
```
3. Install the required dependencies:
```
pip install -r requirements.txt
```
## Database Setup
Before running the scraper, you need to create the database and tables. Follow these steps:

1. Create the Database:
   Create a database named real_estate in MySQL. If you want to use other database management systems, you need to modify the model.py file accordingly.
3. Create Tables:
    Create tables based on the 0_RealEstate_Table_Structures_MySQL_Dump.sql file.
## Environment Variables
* Create a .env file in the project root directory.
* To get access to the necessary environment variables, please contact me directly.

## Usage
Run the scraper using:
```
python main.py
```
## Contributing
* Fork the repository.
* Create a new branch (git checkout -b feature-branch).
* Commit your changes (git commit -m 'Add new feature').
* Push to the branch (git push origin feature-branch).
* Open a pull request.
## Contact
For access to environment variables or any other inquiries, please contact me at:

* **Email**: samadeagle@yahoo.com
* **Telegram**: https://t.me/SamadTnd
## License
This project is licensed under the MIT License.
