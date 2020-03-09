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
- To execute, run cashier.py. 
        - Current code is out of date
        - Used in previous tests of cashier
- Has testing for cashier
- Modules necessary: numpy
- External necessities: variables.py, customer.py
- Class has information and behaviors to cashier class and object
- This is the agent of the lines environment

=======================================================================
'''

# =======================================================================
# ============================= Imports =================================
# =======================================================================

import numpy as np

# Module for testing:
import variables as v
from customer import customer

# =======================================================================
# ================================= Class ===============================
# =======================================================================

class cashier:
    # Cost to maintain cashier
    # Not implemented
    maintenance_cost = 0

    # Cashier's IPM
    # Implemented
    IPM = 0

    # % chance cashier will be talkative, 0-1
    chitchatness = 0
    #how much the cashier will chat for the current transaction
    chatLevel = 0

    # Totals items checked by the cashier at the point
    # Implemented
    total_items_checked = 0

    # Checks if cashier is a self-checkout or not
    # Implemented
    self_checkout = False

    total_number_of_items_in_systems = 0

    #forgetfullness
    forgetfulness = 0

    #number of customers helped
    helped = 0

    def __init__(self, IPM, chitchatter, maintenance_cost, forgetful = 0, self_checkout=False):
        """ Initiates cashier

        Precondition:
        - IPM: Items Per Minute cashier can go through
        - chitchatter: variable used to create the chit chat random information. 
        Used to influence IPM
        - maintenance_cost: cost to maintain this cashier
        - forgetful: Variable used for the fogetfull variable. Used to influence IPM. 
        Default = 0
        - self_checkout: Variable to keep track if this is a self-checkout. 
        True if it is, false if not. Default = False

        Postcondition:
        - Cashier customer selection
        """
        self.complete_queue = []
        self.cashier_queue = []
        self.IPM = IPM
        self.chitchatness = chitchatter
        self.self_checkout = self_checkout
        self.maintenance_cost = maintenance_cost
        self.forgetfulness = forgetful

    def add_customer_to_queue(self, customer):
        """ adds a customer to this cashier's queue

        Precondition:
        - customer: customer to be added to the cashier queue

        Postcondition:
        - Customer has bees added to the queue. Related tracking variiables updated
        """
        self.total_number_of_items_in_systems = \
            self.total_number_of_items_in_systems + customer.number_of_items
        self.cashier_queue.insert(0, customer)
        self.complete_queue.append(customer)

        # self-checkout insert
        if(self.self_checkout and self.queue_size() == 1):
            self.IPM = self.cashier_queue[-1].IPM

    def line_empty(self):
        ''' Checks if line is tempty

        Postcondition:
        - True if line is empty, false if not
        '''
        return len(self.cashier_queue) <= 0

    def checkout_current_customer_items(self):
        ''' Checkout items from customer being checkout

        Postcondition:
        - Number of items customer has is updated
        - Internal trackers changed
        - Pop customer if it is empty of items
        '''
        # Checks if line is empty
        if (not self.line_empty()):

            #if this is the first interaction with the customer change there
            #status from waiting to being helped
            if self.cashier_queue[-1].waiting == True:
                self.cashier_queue[-1].waiting = False
                self.cashier_queue[-1].being_helped = True
                self.helped += 1

                #if not a selfcheck out find how out much conversation will
                #take place
                if(not self.self_checkout):
                    self.conversation()


            # Calculate time subtraction
            subtract_me = (self.IPM / v.TIME_STEP)

            #calculate if chattiness from cashier/customer will effect number
            #of items scanned
            if self.chatLevel == 3:
                subtract_me = subtract_me * .6

            elif self.chatLevel == 2:
                subtract_me = subtract_me * .7

            elif self.chatLevel == 1:
                subtract_me = subtract_me * .75
            
            # Select number to be added such that self.cashier_queue[-1].number_of_items 
            # doesn't become smaller than 0
            subtract_me = min(self.cashier_queue[-1].number_of_items, subtract_me)

            # adds min between IPM, and what the customer has in total
            self.cashier_queue[-1].number_items_checked = min(self.cashier_queue[-1].number_of_items, subtract_me)
            self.cashier_queue[-1].number_of_items = self.cashier_queue[-1].number_of_items - \
                                                     self.cashier_queue[-1].number_items_checked

            # Adds to total items checked
            self.total_items_checked = self.total_items_checked + subtract_me

            # if there are no items, customer leaves
            if self.cashier_queue[-1].number_of_items == 0:
                self.cashier_queue.pop()
                self.chatLevel = 0
                
                if (not self.line_empty()):
                    if(self.self_checkout):
                        self.IPM = self.cashier_queue[-1].IPM

    def queue_size(self):
        ''' returns size of the queue

        Postcondition: Returns int that is the length of the queue of customers 
        waiting to be attended by the cashier
        '''
        return len(self.cashier_queue)

    def forgetful(self):
        """ Sees if cashier has been forgetfull during this period
        Roll random number between 0-1 and see if if it less than or greater
        than cashiers forgetfulness, if it is below than they will take
        longer to call up next customer

        Postcondition:
        - True if random is smaller than forgetfulness variable, False
        if not
        """
        return np.random.rand() < self.forgetfulness

    def conversation(self):
        """ Defines if there is a conversation happening
        This will set the level of conversation between the customer and
        cashier, based on chat levels of each.

        Default chat level is 0

        Postcondition:
        - self.chatLevel has a variable select into it between 0 and 3
        """
        customersChatChance = np.random.rand()
        cashiersChatChance = np.random.rand()

        if customersChatChance < self.cashier_queue[-1].chitchatness and \
            cashiersChatChance < self.chitchatness:
            self.chatLevel = 3

        elif cashiersChatChance < self.chitchatness:
            self.chatLevel = 2

        elif customersChatChance < self.cashier_queue[-1].chitchatness:
            self.chatLevel = 1

        else:
            self.chatLevel = 0

    def comparing_factor(self):
        return self.queue_size()*self.total_number_of_items_in_systems*self.IPM

    def __lt__(self, other):
        # sort for smallest to largest
        return self.comparing_factor() < other.comparing_factor() 

if __name__ == "__main__":
    ''' Cashier testing site
    (OUTDATED)
    '''

    #Standard creation tests
    test_cashier = cashier(45, 3, 9)
    test_cashier2 = cashier(42, 3, 9)

    test_customer = customer(2, 3)

    # Check if queue addition works
    test_cashier.add_customer_to_queue(test_customer)
    if test_cashier.queue_size() == 1:
        print("Customer addition works")
        print("Queue size works")

    # Check self checkout systems
    if (not test_cashier.self_checkout):
        print("Self-checkout casting works")

    # Check if checking systems works
    test_cashier.checkout_current_customer_items()
    if test_cashier.total_items_checked == 3:
        print("Checking works")
        print("Check for number of items work")

    # Further checks poping system
    test_cashier.checkout_current_customer_items()

    if test_cashier.queue_size() == 0:
        print("Pops out cashier correctly")

    # Checks comparison booleans
    print(test_cashier < test_cashier2)
    print(test_cashier > test_cashier2)

    test_cashier.add_customer_to_queue(test_customer)

    # Comparison:
    print(test_cashier < test_cashier2)
    print(test_cashier > test_cashier2)

    # Checks if sorts can work
    sorter_list = [test_cashier, test_cashier2]
    sorter_list.sort()
    print("TEST END")
