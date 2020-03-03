# =======================================================================
# ============================= Imports==================================
# =======================================================================

import variables as v
import numpy as np
import operator

from cashier import cashier
from customer import customer
from equal_distribution_line import equal_distribution_line

# =======================================================================
# ================================= Class ===============================
# =======================================================================

class random_line(equal_distribution_line):
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

    def create_customer_list(self):
        ''' Create a list of customers
        '''
        # Creates temporary list:
        self.customer_list = []

        # Adds customer as numbers increase
        for i in range(self.total_number_of_customers):
            items = self.number_of_items_per_customer()
            # items = int(np.random.normal(v.MEAN_NUMBER_OF_ITEMS_PER_CUSTOMER,v.STANDAR_DEVIATION_OF_ITEMS_FOR_CUSTOMER))
            self.total_number_of_items_in_system = self.total_number_of_items_in_system \
                                                   + items
            # Creates customer, and adds them to list:
            self.customer_list.append \
                    (
                    customer( \
                        np.random.normal(v.CUSTOMER_AVERAGE_IPM, v.CUSTOMER_STD_DEV_IPM), \
                        items, \
                        int(np.random.rand() * v.CUSTOMER_CHITCHATNESS))
                )
