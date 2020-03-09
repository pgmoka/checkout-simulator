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
- External necessities: variables.py, customer_selection_line.py,
equal_distribution_line.py, cashier_selector_line.py, and cashier.py.
- Sets up model with proper environment and dependencies
- Holds lists with relevant model information

=======================================================================
'''

#=======================================================================
#============================= Imports==================================
#=======================================================================

# Python modules
import numpy as np
import matplotlib.pyplot as plt

# Create simulation code
from visualization import visual
import variables as v
from customer_selection_line import customer_selection_line
from equal_distribution_line import equal_distribution_line
from cashier_selector_line import cashier_selector_line
from cashier import cashier

#=======================================================================
#================================= Class ===============================
#=======================================================================

class model:
    line = 0

    def __init__(self, model_being_ran, number_of_customers, \
        number_of_cashiers, number_of_selfcheckouts, cashier_IPM_p_influence=0, customer_IPM_p_influence=0,\
        minimum_wage = 17.50, self_checkout_maintenance_cost=2.19, model_name="Default Model", item_creation_sensitivity=0,\
        chitchatness_influence = 0):
        '''Initializes method

        Precondition:
        - model_being_ran: String name of the type of the environment to be created
        and tested
        - number_of_customers: int number of customers to inialize list of customers
        - number_of_cashiers: int number of cashiers to inialize in the total
        list of cashiers, and self serving cashiers
        - number_of_selfcheckouts: int number of self-checkout cashier to inialize 
        in the total list of cashiers, and self serving cashiers
        - cashier_IPM_p_influence: addition to the p variable for the creation of
        the IPM for cashiers. Used for sensitivity testing. Default = 0
        - customer_IPM_p_influence: addition to the p variable for the creation of
        the IPM for customers. Used for sensitivity testingDefault = 0
        - minimum_wage: int of minimum wage of cashiers to be added in the system.
        Default = 17.50
        - self_checkout_maintenance_cost: int of amount of pay necessary to maintain
        self-checkout machines working. Default = 2.19 
        - model_name: Name of model itself. Used for information tracking. 
        Default ="Default Model"
        - item_creation_sensitivity: variables added to the randomness creation of items
        such that increasing this will increase the probability of smallers items. Used
        for sensitivity testing. Default = 0
        - chitchatness_influence: variables added to the randomness creation of the chitchatness
        variable. Used for sensitivity testing. Default = 0

        Postcondition:
        - Creation of model
            - Creation of tracking lists
            - Creation of environments
        '''

        # Analysis variables:
        self.list_of_customers_out_of_system = []
        self.list_of_customers_in_line = []
        self.list_of_customers_on_cashier_queue = []
        self.list_of_items_checked = []
        
        # Maintenance cost variables:
        self.minimum_wage = minimum_wage
        self.self_checkout_maintenance_cost = self_checkout_maintenance_cost

        # Environment tested selection:
        self.line = self.create_line(model_being_ran, number_of_customers, \
            number_of_cashiers, number_of_selfcheckouts,cashier_IPM_p_influence, customer_IPM_p_influence,\
                item_creation_sensitivity_test=item_creation_sensitivity, chitchatness_influence = chitchatness_influence)

        # Name:
        self.name = model_name
    
    def execute_simulation(self, number_of_steps, show=False, showAnim=False):
        ''' Executes simulation with a number steps given

        Precondition:
        - number_of_steps: int number of epochs simulation will run for
        - show: Variable set True if information is to be shown, and False if
        no graph is to be displayed. Default = False
        - showAnim: Variable set True if animation is to be shown, and False if
        no animation is to be displayed. Default = False

        Postcondition:
        - Execution of the model
        - If variable set, showing of inner lists
        - If varaiable set, animation of model
        '''
        for i in range(number_of_steps):
            self.execute_phase_one()
            self.execute_phase_two()
            self.execute_phase_three()

            # Add list
            self.list_of_customers_out_of_system.append(
                self.line.customers_that_left)

            self.list_of_customers_in_line.append(
                self.line.customers_waiting_to_queue)

            self.list_of_customers_on_cashier_queue.append(
                self.line.customers_being_served)

            self.list_of_items_checked.append(
                self.line.total_number_of_items_in_system - self.line.total_number_of_checked_items)

            if showAnim:
                showAnim = visual().print_env(self, update_time=.01)

        # print("Items", self.list_of_items_checked)
        # print("Customers", self.list_of_customers_in_line)
        # print("Queue", self.list_of_customers_on_cashier_queue)
        # print("Customers Finished", self.list_of_customers_out_of_system)
        if show:
            plt.figure(1)
            plt.title("Customer out of system over time")
            plt.plot(self.list_of_customers_out_of_system)

            plt.figure(2)
            plt.title("Customers in line over time")
            plt.plot(self.list_of_customers_in_line)

            plt.figure(3)
            plt.title("Customers at cashier queues over time")
            plt.plot(self.list_of_customers_on_cashier_queue)

            plt.figure(4)
            plt.title("Items checked over time")
            plt.plot(self.list_of_items_checked)

            plt.show()

        return self.list_of_customers_out_of_system, \
            self.list_of_customers_in_line, \
            self.list_of_customers_on_cashier_queue,\
            self.list_of_items_checked,\
            self.line.cost_for_maintenance
                
        print("SIMULATION COMPLETE")

    def execute_phase_one(self):
        ''' Applies math related to the rotation of customers

        Precondition:
        - Creation of model
        '''
        self.line.rotate_customers()
    
    def execute_phase_two(self):
        ''' Applies math related to the checkouts

        Precondition:
        - Execution of execute_phase_one
        '''
        self.line.apply_checkouts()

    def execute_phase_three(self):
        ''' Applies math on updating system

        Precondition:
        - Execution of execute_phase_two
        '''
        self.line.update_customers_out_of_system()
        self.line.update_checkedout_items()

    def create_line(self, model_being_ran, number_of_customers, \
        number_of_cashiers, number_of_selfcheckouts,cashier_IPM_p_influence,customer_IPM_p_influence,\
            item_creation_sensitivity_test=0, chitchatness_influence = 0):
        ''' Helper method for the creation of lines
        
        Precondition:
        - model_being_ran: String name of the type of the environment to be created
        and tested
        - number_of_customers: int number of customers to inialize list of customers
        - number_of_cashiers: int number of cashiers to inialize in the total
        list of cashiers, and self serving cashiers
        - number_of_selfcheckouts: int number of self-checkout cashier to inialize 
        in the total list of cashiers, and self serving cashiers
        - cashier_IPM_p_influence: addition to the p variable for the creation of
        the IPM for cashiers. Used for sensitivity testing. Default = 0
        - customer_IPM_p_influence: addition to the p variable for the creation of
        the IPM for customers. Used for sensitivity testingDefault = 0
        - item_creation_sensitivity_test: variables added to the randomness creation of items
        such that increasing this will increase the probability of smallers items. Used
        for sensitivity testing. Default = 0
        - chitchatness_influence: variables added to the randomness creation of the chitchatness
        variable. Used for sensitivity testing. Default = 0

        Postcondition:
        - Return line environment to be used by the model
        '''
        if(model_being_ran == "customer"):
            return customer_selection_line(number_of_cashiers, number_of_customers,number_of_selfcheckouts,\
                self.minimum_wage, self.self_checkout_maintenance_cost,cashier_IPM_p_influence,customer_IPM_p_influence,\
                    item_creation_sensitivity_test=item_creation_sensitivity_test, chitchatness_influence=chitchatness_influence)
        elif(model_being_ran =="equal"):
            return equal_distribution_line(number_of_cashiers, number_of_customers,number_of_selfcheckouts,\
                self.minimum_wage, self.self_checkout_maintenance_cost,cashier_IPM_p_influence,customer_IPM_p_influence,\
                    item_creation_sensitivity_test=item_creation_sensitivity_test, chitchatness_influence=chitchatness_influence)
        else:
            return cashier_selector_line(number_of_cashiers, number_of_customers,number_of_selfcheckouts,\
                self.minimum_wage, self.self_checkout_maintenance_cost,cashier_IPM_p_influence,customer_IPM_p_influence,\
                    item_creation_sensitivity_test=item_creation_sensitivity_test, chitchatness_influence=chitchatness_influence)

