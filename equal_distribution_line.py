# =======================================================================
# ============================= Imports==================================
# =======================================================================

import variables as v
import numpy as np
import matplotlib.pyplot as plt

from cashier import cashier
from customer import customer


# =======================================================================
# ================================= Class ===============================
# =======================================================================

class equal_distribution_line:
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

    def __init__(self,
                 number_of_cashiers,
                 number_of_incoming_customers,
                 number_of_automated_cashiers,
                 minimum_wage,
                 self_checkout_maintenance_cost,
                 cashier_IPM_p_influence,
                 customer_IPM_p_influence,
                 item_creation_sensitivity_test=0):

        ''' Initializes line
        '''
        self.cashier_list = []
        self.number_of_cashiers = number_of_cashiers
        self.total_number_of_customers = number_of_incoming_customers
        self.customers_waiting_to_queue = number_of_incoming_customers
        self.create_customer_list(customer_IPM_p_influence, item_creation_sensitivity=item_creation_sensitivity_test)
        self.minimum_wage = minimum_wage
        self.self_checkout_maintenance_cost = self_checkout_maintenance_cost

        # Creates boolean array for keeping track of what cashiers 
        # are automated, and what are 'normal'
        self.automated_cashier_tracker = \
            np.concatenate( \
                (np.ones(number_of_automated_cashiers, dtype=bool), np.zeros(number_of_cashiers, dtype=bool)))

        self.create_cashier_list(cashier_IPM_p_influence)
        self.update_total_maintenance_cost()

    def create_cashier_list(self,cashier_IPM_p_influence):
        ''' creates list of cashiers
        Precondition:
        - Creation of self.automated_cashier_tracker
        - Creation of self.customer_list
        '''
        for i in self.automated_cashier_tracker:
            # Create normal cashier if list demands
            if (not i):
                # Create IPM from normal distribution from global variables
                # Create how chatty from global variables

                # Transformations for binomial distribution:
                # p = 1 - ((v.CASHIER_STD_DEV_IPM**2)/v.CASHIER_AVERAGE_IPM)
                # n = v.CASHIER_AVERAGE_IPM/p

                self.cashier_list.append(
                    cashier(
                        np.random.binomial(v.CASHIER_n,v.CASHIER_p+cashier_IPM_p_influence),
                        int(np.random.rand() * v.CASHIER_CHITCHATNESS),
                        self.minimum_wage
                    )
                )
            else:
                # else create automated. No info needed
                self.cashier_list.append(
                    cashier(
                        -1,
                        0,
                        self.self_checkout_maintenance_cost,
                        self_checkout=True
                    )
                )

    def create_customer_list(self, customer_IPM_p_influence, item_creation_sensitivity=0):
        ''' Create a list of customers
        '''
        # Creates temporary list:
        self.customer_list = []

        # Adds customer as numbers increase
        for i in range(self.total_number_of_customers):
            # items = self.number_of_items_per_customer()
            # # items = int(np.random.normal(v.MEAN_NUMBER_OF_ITEMS_PER_CUSTOMER,v.STANDAR_DEVIATION_OF_ITEMS_FOR_CUSTOMER))
            # self.total_number_of_items_in_system = self.total_number_of_items_in_system \
            #                                        + items
            # Creates customer, and adds them to list:
            self.customer_list.append \
                    (
                    customer( \
                        np.random.binomial(v.CUSTOMER_n, v.CUSTOMER_p+customer_IPM_p_influence), \
                        int(np.random.rand() * v.CUSTOMER_CHITCHATNESS),\
                        item_creation_lever=item_creation_sensitivity)
                )

            self.total_number_of_items_in_system = self.total_number_of_items_in_system \
                                                   + self.customer_list[-1].number_of_items

    def add_customers(self, number_added,item_creation_sensitivity=0):
        '''
        '''
        self.total_number_of_customers += number_added
        self.customers_waiting_to_queue += number_added

        # Adds customer as numbers increase
        for i in range(number_added):
            # items = self.number_of_items_per_customer()
            # # items = int(np.random.normal(v.MEAN_NUMBER_OF_ITEMS_PER_CUSTOMER,v.STANDAR_DEVIATION_OF_ITEMS_FOR_CUSTOMER))
            # self.total_number_of_items_in_system = self.total_number_of_items_in_system \
            #                                        + items
            # Creates customer, and adds them to list:
            self.customer_list.append(
                    customer(\
                        np.random.binomial(v.CUSTOMER_n, v.CUSTOMER_p), \
                        int(np.random.rand() * v.CUSTOMER_CHITCHATNESS), \
                        item_creation_lever=item_creation_sensitivity)
                        )

            self.total_number_of_items_in_system = self.total_number_of_items_in_system \
                                                   + self.customer_list[-1].number_of_items


    def rotate_customers(self):
        ''' Create a list of customers
        '''
        for individual_cashier_iterator in range(len(self.cashier_list)):
            if (len(self.customer_list) > 0):
                # Updates waiting queue:
                self.customers_waiting_to_queue = self.customers_waiting_to_queue - 1
                self.cashier_list[individual_cashier_iterator].add_customer_to_queue(self.customer_list.pop())

    def update_customers_out_of_system(self):
        ''' updates number of customers that have left the system
        '''
        self.customers_being_served = 0
        for individual_cashier in self.cashier_list:
            # total customers in all stores
            self.customers_being_served = self.customers_being_served + individual_cashier.queue_size()
        # makes final math
        self.customers_that_left = self.total_number_of_customers - \
            self.customers_being_served - self.customers_waiting_to_queue

    def update_checkedout_items(self):
        '''Updates total number of checked out items in the system
        '''
        total_now = 0
        for individual_cashier in self.cashier_list:
            total_now = total_now \
                        + individual_cashier.total_items_checked
        self.total_number_of_checked_items = total_now

    def apply_checkouts(self):
        ''' Create a list of customers
        '''
        for individual_cashier in self.cashier_list:
            individual_cashier.checkout_current_customer_items()

    def update_total_maintenance_cost(self):
        ''' updates cost for self maintenance of overall system
        '''
        for individual_cashier in self.cashier_list:
            self.cost_for_maintenance = self.cost_for_maintenance + \
                                        individual_cashier.maintenance_cost

    def number_of_items_per_customer(self):
        ''' calculates distribution of of items
        '''
        # -(0 - 15)(uniform) = 30% 
        # -(15-30) (uniform)  = 30% 
        # -(30-70)(normal->split in the middle) = 25% 
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
