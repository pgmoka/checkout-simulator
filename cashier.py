#=======================================================================
#============================= Imports==================================
#=======================================================================

import variables as v
import numpy as np

# Module for testing:
from customer import customer

#=======================================================================
#================================= Class ===============================
#=======================================================================

class cashier:
    # Cost to maintain cashier
    # Not implemented
    maintenance_cost = 0

    # Cashier's IPM
    # Implemented
    IPM = 0

    # Not implemented
    additional_chatter = 0

    # Totals items checked by the cashier at the point
    # Implemented
    total_items_checked = 0

    # Checks if cashier is a self-checkout or not
    # Implemented
    self_checkout = False

    total_number_of_items_in_systems = 0
    #forgetfullness 

    def __init__(self, IPM, chitchatter, maintenance_cost, self_checkout=False):
        """ Initiates cashier
        """
        self.complete_queue = []
        self.cashier_queue = []
        self.IPM = IPM
        self.additional_chatter = chitchatter
        self.self_checkout = self_checkout
        self.maintenance_cost = maintenance_cost

    def add_customer_to_queue(self, customer):
        """ adds a customer to this cashier's queue
        """
        self.total_number_of_items_in_systems = \
            self.total_number_of_items_in_systems + customer.number_of_items
        self.cashier_queue.insert(0, customer)
        self.complete_queue.append(customer)

    def line_empty(self):
        ''' Checks if line is tempty
        '''
        return len(self.cashier_queue) <= 0

    def checkout_current_customer_items(self):
        ''' Checkout items from customer being checkout
        '''
        # Checks if line is empty
        if (not self.line_empty()):
            # Calculate subtraction factor
            if (self.self_checkout):
                subtract_me = self.cashier_queue[-1].IPM/v.TIME_STEP
            else:
                # Calculate time subtraction
                subtract_me = self.IPM/v.TIME_STEP

            # adds min between IPM, and what the customer has in total
            self.cashier_queue[-1].number_of_items = self.cashier_queue[-1].number_of_items -\
                min(self.cashier_queue[-1].number_of_items, subtract_me)

            # Adds to total items checked
            self.total_items_checked = self.total_items_checked + \
                min(self.cashier_queue[-1].number_of_items, subtract_me)
            # if there are no items, customer leaves
            if (self.cashier_queue[-1].number_of_items == 0):
                self.cashier_queue.pop()
                
    def queue_size(self):
        ''' returns size of the queue
        '''
        return len(self.cashier_queue)

    def __lt__(self, other):
        # sort for smallest to largest
        return self.queue_size() < other.queue_size() 

if __name__ == "__main__":
    ''' Cashier testing site
    '''
    test_cashier = cashier(45, 3, 9)
    test_cashier2 = cashier(42, 3, 9)

    test_customer = customer(2, 6, 3)

    test_cashier.add_customer_to_queue(test_customer)
    if test_cashier.queue_size() == 1:
        print("Customer addition works")
        print("Queue size works")

    if(not test_cashier.self_checkout):
        print("Self-checkout casting works")

    test_cashier.checkout_current_customer_items()
    if test_cashier.total_items_checked == 3:
        print("Checking works")
        print("Check for number of items work")

    test_cashier.checkout_current_customer_items()

    if test_cashier.queue_size() == 0:
        print("Pops out cashier correctly")
    
    print(test_cashier<test_cashier2)
    print(test_cashier>test_cashier2)

    test_cashier.add_customer_to_queue(test_customer)

    # Comparison:
    print(test_cashier<test_cashier2)
    print(test_cashier>test_cashier2)

    sorter_list = [test_cashier, test_cashier2]
    sorter_list.sort()
    print("What")