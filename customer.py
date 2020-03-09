'''
-----------------------------------------------------------------------
                      Additional Documentation

Made by Zachary A Brader, Kieran Coito, Pedro Goncalves Mokarzel
while attending University of Washington Bothell
Made in 03/09/2020
Based on instruction in CSS 458, 
taught by professor Johnny Lin
Notes:
- Written for Python 3.7.3.
- No executable
- Modules necessary: numpy
- External necessities: variables.py
- Used for holding the informations related to the customers
- Internal method used for creation of items

=======================================================================
'''

# =======================================================================
# ============================= Imports==================================
# =======================================================================

import numpy as np
import variables as v

# =======================================================================
# ================================= Class ===============================
# =======================================================================

class customer:
    ''' Saves information related to the customers
    Class keeps information from customer saved

    Note that it does not have any behaviors since we
    are not keeping track of customer behaviors. This
    is a class for helping keep track of information
    '''

    # can have kids

    # age - which can then influence chances to have kids

    # language barrier maybe

    IPM = 0

    number_of_items = 0

    chitchatness = 0

    def __init__(self, IPM, chitchatness,item_creation_lever=0):
        ''' Customer initialization method

        Precondition:
        - IPM: Customer's IPM. Used by self checkout
        - number_of_items: Number of items carried by
        customer
        - chitchatness: how chit chatti the customer is
        - item_creation_lever: Default = 0

        Postcondition:
        - Creation of customer, with information provided, and
        the number of items based on a random variable
        '''

        self.IPM = IPM
        self.number_of_items = self.number_of_items_per_customer(item_creation_lever)
        self.total_items = self.number_of_items
        self.chitchatness = chitchatness
        self.waiting = True
        self.being_helped = False

    def number_of_items_per_customer(self, item_creation_lever):
        ''' calculates distribution of of items for customer

        Precondition:
        - item_creation_lever: float to be added to the probability. This
        makes it so, the larger the probability the number of smaller items
        increases

        Postcondition:
        - Returns a random integer that is the number of items
        that the customer has in their basket
        '''
        # -(0 - 15)(uniform) = 40%
        # -(15-30) (uniform)  = 40%
        # -(30-70)(normal->split in the middle) = 15%
        # -(70-200)(log distribution(major between 70-100)) = 15%

        # Number for selection
        random_selector = np.random.rand()
        random_selector = random_selector % 1
        number_of_items = 0

        if (random_selector < 0.8+item_creation_lever):
            # for 0 - 30
            number_of_items = int(np.random.rand() * 30)

        elif (random_selector < 0.95+item_creation_lever):
            # for 30 - 70
            number_of_items = int(np.random.binomial(100, 0.2) + 30)
        else:
            # for 70-200
            number_of_items = int(np.random.lognormal(3, 0.63) + 70)

        return number_of_items
