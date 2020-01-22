#! /usr/bin/env python3
# coding: utf-8
'''We import requests to load all the targeted datas from the OFF API\
and mysql.connector to fill the database'''
import requests as rq
import mysql.connector as con

from Models.Database import Database
from Settings.constants import API_PAGE_SIZE, API_PAGES_NUMBER, API_CATEGORIES, API_URL_SOURCE, \
                                DB_PRODUCTS_INSERT, DB_CATEGORIES_INSERT


class APIRequest:
    '''Class to load a data list from the OFF API products into the database'''
    def __init__(self, database):
        '''Define the category products we want'''
        self.categories = API_CATEGORIES
        self.products_list = []
        self.db = Database()