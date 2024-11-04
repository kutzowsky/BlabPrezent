#!/usr/bin/env python

import sqlite3
from src.config import settings


_DB_DUMP_FILE = 'db_schema.sql'


def save_user_data(username, address):
    sql_query = "INSERT INTO Addresses VALUES (?, ?)"
    _execute_sql_query(sql_query, (username, address))


def delete_user_data(username):
    sql_query = "DELETE FROM Addresses WHERE user LIKE ?"
    _execute_sql_query(sql_query, (username,))


def get_participants():
    sql_query = "SELECT user FROM Addresses"
    users_tuples = _execute_sql_query(sql_query)
    users_strings = [user_tuple[0] for user_tuple in users_tuples]

    return users_strings


def save_gift_assignment(sender, receiver):
    sql_query = "INSERT INTO Gifts (sender, receiver) VALUES (?, ?)"
    _execute_sql_query(sql_query, (sender, receiver))


def get_gift_assignments():
    sql_query = "SELECT sender, receiver FROM Gifts"
    return _execute_sql_query(sql_query)


def get_address_for(user):
    sql_query = "SELECT address FROM Addresses WHERE user LIKE ?"
    return _execute_sql_query(sql_query, (user,)).fetchone()[0]


def is_participant(user):
    sql_query = "SELECT address FROM Addresses WHERE user LIKE ?"
    return _execute_sql_query(sql_query, (user,)).fetchone() is not None


def save_send_confirmation(user, datetime):
    sql_query = "UPDATE Gifts SET sent=? WHERE sender=?"
    _execute_sql_query(sql_query, (datetime, user))


def save_received_confirmation(user, datetime):
    sql_query = "UPDATE Gifts SET Received=? WHERE Receiver=?"
    _execute_sql_query(sql_query, (datetime, user))


def has_send_confirmation(user):
    sql_query = "SELECT sender from Gifts WHERE sender LIKE ?"
    return _execute_sql_query(sql_query, (user,)).fetchone() is not None


def get_gift_sender_for(user):
    sql_query = "SELECT sender from Gifts WHERE receiver LIKE ?"
    return _execute_sql_query(sql_query, (user,)).fetchone()[0]


def get_gift_receiver_from(user):
    sql_query = "SELECT receiver from Gifts WHERE sender LIKE ?"
    return _execute_sql_query(sql_query, (user,)).fetchone()[0]


def create_db():
    connection = sqlite3.connect(settings.General.database_file)

    with open(_DB_DUMP_FILE, 'r') as sql_file:
        sql_content = sql_file.read()
        with connection:
            cursor = connection.cursor()
            cursor.executescript(sql_content)


def _execute_sql_query(query, args=None):
    connection = sqlite3.connect(settings.General.database_file)

    with connection:
        cursor = connection.cursor()
        if args is None:
            return cursor.execute(query)
        else:
            return cursor.execute(query, args)
