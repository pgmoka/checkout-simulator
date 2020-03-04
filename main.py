#=======================================================================
#============================= Imports==================================
#=======================================================================

# Python modules
import numpy as np
import matplotlib.pyplot as plt

# Create simulation code
import variables as v
from model import model

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
self_check_model = model("equal", 16, 4, 4)

self_check_model.execute_simulation(number_of_epochs_for_simulation, show=True, showAnim=True)
print("END OF EXECUTION")