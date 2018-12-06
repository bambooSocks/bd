import numpy as np
import matplotlib.pyplot as plt

##
## @brief      Calculate the deflection of a load
##
## @param      pos        Array of positions in wich the deflection is calculated
## @param      beamLen    The beam length
## @param      loadPos    The position of  a single load
## @param      loadForce  The force applied in the single position
## @param      beamSup    The type of support, either "both" or "cantilever"
##
## @return     Returns an array of deflection in all the positions specified
##
## @author     Johan Emil Levin-Jensen
##
def beamDeflection(pos, beamLen, loadPos, loadForce, beamSup):  
    deflection = np.zeros(np.size(pos))
    EI = 6*2e11*1e-3      # A constant that is in all the calculations
    
    for idx, p in enumerate(pos):      # p is the current position, idx is the index in the array of positions
        
        #When beamsupport is set to both 
        if beamSup == "both":
            if p < loadPos:
                k=loadForce*(beamLen-loadPos)*p/(EI*beamLen)
                j=beamLen**2-p**2-(beamLen-loadPos)**2
            
            if p >= loadPos:
                k=loadForce*loadPos*(beamLen-p)/(EI*beamLen)
                j=(beamLen**2-(beamLen-p)**2-loadPos**2)
        
        #When beamsupport is set to cantilever
        if beamSup == "cantilever":
            if p < loadPos:
                k=loadForce*p**2/EI
                j=3*loadPos-p
                
            if p >= loadPos:
                k=loadForce*loadPos**2/EI
                j=3*p-loadPos
        
        #Calculates the final deflection and puts it into array
        deflection[idx]=k*j
    
    return deflection

##
## @brief      Calulates the deflection in multiple locations for multiple loads
##
## @param      pos        Array of postions in which the position is calculated
## @param      beamLen    The beam length
## @param      loadPos    Array of positions for loads to be applied
## @param      loadForce  Array of loads to be applied in positions
## @param      beamSup    The type of support, either "both" or "cantilever"
##
## @return     Returns an array of deflections in all the pos
##
## @author     Johan Emil Levin-Jensen
##
def beamSuperposition(pos, beamLen, loadPos, loadForce, beamSup):
    deflection = np.zeros(np.size(pos))
    
    #Loops through all the loads and calculates the final deflection by use of superposition principle
    for idx, lp in enumerate(loadPos):
        deflection += beamDeflection(pos,beamLen,lp,loadForce[idx],beamSup)

    return deflection

##
## @brief      Plots the beam for multiple loads.
##
## @param      beamLen    The beam length
## @param      loadPos    The load position
## @param      loadForce  The load force
## @param      beamSup    The beam sup
##
## @return     Returns plot of the beam, with marked positions of loads and shows the magnitude for each force.
## 
## @author     Jędrzej Konrad Kolbert modified by Matej Majtan
##
def beamPlot(beamLen, loadPos, loadForce, beamSup):
    # Creating variables for the plot of the beam
    x = np.arange(0., beamLen + beamLen/100, beamLen/100)
    y1 = beamSuperposition(x, beamLen, loadPos, loadForce, beamSup)
    
    # Creating variables for the plot of load points
    if loadForce.any():
        y2 = beamSuperposition(loadPos, beamLen, loadPos, loadForce, beamSup)
    
    # Setting up the plot area
    fig = plt.figure()
    fig.set_figheight(10)
    fig.set_figwidth(10)
    
    plt.plot(x, y1, 'r-') # Plotting the beam 
    

    if loadForce.any():    # Plotting positions of loads
        plt.plot(loadPos, y2, 'b*')
    
    plt.gca().invert_yaxis() # Measuring deflection downwards 
    
    # Setting up title, labels, grid  and ticks 
    plt.title("Beam deflection\nBeam type: {:s}".format(beamSup))
    plt.xlabel("Computed position")
    plt.ylabel("Deflection")
    plt.xlim([0, 1.05*beamLen])
    plt.ticklabel_format(style='sci', axis='y1', scilimits=(0,0)) # Changing tick labels numbers to scientific format
    plt.tight_layout()
    plt.grid(color='grey', linestyle='--', linewidth=0.5) # Making grid lines
    
    plt.axhline(y=np.max(y1),linewidth=1, color='g')     #The line showing max. deflection
    
    # Sorting data for the legend
    if loadForce.any():
        force = np.array([(loadPos[idx], loadForce[idx]) for idx in range(len(lp))], dtype=[('pos',int),('force',int)])
        force.sort(axis=0, order=['pos'])
        force = np.array([np.array([i[0], i[1]]) for i in force])
        force = force[:,1] # Magnitudes of forces sorted in the way corresponding to plotted load positions
        
        #Making the string containing magnitudes 
        f_format = np.array([])
        for i in range(np.size(y2)):
            x = 'F{:d} = {:.2E} N'.format(i+1, force[i])
            f_format = np.append(f_format,x)
            i += i  
        f_format = "\n".join(f_format)
        
        #Plotting the legend
        plt.legend(('Beam',('Load position\nForce magnitude:\n{}'.format(f_format)),('Max. difl. = {:.2E} m'.format(np.max(y1)))), loc = 'best')
    
    plt.show()
    
if __name__ == '__main__':
    bl = 70
    lp = np.random.uniform(low=0, high=bl, size=(40,))
    lf = np.random.uniform(low=-40, high=50, size=(40,))
    bs = 'both'
    beamPlot(bl, lp, lf, bs)