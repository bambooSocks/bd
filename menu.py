import json
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
            print("Input has to be {}".format("an interger" if dtype == "i" else "a float"))
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
        print()
        if not(np.any(choice == np.arange(len(options))+1)):
        	print("Please enter a number in range {}-{}".format(min(np.arange(len(options))+1), max(np.arange(len(options))+1)))

    print()   # new line

    return choice 
##
# @brief      Asks user to input new load values
##
# @param      loadArray  the array that should be appended with new load values
##
# @return     the array with new load input
##
# @author     Matej Majtan
##
def addLoad(loadArray, beamLen):
    lp = 0
    lf = inputNumber("Input force of the load: ", "f")
    while lp <= 0 or lp > beamLen:
        lp = inputNumber("Input position of the load: ", "f")
        if lp <= 0 or lp > beamLen:
            print("Please enter a position that is in the range of the beam lenght")
    print()     # new line
    return np.append(loadArray, [[lf, lp]], axis=0)


##
# @brief      Saves a file.
##
# @param      filename     Name of the file data should be saved into (.json at the end is optional)
# @param      beamLenght   the length of the beam that should be saved
# @param      beamSupport  the type of the beam support that should be saved
# @param      loadArray    the numpy array of loads and its positions that should be saved
##
# @author     Matej Majtan
##
def saveFile(filename, beamLenght, beamSupport, loadArray):
        # reate a dictionary used by the json module to create the json file
    data = {"beamLenght": beamLenght,
            "beamSupport": beamSupport,
            "loadArray": [list(i) for i in loadArray]
            }

    # open a file and dump the json data into it
    with open(filename if filename.endswith(".json") else filename + ".json", "w") as write_file:
        json.dump(data, write_file)


##
# @brief      Loads a json file  to the system
##
# @param      filename  Name of the file data should be loaded from (.json at the end is optional)
##
# @return     tuple with leaded data for beam length, beam support and load array
##
# @author     Matej Majtan
##
def loadFile(filename):
    data = {}
    with open(filename if filename.endswith(".json") else filename + ".json", "r") as read_file:
        data = json.load(read_file)

    # TODO: add checking for correct file (data in it)
    return (data["beamLenght"], data["beamSupport"], np.array([np.array(i) for i in data["loadArray"]]))