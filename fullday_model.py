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
- Runs model with the population of a day trickleling into the line
- Holds relevant information

=======================================================================
'''

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

#Variables that can be changed to change model behavior
HIGH_VALUE = 500
NORMAL_VALUE = 300
LOW_VALUE = 100
HOURS_OF_OPERATION = 3

class Fullday:
    """
    This model
    """
    line = 0

    #constant
    hours_open = HOURS_OF_OPERATION

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
        This method will execute the full day simulation

        precondition:
            The model has been initialized

        postcondition:
            all major statistics are saved in arrays that represent the entire
            simulation
        """
        #set counters for when to add customers
        currentHour = 0
        currentSegment = 0

        for i in range( self.hours_open * 60 * v.TIME_STEP ):

            #only add customers every 5 minutes of simulation time
            if i == currentSegment:
                self.execute_phase_zero(self.hourly_population[currentHour])
                currentHour += 1
                currentSegment += v.TIME_STEP * 2

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
                showAnim = visual().print_env(self, update_time=.001, start_time=9)

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
        This method will set the total population for the entire days model
        and set it to the specified density that is specified during creation.

        precondition: model has began initilization

        postcondition: an array that represents population density over time
        is created.
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
        This method will set the total population for the entire days model

        precondition: model has a set time of hours open

        postcondition: the number of customers
        """
        if populationLevel == 'low':
            #this is the number of customers per hour on a slow day
            return self.hours_open * LOW_VALUE

        elif populationLevel == 'high':
            # this is the number of customers per hour on a busy day
            return self.hours_open * HIGH_VALUE

        else:
            # this is the number of customers per hour on a regular day
            return self.hours_open * NORMAL_VALUE

    def busyDay(self):
        """
        This will generate the population density curve for a day where
        the customer traffic is higher than normal

        precondition: model has specified type of day

        postcondition: array of how the days population density will change
        over the hours open
        """
        #set array to be 12 entries evenly distributed from 0 to pi
        hourly_array = np.arange(start=0,
                                 stop=np.pi,
                                 step=1/ (self.hours_open*30))

        #fit array to sin(x) * 1.5
        hourly_array = np.sin(hourly_array) * 1.5

        #normalize array to have a sum of 1
        hourly_array = hourly_array/np.sum(hourly_array)

        return hourly_array

    def normalDay(self):
        """
        This will generate the population density curve for a day where
        the customer traffic is normal

        precondition: model has specified type of day

        postcondition: array of how the days population density will change
        over the hours open
        """
        hourly_array = np.arange(start=0,
                                 stop=np.pi,
                                 step=np.pi/ (self.hours_open*30))

        hourly_array = np.sin(hourly_array)

        #normalize array to have a sum of 1
        hourly_array = hourly_array/np.sum(hourly_array)

        return hourly_array

    def slowDay(self):
        """
        This will generate the population density curve for a day where
        the customer traffic is lower than normal

        precondition: model has specified type of day

        postcondition: array of how the days population density will change
        over the hours open
        """
        hourly_array = np.arange(start=0,
                                 stop=np.pi,
                                 step=np.pi/ (self.hours_open*30))

        hourly_array = np.sin(hourly_array) * .5

        #normalize array to have a sum of 1
        hourly_array = hourly_array/np.sum(hourly_array)

        return hourly_array

    def frontLoaded(self):
        """
        This will generate the population density curve for a day where
        the customer traffic happens in the earlier part of the open hours

        precondition: model has specified type of day

        postcondition: array of how the days population density will change
        over the hours open
        """
        hourly_array = np.arange(start=0,
                                 stop=np.pi,
                                 step=np.pi / (self.hours_open*30))

        hourly_array = np.cos(hourly_array - .75)
        hourly_array = np.where(hourly_array > 0, hourly_array, .1)

        #normalize array to have a sum of 1
        hourly_array = hourly_array/np.sum(hourly_array)

        return hourly_array

    def backLoaded(self):
        """
        This will generate the population density curve for a day where
        the customer traffic happens in the latter part of the open hours

        precondition: model has specified type of day

        postcondition: array of how the days population density will change
        over the hours open
        """
        hourly_array = np.arange(start=0,
                                 stop=np.pi,
                                 step=np.pi / (self.hours_open*30))

        hourly_array = np.cos(hourly_array - 2.25)
        hourly_array = np.where(hourly_array > 0, hourly_array, .1)

        #normalize array to have a sum of 1
        hourly_array = hourly_array/np.sum(hourly_array)

        return hourly_array

    def execute_phase_zero(self, number_of_customers):
        ''' Applies math related to adding customers to the running model

        Precondition:
        - Creation of model
        '''
        self.line.add_customers(int(number_of_customers))

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

    def create_line(self, model_being_ran, number_of_customers,
                    number_of_cashiers, number_of_selfcheckouts):
        """
         Helper method for the creation of lines

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
        """
        if (model_being_ran == "customer"):
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

