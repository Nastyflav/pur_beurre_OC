#! /usr/bin/env python3
# coding: utf-8
'''Manage the database in every ways, connexion, creation, insertion, error issues'''

import mysql.connector as con

from Models.APIRequest import APIRequest
from Models.Interface import Interface
from Settings.constants import *


class Database:
    '''Manage all the primary aspects regarding the database as connexion, error issues, data selection'''
    def __init__(self, api):
        self.db_name = 'purbeurre'
        self.filename = FILENAME
        self.api = api
        self.orm = Interface()
        self.connexion = False # No connexion yet
        self.curs = False

    def database_connexion(self):
        '''Use mysql.connector to allow access to the chosen database'''
        self.connexion = con.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
        self.curs = self.connexion.cursor()

    def database_selection(self):
        '''To aim the database we want to use'''
        try :
            self.connexion.database = self.db_name
        except con.Error :
            return False

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

    def database_closing(self):
        '''Closing the database'''
        self.curs.close()
        self.connexion.close()

    def products_recording(self, api):
        '''Fill the products and the categories tables with every sorted element from the API request'''
        categories = api.categories
        products = api.products_list
        for x, data in zip(categories, products):
            self.curs.executemany(DB_CATEGORIES_INSERT, [(x,) for x in categories])
            self.connexion.commit()

            for product in data['products']:
                try :
                    name = product['product_name']
                    descr = product['generic_name_fr']
                    store = product['stores']
                    nova = product['nova_groups']
                    code = product['code']
                    link = product['url']
                    self.curs.executemany(DB_PRODUCTS_INSERT, [(name, descr, x, store, nova, code, link) for product in data])
                except KeyError :
                    print()
            self.connexion.commit()

    def select_categories(self):
        '''Select all the existing categories in the database'''
        self.curs.execute(DB_CATEGORIES_SELECTION)
        self.selected_cat = self.curs.fetchall()
        self.selected_cat = self.orm.get_categories(self.selected_cat)
        return self.selected_cat

    def select_products(self, selected_category):
        '''Pick the product by using its category and then its grade'''
        self.curs.execute(DB_PRODUCTS_SELECTION.format(selected_category))
        self.selected_products = self.curs.fetchall()
        self.selected_products = self.orm.get_products(self.selected_products)
        return self.selected_products

    def select_substitutes(self, selected_category, selected_product):
        '''Pick a bunch of products with higher nutritional grade'''
        self.curs.execute(DB_SUBS_SELECTION.format(selected_category, selected_product))
        self.total_data = self.curs.fetchall()
        self.total_data = self.orm.get_substitutes(self.total_data)
        self.original_prod = self.total_data[0]
        self.substitute = self.total_data[1]
        return self.original_prod, self.substitute

    def show_substitute(self, selected_sub):
        '''Extract from the database all the datas for one selected substitute'''
        self.curs.execute(DB_SUB_DETAILS.format(selected_sub))
        self.selected_substitute = self.curs.fetchall()
        self.selected_substitute = self.orm.show_sub_details(self.selected_substitute)
        return self.selected_substitute

    def save_favorites(self, substitute_id, original_id):
        '''Allow the user to save his query into the database'''
        self.curs.execute(DB_FAVORITES_INSERT,(substitute_id, original_id))
        self.connexion.commit()

    def select_favorites(self):
        '''Pick all the user's favorites'''
        self.curs.execute(DB_FAVORITES_SELECTION)
        self.selected_favs = self.curs.fetchall()
        self.curs.execute(DB_ORIGINAL_PRODUCTS_SELECTION)
        self.selected_original = self.curs.fetchall()
        self.total_favorites = self.orm.get_favorites(self.selected_favs, self.selected_original)
        self.id = self.total_favorites[0]
        self.favorite = self.total_favorites[1]
        self.original = self.total_favorites[2]
        return self.id, self.favorite, self.original

    def show_favorite(self, selected_fav):
        '''Extract from the database all the datas for one selected substitute'''
        self.curs.execute(DB_FAV_DETAILS.format(selected_fav))
        self.selected_favorite = self.curs.fetchall()
        self.selected_favorite = self.orm.show_sub_details(self.selected_favorite)
        return self.selected_favorite
