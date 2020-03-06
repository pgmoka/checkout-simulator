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
    self_check_model = model("equal", 20, 4, 0,cashier_IPM_p_influence=0.1, customer_IPM_p_influence=0.2)
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
# self_check_model = model("customer", 21, 5, 2)

# p = 0.2
# n = 100
# plt.hist(np.random.binomial(n,p,1000)+30)
# # plt.hist(np.random.normal(20, 8.9,1000))
# plt.show()

self_check_model = model("customer", 21, 5, 2,cashier_IPM_p_influence=0.1, customer_IPM_p_influence=0.2)

# self_check_model = model("equal", 21, 5, 2)

list_of_customers_out_of_system, \
        list_of_customers_in_line, \
        list_of_customers_on_cashier_queue,\
        list_of_items_checked,\
        cost_for_maintenance\
            = self_check_model.execute_simulation(number_of_epochs_for_simulation, show=False, showAnim=True)

print("END OF EXECUTION")