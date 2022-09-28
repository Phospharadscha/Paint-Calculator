import unittest

#########################################################################################
################################# Testing ###############################################
#########################################################################################

class TestInputHandling(unittest.TestCase):
    def test_int_pos(self):
        pos_integers = ["1", "2", "10", "20", "250", "1050"]
        for i in pos_integers: 
            self.assertEqual(get_int_input(i, True), "Valid Input")
            self.assertEqual(get_int_input(i, False), "Valid Input")
    
    def test_int_negative(self):
        neg_integers = ["-1", "-2", '-10', "-20", "-250", "-1050"]
        for i in neg_integers: 
            self.assertEqual(get_int_input(i, True), 'Error: Please enter a positive whole number: ')
            self.assertEqual(get_int_input(i, False), 'Error: Please enter a positive, non zero, whole number: ')

    def test_int_zero(self):
        self.assertEqual(get_int_input("0", True), "Valid Input")
        self.assertEqual(get_int_input("0", False), 'Error: Please enter a positive, non zero, whole number: ')
    

    def test_int_float(self):
        floats = ["1.0", "2.1", "10.21", "20.321", "250.4321", "1050.54321", "-1.0", "-2.1", "-10.21", "-20.321", "-250.4321", "-1050.54321"]
        for i in floats: 
            self.assertEqual(get_int_input(i, True), 'Error: Please enter a positive whole number: ')
            self.assertEqual(get_int_input(i, False), 'Error: Please enter a positive, non zero, whole number: ') 
    
    def test_int_string(self):
        strings = ["Test", "Wall", "Room", "La-Li-Lu-Le-Lo"]
        for i in strings:
            self.assertEqual(get_int_input(i, True), 'Error: Please enter a positive whole number: ')
            self.assertEqual(get_int_input(i, False), 'Error: Please enter a positive, non zero, whole number: ')  

    def test_float_pos(self):
        pos_floats = ["1.0", "2.1", "10.21", "20.321", "250.4321", "1050.54321"]
        for i in pos_floats: 
            self.assertEqual(get_float_input(i, True), "Valid Input")
            self.assertEqual(get_float_input(i, False), "Valid Input")
    
    def test_float_negative(self):
        neg_floats = ["-1.0", "-2.1", "-10.21", "-20.321", "-250.4321", "-1050.54321"]
        for i in neg_floats: 
            self.assertEqual(get_float_input(i, True), "Error: Please enter a positive number: ")
            self.assertEqual(get_float_input(i, False), "Error: Please enter a positive, non zero, number: ")
               
    def test_float_zero(self):
        self.assertEqual(get_float_input("0", True), "Valid Input")
        self.assertEqual(get_float_input("0", False), 'Error: Please enter a positive, non zero, number: ')
        
    def test_float_int(self):
        integers_pos = ["1", "2", "10", "20", "250", "1050"]
        integers_neg = ["-1", "-2", '-10', "-20", "-250", "-1050"]
        
        for i in integers_pos: 
            self.assertEqual(get_float_input(i, True), 'Valid Input')
            self.assertEqual(get_float_input(i, False), 'Valid Input') 
        
        for i in integers_neg: 
            self.assertEqual(get_float_input(i, True), 'Error: Please enter a positive number: ')
            self.assertEqual(get_float_input(i, False), 'Error: Please enter a positive, non zero, number: ')  
        
    def test_float_string(self):
        strings = ["Test", "Wall", "Room", "La-Li-Lu-Le-Lo"]
        for i in strings:
            self.assertEqual(get_float_input(i, True), 'Error: Please enter a positive number: ')
            self.assertEqual(get_float_input(i, False), 'Error: Please enter a positive, non zero, number: ')  

        

    




#########################################################################################
############################## Methods being tested #####################################
#########################################################################################
"""Methods have been altered to remove the GUI elements
Now. they Just return a string used which reference "branch" has been addressed
"""

def get_float_input(usr_input, allow_zero):
    """ Returns a provided string input as a float. 
    When called, you can specify if you want the a valid input to be non-zero, or if zero can be included. 
    """
    # Temporary assignment of values
    user_input = ""
    valid_input = False
    
    # Loops until a valid input is given
    # Attempt casting of string into float
    try:
        user_input = float(usr_input)
        valid_input = True
    except ValueError:
        valid_input = False

    # If the input is invalid, or if it's valid but less than 0, then:
    if not valid_input or user_input < 0 or user_input == 0:
        if allow_zero and user_input == 0:
            return "Valid Input"
        
        text = "Error: Please enter a positive"
        # Alter string if zero is not allowed as a valid input
        if not allow_zero:
            text += ", non zero,"
        text += " number: "
        
        return text
    elif valid_input:
        return "Valid Input"
    
def get_int_input(usr_input, allow_zero):
    """ Returns a provided string input as a float. 
    When called, you can specify if you want the a valid input to be non-zero, or if zero can be included. 
    """
    # Temporary assignment of values
    user_input = ""
    valid_input = False
    
    # Loops until a valid input is given
    # Attempt casting of string into float
    try:
        user_input = int(usr_input)
        valid_input = True
    except ValueError:
        valid_input = False

    # If the input is invalid, or if it's valid but less than 0, then:
    if not valid_input or user_input < 0 or user_input == 0:
        if allow_zero and user_input == 0:
            return "Valid Input"
        
        text = "Error: Please enter a positive"
        # Alter string if zero is not allowed as a valid input
        if not allow_zero:
            text += ", non zero,"
        text += " whole number: "
        return text
    elif valid_input:
        return "Valid Input"

if __name__ == "__main__":
    unittest.main(verbosity=2)