import numpy as np


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