#! /usr/bin/env python3
# coding: utf-8


class Favorites:
    """A very small class to define what it is, and to be properly used by the Interface"""
    def __init__(self, id, sub_id, original_id):
        self.id = id
        self.sub_id = sub_id
        self.original_id = original_id