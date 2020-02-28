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
    IPM = 0

    number_of_items = 0

    chitchatness = 0

    def __init__(self, IPM, number_of_items, chitchatness):
        ''' Customer initialization method
        Precondition:
        - IPM: Customer's IPM. Used by self checkout
        - number_of_items: Number of items carried by
        customer
        - chitchatness: how chit chatti the customer is
        '''

        self.IPM = IPM
        self.number_of_items = number_of_items
        self.chitchatness = chitchatness