import mysql.connector
from mysql.connector import errorcode
import sqlite3


class InsertJob:
    def __init__(self):
        DB_NAME = 'job_applydb'
        self.connection = mysql.connector.connect(host='localhost', port=3306, user='root', database=DB_NAME)
        self.cursor = self.connection.cursor()

    def insert(self,data):
        """
        Inserts data into the 'tbl_joblist' table of the 'job_applydb' database.

        Parameters:
            data (list of dictionaries): A list of dictionaries where each dictionary represents a row of data to be inserted.

        Returns:
            None

        Raises:
            mysql.connector.Error: If there is an error while connecting to the MySQL database or executing the query.

        Notes:
            - The 'job_applydb' database must be created beforehand in the MySQL server.
            - The 'tbl_joblist' table must exist in the 'job_applydb' database with matching column names as the data to be inserted.
            - The 'data' parameter should be a list of dictionaries, where each dictionary contains key-value pairs representing the column names and their corresponding values for a single row of data.

        Example:
            data = [
                {
                    'job_link': 'https://example.com/job/1',
                    'job_title': 'Software Engineer',
                    'company_name': 'ABC Corp',
                    'job_type': 'Full-time',
                    'location': 'New York',
                    'job_description': 'Lorem ipsum...',
                    'posted_by_name': 'John Doe',
                    'posted_by_designation': 'HR Manager',
                    'posting_time': '2023-07-22 12:00:00',
                    'is_relevant': True,
                    'easy_apply': False,
                },
                # Add more rows of data as dictionaries...
            ]

            insert_data_into_table(data)
        """

        try:
            # Establish a connection to the MySQL server and select the 'job_applydb' database
            # print(cursor)
            # SQL query to insert data into the 'tbl_joblist' table

            self.connection.start_transaction()
            insert_query = """
            INSERT INTO tbl_joblist (
                job_link, job_title, company_name, job_type, location,
                job_description, posted_by_name, posted_by_designation,poster_url, posting_time,keywords,
                is_relevant, easy_apply)
                 VALUES ( %(job_link)s, %(job_title)s, %(company_name)s, %(job_type)s, %(location)s,
                %(job_description)s, %(posted_by_name)s, %(posted_by_designation)s,%(poster_url)s, %(posting_time)s,
                %(keywords)s, %(is_relevant)s, %(easy_apply)s)
            """

            # Execute the insert query for each row of data in 'data'
            self.cursor.execute(insert_query, data)
            self.connection.commit()
            print("Data inserted successfully.")
        except mysql.connector.Error as err:
            self.connection.rollback()
            print("Error occurred:", err)

    def close(self,):
        # Close the cursor and the connection to the MySQL server
        self.cursor.close()
        self.connection.close()
    # insert_data_into_table([0])
