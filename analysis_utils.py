#=======================================================================
#============================= Imports==================================
#=======================================================================

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

def configuration(number_of_epochs_for_simulation):
    '''Makes tests relative to config, involving:
        - Number of customers out of system
        - Number of customers in line
        - Number of customers in queue
        - Number checked items
    '''
    self_check_model = model("equal", 20, 4, 0,cashier_IPM_p_influence=0.1, customer_IPM_p_influence=0.2)
    list_of_customers_out_of_system, \
        list_of_customers_in_line, \
        list_of_customers_on_cashier_queue,\
        list_of_items_checked,\
        cost_for_maintenance\
            = self_check_model.execute_simulation(number_of_epochs_for_simulation, show=True, showAnim=True)

# ------------------------------- Sensitivity ---------------------------

def sensitivity_chitchatness_analysis(number_of_epochs_for_simulation):
    pass

def sensitivity_cashierIPM_analysis(number_of_epochs_for_simulation):
    '''
    '''
    # Numbers for simulation
    number_of_av_simulations = 100
    sensitivity_range = 10

    # Sets up analysis list
    sens_analysis_list_of_customers_out_of_system = []
    sens_analysis_list_of_customers_in_line = []
    sens_analysis_list_of_customers_on_cashier_queue = []
    sens_analysis_list_of_items_checked = []
    sens_analysis_cost_for_maintenance = []

    for simulation_i in range(sensitivity_range):
        sens_customers_out_of_system_average = 0
        sens_customers_in_line_average = 0
        sens_customers_on_cashier_queue_average = 0
        sens_items_checked_average = 0

        # Number
        for i in range(number_of_av_simulations):
            self_check_model = model("customer", 100, 10, 0,cashier_IPM_p_influence=simulation_i/100, customer_IPM_p_influence=0)

            list_of_customers_out_of_system, \
                    list_of_customers_in_line, \
                    list_of_customers_on_cashier_queue,\
                    list_of_items_checked,\
                    cost_for_maintenance\
                        = self_check_model.execute_simulation(number_of_epochs_for_simulation, show=False, showAnim=False)

            # Adds to average
            sens_customers_out_of_system_average = sens_customers_out_of_system_average\
                + list_of_customers_out_of_system[-1]

            sens_customers_in_line_average = sens_customers_in_line_average\
                + list_of_customers_in_line[-1]

            sens_customers_on_cashier_queue_average = sens_customers_on_cashier_queue_average\
                + list_of_customers_on_cashier_queue[-1]

            sens_items_checked_average = sens_items_checked_average\
                + list_of_items_checked[-1]

        
        # Calulates average
        sens_customers_out_of_system_average = sens_customers_out_of_system_average/number_of_av_simulations
        sens_customers_in_line_average = sens_customers_in_line_average/number_of_av_simulations
        sens_customers_on_cashier_queue_average = sens_customers_on_cashier_queue_average/number_of_av_simulations
        sens_items_checked_average = sens_items_checked_average/number_of_av_simulations

        # Appends to average list
        sens_analysis_list_of_customers_out_of_system.append(sens_customers_out_of_system_average)
        sens_analysis_list_of_customers_in_line.append(sens_customers_in_line_average)
        sens_analysis_list_of_customers_on_cashier_queue.append(sens_customers_on_cashier_queue_average)
        sens_analysis_list_of_items_checked.append(sens_items_checked_average)

    
    plt.figure(1)
    plt.title("Sensitivity Analysis for Customers Out of the System")
    plt.xlabel("Probability Increment")
    plt.ylabel("Mean of Customers Out of System at %d"%number_of_epochs_for_simulation)
    plt.plot(sens_analysis_list_of_customers_out_of_system)
    plt.savefig("sens_analysis_list_of_customers_out_of_system.png")
    print ("Test complete")

def sensitivity_customerIPM_analysis(number_of_epochs_for_simulation):
    pass

def sensitivity_itemNumb_analysis(number_of_epochs_for_simulation):
    pass

# ------------------------------- Population ---------------------------
