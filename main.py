# system modules
import numpy as np
import os.path
# custom modules
import bd
import menu

# Global variables
# array of main menu items
main_m = np.array(["Configure beam", "Configure loads",
                   "Save beam and loads", "Load beam and loads", "Generate plot", "Quit"])
# variables storing beam settings
bl = 0.
bs = "both"
# empty array with zero rows and two columns used for storing the loads and its positions
l = np.empty(shape=[0, 2], dtype=float)

# main loop start
while True:
    opt = menu.displayMenu(main_m)

    # Configure beam option chosen
    if opt == 1:
        while True:
            # if any loads are configured, asks to clear them before procceding (makes sure no load is outside beam)
            if l.any():
                print("Loads are configured and will have to be cleared to continue, do you want to proceed?")
                lc_m = menu.displayMenu(["yes","no"])
                if lc_m == 1:
                  l = np.empty(shape=[0, 2], dtype=float)
                if lc_m == 2:
                    break
            # ask for beam length until a positive value is entered
            bl = 0
            while bl <= 0:
                bl = menu.inputNumber("Please enter a valid beam length: ", "f")
                if bl <= 0:
                    print("The beam lenght has to be a positive number!")
    
            # ask user which beam support should be used
            print("\nChoose the beam support:")
            bs_m = menu.displayMenu(["both", "cantilever"])
            if bs_m == 1:
                bs = "both"
            elif bs_m == 2:
                bs = "cantilever"
            break

    # Configure loads option chosen
    elif opt == 2:
        while True:
            # check whether the array is empty
            if np.any(l):
                # show the current loads
                print("Current configured loads:")
                print("force\t\tposition")
                print("".join(["{}\t\t{}\n".format(i, j) for i, j in l]))

                # give an option for adding or removing
                lm = menu.displayMenu(["Add a load", "Remove a load", "Back"])

                # add load chosen
                if lm == 1:
                    l = menu.addLoad(l,bl)
                # remove load chosen
                elif lm == 2:
                    print("Please choose entry you wish to delete:")
                    print("   force\tposition")
                    # create a list of the current loads and their positions
                    rm_menu = ["{}\t{}".format(i, j) for i, j in l]
                    rm_menu.append("Back")
                    # show the menu
                    rm = menu.displayMenu(rm_menu)
                    # check whether the back option hasn't been chosen
                    if rm != len(rm_menu):
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
                        # check whether the beam length was given
                    if bl == 0:
                        print("You need to first specify the beam length")
                    else:
                        l = menu.addLoad(l,bl)
                # back chosen
                elif lm == 2:
                    break

    # Save beam and loads option chosen
    elif opt == 3:
        file = input("Please enter the file name (*.json sufix will be added automatically): ")
        menu.saveFile(file, bl, bs, l)
        print("Data successfully saved")
    # Load beam and loads option chosen
    elif opt == 4:
        file = input("Please enter the file name: ")
        # check whether the file exists
        if os.path.isfile(file if file.endswith(".json") else file + ".json"):
            bl, bs, l = menu.loadFile(file)
            print("Data successfully loaded")
        else:
            print("No such file found")
    # Generate plot option chosen
    elif opt == 5:
        if bl == 0.:
            print("Please configure the beam before plotting the data\n")
        else:
            if not l.any():
                print("Warning: No loads were entered\n")
            # plot the given values
            bd.beamPlot(bl, l.T[1], l.T[0], bs)
    # Quit option chosen
    elif opt == 6:
        break
