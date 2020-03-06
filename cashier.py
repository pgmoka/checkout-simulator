# =======================================================================
# ============================= Imports =================================
# =======================================================================

import variables as v
import numpy as np

# Module for testing:
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

    def __init__(self, IPM, chitchatter, maintenance_cost, forgetful = 0, self_checkout=False):
        """ Initiates cashier
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
        '''
        return len(self.cashier_queue) <= 0

    def checkout_current_customer_items(self):
        ''' Checkout items from customer being checkout
        '''
        # Checks if line is empty
        if (not self.line_empty()):

            #if this is the first interaction with the customer change there
            #status from waiting to being helped
            if self.cashier_queue[-1].waiting == True:
                self.cashier_queue[-1].waiting = False
                self.cashier_queue[-1].being_helped = True

                #if not a selfcheck out find how out much conversation will
                #take place
                if(not self.self_checkout):
                    self.conversation()


            # Calculate time subtraction
            subtract_me = self.IPM / v.TIME_STEP
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
        '''
        return len(self.cashier_queue)

    def forgetful(self):
        """
        Roll random number between 0-1 and see if if it less than or greater
        than cashiers forgetfulness, if it is below than they will take
        longer to call up next customer
        """
        return np.random.rand() < self.forgetfulness

    def conversation(self):
        """
        This will set the level of conversation between the customer and
        cashier, based on chat levels of each.

        Default chat level is 0
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
    '''
    test_cashier = cashier(45, 3, 9)
    test_cashier2 = cashier(42, 3, 9)

    test_customer = customer(2, 3)

    test_cashier.add_customer_to_queue(test_customer)
    if test_cashier.queue_size() == 1:
        print("Customer addition works")
        print("Queue size works")

    if (not test_cashier.self_checkout):
        print("Self-checkout casting works")

    test_cashier.checkout_current_customer_items()
    if test_cashier.total_items_checked == 3:
        print("Checking works")
        print("Check for number of items work")

    test_cashier.checkout_current_customer_items()

    if test_cashier.queue_size() == 0:
        print("Pops out cashier correctly")

    print(test_cashier < test_cashier2)
    print(test_cashier > test_cashier2)

    test_cashier.add_customer_to_queue(test_customer)

    # Comparison:
    print(test_cashier < test_cashier2)
    print(test_cashier > test_cashier2)

    sorter_list = [test_cashier, test_cashier2]
    sorter_list.sort()
    print("What")
