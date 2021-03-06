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
- No executable
- File hold global variables necessary for the overall creation, and
maintenance of the model

=======================================================================
'''

# --- Cashier number:
NUMBER_OF_CASHIER = 5

# --- IPM information for cashier
CASHIER_AVERAGE_IPM = 21

CASHIER_STD_DEV_IPM = 3

# 0.5714
CASHIER_p = 1 - ((CASHIER_STD_DEV_IPM**2)/CASHIER_AVERAGE_IPM)

# 36.75
CASHIER_n = CASHIER_AVERAGE_IPM/CASHIER_p

#must be a number between 0 and 1
CASHIER_CHITCHATNESS = .8

# --- Number of customers:
CUSTOMER_AVERAGE_IPM = 6

CUSTOMER_STD_DEV_IPM = 2

CUSTOMER_p = 1 - ((CUSTOMER_STD_DEV_IPM**2)/CUSTOMER_AVERAGE_IPM)

CUSTOMER_n = CUSTOMER_AVERAGE_IPM/CASHIER_p

#must be a number between 0 and 1
CUSTOMER_CHITCHATNESS = .8

# --- Item creation information:
MEAN_NUMBER_OF_ITEMS_PER_CUSTOMER = 6

STANDAR_DEVIATION_OF_ITEMS_FOR_CUSTOMER = 2

# --- Self checkour time
SELF_CHECKOUT_TIME = 0.85

# --- number used to get time step (60/15)
TIME_STEP = 15

# --- forgetfullness
FORGET = 0.5