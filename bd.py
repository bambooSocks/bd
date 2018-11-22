import numpy as np
import matplotlib.pyplot as plt

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

def beamSuperposition(pos, beamLen, loadPos, loadForce, beamSup):
    deflection = np.zeros(np.size(pos))

    for idx, id in enumerate(loadPos):    # the same here
        deflection += beamDeflection(pos,beamLen,id,loadForce[idx],beamSup)

    return deflection

def beamPlot(beamLen, loadPos, loadForce, beamSup):
    x = np.arange(0., beamLen + beamLen/100, beamLen/100)
    y1 = beamSuperposition(x, beamLen, loadPos, loadForce, beamSup)
    y2 = beamSuperposition(loadPos, beamLen, loadPos, loadForce, beamSup)

    plt.plot(x, y1, 'r-', loadPos, y2, 'b*')
    plt.gca().invert_yaxis()
    plt.title("Beam deflection")
    plt.xlabel("Computed position")
    plt.ylabel("Deflection")
    plt.xlim([0, beamLen])
    
    plt.show()
    
if __name__ == '__main__':
    bl = 6
    lp = np.array([2, 4])
    lf = np.array([5000, 5000])
    bs = 'both'#'cantilever'#
    beamPlot(bl, lp, lf, bs)