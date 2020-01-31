#! /usr/bin/env python3
# coding: utf-8
'''Manage the database in every ways, connexion, creation, insertion, error issues'''

import mysql.connector as con

from Models.APIRequest import APIRequest
from Settings.constants import *


class Database:
    '''Manage all the primary aspects regarding the database as connexion, error issues, data selection'''
    def __init__(self, api):
        self.db_name = 'purbeurre'
        self.filename = FILENAME
        self.api = api
        self.connexion = False # No connexion yet
        self.curs = False

    def database_connexion(self):
        '''Use mysql.connector to allow access to the chosen database'''
        self.connexion = con.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
        self.curs = self.connexion.cursor()

    def database_selection(self):
        '''To aim the database we want to use'''
        self.connexion.database = self.db_name

    def database_creation(self):
        '''Create a database in the user's system using instructions in an init MySQL file'''
        try:
            with open(self.filename, 'r') as cmd_file:
                sql_commands = cmd_file.read()
                sql_commands = sql_commands.split(';') # Split the file in a list by using ';' as a separator for each SQL command
            for command in sql_commands:
                self.curs.execute(command)
        except FileNotFoundError:
            print("Couldn't open commands file \"" + self.filename + "\"")

    def database_check_in(self):
        '''Check if the database already exists'''
        query = 'SELECT * FROM Categories LIMIT 1'
        self.curs.execute(query)
        return self.curs.fetchone()

    def categories_recording(self, category):
        '''Fill the categories with every chosen name'''
        self.curs.execute(""" INSERT INTO Categories (name)
                               VALUES ("{}"); """
                       .format(category))
        self.connexion.commit()

    def cat(self):
        for category in API_CATEGORIES:
            self.categories_recording(category)

    def cat_id(self):
        self.curs.execute('SELECT id FROM categories')
        self.cat_id = self.curs.fetchall()
        print(self.cat_id)
        return self.cat_id

    def products_recording(self, api):
        '''Fill the products table with every sorted element'''
        categories = api.categories
        products = api.products_list
        for x, data in zip(categories, products):
            # print(product[0])
            # exit(0)
            self.curs.execute(""" INSERT IGNORE INTO Categories (name)
                               VALUES ({0})""".format("\'"+x+"\'"))
            self.connexion.commit()
            # self.curs.execute('INSERT IGNORE INTO Products (name, description, category_id, store, nova_groups, barcode, url)\
            #             VALUES (%(product_name)s, %(generic_name_fr)s, (SELECT id FROM Categories WHERE name = %(jus de fruits)s) \
            #                      %(stores)s, %(nova_groups)s, %(code)s, %(url)s)', product)
        self.connexion.commit()

    def save_favorites(self):
        '''Allow the user to save his query into the database'''
        # self.favorites_insert = DB_FAVORITES_INSERT
        # self.fav_data =

    def database_closing(self):
        '''Closing the database'''
        self.curs.close()
        self.connexion.close()

    def select_products(self):
        '''Pick the product using its category and then its name'''
        pass

    def select_substitutes(self):
        '''Pick a bunch of products with higher nutritive grade'''
        pass

    def select_favorites(self):
        '''Pick all the user's favorites'''
        pass 
