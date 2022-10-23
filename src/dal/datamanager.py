#!/usr/bin/env python

import sqlite3

_DBNAME = 'blabprezent.db'


def save_user_data(username, address):
    sql_query = "INSERT INTO Addresses VALUES (?, ?)"
    _execute_sql_query(sql_query, (username, address))


def get_participants():
    sql_query = "SELECT user FROM Addresses"
    users_tuples = _execute_sql_query(sql_query)
    users_strings = [user_tuple[0] for user_tuple in users_tuples]

    return users_strings


def save_gift_assignment(gifter, gifted):
    sql_query = "INSERT INTO GiftAssignment VALUES (?, ?)"
    _execute_sql_query(sql_query, (gifter, gifted))


def get_gift_assignments():
    sql_query = "SELECT gifter, gifted FROM GiftAssignment"
    return _execute_sql_query(sql_query)


def get_address_for(user):
    sql_query = "SELECT address FROM Addresses WHERE user LIKE ?"
    return _execute_sql_query(sql_query, (user,)).fetchone()[0]


def save_send_confirmation(user, datetime):  # sqlite3.IntegrityError jak duplikat
    sql_query = "INSERT INTO SentConfirmations VALUES (?, ?)"
    _execute_sql_query(sql_query, (user, datetime))


def save_received_confirmation(user, datetime):
    sql_query = "INSERT INTO ReceivedConfirmations VALUES (?, ?)"
    _execute_sql_query(sql_query, (user, datetime))


def get_gift_sender_for(user):
    sql_query = "SELECT gifter from GiftAssignment where gifted LIKE ?"
    return _execute_sql_query(sql_query, (user,)).fetchone()[0]


def get_gift_receiver_from(user):
    sql_query = "SELECT gifted from GiftAssignment where gifter LIKE ?"
    return _execute_sql_query(sql_query, (user,)).fetchone()[0]


def _execute_sql_query(query, args=None):
    connection = sqlite3.connect(_DBNAME)

    with connection:
        cursor = connection.cursor()
        if args is None:
            return cursor.execute(query)
        else:
            return cursor.execute(query, args)
