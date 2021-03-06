from proteus import *
from proteus.default_p import *
from beach_erosion_board_waves_3d import *
from proteus.mprans import NCLS#NCLSV2
if useNCLS:
    LevelModelType = NCLS.LevelModel#NCLSV2.OneLevelNCLSV2
"""
The non-conservative level set description of the free surface of a sloshing two-phase flow in a closed box.
"""
## 

##\ingroup test
#\file ls_so_sloshbox_3d_p.py
#
#\brief The non-conservative level set description of the free surface of a sloshing two-phase flow in a closed box.
#
#\todo finish ls_so_sloshbox_3d_p.py doc

if applyCorrection:
    coefficients = NCLS.Coefficients(V_model=0,RD_model=3,ME_model=1,checkMass=False)
elif applyRedistancing:
    coefficients = NCLS.Coefficients(V_model=0,RD_model=2,ME_model=1,checkMass=False)
else:
    coefficients = NCLS.Coefficients(V_model=0,ME_model=1,checkMass=False)

def getDBC_ls(x,flag):
    pass

dirichletConditions = {0:getDBC_ls}

class PerturbedSurface_vof:
    def __init__(self,waterLevel,slopeAngle):
        self.waterLevel=waterLevel
        self.slopeAngle=slopeAngle
    def uOfXT(self,x,t):
        surfaceNormal = [-sin(self.slopeAngle),cos(self.slopeAngle)]
        signedDistance = (x[0] - 0.5)*surfaceNormal[0]+(x[1] - self.waterLevel)*surfaceNormal[1]
        if signedDistance > 0.0:
            vof = 1.0
        else:
            vof = 0.0
        return vof

if runWaveProblem:
    initialConditions = {0:Flat_phi()}
else:
    if VOF:
        initialConditions  = {0:GaussianWaterColumn_vof()}
    else:
        initialConditions  = {0:GaussianWaterColumn_phi()}
    
#if nonconsrv:
fluxBoundaryConditions = {0:'outFlow'}
#else:
#    fluxBoundaryConditions = {0:'noFlow'}
    
advectiveFluxBoundaryConditions =  {}

diffusiveFluxBoundaryConditions = {0:{}}
