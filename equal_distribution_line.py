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
- Modules necessary: numpy, matplotlib.pyplot
- External necessities: variables.py, customer.py, and cashier.py.
- Creates line environment for the use of mode
- Holds lists with relevant to the line
- Holds cashiers and customers
- Used as a base for other lines
- Line will distribute customers from the cashier equally (one each) 
for each update

=======================================================================
'''

# =======================================================================
# ============================= Imports==================================
# =======================================================================

import numpy as np
import matplotlib.pyplot as plt

import variables as v
from cashier import cashier
from customer import customer


# =======================================================================
# ================================= Class ===============================
# =======================================================================

class equal_distribution_line:
    ''' Environment for the model
    When customers go to cashiers, they distribute themselves evenly 
    between the cashiers
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

    def __init__(self,
                 number_of_cashiers,
                 number_of_incoming_customers,
                 number_of_automated_cashiers,
                 minimum_wage,
                 self_checkout_maintenance_cost,
                 cashier_IPM_p_influence,
                 customer_IPM_p_influence,
                 item_creation_sensitivity_test=0,
                 chitchatness_influence=0):

        ''' Initializes line

        Precondition:
        - number_of_cashiers: int of the number of cashiers to have in the environment
        - number_of_incoming_customers: int of the number of cashier to initiate the line with in the begining of the 
        environment
        - number_of_automated_cashiers: int of the number of automated cashiers to have in the environment
        - minimum_wage: int cost to maintain a cashier
        - self_checkout_maintenance_cost: int cost to maintain an automated-cashier 
        - cashier_IPM_p_influence: float number to add to the p in the binomial generation of the IPM of cashiers
        - customer_IPM_p_influence: float number to add to the p in the binomial generation of the IPM of customers
        - item_creation_sensitivity_test: float number to add to the probability in item creation.
        Increasing this number will make it so the chance of generating smaller basket sizes increases. Default = 0
        - chitchatness_influence: float number to add to the probability in chitchatness creation. Increasing
        this number increases the chance of having higher chitchatness. Default = 0

        Postcondition:
        - Environment created
        - Lists with execution information properly created
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

        self.create_cashier_list(cashier_IPM_p_influence, chitchatness_influence=chitchatness_influence)
        self.update_total_maintenance_cost()

    def create_cashier_list(self,cashier_IPM_p_influence,chitchatness_influence = 0):
        ''' creates list of cashiers

        Precondition:
        - Creation of self.automated_cashier_tracker
        - Creation of self.customer_list
        - cashier_IPM_p_influence: float number to add to the p in the binomial generation of the IPM of cashiers
        - chitchatness_influence: float number to add to the probability in chitchatness creation. Increasing
        this number increases the chance of having higher chitchatness. Default = 0

        Postcondition:
        - list of cashiers created as Precondition dictated
        '''
        for i in self.automated_cashier_tracker:
            # Create normal cashier if list demands
            if (not i):

                self.cashier_list.append(
                    cashier(
                        np.random.binomial(v.CASHIER_n,v.CASHIER_p+cashier_IPM_p_influence),
                        int((np.random.rand() * v.CASHIER_CHITCHATNESS)+chitchatness_influence),
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

        Precondition:
        - customer_IPM_p_influence: float number to add to the p in the binomial generation of the IPM of customers
        - item_creation_sensitivity: float number to add to the probability in item creation.
        Increasing this number will make it so the chance of generating smaller basket sizes increases. Default = 0

        Postcondition:
        - self.customer_list is created
        '''
        # Creates temporary list:
        self.customer_list = []

        # Adds customer as numbers increase
        for i in range(self.total_number_of_customers):
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
        ''' Adds customer to the line system

        Precondition:
        - number_added: int number of customers to be added into the environment
        - item_creation_sensitivity: float number to add to the probability in item creation for customer baskets.
        Increasing this number will make it so the chance of generating smaller basket sizes increases. Default = 0
        '''
        self.total_number_of_customers += number_added
        self.customers_waiting_to_queue += number_added

        # Adds customer as numbers increase
        for i in range(number_added):
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
        ''' Rotate customers between the cashiers' queues from the lines
        Customers aredistributed equally between cashiers, one each, no matter quantities

        Precondition:
        - Customers and cashier related lists created

        Postcondition:
        - Removal of customers in the environment list, and then the addition to queues
        '''
        for individual_cashier_iterator in range(len(self.cashier_list)):
            if (len(self.customer_list) > 0):
                # Updates waiting queue:
                self.customers_waiting_to_queue = self.customers_waiting_to_queue - 1
                self.cashier_list[individual_cashier_iterator].add_customer_to_queue(self.customer_list.pop())

    def update_customers_out_of_system(self):
        ''' updates number of customers that have left the system

        Precondition:
        - Initialization of related variables created

        Postcondition:
        - Updates inner tracking variables
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
        
        Precondition:
        - self.total_number_of_checked_items has been created

        Postcondition:
        - Update of self.total_number_of_checked_items
        '''
        total_now = 0
        for individual_cashier in self.cashier_list:
            total_now = total_now \
                        + individual_cashier.total_items_checked
        self.total_number_of_checked_items = total_now

    def apply_checkouts(self):
        ''' Applies the checkout process of each checkouts

        Prcondition:
        - self.cashier_list has been created

        Postcondition:
        - All cashiers in the self.cashier_list have executed
        the checkout 
        '''
        for individual_cashier in self.cashier_list:
            individual_cashier.checkout_current_customer_items()

    def update_total_maintenance_cost(self):
        ''' updates cost for self maintenance of overall system

        Precondition:
        - self.cost_for_maintenance has been created

        Postcondition:
        - maintenance cost of the system is updated based on the current
        queue
        '''
        for individual_cashier in self.cashier_list:
            self.cost_for_maintenance = self.cost_for_maintenance + \
                                        individual_cashier.maintenance_cost

