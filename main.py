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

def type_of_cashier_comparison():
    self_check_model = model("equal", 20, 4, 0)
    list_of_customers_out_of_system, \
        list_of_customers_in_line, \
        list_of_customers_on_cashier_queue,\
        list_of_items_checked,\
        cost_for_maintenance\
            = self_check_model.execute_simulation(number_of_epochs_for_simulation, show=True, showAnim=True)

#=======================================================================
#============================= Exectuion ===============================
#=======================================================================

number_of_epochs_for_simulation = 20
# -------------------------- start of testing:
# # random_line tests:
# random_line_model = model("random", 10, 2,0)

# # Test if customer
# customer_creation_test = random_line_model.line.customer_list

# random_line_model.execute_simulation(number_of_epochs_for_simulation)

# model_line = random_line_model.line

# -------------------------- Self-checkout_test:
self_check_model = model("equal", 21, 10, 20)
# self_check_model = model("random", 20, 4, 0)

self_check_model = model("random", 20, 4, 0)

list_of_customers_out_of_system, \
        list_of_customers_in_line, \
        list_of_customers_on_cashier_queue,\
        list_of_items_checked,\
        cost_for_maintenance\
            = self_check_model.execute_simulation(number_of_epochs_for_simulation, show=True, showAnim=False)

print("END OF EXECUTION")