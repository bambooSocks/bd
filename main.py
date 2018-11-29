import bd
import menu
import numpy as np
import pprint
import json

# array of main menu items
main_m = np.array(["Configure beam", "Configure loads",
                   "Save beam and loads", "Load beam and loads", "Generate plot", "Quit"])
# variables storing beam settings
bl = 0.
bs = "both"
# create empty array with zero rows and two columns
l = np.empty(shape=[0, 2], dtype=float)


##
# @brief      Asks user to input new load values
##
# @param      loadArray  the array that should be appended with new load values
##
# @return     returns the array with new load input
##
# @author     Matej Majtan
##
def addLoad(loadArray):
    lp = 0
    lf = menu.inputNumber("Input force of the load: ", "f")
    while lp <= 0 or lp > bl:
        lp = menu.inputNumber("Input position of the load: ", "f")
    print()     # new line
    return np.append(loadArray, [[lf, lp]], axis=0)


##
# @brief      Saves a file.
##
# @param      filename     Name of the file data should be saved into (.json at the end is optional)
# @param      beamLenght   The beam lenght
# @param      beamSupport  The beam support
# @param      loadArray    The load array
##
# @author     Matej Majtan
##
def saveFile(filename, beamLenght, beamSupport, loadArray):
    data = {"beamLenght": beamLenght,
            "beamSupport": beamSupport,
            "loadArray": [list(i) for i in loadArray]
            }

    with open(filename if filename.endswith(".json") else filename + ".json", "w") as write_file:
        json.dump(data, write_file)


##
# @brief      Loads a file.
##
# @param      filename  Name of the file data should be loaded from (.json at the end is optional)
##
# @return     tuple with leaded data for beam length, beam support and load array
##
def loadFile(filename):
    data = {}
    with open(filename if filename.endswith(".json") else filename + ".json", "r") as read_file:
        data = json.load(read_file)
    return (data["beamLenght"], data["beamSupport"], np.array([np.array(i) for i in data["loadArray"]]))

# main loop start
while True:
    opt = menu.displayMenu(main_m)

    # Configure beam option chosen
    if opt == 1:
        # ask for beam length until a positive value is entered
        bl = 0
        while bl <= 0:
            bl = menu.inputNumber("Please enter a valid beam length: ", "f")

        # ask user which beam support should be used
        print("Choose the beam support:\n")
        bs_m = menu.displayMenu(["both", "cantilever"])
        if bs_m == 1:
            bs = "both"
        elif bs_m == 2:
            bs = "cantilever"

    # Configure loads option chosen
    elif opt == 2:
        while True:
            # check whether the array is empty
            if np.any(l):
                # show the current loads
                print("Current configured loads:")
                print("force\tposition")
                print("".join(["{}\t{}\n".format(i, j) for i, j in l]))

                # give an option for adding or removing
                lm = menu.displayMenu(["Add a load", "Remove a load", "Back"])

                # add load chosen
                if lm == 1:
                    l = addLoad(l)
                # remove load chosen
                elif lm == 2:
                    print("Please choose entry you wish to delete:")
                    rm = menu.displayMenu(
                        ["{}\t{}".format(i, j) for i, j in l])
                    l = np.delete(l, rm - 1, 0)
                # back chosen
                elif lm == 3:
                    break
            else:
                # give an option only for adding
                print("There are no loads in the database:")
                lm = menu.displayMenu(["Add a load", "Back"])

                # add load chosen
                if lm == 1:
                    if bl == 0:
                        print("You need to first specify the beam length")
                    else:
                        l = addLoad(l)
                # back chosen
                elif lm == 2:
                    break

    # Save beam and loads option chosen
    elif opt == 3:
        file = input(
            "Please enter the file name (.json will be added automatically): ")
        saveFile(file, bl, bs, l)
        print("Data successfully saved")
    # Load beam and loads option chosen
    elif opt == 4:
        file = input("Please enter the file name: ")
        bl, bs, l = loadFile(file)
        print("Data successfully loaded")
    # Generate plot option chosen
    elif opt == 5:
        # plot the given values
        bd.beamPlot(bl, l.T[1], l.T[0], bs)
    # Quit option chosen
    elif opt == 6:
        break
