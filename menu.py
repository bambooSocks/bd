
import numpy as np

##
## @brief      Asks for input and checks that it is an integer or float depending on dtype
## 			   If there is no data type specified, keeps asking for input.
##
## @param      prompt  the message that should be displayed when asking for input
## @param      dtype   the type of input: "i" for integers and "f" for float
##
## @return     the entered number
##
## @author     Mikkel N. Schmidt, mnsc@dtu.dk, 2015, modified by Johan Emil Levin-Jensen and Matej Majtan
##
def inputNumber(prompt, dtype):
    
    while True:
        try:
            if dtype == 'i':
                num = int(input(prompt))
            elif dtype == 'f':
                num = float(input(prompt))
            break
        except ValueError:
            print("Not a valid entry")
            pass

    return num

##
## @brief      Displays menu with the options in the input array
##
## @param      options  numpy array or list of strings representing individual menu items
##
## @return     the number of a chosen item
## 
## @note       the return value corresponds to the index of the chosen item plus 1, hence the arrays start at 0
## 			   and the menu at 1.
##
## @author     Mikkel N. Schmidt, mnsc@dtu.dk, 2015, modified by Johan Emil Levin-Jensen and Matej Majtan
##
def displayMenu(options):
	# display the menu
    for i in range(len(options)):
        print("{:d}. {:s}".format(i+1, options[i]))

    choice = 0

    # wait for correct input
    while not(np.any(choice == np.arange(len(options))+1)):
        choice = inputNumber("Please choose a menu item: ","i")

    print("")   # new line

    return choice