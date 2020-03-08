# =======================================================================
# ============================= Imports==================================
# =======================================================================

# Python modules
import numpy as np
import matplotlib.pyplot as plt

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

def configuration(number_of_epochs_for_simulation):
    """Makes tests relative to config, involving:
        - Number of customers out of system
        - Number of customers in line
        - Number of customers in queue
        - Number checked items
    """

    for k in range(1, 5):
        num_self_checkouts = []
        avg_num_cust_left = []
        cashiers_to_selfcheckout = k * 3

        # Number of cashiers operating self checkouts
        for i in range(10):
            # Number of tests for sensitivity
            num_self_checkouts.append(i)
            cust_left = []
            for j in range(100):
                self_check_model = model("equal", 20, 10 - i, i * cashiers_to_selfcheckout, cashier_IPM_p_influence=0.1, customer_IPM_p_influence=0.2)
                customers_left, \
                customers_in_line, \
                customers_in_queue, \
                items_checked, \
                maintenance_costs \
                    = self_check_model.execute_simulation(number_of_epochs_for_simulation,
                                                          show=False, showAnim=False)
                cust_left.append(customers_left[-1])
            avg_num_cust_left.append(sum(cust_left) / 100)

        plt.figure(1)
        plt.title("Sensitivity Analysis for Customers Out of the System With 1 Cashier Operation " + str(cashiers_to_selfcheckout) + " Self Checkouts")
        plt.xlabel("Cashiers Operating Self Checkouts")
        plt.ylabel("Mean of Customers Out of System at %d" % number_of_epochs_for_simulation)
        plt.plot(num_self_checkouts, avg_num_cust_left)
        plt.show()
    #plt.savefig("sens_analysis_list_of_customers_out_of_system.png")
    print("Test complete")


# ------------------------------- Sensitivity ---------------------------

def sensitivity_chitchatness_analysis(number_of_epochs_for_simulation):
    pass

def sensitivity_cashierIPM_analysis_for_all_lines(number_of_epochs_for_simulation):
    """ Sensitivity related to the IPM of cashier, test for all models type
    """

    # Numbers for simulation
    number_of_av_simulations = 200
    sensitivity_range = 10
    x_axis = np.arange(10)/100

    # Runs simulations with the different types of line:
    sens_analysis_list_of_customers_out_of_system_CUSTOMER, sens_analysis_list_of_customers_in_line_CUSTOMER,\
        sens_analysis_list_of_customers_on_cashier_queue_CUSTOMER, sens_analysis_list_of_customer_items_checked_CUSTOMER =\
            sensitivity_cashierIPM_analysis(number_of_epochs_for_simulation,"customer",number_of_av_simulations,sensitivity_range)

    sens_analysis_list_of_customers_out_of_system_CASHIER, sens_analysis_list_of_customers_in_line_CASHIER,\
        sens_analysis_list_of_customers_on_cashier_queue_CASHIER, sens_analysis_list_of_customer_items_checked_CASHIER =\
            sensitivity_cashierIPM_analysis(number_of_epochs_for_simulation,"cashier",number_of_av_simulations,sensitivity_range)
    
    sens_analysis_list_of_customers_out_of_system_EQUAL, sens_analysis_list_of_customers_in_line_EQUAL,\
        sens_analysis_list_of_customers_on_cashier_queue_EQUAL, sens_analysis_list_of_customer_items_checked_EQUAL=\
            sensitivity_cashierIPM_analysis(number_of_epochs_for_simulation,"equal",number_of_av_simulations,sensitivity_range)

    # Prints number of customers out of system
    plt.figure(1)
    plt.title("Sensitivity Analysis for Customers Out of the System")
    plt.xlabel("Probability Increment")
    plt.ylabel("Percentage of Mean of Customers Out of System at %d Epochs"%number_of_epochs_for_simulation)
    plt.plot(x_axis, sens_analysis_list_of_customers_out_of_system_CUSTOMER,'g^',\
        x_axis, sens_analysis_list_of_customers_out_of_system_CASHIER,'bs',\
        x_axis, sens_analysis_list_of_customers_out_of_system_EQUAL,'ro')
    plt.savefig("analysis_images\cashierIPM_sens_analysis_list_of_customers_out_of_system.png")
    

    plt.figure(2)
    plt.title("Sensitivity Analysis for People in Line Average of %d" %number_of_av_simulations)
    plt.xlabel("Probability Increment")
    plt.ylabel("Percentage of Mean of Customers in Line at %d Epochs"%number_of_epochs_for_simulation)
    plt.plot(x_axis, sens_analysis_list_of_customers_in_line_CUSTOMER,'g^',\
        x_axis, sens_analysis_list_of_customers_in_line_CASHIER,'bs',\
        x_axis, sens_analysis_list_of_customers_in_line_EQUAL,'ro')
    plt.savefig("analysis_images\cashierIPM_sens_analysis_list_of_customers_in_line.png")

    plt.figure(3)
    plt.title("Sensitivity Customers in Queue Average of %d" %number_of_av_simulations)
    plt.xlabel("Probability Increment")
    plt.ylabel("Percentage of Mean of Cashiers on Queue in the End of Simulation at %d Epochs"%number_of_epochs_for_simulation)
    plt.plot(x_axis, sens_analysis_list_of_customers_on_cashier_queue_CUSTOMER,'g^',\
        x_axis, sens_analysis_list_of_customers_on_cashier_queue_CASHIER,'bs',\
        x_axis, sens_analysis_list_of_customers_on_cashier_queue_EQUAL,'ro')
    plt.savefig("analysis_images\cashierIPM_sens_analysis_list_of_customers_on_cashier_queue.png")

    plt.figure(4)
    plt.title("Sensitivity Analysis for Items Checked Average of %d" %number_of_av_simulations)
    plt.xlabel("Probability Increment")
    plt.ylabel("Mean of Items checkedout at %d Epochs"%number_of_epochs_for_simulation)
    plt.plot(x_axis, sens_analysis_list_of_customer_items_checked_CUSTOMER,'g^',\
        x_axis, sens_analysis_list_of_customer_items_checked_CASHIER,'bs',\
        x_axis, sens_analysis_list_of_customer_items_checked_EQUAL,'ro')
    plt.savefig("analysis_images\cashierIPM_sens_analysis_list_of_items_checked.png")

def sensitivity_cashierIPM_analysis(number_of_epochs_for_simulation,model_name,number_of_av_simulations,sensitivity_range):
    """ Sensitivity related to the IPM of cashier, test for specific model type
    """

    # Sets up analysis list
    sens_analysis_list_of_customers_out_of_system = []
    sens_analysis_list_of_customers_in_line = []
    sens_analysis_list_of_customers_on_cashier_queue = []
    sens_analysis_list_of_customer_items_checked = []

    number_of_people = 100
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

        sens_customers_out_of_system_average = sens_customers_out_of_system_average/ number_of_people
        sens_customers_in_line_average = sens_customers_in_line_average/ number_of_people
        sens_customers_on_cashier_queue_average = sens_customers_on_cashier_queue_average/ number_of_people

        # Appends to average list
        sens_analysis_list_of_customers_out_of_system.append(sens_customers_out_of_system_average)
        sens_analysis_list_of_customers_in_line.append(sens_customers_in_line_average)
        sens_analysis_list_of_customers_on_cashier_queue.append(sens_customers_on_cashier_queue_average)
        sens_analysis_list_of_customer_items_checked.append(sens_items_customer_checked_average)

    return sens_analysis_list_of_customers_out_of_system, sens_analysis_list_of_customers_in_line,\
        sens_analysis_list_of_customers_on_cashier_queue, sens_analysis_list_of_customer_items_checked


def sensitivity_customerIPM_analysis_for_all_lines(number_of_epochs_for_simulation):
    """ Sensitivity related to the IPM of customer, test for all models type
    """

    # Numbers for simulation
    number_of_av_simulations = 100
    sensitivity_range = 10
    x_axis = np.arange(10)/100

    # Runs simulations with the different types of line:
    sens_analysis_list_of_customers_out_of_system_CUSTOMER, sens_analysis_list_of_customers_in_line_CUSTOMER,\
        sens_analysis_list_of_customers_on_cashier_queue_CUSTOMER, sens_analysis_list_of_customer_items_checked_CUSTOMER =\
            sensitivity_cashierIPM_analysis(number_of_epochs_for_simulation,"customer",number_of_av_simulations,sensitivity_range)

    sens_analysis_list_of_customers_out_of_system_CASHIER, sens_analysis_list_of_customers_in_line_CASHIER,\
        sens_analysis_list_of_customers_on_cashier_queue_CASHIER, sens_analysis_list_of_customer_items_checked_CASHIER =\
            sensitivity_cashierIPM_analysis(number_of_epochs_for_simulation,"cashier",number_of_av_simulations,sensitivity_range)
    
    sens_analysis_list_of_customers_out_of_system_EQUAL, sens_analysis_list_of_customers_in_line_EQUAL,\
        sens_analysis_list_of_customers_on_cashier_queue_EQUAL, sens_analysis_list_of_customer_items_checked_EQUAL=\
            sensitivity_cashierIPM_analysis(number_of_epochs_for_simulation,"equal",number_of_av_simulations,sensitivity_range)

    # Prints number of customers out of system
    plt.figure(1)
    plt.title("Sensitivity Analysis for Customers Out of the System")
    plt.xlabel("Probability Increment")
    plt.ylabel("Percentage of Mean of Customers Out of System at %d Epochs"%number_of_epochs_for_simulation)
    plt.plot(x_axis, sens_analysis_list_of_customers_out_of_system_CUSTOMER,'g^',\
        x_axis, sens_analysis_list_of_customers_out_of_system_CASHIER,'bs',\
        x_axis, sens_analysis_list_of_customers_out_of_system_EQUAL,'ro')
    plt.savefig("analysis_images\customerIPM_sens_analysis_list_of_customers_out_of_system.png")
    

    plt.figure(2)
    plt.title("Sensitivity Analysis for People in Line Average of %d" %number_of_av_simulations)
    plt.xlabel("Probability Increment")
    plt.ylabel("Percentage of Mean of Customers in Line at %d Epochs"%number_of_epochs_for_simulation)
    plt.plot(x_axis, sens_analysis_list_of_customers_in_line_CUSTOMER,'g^',\
        x_axis, sens_analysis_list_of_customers_in_line_CASHIER,'bs',\
        x_axis, sens_analysis_list_of_customers_in_line_EQUAL,'ro')
    plt.savefig("analysis_images\customerIPM_sens_analysis_list_of_customers_in_line.png")

    plt.figure(3)
    plt.title("Sensitivity Customers in Queue Average of %d" %number_of_av_simulations)
    plt.xlabel("Probability Increment")
    plt.ylabel("Percentage of Mean of Cashiers on Queue in the End of Simulation at %d Epochs"%number_of_epochs_for_simulation)
    plt.plot(x_axis, sens_analysis_list_of_customers_on_cashier_queue_CUSTOMER,'g^',\
        x_axis, sens_analysis_list_of_customers_on_cashier_queue_CASHIER,'bs',\
        x_axis, sens_analysis_list_of_customers_on_cashier_queue_EQUAL,'ro')
    plt.savefig("analysis_images\customerIPM_sens_analysis_list_of_customers_on_cashier_queue.png")

    plt.figure(4)
    plt.title("Sensitivity Analysis for Items Checked Average of %d" %number_of_av_simulations)
    plt.xlabel("Probability Increment")
    plt.ylabel("Mean of Items checkedout at %d Epochs"%number_of_epochs_for_simulation)
    plt.plot(x_axis, sens_analysis_list_of_customer_items_checked_CUSTOMER,'g^',\
        x_axis, sens_analysis_list_of_customer_items_checked_CASHIER,'bs',\
        x_axis, sens_analysis_list_of_customer_items_checked_EQUAL,'ro')
    plt.savefig("analysis_images\customerIPM_sens_analysis_list_of_items_checked.png")



def sensitivity_customerIPM_analysis(number_of_epochs_for_simulation,model_name,number_of_av_simulations,sensitivity_range):
    """ Sensitivity related to the IPM of customer, test for specific model type
    """

    # Sets up analysis list
    sens_analysis_list_of_customers_out_of_system = []
    sens_analysis_list_of_customers_in_line = []
    sens_analysis_list_of_customers_on_cashier_queue = []
    sens_analysis_list_of_customer_items_checked = []

    number_of_people = 240
    # Loops between sensitivities
    for simulation_i in range(sensitivity_range):
        sens_customers_out_of_system_average = 0
        sens_customers_in_line_average = 0
        sens_customers_on_cashier_queue_average = 0
        sens_items_customer_checked_average = 0

        # Number of simulations used for average of simulation
        for i in range(number_of_av_simulations):
            self_check_model = model(model_name, number_of_people, 0, 40, cashier_IPM_p_influence=0,
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

        sens_customers_out_of_system_average = sens_customers_out_of_system_average/ number_of_people
        sens_customers_in_line_average = sens_customers_in_line_average/ number_of_people
        sens_customers_on_cashier_queue_average = sens_customers_on_cashier_queue_average/ number_of_people

        # Appends to average list
        sens_analysis_list_of_customers_out_of_system.append(sens_customers_out_of_system_average)
        sens_analysis_list_of_customers_in_line.append(sens_customers_in_line_average)
        sens_analysis_list_of_customers_on_cashier_queue.append(sens_customers_on_cashier_queue_average)
        sens_analysis_list_of_customer_items_checked.append(sens_items_customer_checked_average)

    return sens_analysis_list_of_customers_out_of_system, sens_analysis_list_of_customers_in_line,\
        sens_analysis_list_of_customers_on_cashier_queue, sens_analysis_list_of_customer_items_checked



def sensitivity_itemNumb_analysis_for_all_lines(number_of_epochs_for_simulation):
    """ Sensitivity related to the number of items, test for all models type
    """

    # Numbers for simulation
    number_of_av_simulations = 200
    sensitivity_range = 30
    x_axis = (np.arange(sensitivity_range)/100) - (sensitivity_range/200)

    # Runs simulations with the different types of line:
    sens_analysis_list_of_customers_out_of_system_CUSTOMER, sens_analysis_list_of_customers_in_line_CUSTOMER,\
        sens_analysis_list_of_customers_on_cashier_queue_CUSTOMER, sens_analysis_list_of_customer_items_checked_CUSTOMER =\
            sensitivity_itemNumb_analysis(number_of_epochs_for_simulation,"customer",number_of_av_simulations,sensitivity_range)

    sens_analysis_list_of_customers_out_of_system_CASHIER, sens_analysis_list_of_customers_in_line_CASHIER,\
        sens_analysis_list_of_customers_on_cashier_queue_CASHIER, sens_analysis_list_of_customer_items_checked_CASHIER =\
            sensitivity_itemNumb_analysis(number_of_epochs_for_simulation,"cashier",number_of_av_simulations,sensitivity_range)
    
    sens_analysis_list_of_customers_out_of_system_EQUAL, sens_analysis_list_of_customers_in_line_EQUAL,\
        sens_analysis_list_of_customers_on_cashier_queue_EQUAL, sens_analysis_list_of_customer_items_checked_EQUAL=\
            sensitivity_itemNumb_analysis(number_of_epochs_for_simulation,"equal",number_of_av_simulations,sensitivity_range)

    # Prints number of customers out of system
    plt.figure(1)
    plt.title("Sensitivity Analysis for Customers Out of the System")
    plt.xlabel("Probability Increment")
    plt.ylabel("Percentage of Mean of Customers Out of System at %d Epochs"%number_of_epochs_for_simulation)
    plt.plot(x_axis, sens_analysis_list_of_customers_out_of_system_CUSTOMER,'g^',\
        x_axis, sens_analysis_list_of_customers_out_of_system_CASHIER,'bs',\
        x_axis, sens_analysis_list_of_customers_out_of_system_EQUAL,'ro')
    plt.savefig("analysis_images\itemNumb_sens_analysis_list_of_customers_out_of_system.png")
    

    plt.figure(2)
    plt.title("Sensitivity Analysis for People in Line Average of %d" %number_of_av_simulations)
    plt.xlabel("Probability Increment")
    plt.ylabel("Percentage of Mean of Customers in Line at %d Epochs"%number_of_epochs_for_simulation)
    plt.plot(x_axis, sens_analysis_list_of_customers_in_line_CUSTOMER,'g^',\
        x_axis, sens_analysis_list_of_customers_in_line_CASHIER,'bs',\
        x_axis, sens_analysis_list_of_customers_in_line_EQUAL,'ro')
    plt.savefig("analysis_images\itemNumb_sens_analysis_list_of_customers_in_line.png")

    plt.figure(3)
    plt.title("Sensitivity Customers in Queue Average of %d" %number_of_av_simulations)
    plt.xlabel("Probability Increment")
    plt.ylabel("Percentage of Mean of Cashiers on Queue in the End of Simulation at %d Epochs"%number_of_epochs_for_simulation)
    plt.plot(x_axis, sens_analysis_list_of_customers_on_cashier_queue_CUSTOMER,'g^',\
        x_axis, sens_analysis_list_of_customers_on_cashier_queue_CASHIER,'bs',\
        x_axis, sens_analysis_list_of_customers_on_cashier_queue_EQUAL,'ro')
    plt.savefig("analysis_images\itemNumb_sens_analysis_list_of_customers_on_cashier_queue.png")

    plt.figure(4)
    plt.title("Sensitivity Analysis for Items Checked Average of %d" %number_of_av_simulations)
    plt.xlabel("Probability Increment")
    plt.ylabel("Mean of Items checkedout at %d Epochs"%number_of_epochs_for_simulation)
    plt.plot(x_axis, sens_analysis_list_of_customer_items_checked_CUSTOMER,'g^',\
        x_axis, sens_analysis_list_of_customer_items_checked_CASHIER,'bs',\
        x_axis, sens_analysis_list_of_customer_items_checked_EQUAL,'ro')
    plt.savefig("analysis_images\itemNumb_sens_analysis_list_of_items_checked.png")


def sensitivity_itemNumb_analysis(number_of_epochs_for_simulation,model_name,number_of_av_simulations,sensitivity_range):
    '''
    '''
    number_of_people = 150

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
                                        item_creation_sensitivity=(item_iterator- (sensitivity_range/2))/100)

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

        sens_customers_out_of_system_average = sens_customers_out_of_system_average/ number_of_people
        sens_customers_in_line_average = sens_customers_in_line_average/ number_of_people
        sens_customers_on_cashier_queue_average = sens_customers_on_cashier_queue_average/ number_of_people

        # Appends to average list
        sens_analysis_list_of_customers_out_of_system.append(sens_customers_out_of_system_average)
        sens_analysis_list_of_customers_in_line.append(sens_customers_in_line_average)
        sens_analysis_list_of_customers_on_cashier_queue.append(sens_customers_on_cashier_queue_average)
        sens_analysis_list_of_customer_items_checked.append(sens_items_customer_checked_average)

    return sens_analysis_list_of_customers_out_of_system, sens_analysis_list_of_customers_in_line,\
        sens_analysis_list_of_customers_on_cashier_queue, sens_analysis_list_of_customer_items_checked