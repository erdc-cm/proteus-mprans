from proteus import *
from proteus.default_p import *
from step import *
from proteus.mprans import Kappa

LevelModelType = Kappa.LevelModel
dissipation_model_flag = 1
if use_KOmega == True:
    dissipation_model_flag=2
coefficients = Kappa.Coefficients(V_model=0,ME_model=3,LS_model=1,RD_model=None,dissipation_model=4,
                                  dissipation_model_flag=dissipation_model_flag,#1 -- K-epsilon, 2 -- K-omega
                                  useMetrics=useMetrics,
                                  rho_0=rho_0,nu_0=nu_0,
                                  rho_1=rho_1,nu_1=nu_1,
                                  g=g,
                                  c_mu=0.09,sigma_k=1.0,
                                  sc_uref=kappa_sc_uref,sc_beta=kappa_sc_beta)


def getDBC_k(x,flag):
    if flag == boundaryTags['upstream']:
        return lambda x,t:kInflow

dirichletConditions = {0:getDBC_k}
fluxBoundaryConditions = {0:'outFlow'}

def getAFBC_k(x,flag):
    if flag == boundaryTags['downstream']:
        return None
    if flag != boundaryTags['upstream']:
        return lambda x,t: 0.0
def getDFBC_k(x,flag):
    pass
#    if flag == boundaryTags['downstream']:
#        return lambda x,t: 0.0
#    if flag != boundaryTags['upstream']:
#        return lambda x,t: 0.0
    

advectiveFluxBoundaryConditions =  {0:getAFBC_k}
diffusiveFluxBoundaryConditions = {0:{0:getDFBC_k}}



class ConstantIC:
    def __init__(self,cval=0.0):
        self.cval=cval
    def uOfXT(self,x,t):
        return self.cval
   
initialConditions  = {0:ConstantIC(cval=kInflow*0.001)}
