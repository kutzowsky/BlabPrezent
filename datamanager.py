#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3


def save_user_data(username, address):
    connection = sqlite3.connect('blabprezent.db')

    with connection:
        cursor = connection.cursor()
        sql_query = "INSERT INTO Addresses VALUES (?, ?)"
        cursor.execute(sql_query, (username, address))
