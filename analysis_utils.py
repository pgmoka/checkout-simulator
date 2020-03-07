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
    pass

def sensitivity_customerIPM_analysis(number_of_epochs_for_simulation):
    pass

def sensitivity_itemNumb_analysis(number_of_epochs_for_simulation):
    pass


