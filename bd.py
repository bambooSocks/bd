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
    
    plt.plot(x, y1, 'r-', loadPos, y2, 'b*',)
    plt.gca().invert_yaxis()
    plt.title("Beam deflection\nBeam type: {:s}".format(beamSup))
    plt.xlabel("Computed position")
    plt.ylabel("Deflection")
    plt.xlim([0, beamLen])
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.tight_layout()
    plt.grid(color='grey', linestyle='--', linewidth=0.5)
    
    #pointing forces
    for i in range(np.size(loadPos)):
        plt.annotate("F{:d} = {:.2E}".format(i+1,loadForce[i]), xy=(loadPos[i], y2[i]),  xycoords='data',
                xytext=(-30, 50), textcoords='offset points', arrowprops=dict(arrowstyle="->"))
    
    #max diflection
    plt.axhline(y=np.max(y1),linewidth=0.5, color='g')
    plt.text(0,np.max(y1), 'Max. difl. = {:.2E}'.format(np.max(y1)), fontsize=6)
    
    plt.show()
    
if __name__ == '__main__':
    bl = 600000
    lp = np.random.uniform(low=0, high=bl, size=(4,))
    lf = np.random.uniform(low=0, high=50, size=(4,))
    bs = 'both'#'cantilever'#
    beamPlot(bl, lp, lf, bs)