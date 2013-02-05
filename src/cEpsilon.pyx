import numpy
cimport numpy
from proteus import *
from proteus.Transport import *
from proteus.Transport import OneLevelTransport

cdef extern from "Epsilon.h" namespace "proteus":
    cdef cppclass Epsilon_base:
        void calculateResidual(double* mesh_trial_ref,
                               double* mesh_grad_trial_ref,
                               double* mesh_dof,
                               double* mesh_velocity_dof,
                               double MOVING_DOMAIN,
                               int* mesh_l2g,
                               double* dV_ref,
                               double* u_trial_ref,
                               double* u_grad_trial_ref,
                               double* u_test_ref,
                               double* u_grad_test_ref,
                               double* mesh_trial_trace_ref,
                               double* mesh_grad_trial_trace_ref,
                               double* dS_ref,
                               double* u_trial_trace_ref,
                               double* u_grad_trial_trace_ref,
                               double* u_test_trace_ref,
                               double* u_grad_test_trace_ref,
                               double* normal_ref,
                               double* boundaryJac_ref,
                               int nElements_global,
                               #diffusion terms
                               double nu_0,
                               double nu_1,
                               double sigma_k,
                               double c_mu,
                               double c_1,
                               double c_2,
                               double c_e,
                               #end diffusion
			       double useMetrics, 
                               double alphaBDF,
                               int lag_shockCapturing,
                               double shockCapturingDiffusion,
		               double sc_uref, double sc_alpha,
                               int* u_l2g, 
                               double* elementDiameter,
                               double* u_dof,double* u_dof_old,	
                               double* velocity,
                               double* phi_ls, #level set variable
                               double* q_kappa, #kinetic energy variable
                               #velocity dof
                               double * velocity_dof_u,
                               double * velocity_dof_v,
                               double * velocity_dof_w,
                               #end velocity dof
                               double* q_m,
                               double* q_u,
                               double* q_m_betaBDF,
                               double* cfl,
                               double* q_numDiff_u, 
                               double* q_numDiff_u_last,
                               double* ebqe_penalty_ext,
                               int offset_u, int stride_u, 
                               double* globalResidual,
                               int nExteriorElementBoundaries_global,
                               int* exteriorElementBoundariesArray,
                               int* elementBoundaryElementsArray,
                               int* elementBoundaryLocalElementBoundariesArray,
                               double* ebqe_velocity_ext,
                               int* isDOFBoundary_u,
                               double* ebqe_bc_u_ext,
                               int* isFluxBoundary_u,
                               double* ebqe_bc_flux_u_ext,
                               double* ebqe_phi,double epsFact,
                               double* ebqe_kappa, #kinetic energy 
                               double* ebqe_u,
                               double* ebqe_flux)
        void calculateJacobian(double* mesh_trial_ref,
                               double* mesh_grad_trial_ref,
                               double* mesh_dof,
                               double* mesh_velocity_dof,
                               double MOVING_DOMAIN,
                               int* mesh_l2g,
                               double* dV_ref,
                               double* u_trial_ref,
                               double* u_grad_trial_ref,
                               double* u_test_ref,
                               double* u_grad_test_ref,
                               double* mesh_trial_trace_ref,
                               double* mesh_grad_trial_trace_ref,
                               double* dS_ref,
                               double* u_trial_trace_ref,
                               double* u_grad_trial_trace_ref,
                               double* u_test_trace_ref,
                               double* u_grad_test_trace_ref,
                               double* normal_ref,
                               double* boundaryJac_ref,
                               int nElements_global,
                               #diffusion
                               double nu_0,
                               double nu_1,
                               double sigma_k,
                               double c_mu,
                               double c_1,
                               double c_2,
                               double c_e,
                               #end diffuion
			       double useMetrics, 
                               double alphaBDF,
                               int lag_shockCapturing,
                               double shockCapturingDiffusion,
                               int* u_l2g,
                               double* elementDiameter,
                               double* u_dof, 
                               double* velocity,
                               double* phi_ls, #level set variable
                               double* q_kappa, #kinetic energy 
                               #velocity dof
                               double* velocity_dof_u,
                               double* velocity_dof_v,
                               double* velocity_dof_w,
                               #end velocity dof
                               double* q_m_betaBDF, 
                               double* cfl,
                               double* q_numDiff_u_last, 
                               double* ebqe_penalty_ext,
                               int* csrRowIndeces_u_u,int* csrColumnOffsets_u_u,
                               double* globalJacobian,
                               int nExteriorElementBoundaries_global,
                               int* exteriorElementBoundariesArray,
                               int* elementBoundaryElementsArray,
                               int* elementBoundaryLocalElementBoundariesArray,
                               double* ebqe_velocity_ext,
                               int* isDOFBoundary_u,
                               double* ebqe_bc_u_ext,
                               int* isFluxBoundary_u,
                               double* ebqe_bc_flux_u_ext,
                               int* csrColumnOffsets_eb_u_u,
                               double* ebqe_phi,double epsFact,
                               double* ebqe_kappa)#kinetic energy 
    Epsilon_base* newEpsilon(int nSpaceIn,
                       int nQuadraturePoints_elementIn,
                       int nDOF_mesh_trial_elementIn,
                       int nDOF_trial_elementIn,
                       int nDOF_test_elementIn,
                       int nQuadraturePoints_elementBoundaryIn,
                       int CompKernelFlag)

cdef class cEpsilon_base:
   cdef Epsilon_base* thisptr
   def __cinit__(self,
                 int nSpaceIn,
                 int nQuadraturePoints_elementIn,
                 int nDOF_mesh_trial_elementIn,
                 int nDOF_trial_elementIn,
                 int nDOF_test_elementIn,
                 int nQuadraturePoints_elementBoundaryIn,
                 int CompKernelFlag):
       self.thisptr = newEpsilon(nSpaceIn,
                             nQuadraturePoints_elementIn,
                             nDOF_mesh_trial_elementIn,
                             nDOF_trial_elementIn,
                             nDOF_test_elementIn,
                             nQuadraturePoints_elementBoundaryIn,
                             CompKernelFlag)
   def __dealloc__(self):
       del self.thisptr
   def calculateResidual(self,
                         numpy.ndarray mesh_trial_ref,
                         numpy.ndarray mesh_grad_trial_ref,
                         numpy.ndarray mesh_dof,
                         numpy.ndarray mesh_velocity_dof,
                         double MOVING_DOMAIN,
                         numpy.ndarray mesh_l2g,
                         numpy.ndarray dV_ref,
                         numpy.ndarray u_trial_ref,
                         numpy.ndarray u_grad_trial_ref,
                         numpy.ndarray u_test_ref,
                         numpy.ndarray u_grad_test_ref,
                         numpy.ndarray mesh_trial_trace_ref,
                         numpy.ndarray mesh_grad_trial_trace_ref,
                         numpy.ndarray dS_ref,
                         numpy.ndarray u_trial_trace_ref,
                         numpy.ndarray u_grad_trial_trace_ref,
                         numpy.ndarray u_test_trace_ref,
                         numpy.ndarray u_grad_test_trace_ref,
                         numpy.ndarray normal_ref,
                         numpy.ndarray boundaryJac_ref,
                         int nElements_global,
                         #diffusion terms
                         double nu_0,
                         double nu_1,
                         double sigma_k,
                         double c_mu,
                         double c_1,
                         double c_2,
                         double c_e,
                         #end diffusion
			 double useMetrics, 
                         double alphaBDF,
                         int lag_shockCapturing,
                         double shockCapturingDiffusion,
			 double sc_uref, double sc_alpha,
                         numpy.ndarray u_l2g, 
                         numpy.ndarray elementDiameter,
                         numpy.ndarray u_dof,
                         numpy.ndarray u_dof_old,
                         numpy.ndarray velocity,
                         numpy.ndarray phi_ls, #level set variable
                         numpy.ndarray q_kappa, #kinetic energy 
                         #velocity dof
                         numpy.ndarray velocity_dof_u,
                         numpy.ndarray velocity_dof_v,
                         numpy.ndarray velocity_dof_w,
                         #end velocity dof
                         numpy.ndarray q_m,
                         numpy.ndarray q_u,
                         numpy.ndarray q_m_betaBDF,
                         numpy.ndarray cfl,
                         numpy.ndarray q_numDiff_u, 
                         numpy.ndarray q_numDiff_u_last, 
                         numpy.ndarray ebqe_penalty_ext,
                         int offset_u, int stride_u, 
                         numpy.ndarray globalResidual,
                         int nExteriorElementBoundaries_global,
                         numpy.ndarray exteriorElementBoundariesArray,
                         numpy.ndarray elementBoundaryElementsArray,
                         numpy.ndarray elementBoundaryLocalElementBoundariesArray,
                         numpy.ndarray ebqe_velocity_ext,
                         numpy.ndarray isDOFBoundary_u,
                         numpy.ndarray ebqe_bc_u_ext,
                         numpy.ndarray isFluxBoundary_u,
                         numpy.ndarray ebqe_bc_flux_u_ext,
                         numpy.ndarray ebqe_phi,double epsFact,
                         numpy.ndarray ebqe_kappa,#kinetic energy 
                         numpy.ndarray ebqe_u,
                         numpy.ndarray ebqe_flux):
       self.thisptr.calculateResidual(<double*> mesh_trial_ref.data,
                                       <double*> mesh_grad_trial_ref.data,
                                       <double*> mesh_dof.data,
                                       <double*> mesh_velocity_dof.data,
                                       MOVING_DOMAIN,
                                       <int*> mesh_l2g.data,
                                       <double*> dV_ref.data,
                                       <double*> u_trial_ref.data,
                                       <double*> u_grad_trial_ref.data,
                                       <double*> u_test_ref.data,
                                       <double*> u_grad_test_ref.data,
                                       <double*> mesh_trial_trace_ref.data,
                                       <double*> mesh_grad_trial_trace_ref.data,
                                       <double*> dS_ref.data,
                                       <double*> u_trial_trace_ref.data,
                                       <double*> u_grad_trial_trace_ref.data,
                                       <double*> u_test_trace_ref.data,
                                       <double*> u_grad_test_trace_ref.data,
                                       <double*> normal_ref.data,
                                       <double*> boundaryJac_ref.data,
                                       nElements_global,
                                       #diffusion
                                       nu_0,
                                       nu_1,
                                       sigma_k,
                                       c_mu,
                                       c_1,
                                       c_2,
                                       c_e,
                                       #end diffuion
			               useMetrics, 
                                       alphaBDF,
                                       lag_shockCapturing,
                                       shockCapturingDiffusion,
			               sc_uref, sc_alpha,
                                       <int*> u_l2g.data, 
                                       <double*> elementDiameter.data,
                                       <double*> u_dof.data,
				       <double*> u_dof_old.data,	
                                       <double*> velocity.data,
                                       <double*> phi_ls.data,
                                       <double*> q_kappa.data,#kinetic energy 
                                       #velocity dof
                                       <double*> velocity_dof_u.data,
                                       <double*> velocity_dof_v.data,
                                       <double*> velocity_dof_w.data,
                                      #end velocity dof
                                       <double*> q_m.data,
                                       <double*> q_u.data,
                                       <double*> q_m_betaBDF.data,
                                       <double*> cfl.data,
                                       <double*> q_numDiff_u.data, 
                                       <double*> q_numDiff_u_last.data, 
                                       <double*> ebqe_penalty_ext.data,
                                       offset_u, stride_u, 
                                       <double*> globalResidual.data,
                                       nExteriorElementBoundaries_global,
                                       <int*> exteriorElementBoundariesArray.data,
                                       <int*> elementBoundaryElementsArray.data,
                                       <int*> elementBoundaryLocalElementBoundariesArray.data,
                                       <double*> ebqe_velocity_ext.data,
                                       <int*> isDOFBoundary_u.data,
                                       <double*> ebqe_bc_u_ext.data,
                                       <int*> isFluxBoundary_u.data,
                                       <double*> ebqe_bc_flux_u_ext.data,
                                       <double*> ebqe_phi.data,
                                       epsFact,
                                       <double*> ebqe_kappa.data,#kinetic energy on boundary
                                       <double*> ebqe_u.data,
                                       <double*> ebqe_flux.data)
   def calculateJacobian(self,
                         numpy.ndarray mesh_trial_ref,
                         numpy.ndarray mesh_grad_trial_ref,
                         numpy.ndarray mesh_dof,
                         numpy.ndarray mesh_velocity_dof,
                         double MOVING_DOMAIN,
                         numpy.ndarray mesh_l2g,
                         numpy.ndarray dV_ref,
                         numpy.ndarray u_trial_ref,
                         numpy.ndarray u_grad_trial_ref,
                         numpy.ndarray u_test_ref,
                         numpy.ndarray u_grad_test_ref,
                         numpy.ndarray mesh_trial_trace_ref,
                         numpy.ndarray mesh_grad_trial_trace_ref,
                         numpy.ndarray dS_ref,
                         numpy.ndarray u_trial_trace_ref,
                         numpy.ndarray u_grad_trial_trace_ref,
                         numpy.ndarray u_test_trace_ref,
                         numpy.ndarray u_grad_test_trace_ref,
                         numpy.ndarray normal_ref,
                         numpy.ndarray boundaryJac_ref,
                         int nElements_global,
                         #diffusion
                         double nu_0,
                         double nu_1,
                         double sigma_k,
                         double c_mu,
                         double c_1,
                         double c_2,
                         double c_e,
                         #end diffusion
			 double useMetrics, 
                         double alphaBDF,
                         int lag_shockCapturing,
                         double shockCapturingDiffusion,
                         numpy.ndarray u_l2g,
                         numpy.ndarray elementDiameter,
                         numpy.ndarray u_dof, 
                         numpy.ndarray velocity,
                         numpy.ndarray phi_ls, #level set variable
                         numpy.ndarray q_kappa, #kinetic energy 
                         #velocity dof
                         numpy.ndarray velocity_dof_u,
                         numpy.ndarray velocity_dof_v,
                         numpy.ndarray velocity_dof_w,
                         #end velocity dof
                         numpy.ndarray q_m_betaBDF, 
                         numpy.ndarray cfl,
                         numpy.ndarray q_numDiff_u_last, 
                         numpy.ndarray ebqe_penalty_ext,
                         numpy.ndarray csrRowIndeces_u_u,numpy.ndarray csrColumnOffsets_u_u,
                         globalJacobian,
                         int nExteriorElementBoundaries_global,
                         numpy.ndarray exteriorElementBoundariesArray,
                         numpy.ndarray elementBoundaryElementsArray,
                         numpy.ndarray elementBoundaryLocalElementBoundariesArray,
                         numpy.ndarray ebqe_velocity_ext,
                         numpy.ndarray isDOFBoundary_u,
                         numpy.ndarray ebqe_bc_u_ext,
                         numpy.ndarray isFluxBoundary_u,
                         numpy.ndarray ebqe_bc_flux_u_ext,
                         numpy.ndarray csrColumnOffsets_eb_u_u,
                         numpy.ndarray ebqe_phi,
                         double epsFact,
                         numpy.ndarray ebqe_kappa): #kinetic energy 

       cdef numpy.ndarray rowptr,colind,globalJacobian_a
       (rowptr,colind,globalJacobian_a) = globalJacobian.getCSRrepresentation()
       self.thisptr.calculateJacobian(<double*> mesh_trial_ref.data,
                                       <double*> mesh_grad_trial_ref.data,
                                       <double*> mesh_dof.data,
                                       <double*> mesh_velocity_dof.data,
                                       MOVING_DOMAIN,
                                       <int*> mesh_l2g.data,
                                       <double*> dV_ref.data,
                                       <double*> u_trial_ref.data,
                                       <double*> u_grad_trial_ref.data,
                                       <double*> u_test_ref.data,
                                       <double*> u_grad_test_ref.data,
                                       <double*> mesh_trial_trace_ref.data,
                                       <double*> mesh_grad_trial_trace_ref.data,
                                       <double*> dS_ref.data,
                                       <double*> u_trial_trace_ref.data,
                                       <double*> u_grad_trial_trace_ref.data,
                                       <double*> u_test_trace_ref.data,
                                       <double*> u_grad_test_trace_ref.data,
                                       <double*> normal_ref.data,
                                       <double*> boundaryJac_ref.data,
                                       nElements_global,
                                       #diffusion
                                       nu_0,
                                       nu_1,
                                       sigma_k,
                                       c_mu,
                                       c_1,
                                       c_2,
                                       c_e,
                                       #end diffusion
			               useMetrics, 
                                       alphaBDF,
                                       lag_shockCapturing,
                                       shockCapturingDiffusion,
                                       <int*> u_l2g.data,
                                       <double*> elementDiameter.data,
                                       <double*> u_dof.data, 
                                       <double*> velocity.data,
                                       <double*> phi_ls.data,
                                       <double*> q_kappa.data,
                                       #velocity dofs
                                       <double*> velocity_dof_u.data,
                                       <double*> velocity_dof_v.data,
                                       <double*> velocity_dof_w.data,
                                       #end velocity dofs
                                       <double*> q_m_betaBDF.data, 
                                       <double*> cfl.data,
                                       <double*> q_numDiff_u_last.data, 
                                       <double*> ebqe_penalty_ext.data,
                                       <int*> csrRowIndeces_u_u.data,<int*> csrColumnOffsets_u_u.data,
                                       <double*> globalJacobian_a.data,
                                       nExteriorElementBoundaries_global,
                                       <int*> exteriorElementBoundariesArray.data,
                                       <int*> elementBoundaryElementsArray.data,
                                       <int*> elementBoundaryLocalElementBoundariesArray.data,
                                       <double*> ebqe_velocity_ext.data,
                                       <int*> isDOFBoundary_u.data,
                                       <double*> ebqe_bc_u_ext.data,
                                       <int*> isFluxBoundary_u.data,
                                       <double*> ebqe_bc_flux_u_ext.data,
                                       <int*> csrColumnOffsets_eb_u_u.data,                      
                                       <double*> ebqe_phi.data,epsFact,
                                       <double*> ebqe_kappa.data)
