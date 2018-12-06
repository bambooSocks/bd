import numpy as np
import matplotlib.pyplot as plt

##
## @brief      Calculate the deflection of a single force
##
## @param      pos        The position
## @param      beamLen    The beam length
## @param      loadPos    The load position
## @param      loadForce  The load force
## @param      beamSup    The beam sup
##
## @return     { description_of_the_return_value }
##
## @author     Johan Emil Levin-Jensen
##
def beamDeflection(pos, beamLen, loadPos, loadForce, beamSup):  
    deflection = np.zeros(np.size(pos))
    EI = 1.2e9      # mention this
    
    for idx, id in enumerate(pos):      # mention id name ... not good, it is not descriptive
        if beamSup == "both":
            if id < loadPos:
                k=(loadForce*(beamLen-loadPos)*id)/(EI*beamLen)
                j=(beamLen**2-id**2-(beamLen-loadPos)**2)       # no need for extra parentecies
            
            if id >= loadPos:
                k=(loadForce*loadPos*(beamLen-id))/(EI*beamLen)
                j=(beamLen**2-(beamLen-id)**2-loadPos**2)
        
        if beamSup == "cantilever":
            if id < loadPos:
                k=(loadForce*id**2)/EI
                j=3*loadPos-id
                
            if id >= loadPos:
                k=(loadForce*loadPos**2)/EI
                j=3*id-loadPos
        
        deflection[idx]=k*j
    
    return deflection

##
## @brief      { function_description }
##
## @param      pos        The position
## @param      beamLen    The beam length
## @param      loadPos    The load position
## @param      loadForce  The load force
## @param      beamSup    The beam sup
##
## @return     { description_of_the_return_value }
##
## @author     Johan Emil Levin-Jensen
##
def beamSuperposition(pos, beamLen, loadPos, loadForce, beamSup):
    deflection = np.zeros(np.size(pos))

    for idx, id in enumerate(loadPos):    # the same here
        deflection += beamDeflection(pos,beamLen,id,loadForce[idx],beamSup)

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
    y2 = beamSuperposition(loadPos, beamLen, loadPos, loadForce, beamSup)
    
    fig = plt.figure()
    fig.set_figheight(10)
    fig.set_figwidth(10)
    plt.plot(x, y1, 'r-')
    plt.plot(loadPos, y2, 'b*')
    



    plt.gca().invert_yaxis()
    plt.title("Beam deflection\nBeam type: {:s}".format(beamSup))
    plt.xlabel("Computed position")
    plt.ylabel("Deflection")
    plt.xlim([0, 1.05*beamLen])
    plt.xticks(np.arange(min(x), max(x)+1, bl/10))
    plt.ticklabel_format(style='sci', axis='y1', scilimits=(0,0))
    plt.tight_layout()
    plt.grid(color='grey', linestyle='--', linewidth=0.5) 
    
    

    #max diflection
    plt.axhline(y=np.max(y1),linewidth=1, color='g')
    
    
    #applied forces and legend
    
    force = np.array([])

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