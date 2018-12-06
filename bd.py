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
## @brief      { function_description }
##
## @param      beamLen    The beam length
## @param      loadPos    The load position
## @param      loadForce  The load force
## @param      beamSup    The beam sup
##
## @return     { description_of_the_return_value }
## 
## @author     CHEN CHEN
##
def beamPlot(beamLen, loadPos, loadForce, beamSup):
    x = np.arange(0., beamLen + beamLen/100, beamLen/100)
    y1 = beamSuperposition(x, beamLen, loadPos, loadForce, beamSup)
    if not loadForce.any():
        y2 = beamSuperposition(loadPos, beamLen, loadPos, loadForce, beamSup)
    
    fig = plt.figure()
    fig.set_figheight(10)
    fig.set_figwidth(10)
    plt.plot(x, y1, 'r-')
    if not loadForce.any():
        plt.plot(loadPos, y2, 'b*')
    



    plt.gca().invert_yaxis()
    plt.title("Beam deflection\nBeam type: {:s}".format(beamSup))
    plt.xlabel("Computed position")
    plt.ylabel("Deflection")
    plt.xlim([0, 1.05*beamLen])
    plt.xticks(np.arange(min(x), max(x)+1, beamLen/10))
    plt.ticklabel_format(style='sci', axis='y1', scilimits=(0,0))
    plt.tight_layout()
    plt.grid(color='grey', linestyle='--', linewidth=0.5) 
    
    

    # max deflection
    plt.axhline(y=np.max(y1),linewidth=1, color='g')
    
    
    # applied forces and legend
    
    force = np.array([])

    if not loadForce.any():
        for i in range(np.size(y2)):
            f = 'F({:f} m) = {:.2E} N'.format(loadPos[i], loadForce[i])
            force = np.append(force,f)
            i += i 
        force = np.sort(force)
        force = "\n".join(force)
        plt.legend(('Beam',('Load position\nForce magnitude:\n{}'.format(force)),('Max. difl. = {:.2E} m'.format(np.max(y1)))), loc = 'best')
    
    plt.show()
    
if __name__ == '__main__':
    bl = 70
    lp = np.random.uniform(low=0, high=bl, size=(40,))
    lf = np.random.uniform(low=-40, high=50, size=(40,))
    bs = 'both'
    beamPlot(bl, lp, lf, bs)