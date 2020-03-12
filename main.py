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
- To execute, run "main.py".
- Modules necessary: numpy, matplotlib.pyplot
- External necessities: variables.py, model.py, fullday_model.py, and
analysis_utils.py.
- Executes simulation
- Declares methods for automated analysis execution

=======================================================================
'''
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
#============================= Method ==================================
#=======================================================================

def execute_all_sensitvity_tests():
    ''' Automated method for executing all of the sensitivity test types

    Postcondition:
    - Prints images to the file "analysis_images".
    - A total of 32 images will be printed
    '''
    average_simulation_numb = 200
    number_of_epochs_for_simulation = 30

    # Testing cashierIPM
    sensitivity_cashierIPM_analysis_for_all_lines(number_of_epochs_for_simulation, number_of_av_simulations = average_simulation_numb, number_of_people = 100)
    sensitivity_cashierIPM_analysis_for_all_lines(number_of_epochs_for_simulation, number_of_av_simulations = average_simulation_numb, number_of_people = 20)

    average_simulation_numb = 100
    number_of_epochs_for_simulation = 500

    # Testing customerIPM
    sensitivity_customerIPM_analysis_for_all_lines(number_of_epochs_for_simulation, number_of_av_simulations = average_simulation_numb, number_of_people = 400)
    sensitivity_customerIPM_analysis_for_all_lines(number_of_epochs_for_simulation, number_of_av_simulations = average_simulation_numb, number_of_people = 60)

    average_simulation_numb = 200
    number_of_epochs_for_simulation = 30

    sensitivity_itemNumb_analysis_for_all_lines(number_of_epochs_for_simulation, number_of_av_simulations = average_simulation_numb, number_of_people = 150)
    sensitivity_itemNumb_analysis_for_all_lines(number_of_epochs_for_simulation, number_of_av_simulations = average_simulation_numb, number_of_people = 30)

    average_simulation_numb = 200
    number_of_epochs_for_simulation = 20

    sensitivity_chitchatness_analysis_for_all_lines(number_of_epochs_for_simulation, number_of_av_simulations = average_simulation_numb, number_of_people = 20)
    sensitivity_chitchatness_analysis_for_all_lines(number_of_epochs_for_simulation, number_of_av_simulations = average_simulation_numb, number_of_people = 40)

#=======================================================================
#============================= Exectuion ===============================
#=======================================================================


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

# fulldayTest = Fullday('equal', 5, 6, day_type = 'front')
#
# fulldayTest.execute_simulation(show=False, showAnim=True)

#self_check_model.execute_simulation(number_of_epochs_for_simulation, show=True, showAnim=True)
# self_check_model = model("customer", 21, 5, 2)

# p = 0.2
# n = 100
# plt.hist(np.random.binomial(n,p,1000)+30)
# # plt.hist(np.random.normal(20, 8.9,1000))
# plt.show()

# self_check_model = model("customer", 21, 5, 2,cashier_IPM_p_influence=0.1, chitchatness_influence=0.2)

# list_of_customers_out_of_system, \
#         list_of_customers_in_line, \
#         list_of_customers_on_cashier_queue,\
#         list_of_items_checked,\
#         cost_for_maintenance\
#             = self_check_model.execute_simulation(1000, show=False, showAnim=True)

# average_simulation_numb = 200
# number_of_epochs_for_simulation = 30

# # Testing cashierIPM
# sensitivity_cashierIPM_analysis_for_all_lines(number_of_epochs_for_simulation, number_of_av_simulations = average_simulation_numb, number_of_people = 100)
# sensitivity_cashierIPM_analysis_for_all_lines(number_of_epochs_for_simulation, number_of_av_simulations = average_simulation_numb, number_of_people = 20)

# average_simulation_numb = 100
# number_of_epochs_for_simulation = 500

# # Testing customerIPM
# sensitivity_customerIPM_analysis_for_all_lines(number_of_epochs_for_simulation, number_of_av_simulations = average_simulation_numb, number_of_people = 400)
# sensitivity_customerIPM_analysis_for_all_lines(number_of_epochs_for_simulation, number_of_av_simulations = average_simulation_numb, number_of_people = 60)

# average_simulation_numb = 200
# number_of_epochs_for_simulation = 30

# sensitivity_itemNumb_analysis_for_all_lines(number_of_epochs_for_simulation, number_of_av_simulations = average_simulation_numb, number_of_people = 150)
# sensitivity_itemNumb_analysis_for_all_lines(number_of_epochs_for_simulation, number_of_av_simulations = average_simulation_numb, number_of_people = 30)

average_simulation_numb = 200
number_of_epochs_for_simulation = 20

plot_all_mean_values(number_of_epochs_for_simulation)

# sensitivity_chitchatness_analysis_for_all_lines(number_of_epochs_for_simulation, number_of_av_simulations = average_simulation_numb, number_of_people = 20)
# sensitivity_chitchatness_analysis_for_all_lines(number_of_epochs_for_simulation, number_of_av_simulations = average_simulation_numb, number_of_people = 40)

# sensitivity_customer_number_analysis_for_all_lines(number_of_epochs_for_simulation, number_of_av_simulations = average_simulation_numb, number_of_people = 5)

#mean_values(number_of_epochs_for_simulation, show=True)
#lag_correlation_analysis(number_of_epochs_for_simulation)

#full_day_analysis_backLoaded()
#full_day_analysis_frontLoaded()
#full_day_analysis_normal()

print("END OF EXECUTION")