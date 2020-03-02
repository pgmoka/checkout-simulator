
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

class equal_distribution_line:
    # List of customers in queue
    # Implemented
    customer_list = 0

    # Array to keep track of automated cashier
    # Implemented
    automated_cashier_tracker = 0

    # Maintain cost of maintecance for all lines
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

    def __init__(self, number_of_cashiers, number_of_incoming_customers, \
        number_of_automated_cashiers, minimum_wage, self_checkout_maintenance_cost):
        ''' Initializes line
        '''
        self.cashier_list = []
        self.number_of_cashiers = number_of_cashiers
        self.total_number_of_customers = number_of_incoming_customers
        self.customers_waiting_to_queue = number_of_incoming_customers
        self.create_customer_list()
        self.minimum_wage = minimum_wage 
        self.self_checkout_maintenance_cost = self_checkout_maintenance_cost

        # Creates boolean array for keeping track of what cashiers 
        # are automated, and what are 'normal'
        self.automated_cashier_tracker= \
            np.concatenate(\
                (np.ones(number_of_automated_cashiers, dtype=bool),np.zeros(number_of_cashiers, dtype=bool)))

        self.create_cashier_list()
        self.update_total_maintenance_cost()
        print("Creation completed")
    

    def create_cashier_list(self):
        ''' creates list of cashiers
        Precondition:
        - Creation of self.automated_cashier_tracker
        - Creation of self.customer_list
        '''
        for i in self.automated_cashier_tracker:
            # Create normal cashier if list demands
            if(not i):
                # Create IPM from normal distribution from global variables
                # Create how chatty from global variables
                self.cashier_list.append\
                    (\
                        cashier\
                        (\
                            np.random.normal(v.CASHIER_AVERAGE_IPM,v.CASHIER_STD_DEV_IPM),\
                            int(np.random.rand()*v.CASHIER_CHITCHATNESS),
                            self.minimum_wage\
                        )\
                    
                    )
            else:
            # else create automated. No info needed
                self.cashier_list.append\
                    (\
                        cashier\
                        (\
                            -1,\
                            0,
                            self.self_checkout_maintenance_cost,
                            self_checkout=True\
                        )\
                    )


    def create_customer_list(self):
        ''' Create a list of customers
        '''
        # Creates temporary list:
        self.customer_list = []

        # Adds customer as numbers increase
        for i in range(self.total_number_of_customers):

            # Creates customer, and adds them to list:
            self.customer_list.append\
                (
                customer(\
                    np.random.normal(v.CUSTOMER_AVERAGE_IPM,v.CUSTOMER_STD_DEV_IPM),\
                    int(np.random.normal(v.MEAN_NUMBER_OF_ITEMS_PER_CUSTOMER,v.STANDAR_DEVIATION_OF_ITEMS_FOR_CUSTOMER)),\
                    int(np.random.rand()*v.CUSTOMER_CHITCHATNESS))
                )

    def rotate_customers(self):
        ''' Create a list of customers
        '''
        for individual_cashier_iterator in range(len(self.cashier_list)):
            if(len(self.customer_list)>0):

                # Updates waiting queue:
                self.customers_waiting_to_queue =  self.customers_waiting_to_queue - 1
                self.cashier_list[individual_cashier_iterator].add_customer_to_queue(self.customer_list.pop())

    def update_customers_out_of_system(self):
        ''' updates number of customers that have left the system
        '''
        self.customers_being_served = 0
        for individual_cashier in self.cashier_list: 
            # total customers in all stores
            self.customers_being_served = self.customers_being_served + individual_cashier.queue_size()
        # makes final math
        self.customers_that_left = self.total_number_of_customers - self.customers_being_served\
            - self.customers_waiting_to_queue

    def apply_checkouts(self):
        ''' Create a list of customers
        '''
        for individual_cashier in self.cashier_list:
            individual_cashier.checkout_current_customer_items()

    def update_total_maintenance_cost(self):
        ''' updates cost for self maintenance of overall system
        '''
        for individual_cashier in self.cashier_list:
            self.cost_for_maintenance = self.cost_for_maintenance +\
                individual_cashier.maintenance_cost