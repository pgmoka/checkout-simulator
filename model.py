
#=======================================================================
#============================= Imports==================================
#=======================================================================

# Python modules
import numpy as np

# Create simulation code
import variables as v
from random_line import random_line
from cashier import cashier

#=======================================================================
#================================= Class ===============================
#=======================================================================

class model:
    line = 0

    phase = 0
    '''Initializes method
    '''
    def __init__(self, model_being_ran, model_name="Default Model"):
        self.line = self.create_line(model_being_ran)
        self.name = model_name
        self.phase = 1
    
    ''' Executes simulation with a number steps
    '''
    def execute_simulation(self, number_of_steps):
        for i in range(number_of_steps):
            print("EXECUTE SIMULATION")

    ''' Helper method for the creation of lines
    '''
    def create_line(self, model_being_ran):
        if(model_being_ran == "random"):
            return random_line(1,5)
        else:
            return random_line(1,5)
