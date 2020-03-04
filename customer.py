#=======================================================================
#============================= Imports==================================
#=======================================================================

import variables as v
import numpy as np

#=======================================================================
#================================= Class ===============================
#=======================================================================

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

    #

    IPM = 0

    number_of_items = 0

    chitchatness = 0

    def __init__(self, IPM, chitchatness):
        ''' Customer initialization method
        Precondition:
        - IPM: Customer's IPM. Used by self checkout
        - number_of_items: Number of items carried by
        customer
        - chitchatness: how chit chatti the customer is
        '''

        self.IPM = IPM
        self.number_of_items = self.number_of_items_per_customer()
        self.chitchatness = chitchatness

    def number_of_items_per_customer(self):
        ''' calculates distribution of of items
        '''
        # -(0 - 15)(uniform) = 40%
        # -(15-30) (uniform)  = 40%
        # -(30-70)(normal->split in the middle) = 15%
        # -(70-200)(log distribution(major between 70-100)) = 15%

        # Number for selection
        random_selector = np.random.rand()
        number_of_items = 0
        if (random_selector < 1):
            number_of_items = int(np.random.rand() * 5)+3
        elif (random_selector < 0.8):
            # for 0 - 30
            number_of_items = int(np.random.rand() * 30)
        elif (random_selector < 0.95):
            # for 30 - 70
            number_of_items = int(np.random.normal(20, 8.9) + 30)
        else:
            # for 70-200
            number_of_items = int(np.random.lognormal(3, 0.63) + 70)
        return number_of_items
