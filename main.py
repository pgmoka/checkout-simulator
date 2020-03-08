#=======================================================================
#============================= Imports==================================
#=======================================================================

# Python modules
import numpy as np
import matplotlib.pyplot as plt

# Create simulation code
import variables as v
from model import model
from fullday_model import Fullday
from analysis_utils import *
#=======================================================================
#============================= Exectuion ===============================
#=======================================================================

number_of_epochs_for_simulation = 30
# -------------------------- start of testing:
# # random_line tests:
# random_line_model = model("random", 10, 2,0)

# # Test if customer
# customer_creation_test = random_line_model.line.customer_list

# random_line_model.execute_simulation(number_of_epochs_for_simulation)

# model_line = random_line_model.line

# -------------------------- Self-checkout_test:
#self_check_model = model("equal", 20, 4, 0)
#self_check_model = model("random", 20, 4, 0)
#self_check_model = model("selector", 20, 4, 0)

# fulldayTest = Fullday('customer', 5, 6, population = 'low', day_type = 'front')


# fulldayTest.execute_simulation(show=True, showAnim=True)

#self_check_model.execute_simulation(number_of_epochs_for_simulation, show=True, showAnim=True)
# self_check_model = model("customer", 21, 5, 2)

# p = 0.2
# n = 100
# plt.hist(np.random.binomial(n,p,1000)+30)
# # plt.hist(np.random.normal(20, 8.9,1000))
# plt.show()

# self_check_model = model("customer", 21, 5, 2,cashier_IPM_p_influence=0.1, customer_IPM_p_influence=0.2)

# self_check_model = model("equal", 200, 5, 2)

# list_of_customers_out_of_system, \
#         list_of_customers_in_line, \
#         list_of_customers_on_cashier_queue,\
#         list_of_items_checked,\
#         cost_for_maintenance\
#             = self_check_model.execute_simulation(number_of_epochs_for_simulation, show=False, showAnim=True)

# sensitivity_cashierIPM_analysis_for_all_lines(number_of_epochs_for_simulation)
# sensitivity_customerIPM_analysis_for_all_lines(number_of_epochs_for_simulation)
sensitivity_itemNumb_analysis_for_all_lines(number_of_epochs_for_simulation)

print("END OF EXECUTION")