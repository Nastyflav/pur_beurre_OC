#! /usr/bin/env python3
# coding: utf-8


class KeyboardController:
    '''Deals with every user / terminal interactions, only by pressing keys on keyboard'''
    def __init__(self):
        pass

    def binary_choice(self):
        '''When the user have to chose between two entries'''
        print()
        user_answer = input('Validez votre choix avec Entrée : ')
        if user_answer not in ['1', '2']:
            print('Cette option n\'existe pas, veuillez choisir entre les numéros proposés')
            user_answer = self.binary_choice()
        return int(user_answer)

    def cat_choice(self, cat_nb):
        '''When the user choses a category to explore'''
        print()
        user_answer = input('Validez votre choix avec Entrée : ')
        try :
            if int(user_answer) not in cat_nb:
                print('Cette catégorie n\'existe pas, veuillez choisir entre les numéros proposés')
                user_answer = self.cat_choice(cat_nb)
            return int(user_answer)
        except ValueError: #in case of the user only presses Enter
            print('Cette option n\'existe pas, veuillez choisir entre les numéros proposés')
            user_answer = self.cat_choice(cat_nb)
            return int(user_answer)

    def prod_choice(self, prod_nb):
        '''When the user choses a product to substitute'''
        print()
        user_answer = input('Validez votre choix avec Entrée : ')
        try:
            if int(user_answer) not in prod_nb:
                print('Ce produit n\'est pas disponible, veuillez choisir entre les numéros proposés')
                user_answer = self.prod_choice(prod_nb)
            return int(user_answer)
        except ValueError:
            print('Cette option n\'existe pas, veuillez choisir entre les numéros proposés')
            user_answer = self.prod_choice(prod_nb)
            return int(user_answer)

    def sub_choice(self, prod_nb):
        '''When the user choses a substitute among a list of proposals'''
        print()
        user_answer = input('Consultez les détails du produit en entrant son numéro suivi de Entrée : ')
        try :
            if int(user_answer) not in prod_nb:
                print('Ce produit n\'est pas disponible, veuillez choisir entre les numéros proposés')
                user_answer = self.sub_choice(prod_nb)
            return int(user_answer)
        except ValueError:
            print('Cette option n\'existe pas, veuillez choisir entre les numéros proposés')
            user_answer = self.prod_choice(prod_nb)
            return int(user_answer)

    def fav_choice(self, fav_nb):
        '''When the user choses a favorite among a list of proposals'''
        print()
        user_answer = input('Consultez les détails du produit de votre choix en tapant son numéro ou tapez O pour retourner à l\'accueil : ')
        if int(user_answer) == 0:
            return int(user_answer)
        else :
            try:
                if int(user_answer) not in fav_nb:
                    print('Ce produit n\'est pas sauvegardé, veuillez choisir entre les numéros proposés')
                    user_answer = self.fav_choice(fav_nb)
                return int(user_answer)
            except ValueError:
                print('Cette option n\'existe pas, veuillez choisir entre les numéros proposés')
                user_answer = self.fav_choice(fav_nb)
                return int(user_answer)
