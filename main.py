import bd
import menu
import numpy as np
import pprint

main_m = np.array(["Configure beam", "Configure loads",
                   "Save beam and loads", "Load beam and loads", "Generate plot", "Quit"])
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
    lf = menu.inputNumber("Input force of the load: ", "f")
    lp = menu.inputNumber("Input position of the load: ", "f")
    print()		# new line
    return np.append(loadArray, [[lf, lp]], axis=0)


while True:
    opt = menu.displayMenu(main_m)

    # Configure beam option chosen
    if opt == 1:
        bl = 0
        while bl <= 0:
            bl = menu.inputNumber("Beam length: ", "f")

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
                    rm = menu.displayMenu(["{}\t{}".format(i, j) for i, j in l])
                    l = np.delete(l, rm-1, 0)
                # back chosen
                elif lm == 3:
                    break
            else:
                # give an option only for adding
                print("There are no loads in the database:")
                lm = menu.displayMenu(["Add a load", "Back"])

                # add load chosen
                if lm == 1:
                    l = addLoad(l)
                # back chosen
                elif lm == 2:
                    break

    # Save beam and loads option chosen
    elif opt == 3:
        pass
    # Load beam and loads option chosen
    elif opt == 4:
        pass
    # Generate plot option chosen
    elif opt == 5:
        bd.beamPlot(bl, l.T[1], l.T[0], bs)
    # Quit option chosen
    elif opt == 6:
        break
