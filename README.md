
# ETL Pipeline for Google Books Data

## Overview

This project implements an ETL (Extract, Transform, Load) pipeline using Apache Airflow to automate the process of extracting book data from the Google Books API, transforming it into a CSV file, and then loading it into a SQLite database. The pipeline is orchestrated by Airflow, which schedules and monitors the tasks.

## Project Structure

- **DAG (`ETL_DAG`)**: Defines the workflow for the ETL process, scheduled to run daily.
- **Extract Task**: 
  - Fetches book data related to "learning" from the Google Books API.
  - Transforms the JSON response into a structured CSV format.
  - Saves the data to `books_data.csv`.
- **Load Task**: 
  - Reads the CSV file and inserts the data into a SQLite database (`google_books.db`).
  - Creates a table if it doesn’t already exist, ensuring the data is structured and stored effectively.

## Key Components

- **Apache Airflow**: Used for scheduling and managing the workflow.
- **Google Books API**: Source of the book data, queried using HTTP requests.
- **SQLite**: Lightweight database used to store the extracted data.
- **Python**: Programming language used to implement the logic of the ETL process.

## Files

- **`ETL_DAG.py`**: The main Python script defining the DAG and the tasks for extracting and loading the data.
- **`books_data.csv`**: The CSV file generated during the extraction phase, containing the fetched book data.
- **`google_books.db`**: SQLite database file where the book data is stored after being loaded.

## How It Works

1. **Extract Data**: 
   - The DAG begins with the `extract_data` task.
   - This task sends a request to the Google Books API to fetch data on books with the keyword "learning".
   - The response is parsed, and relevant details such as Title, Authors, Published Date, Description, and Page Count are extracted.
   - This data is saved to a CSV file (`books_data.csv`).

2. **Upload to Database**:
   - The `upload_to_db` task reads the `books_data.csv` file.
   - A SQLite database (`google_books.db`) is created if it doesn’t exist, with a table to store the book data.
   - The task then inserts the extracted data into this database, making it available for future queries and analysis.

3. **Workflow**:
   - The `extract_data` task must complete before the `upload_to_db` task can start, ensuring that data is always available before attempting to load it into the database.

##Prerequisites

- **Python 3.x**
- **Apache Airflow**
- **SQLite** 
- **Google Books API Key**: Replace `YOUR_GOOGLE_API_KEY` in the script with your actual API key.

##Getting Started

1. **Setup Airflow**:
   - Install Airflow using pip: `pip install apache-airflow`
   - Initialize the Airflow database: `airflow db init`
   - Start the Airflow web server: `airflow webserver --port 8080`
   - Start the Airflow scheduler: `airflow scheduler`

2. **Run the Pipeline**:
   - Place the `ETL_DAG.py` file in your Airflow `dags_folder`.
   - Access the Airflow web interface at `http://localhost:8080`.
   - Trigger the DAG manually or let it run on its scheduled interval.

## Conclusion

This project demonstrates a basic yet powerful ETL pipeline using Python and Airflow. It serves as a foundation for more complex data engineering workflows, and can be expanded with additional features as needed. By leveraging the power of Airflow, the pipeline ensures that data is consistently extracted, transformed, and loaded, enabling data-driven insights and decision-making.
