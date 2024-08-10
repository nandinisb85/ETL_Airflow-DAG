import requests
import json
import csv
import pandas as pd
from datetime import timedelta
from airflow import DAG
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
import sqlite3

default_args = {
'owner': 'Nandini Bhusanurmath',
'start_date': datetime(2021, 1, 1),
'email': ['nandini@gmail.com'],
'email_on_failure': False,
'email_on_retry': False,
'retries': 1,
'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id="ETL_DAG",
    default_args=default_args,
    description="Extract and Upload Data",
    schedule_interval=timedelta(days=1),
)

def extract_data():
    url = 'https://www.googleapis.com/books/v1/volumes?q=learning+intitle:keyes&key=YOUR_GOOGLE_API_KEY'
    response = requests.get(url)
    data = response.json()
    books = []
    for item in data.get('items', []):
        book = {
        'Title': item['volumeInfo'].get('title', 'N/A'),
        'Authors': item['volumeInfo'].get('authors', ['N/A']),
        'Published Date': item['volumeInfo'].get('publishedDate', 'N/A'),
        'Description': item['volumeInfo'].get('description', 'N/A'),
        'Page Count': item['volumeInfo'].get('pageCount', 'N/A')
        }
        books.append(book)
        csv_filename = 'books_data.csv'
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['Title', 'Authors', 'Published Date', 'Description', 'Page Count'])
            writer.writeheader()
            writer.writerows(books)

extract_data = PythonOperator(
    task_id="extract_data", python_callable=extract_data, dag=dag
)


def upload_to_db():
    conn = sqlite3.connect('google_books.db')
    cursor = conn.cursor()
    create_table = '''CREATE TABLE books(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                authors TEXT,
                published_date TEXT,
                description TEXT,
                page_count INTEGER);
                '''
    cursor.execute(create_table)
    file = open('books_data.csv')
    contents = csv.reader(file)
    insert_records = """
       INSERT INTO books (title, authors, published_date, description, page_count)
       VALUES (?, ?, ?, ?, ?)
    """
    cursor.executemany(insert_records, contents)

    conn.commit()
    conn.close()


upload_to_db = PythonOperator(
    task_id="upload_to_db", python_callable=upload_to_db, dag=dag
)

(
    extract_data
    >> upload_to_db
)
