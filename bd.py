import numpy as np
import matplotlib.pyplot as plt


def beamDeflection(pos,beamLen,loadPos,loadForce,beamSup):
    
    deflection = np.zeros(np.size(pos))
    EI = 1.2e9
    
    for idx, id in enumerate(pos):
        if beamSup == "both":
            if id < loadPos:
                k=(loadForce*(beamLen-loadPos)*id)/(EI*beamLen)
                j=(beamLen**2-id**2-(beamLen-loadPos)**2)
            
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

def beamSuperposition(pos,beamLen,loadPos,loadForce,beamSup):
    
    deflection=np.zeros(np.size(pos))

    for idx, id in enumerate(loadPos):    
        deflection += beamDeflection(pos,beamLen,id,loadForce[idx],beamSup)

    return deflection


bl= 6
lp = np.array([0.4,0.6])
lf = np.array([-5.00,-6.00])
bs = 'cantilever'#'both'


def beamPlot(beamLen, loadPos, loadForce, beamSup):
    x = np.sort(np.random.uniform(low=0.0, high=beamLen, size=(100,)))
    y = beamSuperposition(x,beamLen, loadPos, loadForce, beamSup)
    #y = beamDeflection(x, beamLen, loadPos, loadForce, beamSup)
    a = np.array([loadPos])
    y1 = beamDeflection(a, beamLen, loadPos, loadForce, beamSup)
    #plt.plot(a, y, 'b*')
    plt.plot(x, y, 'r-', a, y1, 'b*')
    plt.title("Beam deflection")
    plt.xlabel("Computed position")
    plt.ylabel("Deflection")
    plt.xlim([0, beamLen])
    
    
    plt.show()
    
beamPlot(bl, lp, lf, bs)