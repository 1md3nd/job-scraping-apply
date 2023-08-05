import mysql.connector

from mysql.connector.errors import DatabaseError


class CheckJob:
    def __init__(self):
        DB_NAME = 'job_applydb'
        try:
            self.connection = mysql.connector.connect(host='localhost', port=3306, user='root', database=DB_NAME)
            self.cursor = self.connection.cursor()
        except DatabaseError:
            print("Can't connect to database make sure its running!!")
            raise DatabaseError

    def find_non_applied_jobs(self,table_name):
        query = f"""SELECT job_link
                FROM {table_name}
                WHERE is_relevant = TRUE AND easy_apply = TRUE AND applied = FALSE AND apply_problem = FALSE;
                """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.connection.commit()
        job_links_list = [row[0] for row in result]
        return job_links_list

    def update_job_applied(self,table_name, job_link, applied_date):
        try:
            # Begin the transaction explicitly
            self.connection.start_transaction()

            # Execute your SQL statements using cursor.execute()
            self.cursor.execute(f"UPDATE {table_name} SET applied = TRUE, applied_date ='{applied_date}' WHERE "
                                f"job_link = '{job_link}';")
            # print('update')
            # Commit the transaction to make the changes permanent in the database
            self.connection.commit()

        except Exception as e:
            # If an error occurs, rollback the transaction to undo any changes made
            self.connection.rollback()
            print("Error:", e)

    def update_job_cant_apply(self,table_name, job_link):
        try:
            # Begin the transaction explicitly
            self.connection.start_transaction()

            # Execute your SQL statements using cursor.execute()
            self.cursor.execute(f"UPDATE {table_name} SET applied = FALSE, apply_problem = TRUE WHERE "
                                f"job_link = '{job_link}';")
            # print('update!')
            # Commit the transaction to make the changes permanent in the database
            self.connection.commit()

        except Exception as e:
            # If an error occurs, rollback the transaction to undo any changes made
            self.connection.rollback()
            print("Error:", e)

    def insert_indeed_job(self, data):
        try:
            insert_query = """
                    INSERT INTO indeed_jobdb (
                        job_link, job_title, company_name, job_type, location,
                        job_description, easy_apply, is_relevant, keywords)
                         VALUES ( %(job_link)s, %(job_title)s, %(company_name)s, %(job_type)s, %(location)s,
                        %(job_description)s,  %(easy_apply)s, %(is_relevant)s, %(keywords)s)
                    """
            # Execute the insert query for each row of data in 'data'
            self.cursor.execute(insert_query, data)
            self.connection.commit()
            print("Data inserted successfully.")
        except mysql.connector.Error as err:
            self.connection.rollback()
            print("Error occurred:", err)
