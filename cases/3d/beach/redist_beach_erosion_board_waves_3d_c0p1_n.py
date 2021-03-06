from proteus import *
from proteus.default_n import *
from redist_beach_erosion_board_waves_3d_p import *
from beach_erosion_board_waves_3d import *

if rdtimeIntegration == 'newton':    
    timeIntegration = NoIntegration
    stepController = Newton_controller
elif rdtimeIntegration == 'tte':
    timeIntegration = BackwardEuler_cfl
    timeIntegration = PsiTCtte
elif rdtimeIntegration == 'osher-fmm':
    timeIntegration = BackwardEuler_cfl
    stepController = Osher_FMM_controller
    runCFL=1.0
else:
    timeIntegration = BackwardEuler_cfl
    stepController = Osher_PsiTC_controller 
   #stepController = Osher_controller
    runCFL=1.0
#     timeIntegration = PsiTCtte
#     stepController = PsiTCtte_controller
#     rtol_res[0] = 0.0
#     atol_res[0] = 0.1*L[0]/(nn-1.0)#10% of he
#runCFL=1.0
#DT=None

if spaceOrder == 1:
    femSpaces = {0:C0_AffineLinearOnSimplexWithNodalBasis}
if spaceOrder == 2:
    femSpaces = {0:C0_AffineQuadraticOnSimplexWithNodalBasis}

elementQuadrature = SimplexGaussQuadrature(nd,sloshbox_quad_order)

elementBoundaryQuadrature = SimplexGaussQuadrature(nd-1,sloshbox_quad_order)

subgridErrorType = HamiltonJacobi_ASGS
if LevelModelType == RDLS.LevelModel:#RDLSV2.OneLevelRDLSV2 and not RDLSV2.debugRDLS:
    subgridErrorType = HamiltonJacobi_ASGS_opt
if rdtimeIntegration == 'newton':
    subgridError = subgridErrorType(coefficients,nd,stabFlag='2',lag=False)
else:
    subgridError = subgridErrorType(coefficients,nd,stabFlag='2',lag=True)
    
#subgridError = HamiltonJacobi_ASGS(coefficients,nd,lag=True)

shockCapturing = None
#shockCapturing = ResGrad_SC(coefficients,nd,shockCapturingFactor=0.9,lag=False)
if rdtimeIntegration == 'newton':    
    shockCapturing = ResGradQuad_SC(coefficients,nd,shockCapturingFactor=rd_shockCapturingFactor,lag=False)
else:
    shockCapturing = ResGradQuad_SC(coefficients,nd,shockCapturingFactor=rd_shockCapturingFactor,lag=True)
    
massLumping = False


#multilevelNonlinearSolver  = MultilevelEikonalSolver
#levelNonlinearSolver = UnstructuredFMMandFSWsolvers.FMMEikonalSolver
multilevelNonlinearSolver  = NLNI
levelNonlinearSolver = Newton
if rdtimeIntegration != 'newton':    
    maxLineSearches = 0
nonlinearSmoother = NLGaussSeidel

fullNewtonFlag = True

#this needs to be set appropriately for pseudo-transient
tolFac = 0.0

nl_atol_res = 0.01*L[0]/nn

atol_res[0] = 1.0e-6 #for pseudo transient
rtol_res[0] = 0.0

numericalFluxType = DoNothing

maxNonlinearIts = 50 #1 for PTC

matrix = SparseMatrix

if usePETSc:
    numericalFluxType = DoNothing
    
    multilevelLinearSolver = PETSc
    
    levelLinearSolver = PETSc
else:
    multilevelLinearSolver = LU
    
    levelLinearSolver = LU

linearSmoother = GaussSeidel

linTolFac = 0.001

conservativeFlux = None
