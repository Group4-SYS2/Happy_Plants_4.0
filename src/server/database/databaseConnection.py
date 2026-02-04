import asyncio
from sys import excepthook

from supabase import create_client, Client

import psycopg2
import configparser

def registerUser(email, password):
    conn = connect()
    cursor = conn.cursor()

    query = "INSERT INTO users (email, password, role) VALUES (%s, %s, 'user')"

    try:
        cursor.execute(query, (email, password))

    except Exception as error:
        disconnect(conn)
        return {"status" : "error", "message" : str(error)}


    else:
        if cursor.rowcount != 0:
            disconnect(conn)
            return {"status" : "success"}
        else:
            disconnect(conn)
            return {"status" : "error", "message" : "Error adding user"}

def loginUser(email, password):
    conn = connect()
    cursor = conn.cursor()

    query = "SELECT email, role, user_id FROM users WHERE email = %s AND password = %s"

    cursor.execute(query, (email, password))

    data = cursor.fetchone()

    disconnect(conn)

    if data:
        return {"status": "success", "user_id": data[0], "role": data[1], "userId" : data[2]}
    else:
        return {"status": "error", "message": "Incorrect username or password"}


def connect():
    print("Connecting to PostgreSQL database...")
    try:
        connection = psycopg2.connect(
            user="postgres.fnugbmdbadpadwiqqjii",
            password="happyplantsgrupp4",
            host="aws-1-eu-west-1.pooler.supabase.com",
            port=5432,
            dbname="postgres"
        )

        print("Connection successful!")

    except Exception as e:
        print("Error establishing connection")
        print(e)

    return connection

def disconnect(connection):
    connection.cursor().close()
    connection.close()
    print("Connection closed")
