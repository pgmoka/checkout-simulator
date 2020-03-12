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
# ============================= Imports =================================
# =======================================================================

# Python modules
import numpy as np
import matplotlib.pyplot as plt
from os.path import join

# Create simulation code
import variables as v
from model import model
from fullday_model import Fullday

# =======================================================================
# =============================== Methods ===============================
# =======================================================================


# ----------------------------- Mean, Lag, Lag Analysis ---------------------------


def mean_values(number_of_epochs_for_simulation, model_name="equal",
                number_of_av_simulations=200, number_of_people=100,
                configCashiers=10, configSelfCheck=10, show=False):
    mean_cust_left = np.zeros(number_of_epochs_for_simulation)
    mean_cust_waiting = np.zeros(number_of_epochs_for_simulation)
    mean_cust_queue = np.zeros(number_of_epochs_for_simulation)
    mean_items_checked = np.zeros(number_of_epochs_for_simulation)
    mean_maintenance = np.zeros(number_of_epochs_for_simulation)
    for j in range(number_of_av_simulations):
        self_check_model = model(model_name, number_of_people, configCashiers, configSelfCheck,
                                 cashier_IPM_p_influence=0.1,
                                 customer_IPM_p_influence=0.2)
        customers_left, \
        customers_in_line, \
        customers_in_queue, \
        items_checked, \
        maintenance_costs \
            = self_check_model.execute_simulation(number_of_epochs_for_simulation,
                                                  show=False, showAnim=False)

        mean_cust_left += np.array(customers_left)
        mean_cust_waiting += np.array(customers_in_line)
        mean_cust_queue += np.array(customers_in_queue)
        mean_items_checked += np.array(items_checked)
        mean_maintenance += np.array(maintenance_costs)

    mean_cust_left /= number_of_av_simulations
    mean_cust_waiting /= number_of_av_simulations
    mean_cust_queue /= number_of_av_simulations
    mean_items_checked /= number_of_av_simulations
    mean_maintenance /= number_of_av_simulations

    if show:
        plot_means(model_name, number_of_epochs_for_simulation, \
               mean_cust_left, mean_cust_waiting, mean_cust_queue, \
               mean_items_checked, mean_maintenance)

    return model_name, number_of_epochs_for_simulation, \
           mean_cust_left, mean_cust_waiting, mean_cust_queue, \
           mean_items_checked, mean_maintenance


def plot_means(model_name, number_of_epochs_for_simulation,
               mean_cust_left, mean_cust_waiting, mean_cust_queue,
               mean_items_checked, mean_maintenance):
    plt.figure(1)
    plt.clf()
    plt.title("Mean Values for Customers Out of System")
    plt.xlabel("Number of Epochs")
    plt.ylabel("Mean of Customers Out of System")
    plt.plot(np.array([x for x in range(number_of_epochs_for_simulation)]),
             mean_cust_left)
    plt.savefig(join("analysis_images", "mean", model_name + "_mean_cust_out_" +
                     str(number_of_epochs_for_simulation) + "_epochs.png"))

    plt.figure(2)
    plt.clf()
    plt.title("Mean Values for Customers In Queues")
    plt.xlabel("Number of Epochs")
    plt.ylabel("Mean of Customers Being Helped")
    plt.plot(np.array([x for x in range(number_of_epochs_for_simulation)]),
             mean_cust_queue)
    plt.savefig(join("analysis_images", "mean", model_name + "_mean_cust_in_queue_" +
                     str(number_of_epochs_for_simulation) + "_epochs.png"))

    plt.figure(3)
    plt.clf()
    plt.title("Mean Values for Items Checked")
    plt.xlabel("Number of Epochs")
    plt.ylabel("Items Checked")
    plt.plot(np.array([x for x in range(number_of_epochs_for_simulation)]),
             mean_items_checked)
    plt.savefig(join("analysis_images", "mean", model_name + "_mean_items_checked_" +
                     str(number_of_epochs_for_simulation) + "_epochs.png"))

    plt.figure(4)
    plt.clf()
    plt.title("Mean Values for Maintenance Costs")
    plt.xlabel("Number of Epochs")
    plt.ylabel("Mean of Maintenance Costs")
    plt.plot(np.array([x for x in range(number_of_epochs_for_simulation)]),
             mean_maintenance)
    plt.savefig(join("analysis_images", "mean", model_name + "_mean_maintenance_" +
                     str(number_of_epochs_for_simulation) + "_epochs.png"))


def lag_correlation_analysis(number_of_epochs_for_simulation,
                number_of_av_simulations=200, number_of_people=100,
                configCashiers=10, configSelfCheck=10, size_lag=10):
    models = ['equal', 'cashier', 'customer']

    for i in range(len(models)):
        model_name = models[i]
        a, b, cust_left, cust_waiting, cust_queue, items_checked, maintenance = \
            mean_values(number_of_epochs_for_simulation, model_name,number_of_av_simulations,
                    number_of_people, configCashiers, configSelfCheck, False)

        lag_correlation_plot(cust_left, title="Customers Left", model_name=model_name)
        lag_correlation_plot(cust_queue, title="Customers In Queues", model_name=model_name)
        lag_correlation_plot(cust_left, title="Items Checked", model_name=model_name)
        lag_correlation_plot(cust_left, title="Maintenance Costs", model_name=model_name)


def lag_correlation_plot(a, b, size_lag=10, title="", model_name=""):
    lagCorrelationZero = [correlate(np.array(a), np.array(a))]
    lagCorrelationPos = []
    lagCorrelationNeg = []
    lagNeg = []
    lagPos = []
    for i in range(size_lag, 0, -1):
        lagCorrelationNeg.append(correlate(np.array(a[i:-1]), np.array(a[1:-i])))
        lagNeg.append(i * -1)
    for i in range(1, size_lag + 1):
        lagPos.append(i)
        lagCorrelationPos.append(correlate(np.array(a[1:-i]), np.array(a[i:-1])))
    plt.figure(1)
    plt.clf()
    # Plot the array
    plt.plot(np.concatenate([np.array(lagNeg), np.array([0]), np.array(lagPos)]),
             np.concatenate([np.array(lagCorrelationNeg), np.array(lagCorrelationZero), np.array(lagCorrelationPos)]),
             '-')
    # Add an x-label
    plt.xlabel("Lag")
    # Add a y-label
    plt.ylabel("Correlation")
    plt.title(title)
    plt.savefig(join("analysis_images", "lag", model_name + "_" + title +  ".png"))


def average(x):
    return np.sum(x) / float(np.size(x))


def variance(x):
    temp = (x - average(x)) ** 2
    temp = np.sum(temp)
    return temp / (np.size(x) - 1)


def correlate(x, y):
    num = np.sum((x - average(x)) * (y - average(y)))
    den = (np.size(x) - 1) * np.sqrt(variance(x) * np.sqrt(variance(y)))
    return num / den


# ----------------------------- Configuration ---------------------------


def configuration(number_of_epochs_for_simulation, number_of_av_simulations=200,
                  sensitivity_range=10, number_of_people=100):
    """ Makes tests relative to config, involving:
        - Number of customers out of system
        - Number of customers in queue
        - Number checked items
        - Costs of Maintenance

        This will be preformed for all types of lines.

        Precondition:
        - number_of_epochs_for_simulation: number of epochs each simulation is going to
        be ran for
        - number_of_av_simulations: Numbe of simulations that are going to be ran to
        calculate the average. Default = 200
        - sensitivity_range: Range for the sensitivity test. Default = 10
        - number_of_people: number of people to enter the system. Default = 100

        Postcondition:
        - 4 png images stored inside analysis_images/configuration that will show
            the final average results of an average of a set number of tests for
            a certain configuration.
    """

    # Preform tests using equal distribution line
    for k in range(1, 5):
        sensitivity_cashiers_to_self_checkout(number_of_epochs_for_simulation, "equal",
                                              number_of_av_simulations, sensitivity_range, number_of_people, 3 * k)

    # Preform tests using customer line
    for k in range(1, 5):
        sensitivity_cashiers_to_self_checkout(number_of_epochs_for_simulation, "customer",
                                              number_of_av_simulations, sensitivity_range, number_of_people, 3 * k)

    # Preform tests using cashier line
    for k in range(1, 5):
        sensitivity_cashiers_to_self_checkout(number_of_epochs_for_simulation, "cashier",
                                              number_of_av_simulations, sensitivity_range, number_of_people, 3 * k)
    print("Test complete")


def sensitivity_cashiers_to_self_checkout(number_of_epochs_for_simulation, model_name, number_of_av_simulations,
                                          sensitivity_range=10, number_of_people=100, cashiers_to_self_checkouts=3):
    ''' Preform a number of tests and gather the average values for each tracked
        piece of data.


        Precondition:
        - number_of_epochs_for_simulation: number of epochs each simulation is going to
        be ran for
        - number_of_av_simulations: Numbe of simulations that are going to be ran to
        calculate the average. Default = 200
        - sensitivity_range: Range for the sensitivity test. Default = 10
        - number_of_people: number of people to enter the system. Default = 100
        - cashiers_to_self_checkouts: The number of self checkouts to replace a single
        cashier with. Default = 3

        Postcondition:
        - 5 png images stored inside analysis_images/configuration that will show
            the final average results of an average of a set number of tests for
            a certain configuration.
    '''
    # Create a set of variables to store averages and time
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

        # Run a number of simulations to get the average
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
            # Add the average to the array
            cust_left.append(customers_left[-1])
            maintenance.append(maintenance_costs)
            items.append(items_checked[-1])
            cust_line.append(customers_in_line[-1])
            cust_queue.append(customers_in_queue[-1])

        # Return the average of this configuration into an array
        avg_num_cust_left.append(sum(cust_left) / number_of_av_simulations)
        avg_num_cust_being_helped.append(sum(cust_queue) / number_of_av_simulations)
        avg_num_items_checked.append(sum(items) / number_of_av_simulations)
        avg_num_maintenance.append(sum(maintenance) / number_of_av_simulations)
        avg_num_cust_not_in_line.append(sum(cust_line) / number_of_av_simulations)

    # Plot each set of data
    plt.figure(1)
    plt.clf()
    plt.title("Sensitivity Analysis for Customers Helped with Different Configurations")
    plt.xlabel("Cashiers Operating Self Checkouts")
    plt.ylabel("Mean of Customers Out of System at %d" % number_of_epochs_for_simulation)
    plt.plot(num_self_checkouts, avg_num_cust_left)
    plt.savefig(join("analysis_images", "configuration", model_name +
                     "_cashier_to_" + str(cashiers_to_self_checkouts) +
                     "_checkouts_list_of_customers_out_of_system.png"))

    plt.figure(2)
    plt.clf()
    plt.title("Sensitivity Analysis for Customers Waiting with Different Configurations")
    plt.xlabel("Cashiers Operating Self Checkouts")
    plt.ylabel("Mean of Customers Waiting at %d" % number_of_epochs_for_simulation)
    plt.plot(num_self_checkouts, avg_num_cust_not_in_line)
    plt.savefig(join("analysis_images", "configuration", model_name +
                     "_cashier_to_" + str(cashiers_to_self_checkouts) +
                     "_checkouts_list_of_cust_waiting.png"))

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
    """ Sensitivity related to the number of cashier chitchatness, test for specific model type

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


def sensitivity_customer_number_analysis_for_all_lines(number_of_epochs_for_simulation, number_of_av_simulations=200, \
                                                       sensitivity_range=80, number_of_people=100):
    """ Sensitivity related number of customers in the system, test for all models type

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
    x_axis = np.arange(sensitivity_range)

    # Runs simulations with the different types of line:
    sens_analysis_list_of_customers_out_of_system_CUSTOMER, sens_analysis_list_of_customers_in_line_CUSTOMER, \
    sens_analysis_list_of_customers_on_cashier_queue_CUSTOMER, sens_analysis_list_of_customer_items_checked_CUSTOMER = \
        sensitivity_number_of_customers_analysis(number_of_epochs_for_simulation, "customer", number_of_av_simulations,
                                                 sensitivity_range, \
                                                 number_of_people=number_of_people)

    sens_analysis_list_of_customers_out_of_system_CASHIER, sens_analysis_list_of_customers_in_line_CASHIER, \
    sens_analysis_list_of_customers_on_cashier_queue_CASHIER, sens_analysis_list_of_customer_items_checked_CASHIER = \
        sensitivity_number_of_customers_analysis(number_of_epochs_for_simulation, "cashier", number_of_av_simulations,
                                                 sensitivity_range, \
                                                 number_of_people=number_of_people)

    sens_analysis_list_of_customers_out_of_system_EQUAL, sens_analysis_list_of_customers_in_line_EQUAL, \
    sens_analysis_list_of_customers_on_cashier_queue_EQUAL, sens_analysis_list_of_customer_items_checked_EQUAL = \
        sensitivity_number_of_customers_analysis(number_of_epochs_for_simulation, "equal", number_of_av_simulations,
                                                 sensitivity_range, \
                                                 number_of_people=number_of_people)

    # Prints number of customers out of system
    plt.figure(14)
    plt.clf()
    plt.title("Sensitivity Analysis for Customers Out of the System")
    plt.xlabel("Increment in the Number of Customers")
    plt.ylabel("Percentage of Mean of Customers Out of System at %d Epochs" % number_of_epochs_for_simulation)
    plt.plot(x_axis, sens_analysis_list_of_customers_out_of_system_CUSTOMER, 'g', \
             x_axis, sens_analysis_list_of_customers_out_of_system_CASHIER, 'b', \
             x_axis, sens_analysis_list_of_customers_out_of_system_EQUAL, 'r')
    plt.savefig(
        "analysis_images\\number_of_customers_sens_analysis_list_of_customers_out_of_system_%d.png" % number_of_people)

    plt.figure(15)
    plt.clf()
    plt.title("Sensitivity Analysis for People in Line Average of %d" % number_of_av_simulations)
    plt.xlabel("Increment in the Number of Customers")
    plt.ylabel("Percentage of Mean of Customers in Line at %d Epochs" % number_of_epochs_for_simulation)
    plt.plot(x_axis, sens_analysis_list_of_customers_in_line_CUSTOMER, 'g', \
             x_axis, sens_analysis_list_of_customers_in_line_CASHIER, 'b', \
             x_axis, sens_analysis_list_of_customers_in_line_EQUAL, 'r')
    plt.savefig(
        "analysis_images\\number_of_customers_sens_analysis_list_of_customers_in_line_%d.png" % number_of_people)

    plt.figure(16)
    plt.clf()
    plt.title("Sensitivity Customers in Queue Average of %d" % number_of_av_simulations)
    plt.xlabel("Increment in the Number of Customers")
    plt.ylabel(
        "Percentage of Mean of Cashiers on Queue in the End of Simulation at %d Epochs" % number_of_epochs_for_simulation)
    plt.plot(x_axis, sens_analysis_list_of_customers_on_cashier_queue_CUSTOMER, 'g', \
             x_axis, sens_analysis_list_of_customers_on_cashier_queue_CASHIER, 'b', \
             x_axis, sens_analysis_list_of_customers_on_cashier_queue_EQUAL, 'r')
    plt.savefig(
        "analysis_images\\number_of_customers_sens_analysis_list_of_customers_on_cashier_queue_%d.png" % number_of_people)

    plt.figure(17)
    plt.clf()
    plt.title("Sensitivity Analysis for Items Checked Average of %d" % number_of_av_simulations)
    plt.xlabel("Increment in the Number of Customers")
    plt.ylabel("Mean of Items checkedout at %d Epochs" % number_of_epochs_for_simulation)
    plt.plot(x_axis, sens_analysis_list_of_customer_items_checked_CUSTOMER, 'g', \
             x_axis, sens_analysis_list_of_customer_items_checked_CASHIER, 'b', \
             x_axis, sens_analysis_list_of_customer_items_checked_EQUAL, 'r')
    plt.savefig("analysis_images\\number_of_customers_sens_analysis_list_of_items_checked_%d.png" % number_of_people)


def sensitivity_number_of_customers_analysis(number_of_epochs_for_simulation, model_name, number_of_av_simulations,
                                             sensitivity_range, \
                                             number_of_people=150):
    """ Sensitivity related to the number of customers in the system, test for specific model type

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
            self_check_model = model(model_name, number_of_people + (item_iterator), 10, 0)

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


def full_day_analysis_frontLoaded():
    """

    """
    #list_of_customers_out_of_system
    #list_of_customers_in_line
    #list_of_customers_on_cashier_queue
    #list_of_items_checked

    # run full day simulation for all three line types
    equal = Fullday('equal', 6, 4, day_type='front')
    customer = Fullday('customer', 6, 4, day_type='front')
    cashier = Fullday('cashier', 6, 4, day_type='front')
    equal.execute_simulation()
    customer.execute_simulation()
    cashier.execute_simulation()

    customers_out = plt.plot(equal.list_of_customers_out_of_system,
                            'r',
                            customer.list_of_customers_out_of_system,
                            'b',
                            cashier.list_of_customers_out_of_system,
                            'g')
    plt.xlabel("Time in epochs (4 second increments)")
    plt.ylabel("Customers who have left the store")
    plt.title("Customers out of the system over a full day")
    plt.legend(["Equal Line", "Customer select line", "Cashier select line"])
    plt.savefig("customers_out_frontloaded.png")
    plt.show()

    customers_in_line = plt.plot(equal.list_of_customers_in_line,
                                 'r',
                                 customer.list_of_customers_in_line,
                                 'b',
                                 cashier.list_of_customers_in_line,
                                 'g')
    plt.legend(["Equal Line", "Customer select line", "Cashier select line"])
    plt.xlabel("Time in epochs (4 second increments)")
    plt.ylabel("Customers not line")
    plt.title("Customers not in line over time")
    plt.savefig("customers_not_line_frontloaded.png")
    plt.show()

    customer_in_queue = plt.plot(equal.list_of_customers_on_cashier_queue,
                                 'r',
                                 customer.list_of_customers_on_cashier_queue,
                                 'b',
                                 cashier.list_of_customers_on_cashier_queue,
                                 'g')
    plt.legend(["Equal Line", "Customer select line", "Cashier select line"])
    plt.xlabel("Time in epochs (4 second increments)")
    plt.ylabel("Customers in specific cashier queues")
    plt.title("Customers in line over time")
    plt.savefig("customers_in_queue_frontloaded.png")
    plt.show()

    items_check = plt.plot(equal.list_of_items_checked, 'r',
                           customer.list_of_items_checked, 'b',
                           cashier.list_of_items_checked, 'g')

    plt.legend(["Equal Line", "Customer select line", "Cashier select line"])
    plt.xlabel("Time in epochs (4 second increments)")
    plt.ylabel("Numer of items scanned out of the store")
    plt.title("Items scanned out of the store over time")
    plt.savefig("items_out_frontloaded.png")
    plt.show()



def full_day_analysis_backLoaded():
    """

    """
    #run full day simulation for all three line types
    equal = Fullday('equal', 6, 4, day_type='back')
    customer = Fullday('customer', 6, 4, day_type='back')
    cashier = Fullday('cashier', 6, 4, day_type='back')
    equal.execute_simulation()
    customer.execute_simulation()
    cashier.execute_simulation()


    time_axis = np.arange(start=9, step=(12 * 60 * v.TIME_STEP))
    customers_out = plt.plot(equal.list_of_customers_out_of_system,
                            'r',
                            customer.list_of_customers_out_of_system,
                            'b',
                            cashier.list_of_customers_out_of_system,
                            'g')

    plt.xlabel("Time in epochs (4 second increments)")
    plt.ylabel("Customers who have left the store")
    plt.title("Customers out of the system over a full day")
    plt.legend(["Equal Line", "Customer select line", "Cashier select line"])
    plt.savefig("customers_out_backloaded.png")
    plt.show()

    customers_in_line = plt.plot(equal.list_of_customers_in_line,
                                 'r',
                                 customer.list_of_customers_in_line,
                                 'b',
                                 cashier.list_of_customers_in_line,
                                 'g')
    plt.legend(["Equal Line", "Customer select line", "Cashier select line"])
    plt.xlabel("Time in epochs (4 second increments)")
    plt.ylabel("Customers not line")
    plt.title("Customers not in line over time")
    plt.savefig("customers_not_line_backloaded.png")
    plt.show()

    customer_in_queue = plt.plot(equal.list_of_customers_on_cashier_queue,
                                 'r',
                                 customer.list_of_customers_on_cashier_queue,
                                 'b',
                                 cashier.list_of_customers_on_cashier_queue,
                                 'g')
    plt.legend(["Equal Line", "Customer select line", "Cashier select line"])
    plt.xlabel("Time in epochs (4 second increments)")
    plt.ylabel("Customers in specific cashier queues")
    plt.title("Customers in line over time")
    plt.savefig("customers_in_queue_backloaded.png")
    plt.show()

    items_check = plt.plot(equal.list_of_items_checked, 'r',
                           customer.list_of_items_checked, 'b',
                           cashier.list_of_items_checked, 'g')

    plt.legend(["Equal Line", "Customer select line", "Cashier select line"])
    plt.xlabel("Time in epochs (4 second increments)")
    plt.ylabel("Numer of items scanned out of the store")
    plt.title("Items scanned out of the store over time")
    plt.savefig("items_out_backloaded.png")
    plt.show()


def full_day_analysis_normal():
    """

    """

    # run full day simulation for all three line types
    equal = Fullday('equal', 6, 4)
    customer = Fullday('customer', 6, 4)
    cashier = Fullday('cashier', 6, 4)
    equal.execute_simulation()
    customer.execute_simulation()
    cashier.execute_simulation()

    time_axis = np.arange(start=9, step=(12 * 60 * v.TIME_STEP))

    customers_out = plt.plot(equal.list_of_customers_out_of_system,
                            'r',
                            customer.list_of_customers_out_of_system,
                            'b',
                            cashier.list_of_customers_out_of_system,
                            'g')
    plt.xlabel("Time in epochs (4 second increments)")
    plt.ylabel("Customers who have left the store")
    plt.title("Customers out of the system over a full day")
    plt.legend(["Equal Line", "Customer select line", "Cashier select line"])
    plt.savefig("customers_out_normal.png")
    plt.show()

    customers_in_line = plt.plot(equal.list_of_customers_in_line,
                                 'r',
                                 customer.list_of_customers_in_line,
                                 'b',
                                 cashier.list_of_customers_in_line,
                                 'g')
    plt.legend(["Equal Line", "Customer select line", "Cashier select line"])
    plt.xlabel("Time in epochs (4 second increments)")
    plt.ylabel("Customers not line")
    plt.title("Customers not in line over time")
    plt.savefig("customers_not_line_normal.png")
    plt.show()

    customer_in_queue = plt.plot(equal.list_of_customers_on_cashier_queue,
                                 'r',
                                 customer.list_of_customers_on_cashier_queue,
                                 'b',
                                 cashier.list_of_customers_on_cashier_queue,
                                 'g')

    plt.legend(["Equal Line", "Customer select line", "Cashier select line"])
    plt.xlabel("Time in epochs (4 second increments)")
    plt.ylabel("Customers in specific cashier queues")
    plt.title("Customers in line over time")
    plt.savefig("customers_in_queue_normal.png")
    plt.show()

    items_check = plt.plot(equal.list_of_items_checked, 'r',
                           customer.list_of_items_checked, 'b',
                           cashier.list_of_items_checked, 'g')

    plt.legend(["Equal Line", "Customer select line", "Cashier select line"])
    plt.xlabel("Time in epochs (4 second increments)")
    plt.ylabel("Numer of items scanned out of the store")
    plt.title("Items scanned out of the store over time")
    plt.savefig("items_out_normal.png")
    plt.show()

