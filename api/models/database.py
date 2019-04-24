import psycopg2
from psycopg2 import extras
from pprint import pprint
import os
from datetime import datetime

class DatabaseConnect:
    """class that establishes database connection, creates various tables and drops the tables """

    def __init__(self):

        # if os.getenv('DB_NAME') == "testdb":
        #     self.dbname = "testdb"
        #     self.user = "postgres"
        #     self.password = "David..2"
        #     self.host = "127.0.0.1"
        # # elif os.getenv('DB_NAME') == "proddb":
        # #     self.dbname = "ddo76jqcvdgpp6"
        # #     self.user = "iahxwhjlgkymau"
        # #     self.password = "86ca7ea32a682d6e997410bd6ce1093093a51f2b3ba4ba9c9bb5a2efb0598e41"
        # #     self.host = "ec2-54-221-253-228.compute-1.amazonaws.com"
        # else:
        self.dbname = "ireporter"
        self.user = "postgres"
        self.password = "David..2"
        self.host = "127.0.0.1"
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                host= self.host,
                password=self.password, 
                port=5432
            )
            self.connection.autocommit = True
            self.cur = self.connection.cursor(
                cursor_factory = psycopg2.extras.RealDictCursor)

            print('Connected to the database successfully')
            self.create_tables()

        except(Exception, psycopg2.DatabaseError) as error:
            print(error)

    def create_tables(self):
        """function that creates tables in the database"""
        user_table = """CREATE TABLE IF NOT EXISTS users(
            id serial PRIMARY KEY NOT NULL,
            user_id VARCHAR(100) NOT NULL,
            user_name VARCHAR(100) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL,
            first_name VARCHAR(100)  NOT NULL,
            last_name VARCHAR(100)  NOT NULL,
            other_names VARCHAR(100)  NOT NULL,
            phone_number VARCHAR(15)  NOT NULL, 
            registered_on VARCHAR(100) NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE) 
            """

        incidents_table = """
            CREATE TABLE IF NOT EXISTS incidents(
            incident_id serial PRIMARY KEY,
            incident_type VARCHAR (20),
            title VARCHAR(20),
            description VARCHAR(100),
            location varchar(32) NOT NULL,
            status VARCHAR(100) DEFAULT'draft',
            images VARCHAR(100),
            videos VARCHAR(100),
            comment VARCHAR(100),
            created_on VARCHAR(100),
            created_by VARCHAR(100),
            FOREIGN KEY (created_by) REFERENCES users(userId)
            )
            """
            
        self.cur.execute(user_table)
        self.cur.execute(incidents_table)
        print("tables created successfully")

    def drop_tables(self):
        # """function that drops the tables"""

        query = "DROP TABLE IF EXISTS users, incidents"
        self.cur.execute(query)
        return print('tables dropped successfully')
    

    def create_incident(self, incident_type, location, status,title, images, videos, created_by, comment, created_on):
        create_incident = "INSERT INTO incidents(incident_type, location, status,title, images, videos, created_by, comment, created_on) VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
            incident_type, location, status,title, images, videos, created_by, comment, created_on)
        self.cur.execute(create_incident)
        incident_id = self.cur.fetchone()
        if incident_id:
            return dict(incident_id)['incident_id']

