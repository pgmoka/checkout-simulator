#=======================================================================
#============================= Imports==================================
#=======================================================================

# Python modules
import numpy as np

# Create simulation code
import variables as v
from model import model

#=======================================================================
#============================= Exectuion ===============================
#=======================================================================

# random_line tests:
random_line_model = model("random")

# Test if customer
customer_creation_test = random_line_model.line.customer_list
print("END OF EXECUTION")