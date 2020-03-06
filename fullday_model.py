# =======================================================================
# ============================= Imports==================================
# =======================================================================

# Python modules
import numpy as np
import matplotlib.pyplot as plt

# Create simulation code
from visualization import visual
import variables as v
from random_line import random_line
from equal_distribution_line import equal_distribution_line
from selector_line import selector_line
from cashier import cashier


# =======================================================================
# ================================= Class ===============================
# =======================================================================


"""
things needed for this 

-method in equal distribution line that allows for customers outside of init 
 system to be added
 
-day will always be 12 hours 


"""

class Fullday:
    line = 0

    hours_open = 12

    def __init__(self,
                 model_being_ran,
                 number_of_customers,
                 number_of_cashiers,
                 number_of_selfcheckouts,
                 day_type = 'normal',
                 minimum_wage=12,
                 self_checkout_maintenance_cost=4,
                 model_name="Default Model"):
        '''
        Initializes method
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
                                     number_of_cashiers,
                                     number_of_selfcheckouts)

        # Name:
        self.name = model_name

    def execute_simulation(self, show=False, showAnim=False):
        ''' Executes simulation with a number steps
        '''


        for i in range(number_of_steps):
            self.execute_phase_one()
            self.execute_phase_two()
            self.execute_phase_three()

            # Add list
            self.list_of_customers_out_of_system.append(
                self.line.customers_that_left)
            # print("Customers left", self.list_of_customers_out_of_system[-1])

            self.list_of_customers_in_line.append(
                self.line.customers_waiting_to_queue)
            # print("Customers in line", self.list_of_customers_in_line[-1])

            self.list_of_customers_on_cashier_queue.append(
                self.line.customers_being_served)
            # print("Customers in queue", self.list_of_customers_on_cashier_queue[-1])

            self.list_of_items_checked.append(
                self.line.total_number_of_items_in_system - self.line.total_number_of_checked_items)
            # print("Items checked", self.list_of_items_checked[-1])

            if showAnim:
                visual().print_env(self)
                plt.pause(1)

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
        if showAnim:
            visual().print_env(self)
            # visual().display_simulation(num_cashiers=4, customer_left=self.list_of_customers_out_of_system, queue_values=self.list_of_customers_on_cashier_queue, line_values=self.list_of_customers_in_line, items_left=self.list_of_items_checked)

        print("SIMULATION COMPLETE")



    def frontLoadedDay(self, hourly_array, population):
        pass

    def normalDay(self, hourly_array, population):
        pass

    def slowDay(self, hourly_array, population):
        pass



    def execute_phase_one(self):
        ''' Applies math related to the rotation of customers
        '''
        self.line.rotate_customers()

    def execute_phase_two(self):
        ''' Applies math related to the checkouts
        '''
        self.line.apply_checkouts()

    def execute_phase_three(self):
        ''' Applies math on updating system
        '''
        self.line.update_customers_out_of_system()
        self.line.update_checkedout_items()

    def create_line(self, model_being_ran, number_of_customers,
                    number_of_cashiers, number_of_selfcheckouts):
        '''
            Helper method for the creation of lines
        '''
        if (model_being_ran == "random"):
            return random_line(number_of_cashiers, number_of_customers,
                               number_of_selfcheckouts,
                               self.minimum_wage,
                               self.self_checkout_maintenance_cost)

        elif (model_being_ran == "equal"):
            return equal_distribution_line(number_of_cashiers,
                                           number_of_customers,
                                           number_of_selfcheckouts,
                                           self.minimum_wage,
                                           self.self_checkout_maintenance_cost)

        else:
            return selector_line(number_of_cashiers, number_of_customers,
                                 number_of_selfcheckouts,
                                 self.minimum_wage,
                                 self.self_checkout_maintenance_cost)
