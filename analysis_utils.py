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
- External necessities: variables.py, and model.py
- Holds methods used for the analysis of our model

=======================================================================
'''
# =======================================================================
# ============================= Imports==================================
# =======================================================================

# Python modules
import numpy as np
import matplotlib.pyplot as plt
from os.path import join

# Create simulation code
import variables as v
from model import model

# =======================================================================
# =============================== Methods ===============================
# =======================================================================

# ----------------------------- Configuration ---------------------------

"""
Pedro Notes:
 - The outer loop for loop
 - Customer
 - Cashier IPMS
 - 4 Images based on each generated list
 - Y axis list quantity
 - X axis related to number of cashiers operating self checkout (0 - 10)
 - One graph for each configuration
 - 3, 6, 9, 12
 - Only care about the final state of system
 - 
"""


def configuration(number_of_epochs_for_simulation, number_of_av_simulations=200,
                                                   sensitivity_range=10, number_of_people=100):
    """Makes tests relative to config, involving:
        - Number of customers out of system
        - Number of customers in line
        - Number of customers in queue
        - Number checked items
    """

    for k in range(1, 5):
        sensitivity_cashiers_to_self_checkout(number_of_epochs_for_simulation, "equal",
                                              number_of_av_simulations, sensitivity_range, number_of_people, 3*k)

    for k in range(1, 5):
        sensitivity_cashiers_to_self_checkout(number_of_epochs_for_simulation, "customer",
                                              number_of_av_simulations, sensitivity_range, number_of_people, 3*k)

    for k in range(1, 5):
        sensitivity_cashiers_to_self_checkout(number_of_epochs_for_simulation, "cashier",
                                              number_of_av_simulations, sensitivity_range, number_of_people, 3*k)
    print("Test complete")


def sensitivity_cashiers_to_self_checkout(number_of_epochs_for_simulation, model_name, number_of_av_simulations,
                                    sensitivity_range=10, number_of_people=100, cashiers_to_self_checkouts=3):
    num_self_checkouts = []
    avg_num_cust_left = []
    avg_num_cust_not_in_line = []
    avg_num_cust_being_helped = []
    avg_num_items_checked = []
    avg_num_maintenance = []

    # Number of cashiers operating self checkouts
    for i in range(sensitivity_range):
        # Number of tests for sensitivity
        num_self_checkouts.append(i)
        cust_left = []
        cust_line = []
        cust_queue = []
        items = []
        maintenance = []
        for j in range(number_of_av_simulations):
            self_check_model = model(model_name, number_of_people, 10 - i, i * cashiers_to_self_checkouts,
                                     cashier_IPM_p_influence=0.1,
                                     customer_IPM_p_influence=0.2)
            customers_left, \
            customers_in_line, \
            customers_in_queue, \
            items_checked, \
            maintenance_costs \
                = self_check_model.execute_simulation(number_of_epochs_for_simulation,
                                                      show=False, showAnim=False)

            cust_left.append(customers_left[-1])
            maintenance.append(maintenance_costs)
            items.append(items_checked[-1])
            cust_line.append(customers_in_line[-1])
            cust_queue.append(customers_in_queue[-1])

        avg_num_cust_left.append(sum(cust_left) / number_of_av_simulations)
        avg_num_cust_being_helped.append(sum(cust_queue) / number_of_av_simulations)
        avg_num_items_checked.append(sum(items) / number_of_av_simulations)
        avg_num_maintenance.append(sum(maintenance) / number_of_av_simulations)
        avg_num_cust_not_in_line.append(sum(cust_line) / number_of_av_simulations)

    plt.figure(1)
    plt.clf()
    plt.title("Sensitivity Analysis for Customers Helped with Different Configurations")
    plt.xlabel("Cashiers Operating Self Checkouts")
    plt.ylabel("Mean of Customers Out of System at %d" % number_of_epochs_for_simulation)
    plt.plot(num_self_checkouts, avg_num_cust_left)
    plt.savefig(join("analysis_images", "configuration", model_name +
                     "_cashier_to_" + str(cashiers_to_self_checkouts) +
                     "_checkouts_list_of_customers_out_of_system.png"))

    # plt.figure(2)
    # plt.clf()
    # plt.title("Sensitivity Analysis for Customers Not in Line with Different Configurations")
    # plt.xlabel("Cashiers Operating Self Checkouts\n(1 Cashier = " + str(cashiers_to_self_checkouts) + " Self Checkouts)")
    # plt.ylabel("Mean of Customers Still In Line at %d" % number_of_epochs_for_simulation)
    # plt.plot(num_self_checkouts, avg_num_cust_not_in_line)
    # plt.savefig(join("analysis_images", "configuration", model_name + "_cashier_to_" + str(
    #     cashiers_to_self_checkouts) + "_checkouts_cust_waiting_outside_lines.png"))

    plt.figure(3)
    plt.clf()
    plt.title("Sensitivity Analysis for Customers In Cashier's Lines with Different Configurations")
    plt.xlabel(
        "Cashiers Operating Self Checkouts\n(1 Cashier = " + str(cashiers_to_self_checkouts) + " Self Checkouts)")
    plt.ylabel("Mean of Customers Still In Line at %d" % number_of_epochs_for_simulation)
    plt.plot(num_self_checkouts, avg_num_cust_being_helped)
    plt.savefig(join("analysis_images", "configuration", model_name + "_cashier_to_" + str(
        cashiers_to_self_checkouts) + "_checkouts_cust_in_lines.png"))

    plt.figure(4)
    plt.clf()
    plt.title("Sensitivity Analysis for Total Items Checked with Different Configurations")
    plt.xlabel(
        "Cashiers Operating Self Checkouts\n(1 Cashier = " + str(cashiers_to_self_checkouts) + " Self Checkouts)")
    plt.ylabel("Mean of Customers Still In Line at %d" % number_of_epochs_for_simulation)
    plt.plot(num_self_checkouts, avg_num_items_checked)
    plt.savefig(join("analysis_images", "configuration", model_name + "_cashier_to_" + str(
        cashiers_to_self_checkouts) + "_checkouts_items_checked.png"))

    plt.figure(5)
    plt.clf()
    plt.title("Sensitivity Analysis for Maintenance Costs with Different Configurations")
    plt.xlabel(
        "Cashiers Operating Self Checkouts\n(1 Cashier = " + str(cashiers_to_self_checkouts) + " Self Checkouts)")
    plt.ylabel("Mean of Customers Still In Line at %d" % number_of_epochs_for_simulation)
    plt.plot(num_self_checkouts, avg_num_maintenance)
    plt.savefig(join("analysis_images", "configuration", model_name + "_cashier_to_" + str(
        cashiers_to_self_checkouts) + "_checkouts_maintenance_costs.png"))

    #plt.show()

# ------------------------------- Sensitivity ---------------------------

def sensitivity_cashierIPM_analysis_for_all_lines(number_of_epochs_for_simulation, number_of_av_simulations=200,
                                                  sensitivity_range=10, number_of_people=100):
    """ Sensitivity related to the IPM of cashier, test for all models type

    Precondition:
    - number_of_epochs_for_simulation: number of epochs each simulation is going to
    be ran for
    - number_of_av_simulations: Numbe of simulations that are going to be ran to
    calculate the average. Default = 200
    - sensitivity_range: Range for the sensitivity test. Default = 10
    - number_of_people: number of people to enter the system. Default = 100

    Postcondition:
    - 4 png images saved to a file called "analysis_images"
        - x-axis has the sensitivity test
        - y-axis has the quantity related to the test
        - Related to the outputs printed at the test.
    """

    # Numbers for simulation
    x_axis = np.arange(sensitivity_range) / 100

    # Runs simulations with the different types of line:
    sens_analysis_list_of_customers_out_of_system_CUSTOMER, sens_analysis_list_of_customers_in_line_CUSTOMER, \
    sens_analysis_list_of_customers_on_cashier_queue_CUSTOMER, sens_analysis_list_of_customer_items_checked_CUSTOMER = \
        sensitivity_cashierIPM_analysis(number_of_epochs_for_simulation, "customer", number_of_av_simulations,
                                        sensitivity_range, \
                                        number_of_people=number_of_people)

    sens_analysis_list_of_customers_out_of_system_CASHIER, sens_analysis_list_of_customers_in_line_CASHIER, \
    sens_analysis_list_of_customers_on_cashier_queue_CASHIER, sens_analysis_list_of_customer_items_checked_CASHIER = \
        sensitivity_cashierIPM_analysis(number_of_epochs_for_simulation, "cashier", number_of_av_simulations,
                                        sensitivity_range, \
                                        number_of_people=number_of_people)

    sens_analysis_list_of_customers_out_of_system_EQUAL, sens_analysis_list_of_customers_in_line_EQUAL, \
    sens_analysis_list_of_customers_on_cashier_queue_EQUAL, sens_analysis_list_of_customer_items_checked_EQUAL = \
        sensitivity_cashierIPM_analysis(number_of_epochs_for_simulation, "equal", number_of_av_simulations,
                                        sensitivity_range, \
                                        number_of_people=number_of_people)

    # Prints number of customers out of system
    plt.figure(1)
    plt.clf()
    plt.title("Sensitivity Analysis for Customers Out of the System")
    plt.xlabel("Probability Increment")
    plt.ylabel("Percentage of Mean of Customers Out of System at %d Epochs" % number_of_epochs_for_simulation)
    plt.plot(x_axis, sens_analysis_list_of_customers_out_of_system_CUSTOMER, 'g^', \
             x_axis, sens_analysis_list_of_customers_out_of_system_CASHIER, 'bs', \
             x_axis, sens_analysis_list_of_customers_out_of_system_EQUAL, 'ro')
    plt.savefig("analysis_images\cashierIPM_sens_analysis_list_of_customers_out_of_system_%d.png" % number_of_people)

    plt.figure(2)
    plt.clf()
    plt.title("Sensitivity Analysis for People in Line Average of %d" % number_of_av_simulations)
    plt.xlabel("Probability Increment")
    plt.ylabel("Percentage of Mean of Customers in Line at %d Epochs" % number_of_epochs_for_simulation)
    plt.plot(x_axis, sens_analysis_list_of_customers_in_line_CUSTOMER, 'g^', \
             x_axis, sens_analysis_list_of_customers_in_line_CASHIER, 'bs', \
             x_axis, sens_analysis_list_of_customers_in_line_EQUAL, 'ro')
    plt.savefig("analysis_images\cashierIPM_sens_analysis_list_of_customers_in_line_%d.png" % number_of_people)

    plt.figure(3)
    plt.clf()
    plt.title("Sensitivity Customers in Queue Average of %d" % number_of_av_simulations)
    plt.xlabel("Probability Increment")
    plt.ylabel(
        "Percentage of Mean of Cashiers on Queue in the End of Simulation at %d Epochs" % number_of_epochs_for_simulation)
    plt.plot(x_axis, sens_analysis_list_of_customers_on_cashier_queue_CUSTOMER, 'g^', \
             x_axis, sens_analysis_list_of_customers_on_cashier_queue_CASHIER, 'bs', \
             x_axis, sens_analysis_list_of_customers_on_cashier_queue_EQUAL, 'ro')
    plt.savefig("analysis_images\cashierIPM_sens_analysis_list_of_customers_on_cashier_queue_%d.png" % number_of_people)

    plt.figure(4)
    plt.clf()
    plt.title("Sensitivity Analysis for Items Checked Average of %d" % number_of_av_simulations)
    plt.xlabel("Probability Increment")
    plt.ylabel("Mean of Items checkedout at %d Epochs" % number_of_epochs_for_simulation)
    plt.plot(x_axis, sens_analysis_list_of_customer_items_checked_CUSTOMER, 'g^', \
             x_axis, sens_analysis_list_of_customer_items_checked_CASHIER, 'bs', \
             x_axis, sens_analysis_list_of_customer_items_checked_EQUAL, 'ro')
    plt.savefig("analysis_images\cashierIPM_sens_analysis_list_of_items_checked_%d.png" % number_of_people)


def sensitivity_cashierIPM_analysis(number_of_epochs_for_simulation, model_name, number_of_av_simulations,
                                    sensitivity_range, \
                                    number_of_people=100):
    """ Sensitivity related to the IPM of cashier, test for specific model type

    Precondition:
    - number_of_epochs_for_simulation: number of epochs used to run the simulation
    - model_name,number_of_av_simulations: name of the model used during the test
        - Chosen between "equal", "cashier", and "customer"
    - sensitivity_range: range of sensitivity to be tested
    - number_of_people: Number of people to go into the system begin. Default = 100

    Postcondition:
    - sens_analysis_list_of_customers_out_of_system: an int list of the average total number of
    customers out of system at the end of the simulation
    - sens_analysis_list_of_customers_in_line: an int list of the average customers in line
     at the end of the simulation
    - sens_analysis_list_of_customers_on_cashier_queue: an int list of the average customers on 
    queues at the end of the simulation
    - sens_analysis_list_of_customer_items_checked: an int list of the average total items checked
     at the end of the simulation
    """

    # Sets up analysis list
    sens_analysis_list_of_customers_out_of_system = []
    sens_analysis_list_of_customers_in_line = []
    sens_analysis_list_of_customers_on_cashier_queue = []
    sens_analysis_list_of_customer_items_checked = []

    # Loops between sensitivities
    for simulation_i in range(sensitivity_range):
        sens_customers_out_of_system_average = 0
        sens_customers_in_line_average = 0
        sens_customers_on_cashier_queue_average = 0
        sens_items_customer_checked_average = 0

        # Number of simulations used for average of simulation
        for i in range(number_of_av_simulations):
            self_check_model = model(model_name, number_of_people, 10, 0, cashier_IPM_p_influence=simulation_i / 100,
                                     customer_IPM_p_influence=0)

            list_of_customers_out_of_system, \
            list_of_customers_in_line, \
            list_of_customers_on_cashier_queue, \
            list_of_items_checked, \
            cost_for_maintenance \
                = self_check_model.execute_simulation(number_of_epochs_for_simulation, show=False, showAnim=False)

            # Adds to average
            sens_customers_out_of_system_average = sens_customers_out_of_system_average \
                                                   + list_of_customers_out_of_system[-1]

            sens_customers_in_line_average = sens_customers_in_line_average \
                                             + list_of_customers_in_line[-1]

            sens_customers_on_cashier_queue_average = sens_customers_on_cashier_queue_average \
                                                      + list_of_customers_on_cashier_queue[-1]

            sens_items_customer_checked_average = sens_items_customer_checked_average \
                                                  + list_of_items_checked[0] - list_of_items_checked[-1]
        # Calulates average
        sens_customers_out_of_system_average = sens_customers_out_of_system_average / number_of_av_simulations
        sens_customers_in_line_average = sens_customers_in_line_average / number_of_av_simulations
        sens_customers_on_cashier_queue_average = sens_customers_on_cashier_queue_average / number_of_av_simulations
        sens_items_customer_checked_average = sens_items_customer_checked_average / number_of_av_simulations

        sens_customers_out_of_system_average = sens_customers_out_of_system_average / number_of_people
        sens_customers_in_line_average = sens_customers_in_line_average / number_of_people
        sens_customers_on_cashier_queue_average = sens_customers_on_cashier_queue_average / number_of_people

        # Appends to average list
        sens_analysis_list_of_customers_out_of_system.append(sens_customers_out_of_system_average)
        sens_analysis_list_of_customers_in_line.append(sens_customers_in_line_average)
        sens_analysis_list_of_customers_on_cashier_queue.append(sens_customers_on_cashier_queue_average)
        sens_analysis_list_of_customer_items_checked.append(sens_items_customer_checked_average)

    return sens_analysis_list_of_customers_out_of_system, sens_analysis_list_of_customers_in_line, \
           sens_analysis_list_of_customers_on_cashier_queue, sens_analysis_list_of_customer_items_checked


def sensitivity_customerIPM_analysis_for_all_lines(number_of_epochs_for_simulation, number_of_av_simulations=200, \
                                                   sensitivity_range=10, number_of_people=100):
    """ Sensitivity related to the IPM of customer, test for all models type

    Precondition:
    - number_of_epochs_for_simulation: number of epochs each simulation is going to
    be ran for
    - number_of_av_simulations: Numbe of simulations that are going to be ran to
    calculate the average. Default = 200
    - sensitivity_range: Range for the sensitivity test. Default = 10
    - number_of_people: number of people to enter the system. Default = 100

    Postcondition:
    - 4 png images saved to a file called "analysis_images"
        - x-axis has the sensitivity test
        - y-axis has the quantity related to the test
        - Related to the outputs printed at the test.
    """

    x_axis = np.arange(sensitivity_range) / 100

    # Runs simulations with the different types of line:
    sens_analysis_list_of_customers_out_of_system_CUSTOMER, sens_analysis_list_of_customers_in_line_CUSTOMER, \
    sens_analysis_list_of_customers_on_cashier_queue_CUSTOMER, sens_analysis_list_of_customer_items_checked_CUSTOMER = \
        sensitivity_customerIPM_analysis(number_of_epochs_for_simulation, "customer", number_of_av_simulations,
                                         sensitivity_range, \
                                         number_of_people=number_of_people)

    sens_analysis_list_of_customers_out_of_system_CASHIER, sens_analysis_list_of_customers_in_line_CASHIER, \
    sens_analysis_list_of_customers_on_cashier_queue_CASHIER, sens_analysis_list_of_customer_items_checked_CASHIER = \
        sensitivity_customerIPM_analysis(number_of_epochs_for_simulation, "cashier", number_of_av_simulations,
                                         sensitivity_range, \
                                         number_of_people=number_of_people)

    sens_analysis_list_of_customers_out_of_system_EQUAL, sens_analysis_list_of_customers_in_line_EQUAL, \
    sens_analysis_list_of_customers_on_cashier_queue_EQUAL, sens_analysis_list_of_customer_items_checked_EQUAL = \
        sensitivity_customerIPM_analysis(number_of_epochs_for_simulation, "equal", number_of_av_simulations,
                                         sensitivity_range, \
                                         number_of_people=number_of_people)

    # Prints number of customers out of system
    plt.figure(5)
    plt.clf()
    plt.title("Sensitivity Analysis for Customers Out of the System")
    plt.xlabel("Probability Increment")
    plt.ylabel("Percentage of Mean of Customers Out of System at %d Epochs" % number_of_epochs_for_simulation)
    plt.plot(x_axis, sens_analysis_list_of_customers_out_of_system_CUSTOMER, 'g^', \
             x_axis, sens_analysis_list_of_customers_out_of_system_CASHIER, 'bs', \
             x_axis, sens_analysis_list_of_customers_out_of_system_EQUAL, 'ro')
    plt.savefig("analysis_images\customerIPM_sens_analysis_list_of_customers_out_of_system_%d.png" % number_of_people)

    plt.figure(6)
    plt.clf()
    plt.title("Sensitivity Analysis for People in Line Average of %d" % number_of_av_simulations)
    plt.xlabel("Probability Increment")
    plt.ylabel("Percentage of Mean of Customers in Line at %d Epochs" % number_of_epochs_for_simulation)
    plt.plot(x_axis, sens_analysis_list_of_customers_in_line_CUSTOMER, 'g^', \
             x_axis, sens_analysis_list_of_customers_in_line_CASHIER, 'bs', \
             x_axis, sens_analysis_list_of_customers_in_line_EQUAL, 'ro')
    plt.savefig("analysis_images\customerIPM_sens_analysis_list_of_customers_in_line_%d.png" % number_of_people)

    plt.figure(7)
    plt.clf()
    plt.title("Sensitivity Customers in Queue Average of %d" % number_of_av_simulations)
    plt.xlabel("Probability Increment")
    plt.ylabel(
        "Percentage of Mean of Cashiers on Queue in the End of Simulation at %d Epochs" % number_of_epochs_for_simulation)
    plt.plot(x_axis, sens_analysis_list_of_customers_on_cashier_queue_CUSTOMER, 'g^', \
             x_axis, sens_analysis_list_of_customers_on_cashier_queue_CASHIER, 'bs', \
             x_axis, sens_analysis_list_of_customers_on_cashier_queue_EQUAL, 'ro')
    plt.savefig("analysis_images\customerIPM_sens_analysis_list_of_customers_on_cashier_queue%d.png" % number_of_people)

    plt.figure(8)
    plt.clf()
    plt.title("Sensitivity Analysis for Items Checked Average of %d" % number_of_av_simulations)
    plt.xlabel("Probability Increment")
    plt.ylabel("Mean of Items checkedout at %d Epochs" % number_of_epochs_for_simulation)
    plt.plot(x_axis, sens_analysis_list_of_customer_items_checked_CUSTOMER, 'g^', \
             x_axis, sens_analysis_list_of_customer_items_checked_CASHIER, 'bs', \
             x_axis, sens_analysis_list_of_customer_items_checked_EQUAL, 'ro')
    plt.savefig("analysis_images\customerIPM_sens_analysis_list_of_items_checked_%d.png" % number_of_people)


def sensitivity_customerIPM_analysis(number_of_epochs_for_simulation, model_name, number_of_av_simulations,
                                     sensitivity_range, \
                                     number_of_people=240):
    """ Sensitivity related to the IPM of customer, test for specific model type

    Precondition:
    - number_of_epochs_for_simulation: number of epochs used to run the simulation
    - model_name,number_of_av_simulations: name of the model used during the test
        - Chosen between "equal", "cashier", and "customer"
    - sensitivity_range: range of sensitivity to be tested
    - number_of_people: Number of people to go into the system begin. Default = 100

    Postcondition:
    - sens_analysis_list_of_customers_out_of_system: an int list of the average total number of
    customers out of system at the end of the simulation
    - sens_analysis_list_of_customers_in_line: an int list of the average customers in line
     at the end of the simulation
    - sens_analysis_list_of_customers_on_cashier_queue: an int list of the average customers on 
    queues at the end of the simulation
    - sens_analysis_list_of_customer_items_checked: an int list of the average total items checked
     at the end of the simulation
    """

    # Sets up analysis list
    sens_analysis_list_of_customers_out_of_system = []
    sens_analysis_list_of_customers_in_line = []
    sens_analysis_list_of_customers_on_cashier_queue = []
    sens_analysis_list_of_customer_items_checked = []

    # Loops between sensitivities
    for simulation_i in range(sensitivity_range):
        sens_customers_out_of_system_average = 0
        sens_customers_in_line_average = 0
        sens_customers_on_cashier_queue_average = 0
        sens_items_customer_checked_average = 0

        # Number of simulations used for average of simulation
        for i in range(number_of_av_simulations):
            self_check_model = model(model_name, number_of_people, 0, 10, cashier_IPM_p_influence=0,
                                     customer_IPM_p_influence=simulation_i / 100)

            list_of_customers_out_of_system, \
            list_of_customers_in_line, \
            list_of_customers_on_cashier_queue, \
            list_of_items_checked, \
            cost_for_maintenance \
                = self_check_model.execute_simulation(number_of_epochs_for_simulation, show=False, showAnim=False)

            # Adds to average
            sens_customers_out_of_system_average = sens_customers_out_of_system_average \
                                                   + list_of_customers_out_of_system[-1]

            sens_customers_in_line_average = sens_customers_in_line_average \
                                             + list_of_customers_in_line[-1]

            sens_customers_on_cashier_queue_average = sens_customers_on_cashier_queue_average \
                                                      + list_of_customers_on_cashier_queue[-1]

            sens_items_customer_checked_average = sens_items_customer_checked_average \
                                                  + list_of_items_checked[0] - list_of_items_checked[-1]
        # Calulates average
        sens_customers_out_of_system_average = sens_customers_out_of_system_average / number_of_av_simulations
        sens_customers_in_line_average = sens_customers_in_line_average / number_of_av_simulations
        sens_customers_on_cashier_queue_average = sens_customers_on_cashier_queue_average / number_of_av_simulations
        sens_items_customer_checked_average = sens_items_customer_checked_average / number_of_av_simulations

        sens_customers_out_of_system_average = sens_customers_out_of_system_average / number_of_people
        sens_customers_in_line_average = sens_customers_in_line_average / number_of_people
        sens_customers_on_cashier_queue_average = sens_customers_on_cashier_queue_average / number_of_people

        # Appends to average list
        sens_analysis_list_of_customers_out_of_system.append(sens_customers_out_of_system_average)
        sens_analysis_list_of_customers_in_line.append(sens_customers_in_line_average)
        sens_analysis_list_of_customers_on_cashier_queue.append(sens_customers_on_cashier_queue_average)
        sens_analysis_list_of_customer_items_checked.append(sens_items_customer_checked_average)

    return sens_analysis_list_of_customers_out_of_system, sens_analysis_list_of_customers_in_line, \
           sens_analysis_list_of_customers_on_cashier_queue, sens_analysis_list_of_customer_items_checked


def sensitivity_itemNumb_analysis_for_all_lines(number_of_epochs_for_simulation, number_of_av_simulations=200, \
                                                sensitivity_range=30, number_of_people=100):
    """ Sensitivity related to the number of items, test for all models type

    Precondition:
    - number_of_epochs_for_simulation: number of epochs each simulation is going to
    be ran for
    - number_of_av_simulations: Numbe of simulations that are going to be ran to
    calculate the average. Default = 200
    - sensitivity_range: Range for the sensitivity test. Default = 10
    - number_of_people: number of people to enter the system. Default = 100

    Postcondition:
    - 4 png images saved to a file called "analysis_images"
        - x-axis has the sensitivity test
        - y-axis has the quantity related to the test
        - Related to the outputs printed at the test.
    """

    # Numbers for simulation
    x_axis = (np.arange(sensitivity_range) / 100) - (sensitivity_range / 200)

    # Runs simulations with the different types of line:
    sens_analysis_list_of_customers_out_of_system_CUSTOMER, sens_analysis_list_of_customers_in_line_CUSTOMER, \
    sens_analysis_list_of_customers_on_cashier_queue_CUSTOMER, sens_analysis_list_of_customer_items_checked_CUSTOMER = \
        sensitivity_itemNumb_analysis(number_of_epochs_for_simulation, "customer", number_of_av_simulations,
                                      sensitivity_range, \
                                      number_of_people=number_of_people)

    sens_analysis_list_of_customers_out_of_system_CASHIER, sens_analysis_list_of_customers_in_line_CASHIER, \
    sens_analysis_list_of_customers_on_cashier_queue_CASHIER, sens_analysis_list_of_customer_items_checked_CASHIER = \
        sensitivity_itemNumb_analysis(number_of_epochs_for_simulation, "cashier", number_of_av_simulations,
                                      sensitivity_range, \
                                      number_of_people=number_of_people)

    sens_analysis_list_of_customers_out_of_system_EQUAL, sens_analysis_list_of_customers_in_line_EQUAL, \
    sens_analysis_list_of_customers_on_cashier_queue_EQUAL, sens_analysis_list_of_customer_items_checked_EQUAL = \
        sensitivity_itemNumb_analysis(number_of_epochs_for_simulation, "equal", number_of_av_simulations,
                                      sensitivity_range, \
                                      number_of_people=number_of_people)

    # Prints number of customers out of system
    plt.figure(9)
    plt.clf()
    plt.title("Sensitivity Analysis for Customers Out of the System")
    plt.xlabel("Probability Increment")
    plt.ylabel("Percentage of Mean of Customers Out of System at %d Epochs" % number_of_epochs_for_simulation)
    plt.plot(x_axis, sens_analysis_list_of_customers_out_of_system_CUSTOMER, 'g^', \
             x_axis, sens_analysis_list_of_customers_out_of_system_CASHIER, 'bs', \
             x_axis, sens_analysis_list_of_customers_out_of_system_EQUAL, 'ro')
    plt.savefig("analysis_images\itemNumb_sens_analysis_list_of_customers_out_of_system_%d.png" % number_of_people)

    plt.figure(10)
    plt.clf()
    plt.title("Sensitivity Analysis for People in Line Average of %d" % number_of_av_simulations)
    plt.xlabel("Probability Increment")
    plt.ylabel("Percentage of Mean of Customers in Line at %d Epochs" % number_of_epochs_for_simulation)
    plt.plot(x_axis, sens_analysis_list_of_customers_in_line_CUSTOMER, 'g^', \
             x_axis, sens_analysis_list_of_customers_in_line_CASHIER, 'bs', \
             x_axis, sens_analysis_list_of_customers_in_line_EQUAL, 'ro')
    plt.savefig("analysis_images\itemNumb_sens_analysis_list_of_customers_in_line_%d.png" % number_of_people)

    plt.figure(11)
    plt.clf()
    plt.title("Sensitivity Customers in Queue Average of %d" % number_of_av_simulations)
    plt.xlabel("Probability Increment")
    plt.ylabel(
        "Percentage of Mean of Cashiers on Queue in the End of Simulation at %d Epochs" % number_of_epochs_for_simulation)
    plt.plot(x_axis, sens_analysis_list_of_customers_on_cashier_queue_CUSTOMER, 'g^', \
             x_axis, sens_analysis_list_of_customers_on_cashier_queue_CASHIER, 'bs', \
             x_axis, sens_analysis_list_of_customers_on_cashier_queue_EQUAL, 'ro')
    plt.savefig("analysis_images\itemNumb_sens_analysis_list_of_customers_on_cashier_queue_%d.png" % number_of_people)

    plt.figure(12)
    plt.clf()
    plt.title("Sensitivity Analysis for Items Checked Average of %d" % number_of_av_simulations)
    plt.xlabel("Probability Increment")
    plt.ylabel("Mean of Items checkedout at %d Epochs" % number_of_epochs_for_simulation)
    plt.plot(x_axis, sens_analysis_list_of_customer_items_checked_CUSTOMER, 'g^', \
             x_axis, sens_analysis_list_of_customer_items_checked_CASHIER, 'bs', \
             x_axis, sens_analysis_list_of_customer_items_checked_EQUAL, 'ro')
    plt.savefig("analysis_images\itemNumb_sens_analysis_list_of_items_checked_%d.png" % number_of_people)


def sensitivity_itemNumb_analysis(number_of_epochs_for_simulation, model_name, number_of_av_simulations,
                                  sensitivity_range, \
                                  number_of_people=150):
    """ Sensitivity related to the number of items in the customer's cashier, test for specific model type

    Precondition:
    - number_of_epochs_for_simulation: number of epochs used to run the simulation
    - model_name,number_of_av_simulations: name of the model used during the test
        - Chosen between "equal", "cashier", and "customer"
    - sensitivity_range: range of sensitivity to be tested
    - number_of_people: Number of people to go into the system begin. Default = 100

    Postcondition:
    - sens_analysis_list_of_customers_out_of_system: an int list of the average total number of
    customers out of system at the end of the simulation
    - sens_analysis_list_of_customers_in_line: an int list of the average customers in line
     at the end of the simulation
    - sens_analysis_list_of_customers_on_cashier_queue: an int list of the average customers on 
    queues at the end of the simulation
    - sens_analysis_list_of_customer_items_checked: an int list of the average total items checked
     at the end of the simulation
    """

    # Sets up analysis list
    sens_analysis_list_of_customers_out_of_system = []
    sens_analysis_list_of_customers_in_line = []
    sens_analysis_list_of_customers_on_cashier_queue = []
    sens_analysis_list_of_customer_items_checked = []

    # Loops between sensitivities
    # 0.8 -> 0.95
    for item_iterator in range(sensitivity_range):

        sens_customers_out_of_system_average = 0
        sens_customers_in_line_average = 0
        sens_customers_on_cashier_queue_average = 0
        sens_items_customer_checked_average = 0

        # Number of simulations used for average of simulation
        for i in range(number_of_av_simulations):
            self_check_model = model(model_name, number_of_people, 10, 6, cashier_IPM_p_influence=0,
                                     item_creation_sensitivity=(item_iterator - (sensitivity_range / 2)) / 100)

            list_of_customers_out_of_system, \
            list_of_customers_in_line, \
            list_of_customers_on_cashier_queue, \
            list_of_items_checked, \
            cost_for_maintenance \
                = self_check_model.execute_simulation(number_of_epochs_for_simulation, show=False, showAnim=False)

            # Adds to average
            sens_customers_out_of_system_average = sens_customers_out_of_system_average \
                                                   + list_of_customers_out_of_system[-1]

            sens_customers_in_line_average = sens_customers_in_line_average \
                                             + list_of_customers_in_line[-1]

            sens_customers_on_cashier_queue_average = sens_customers_on_cashier_queue_average \
                                                      + list_of_customers_on_cashier_queue[-1]

            sens_items_customer_checked_average = sens_items_customer_checked_average \
                                                  + list_of_items_checked[0] - list_of_items_checked[-1]
        # Calulates average
        sens_customers_out_of_system_average = sens_customers_out_of_system_average / number_of_av_simulations
        sens_customers_in_line_average = sens_customers_in_line_average / number_of_av_simulations
        sens_customers_on_cashier_queue_average = sens_customers_on_cashier_queue_average / number_of_av_simulations
        sens_items_customer_checked_average = sens_items_customer_checked_average / number_of_av_simulations

        sens_customers_out_of_system_average = sens_customers_out_of_system_average / number_of_people
        sens_customers_in_line_average = sens_customers_in_line_average / number_of_people
        sens_customers_on_cashier_queue_average = sens_customers_on_cashier_queue_average / number_of_people

        # Appends to average list
        sens_analysis_list_of_customers_out_of_system.append(sens_customers_out_of_system_average)
        sens_analysis_list_of_customers_in_line.append(sens_customers_in_line_average)
        sens_analysis_list_of_customers_on_cashier_queue.append(sens_customers_on_cashier_queue_average)
        sens_analysis_list_of_customer_items_checked.append(sens_items_customer_checked_average)

    return sens_analysis_list_of_customers_out_of_system, sens_analysis_list_of_customers_in_line, \
           sens_analysis_list_of_customers_on_cashier_queue, sens_analysis_list_of_customer_items_checked


def sensitivity_chitchatness_analysis_for_all_lines(number_of_epochs_for_simulation, number_of_av_simulations=200, \
                                                    sensitivity_range=30, number_of_people=100):
    """ Sensitivity related to the chitchatness of cashier, test for all models type

    Precondition:
    - number_of_epochs_for_simulation: number of epochs each simulation is going to
    be ran for
    - number_of_av_simulations: Numbe of simulations that are going to be ran to
    calculate the average. Default = 200
    - sensitivity_range: Range for the sensitivity test. Default = 10
    - number_of_people: number of people to enter the system. Default = 100

    Postcondition:
    - 4 png images saved to a file called "analysis_images"
        - x-axis has the sensitivity test
        - y-axis has the quantity related to the test
        - Related to the outputs printed at the test.
    """

    # Numbers for simulation
    x_axis = np.arange(sensitivity_range) / 10

    # Runs simulations with the different types of line:
    sens_analysis_list_of_customers_out_of_system_CUSTOMER, sens_analysis_list_of_customers_in_line_CUSTOMER, \
    sens_analysis_list_of_customers_on_cashier_queue_CUSTOMER, sens_analysis_list_of_customer_items_checked_CUSTOMER = \
        sensitivity_chitchatness_analysis(number_of_epochs_for_simulation, "customer", number_of_av_simulations,
                                          sensitivity_range, \
                                          number_of_people=number_of_people)

    sens_analysis_list_of_customers_out_of_system_CASHIER, sens_analysis_list_of_customers_in_line_CASHIER, \
    sens_analysis_list_of_customers_on_cashier_queue_CASHIER, sens_analysis_list_of_customer_items_checked_CASHIER = \
        sensitivity_chitchatness_analysis(number_of_epochs_for_simulation, "cashier", number_of_av_simulations,
                                          sensitivity_range, \
                                          number_of_people=number_of_people)

    sens_analysis_list_of_customers_out_of_system_EQUAL, sens_analysis_list_of_customers_in_line_EQUAL, \
    sens_analysis_list_of_customers_on_cashier_queue_EQUAL, sens_analysis_list_of_customer_items_checked_EQUAL = \
        sensitivity_chitchatness_analysis(number_of_epochs_for_simulation, "equal", number_of_av_simulations,
                                          sensitivity_range, \
                                          number_of_people=number_of_people)

    # Prints number of customers out of system
    plt.figure(10)
    plt.clf()
    plt.title("Sensitivity Analysis for Customers Out of the System")
    plt.xlabel("Probability Increment")
    plt.ylabel("Percentage of Mean of Customers Out of System at %d Epochs" % number_of_epochs_for_simulation)
    plt.plot(x_axis, sens_analysis_list_of_customers_out_of_system_CUSTOMER, 'g^', \
             x_axis, sens_analysis_list_of_customers_out_of_system_CASHIER, 'bs', \
             x_axis, sens_analysis_list_of_customers_out_of_system_EQUAL, 'ro')
    plt.savefig("analysis_images\chitchatness_sens_analysis_list_of_customers_out_of_system_%d.png" % number_of_people)

    plt.figure(11)
    plt.clf()
    plt.title("Sensitivity Analysis for People in Line Average of %d" % number_of_av_simulations)
    plt.xlabel("Probability Increment")
    plt.ylabel("Percentage of Mean of Customers in Line at %d Epochs" % number_of_epochs_for_simulation)
    plt.plot(x_axis, sens_analysis_list_of_customers_in_line_CUSTOMER, 'g^', \
             x_axis, sens_analysis_list_of_customers_in_line_CASHIER, 'bs', \
             x_axis, sens_analysis_list_of_customers_in_line_EQUAL, 'ro')
    plt.savefig("analysis_images\chitchatness_sens_analysis_list_of_customers_in_line_%d.png" % number_of_people)

    plt.figure(12)
    plt.clf()
    plt.title("Sensitivity Customers in Queue Average of %d" % number_of_av_simulations)
    plt.xlabel("Probability Increment")
    plt.ylabel(
        "Percentage of Mean of Cashiers on Queue in the End of Simulation at %d Epochs" % number_of_epochs_for_simulation)
    plt.plot(x_axis, sens_analysis_list_of_customers_on_cashier_queue_CUSTOMER, 'g^', \
             x_axis, sens_analysis_list_of_customers_on_cashier_queue_CASHIER, 'bs', \
             x_axis, sens_analysis_list_of_customers_on_cashier_queue_EQUAL, 'ro')
    plt.savefig(
        "analysis_images\chitchatness_sens_analysis_list_of_customers_on_cashier_queue_%d.png" % number_of_people)

    plt.figure(13)
    plt.clf()
    plt.title("Sensitivity Analysis for Items Checked Average of %d" % number_of_av_simulations)
    plt.xlabel("Probability Increment")
    plt.ylabel("Mean of Items checkedout at %d Epochs" % number_of_epochs_for_simulation)
    plt.plot(x_axis, sens_analysis_list_of_customer_items_checked_CUSTOMER, 'g^', \
             x_axis, sens_analysis_list_of_customer_items_checked_CASHIER, 'bs', \
             x_axis, sens_analysis_list_of_customer_items_checked_EQUAL, 'ro')
    plt.savefig("analysis_images\chitchatness_sens_analysis_list_of_items_checked_%d.png" % number_of_people)


def sensitivity_chitchatness_analysis(number_of_epochs_for_simulation, model_name, number_of_av_simulations,
                                      sensitivity_range, \
                                      number_of_people=150):
    '''
    '''

    # Sets up analysis list
    sens_analysis_list_of_customers_out_of_system = []
    sens_analysis_list_of_customers_in_line = []
    sens_analysis_list_of_customers_on_cashier_queue = []
    sens_analysis_list_of_customer_items_checked = []

    # Loops between sensitivities
    # 0.8 -> 0.95
    for item_iterator in range(sensitivity_range):

        sens_customers_out_of_system_average = 0
        sens_customers_in_line_average = 0
        sens_customers_on_cashier_queue_average = 0
        sens_items_customer_checked_average = 0

        # Number of simulations used for average of simulation
        for i in range(number_of_av_simulations):
            self_check_model = model(model_name, number_of_people, 10, 0, cashier_IPM_p_influence=0,
                                     chitchatness_influence=(item_iterator / 100))

            list_of_customers_out_of_system, \
            list_of_customers_in_line, \
            list_of_customers_on_cashier_queue, \
            list_of_items_checked, \
            cost_for_maintenance \
                = self_check_model.execute_simulation(number_of_epochs_for_simulation, show=False, showAnim=False)

            # Adds to average
            sens_customers_out_of_system_average = sens_customers_out_of_system_average \
                                                   + list_of_customers_out_of_system[-1]

            sens_customers_in_line_average = sens_customers_in_line_average \
                                             + list_of_customers_in_line[-1]

            sens_customers_on_cashier_queue_average = sens_customers_on_cashier_queue_average \
                                                      + list_of_customers_on_cashier_queue[-1]

            sens_items_customer_checked_average = sens_items_customer_checked_average \
                                                  + list_of_items_checked[0] - list_of_items_checked[-1]
        # Calulates average
        sens_customers_out_of_system_average = sens_customers_out_of_system_average / number_of_av_simulations
        sens_customers_in_line_average = sens_customers_in_line_average / number_of_av_simulations
        sens_customers_on_cashier_queue_average = sens_customers_on_cashier_queue_average / number_of_av_simulations
        sens_items_customer_checked_average = sens_items_customer_checked_average / number_of_av_simulations

        sens_customers_out_of_system_average = sens_customers_out_of_system_average / number_of_people
        sens_customers_in_line_average = sens_customers_in_line_average / number_of_people
        sens_customers_on_cashier_queue_average = sens_customers_on_cashier_queue_average / number_of_people

        # Appends to average list
        sens_analysis_list_of_customers_out_of_system.append(sens_customers_out_of_system_average)
        sens_analysis_list_of_customers_in_line.append(sens_customers_in_line_average)
        sens_analysis_list_of_customers_on_cashier_queue.append(sens_customers_on_cashier_queue_average)
        sens_analysis_list_of_customer_items_checked.append(sens_items_customer_checked_average)

    return sens_analysis_list_of_customers_out_of_system, sens_analysis_list_of_customers_in_line, \
           sens_analysis_list_of_customers_on_cashier_queue, sens_analysis_list_of_customer_items_checked
