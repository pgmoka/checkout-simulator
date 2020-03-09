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
- Modules necessary: numpy, random, and matplotlib.pyplot
- External necessities: variables.py, cashier.py, customer.py, and
equal_distribution_line
- Creates line environment for the use of mode
- Holds lists with relevant to the line
- Holds cashiers and customers
- Used equal_distribution_line as a base for other lines
- Line will give a customer to cashier that looks like it will go the
fastest

=======================================================================
'''

# =======================================================================
# ============================= Imports==================================
# =======================================================================

import numpy as np
import random as r
import matplotlib.pyplot as plt

import variables as v
from cashier import cashier
from customer import customer
from equal_distribution_line import equal_distribution_line

# =======================================================================
# ================================= Class ===============================
# =======================================================================

class customer_selection_line(equal_distribution_line):
    '''
    Inherits equal_distribution_line
    Line acts such that customer chooses the best line
    '''
    # List of customers in queue
    # Implemented
    customer_list = 0

    # Array to keep track of automated cashier
    # Implemented
    automated_cashier_tracker = 0

    # Maintain cost of maintenance for all lines
    # Implemented
    cost_for_maintenance = 0

    # Not implemented
    time_step = 0

    # Number of cashiers in system
    # implemented
    number_of_cashiers = 0

    # Total number of customers processed by the line
    # Initialization implemented
    total_number_of_customers = 0

    # Customers currently being served
    # implemented
    customers_being_served = 0

    # Total number of customers current line
    # Implemented
    customers_waiting_to_queue = 0

    # Customers that have left the system at point of simulation
    # Implemented
    customers_that_left = 0

    # Implementation
    total_number_of_checked_items = 0

    total_number_of_items_in_system = 0

    def rotate_customers(self):
        ''' Rotate customers between the cashiers' queues from the lines
        Customers go to the queue that they consider will go fast

        Precondition:
        - Customers and cashier related lists created

        Postcondition:
        - Removal of customers in the environment list, and then the addition to queues
        '''
        # number_of_customers_entering_queue = int(np.random.rand()*(self.number_of_cashiers-1)) +1
        # test = []
        # for i in range(1000):
        #     test.append(int(rej()*self.number_of_cashiers))
        # plt.hist(test)
        # plt.show()
        for individual_cashier_iterator in range(len(self.cashier_list)):
            if (len(self.customer_list) > 0):
                # Updates waiting queue:

                smallest_cashier = self.cashier_list[0]
                
                for cashier_iterator in self.cashier_list:
                    if(smallest_cashier > cashier_iterator):
                        smallest_cashier = cashier_iterator

                smallest_cashier.add_customer_to_queue(self.customer_list.pop())
                self.customers_waiting_to_queue = self.customers_waiting_to_queue - 1
                # self.cashier_list.sort()
