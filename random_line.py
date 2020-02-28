
#=======================================================================
#============================= Imports==================================
#=======================================================================

import variables as v
import numpy as np


from cashier import cashier
from customer import customer

#=======================================================================
#================================= Class ===============================
#=======================================================================

class random_line:
    # List of customers in queue
    # Initialization implemented
    customer_list = 0

    cashier_list = 0

    automated_cashier_tracker = 0

    cost_for_maintenance = 0

    time_step = 0

    number_of_cashiers = 0

    # Total number of customers processed by the line
    # Initialization implemented
    total_number_of_customers = 0

    customers_being_served = 0

    customers_waiting_to_queue = 0

    customers_that_left = 0

    ''' Initializes line
    '''
    def __init__(self, number_of_cashiers, number_of_incoming_customers):
        self.number_of_cashiers = number_of_cashiers
        self.total_number_of_customers = number_of_incoming_customers
        self.create_customer_list()
        
    ''' Create a list of customers
    '''
    def create_customer_list(self):
        # Creates temporary list:
        self.customer_list = []

        # Adds customer as numbers increase
        for i in range(self.total_number_of_customers):

            # Creates customer, and adds them to list:
            self.customer_list.append(
                customer(\
                    np.random.normal(v.CUSTOMER_AVERAGE_IPM,v.CUSTOMER_STD_DEV_IPM),\
                    int(np.random.normal(v.MEAN_NUMBER_OF_ITEMS_PER_CUSTOMER,v.STANDAR_DEVIATION_OF_ITEMS_FOR_CUSTOMER)),\
                    int(np.random.rand()*v.CUSTOMER_CHITCHATNESS))
                                                  )

    ''' Rotates customers through the cashiers
    '''
    def rotate_customers(self):
        print("EXECUTION DONE")