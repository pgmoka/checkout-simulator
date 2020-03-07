# =======================================================================
# ============================= Imports==================================
# =======================================================================

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
                 number_of_cashiers,
                 number_of_selfcheckouts,
                 population = 'normal',
                 day_type = 'normal',
                 minimum_wage=17,
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
        self.line = self.create_line(model_being_ran,
                                     0,
                                     number_of_cashiers,
                                     number_of_selfcheckouts)

        # Name:
        self.name = model_name

        # set the population and configure how many customers will come in
        # over the course of the day
        self.population = self.setPopulation(population)
        self.day = day_type # save type of day for analysis sake
        self.hourly_population = self.choose_day_type(day_type)

    def execute_simulation(self, show=False, showAnim=False):
        """


        """
        currentHour = 0
        currentSegment = 0

        for i in range( self.hours_open * 60 * v.TIME_STEP ):

            if i == currentSegment:
                self.execute_phase_zero(self.hourly_population[currentHour])
                currentHour += 1
                currentSegment += 75

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
                self.line.total_number_of_items_in_system -
                self.line.total_number_of_checked_items)
            # print("Items checked", self.list_of_items_checked[-1])

            if showAnim:
                visual().print_env(self, update_time=1)
                plt.pause(.01)

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

        print("SIMULATION COMPLETE")

    def choose_day_type(self, day_type):
        """

        """

        if day_type == 'busy':
            hourly_array = self.busyDay()

        elif day_type == 'slow':
            hourly_array = self.slowDay()

        elif day_type == 'front':
            hourly_array = self.frontLoaded()

        elif day_type == 'back':
            hourly_array = self.backLoaded()

        else:
            hourly_array = self.normalDay()

        return hourly_array*self.population

    def setPopulation(self, populationLevel):
        """

        """
        if populationLevel == 'low':
            #this is the number of customers per hour on a slow day
            return self.hours_open * 100

        elif populationLevel == 'high':
            # this is the number of customers per hour on a busy day
            return self.hours_open * 500

        else:
            # this is the number of customers per hour on a regular day
            return self.hours_open * 300


    def busyDay(self):
        """
        Traditional busy day where the middle of the day is very busy while the
        beginning and end of the day are not.
        """
        #set array to be 12 entries evenly distributed from 0 to pi
        hourly_array = np.arange(start=0,
                                 stop=np.pi,
                                 step=1/ (self.hours_open*12))

        #fit array to sin(x) * 1.5
        hourly_array = np.sin(hourly_array) * 1.5

        #normalize array to have a sum of 1
        hourly_array = hourly_array/np.sum(hourly_array)

        return hourly_array

    def normalDay(self):
        """

        """
        hourly_array = np.arange(start=0,
                                 stop=np.pi,
                                 step=np.pi/ (self.hours_open*6))

        hourly_array = np.sin(hourly_array)

        #normalize array to have a sum of 1
        hourly_array = hourly_array/np.sum(hourly_array)

        return hourly_array

    def slowDay(self):
        """

        """
        hourly_array = np.arange(start=0,
                                 stop=np.pi,
                                 step=np.pi/ (self.hours_open*6))

        hourly_array = np.sin(hourly_array) * .5

        #normalize array to have a sum of 1
        hourly_array = hourly_array/np.sum(hourly_array)

        return hourly_array

    def frontLoaded(self):
        """

        """
        hourly_array = np.arange(start=0,
                                 stop=np.pi,
                                 step=np.pi / (self.hours_open*6))

        hourly_array = np.cos(hourly_array - .75)
        hourly_array = np.where(hourly_array > 0, hourly_array, .1)

        #normalize array to have a sum of 1
        hourly_array = hourly_array/np.sum(hourly_array)

        return hourly_array

    def backLoaded(self):
        """

        """
        hourly_array = np.arange(start=0,
                                 stop=np.pi,
                                 step=np.pi / (self.hours_open*6))

        hourly_array = np.cos(hourly_array - 2.25)
        hourly_array = np.where(hourly_array > 0, hourly_array, .1)

        #normalize array to have a sum of 1
        hourly_array = hourly_array/np.sum(hourly_array)

        return hourly_array

    def execute_phase_zero(self, number_of_customers):
        """
        Will add customers to system
        """
        self.line.add_customers(int(number_of_customers))

    def execute_phase_one(self):
        '''
        Applies math related to the rotation of customers
        '''
        self.line.rotate_customers()

    def execute_phase_two(self):
        '''
        Applies math related to the checkouts
        '''
        self.line.apply_checkouts()

    def execute_phase_three(self):
        '''
        Applies math on updating system
        '''
        self.line.update_customers_out_of_system()
        self.line.update_checkedout_items()

    def create_line(self, model_being_ran, number_of_customers,
                    number_of_cashiers, number_of_selfcheckouts):
        """
        Initializes the line environment for the day

        Whichever environemnt is being used will be initialized with the
        intended amount of cashiers and self check outs. However it will
        initialize the environment with 0 customers so that they can be added
        later in predefined intervals.
        """
        if (model_being_ran == "random"):
            return customer_selection_line(number_of_cashiers,
                               number_of_customers,
                               number_of_selfcheckouts,
                               self.minimum_wage,
                               self.self_checkout_maintenance_cost,
                                0,
                                0)

        elif (model_being_ran == "equal"):
            return equal_distribution_line(number_of_cashiers,
                                           number_of_customers,
                                           number_of_selfcheckouts,
                                           self.minimum_wage,
                                           self.self_checkout_maintenance_cost,
                                           0,
                                           0)

        else:
            return cashier_selector_line(number_of_cashiers,
                                 number_of_customers,
                                 number_of_selfcheckouts,
                                 self.minimum_wage,
                                 self.self_checkout_maintenance_cost,
                                 0,
                                 0)

