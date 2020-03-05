# =======================================================================
# ============================= Imports==================================
# =======================================================================

import variables as v
import numpy as np
import random as r
import matplotlib.pyplot as plt

from cashier import cashier
from customer import customer
from equal_distribution_line import equal_distribution_line

# =======================================================================
# ================================= Class ===============================
# =======================================================================

class selector_line(equal_distribution_line):
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
        ''' Create a list of customers
        '''
        # Goes through customers:
        for individual_cashier_iterator in range(len(self.cashier_list)):

            # Check if there is a customer in the list
            if (len(self.customer_list) > 0):

                # checks if line is empty
                if(self.cashier_list[individual_cashier_iterator].queue_size()==0):

                    if(self.cashier_list[individual_cashier_iterator].forgetful()):
                        # Updates waiting queue:
                        self.customers_waiting_to_queue = self.customers_waiting_to_queue - 1
                        self.cashier_list[individual_cashier_iterator].add_customer_to_queue(self.customer_list.pop())
    