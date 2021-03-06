#! /usr/bin/env python
import proteus
from proteus import Domain

import numpy
def discretize_yz_plane(y,z,r,theta):
        y[:] = r*numpy.cos(theta)
        z[:] = r*numpy.sin(theta)
def build_cylinder(nx,ntheta,pad_x=5.0,pad_r_fact=2.0):
    """
    work on building mesh of a cylinder
    """
    from math import sqrt,pow,pi    
    import numpy

    #surrounding domain
    r = 1.0 #cylinder
    xL   = 0.0 #starting point for cylinder
    cyl_length=5.
    x_ll = [-pad_x*0.5,-r - 0.5*pad_r_fact,-r - 0.5*pad_r_fact] #lower left for bounding box
    L = [pad_x+cyl_length,2.0*r + pad_r_fact,2.0*r + pad_r_fact] #domain box

    x = numpy.zeros((nx,ntheta),'d'); y = numpy.zeros((nx,ntheta),'d'); z = numpy.zeros((nx,ntheta),'d')

    dx = cyl_length/float(nx-1)
    dtheta = 2.0*pi/float(ntheta)
    theta = numpy.arange(ntheta,dtype='d')
    theta *= dtheta
    #
    #build x,y,z points on cylinder
    for i in range(nx):
        x[i].fill(xL+i*dx)
        discretize_yz_plane(y[i],z[i],r,theta)
    #
    boundaryTags = { 'bottom': 1, 'front':2, 'right':3, 'back': 4, 'left':5, 'top':6, 'obstacle':7}
    #build poly representation
    #bounding box
    vertices = [[x_ll[0],x_ll[1],x_ll[2]],#0
              [x_ll[0]+L[0],x_ll[1],x_ll[2]],#1
              [x_ll[0]+L[0],x_ll[1]+L[1],x_ll[2]],#2
              [x_ll[0],x_ll[1]+L[1],x_ll[2]],#3
              [x_ll[0],x_ll[1],x_ll[2]+L[2]],#4
              [x_ll[0]+L[0],x_ll[1],x_ll[2]+L[2]],#5
              [x_ll[0]+L[0],x_ll[1]+L[1],x_ll[2]+L[2]],#6
              [x_ll[0],x_ll[1]+L[1],x_ll[2]+L[2]]]#7
    vertexFlags=[boundaryTags['left'],
                 boundaryTags['right'],
                 boundaryTags['right'],
                 boundaryTags['left'],
                 boundaryTags['left'],
                 boundaryTags['right'],
                 boundaryTags['right'],
                 boundaryTags['left']]
    
    facets=[[[0,1,2,3]],
            [[0,1,5,4]],
            [[1,2,6,5]],
            [[2,3,7,6]],
            [[3,0,4,7]],
            [[4,5,6,7]]]
    facetFlags=[boundaryTags['bottom'],
                boundaryTags['front'],
                boundaryTags['right'],
                boundaryTags['back'],
                boundaryTags['left'],
                boundaryTags['top']]
    regions=[[x_ll[0]+0.001*L[0],x_ll[1]+0.5*r,x_ll[2]+0.5*r]]
    regionFlags=[1.0]
    holes=[[x_ll[0]+0.5*L[0],x_ll[1]+0.5*L[1],x_ll[2]+0.5*L[2]]]

    #now loop through points and build facets on cylinder
    #front face
    def vN(i,j):
        offset = 8; 
	if i > 0: offset += (i-1)*ntheta
	return offset + (j % ntheta)
    #mwf debug
    #import pdb
    #pdb.set_trace()
    front_face = [[vN(0,j) for j in range(ntheta)]]
    facets.append(front_face)
    facetFlags.append(boundaryTags['obstacle'])
    for i in range(nx-1):
        for j in range(ntheta):
            vertices.append([x[i,j],y[i,j],z[i,j]])
            vertexFlags.append(boundaryTags['obstacle'])
            #
            facets.append([[vN(i,j),vN(i+1,j),vN(i,j+1)]])
            facetFlags.append(boundaryTags['obstacle'])
            facets.append([[vN(i+1,j),vN(i+1,j+1),vN(i,j+1)]])
            facetFlags.append(boundaryTags['obstacle'])
    #
    for j in range(ntheta):
        vertices.append([x[nx-1,j],y[nx-1,j],z[nx-1,j]])
        vertexFlags.append(boundaryTags['obstacle'])
    back_face = [[vN(nx-1,j) for j in range(ntheta)]]
    facets.append(back_face)
    facetFlags.append(boundaryTags['obstacle'])
    
    domain = proteus.Domain.PiecewiseLinearComplexDomain(vertices=vertices,
                                                         vertexFlags=vertexFlags,
                                                         facets=facets,
                                                         facetFlags=facetFlags,
                                                         regions=regions,
                                                         regionFlags=regionFlags,
                                                         holes=holes)
    #go ahead and add a boundary tags member 
    domain.boundaryTags = boundaryTags
    return x,y,z,domain,x_ll,L

def build_domain_from_axisymmetric_points(x,y,z,x_ll,L,regions=None,regionFlags=None,include_front_and_back=1,theta_offset_user=None,name='axi'):
    """
    basic code for building domain from point set generated as regular grid in x,y,z with x
    as central axis
    """
    from math import sqrt,pow,pi    
    import numpy
    nx = x.shape[0]; 
    if theta_offset_user == None:
        theta_offset = numpy.arange(((nx+1)*x.shape[1],),'i',step=x.shape[1])
    else:
        theta_offset = theta_offset_user
    assert y.shape[0] == nx; assert z.shape[0] == nx
    assert y.shape[1] == x.shape[1] ; assert z.shape[1] == x.shape[1]
    #
    boundaryTags = { 'bottom': 1, 'front':2, 'right':3, 'back': 4, 'left':5, 'top':6, 'obstacle':7}
    #build poly representation
    #bounding box
    vertices = [[x_ll[0],x_ll[1],x_ll[2]],#0
              [x_ll[0]+L[0],x_ll[1],x_ll[2]],#1
              [x_ll[0]+L[0],x_ll[1]+L[1],x_ll[2]],#2
              [x_ll[0],x_ll[1]+L[1],x_ll[2]],#3
              [x_ll[0],x_ll[1],x_ll[2]+L[2]],#4
              [x_ll[0]+L[0],x_ll[1],x_ll[2]+L[2]],#5
              [x_ll[0]+L[0],x_ll[1]+L[1],x_ll[2]+L[2]],#6
              [x_ll[0],x_ll[1]+L[1],x_ll[2]+L[2]]]#7
    vertexFlags=[boundaryTags['left'],
                 boundaryTags['right'],
                 boundaryTags['right'],
                 boundaryTags['left'],
                 boundaryTags['left'],
                 boundaryTags['right'],
                 boundaryTags['right'],
                 boundaryTags['left']]
    
    facets=[[[0,1,2,3]],
            [[0,1,5,4]],
            [[1,2,6,5]],
            [[2,3,7,6]],
            [[3,0,4,7]],
            [[4,5,6,7]]]
    facetFlags=[boundaryTags['bottom'],
                boundaryTags['front'],
                boundaryTags['right'],
                boundaryTags['back'],
                boundaryTags['left'],
                boundaryTags['top']]
    if regions == None:
	    regions=[[x_ll[0]+0.001*L[0],x_ll[1]+0.001*L[1],x_ll[2]+0.001*L[2]]]
    if regionFlags == None:
	    regionFlags=[1.0]
    holes=[[x_ll[0]+0.5*L[0],x_ll[1]+0.5*L[1],x_ll[2]+0.5*L[2]]]

    #now loop through points and build facets on cylinder
    #front face
    def vN(i,j):
        offset = 8 + theta_offset[i]
        return offset + (j % (theta_offset[i+1]-theta_offset[i]))

    #mwf debug
    #import pdb
    #pdb.set_trace()
    if include_front_and_back >= 1:
        front_face = [[vN(0,j) for j in range(theta_offset[1]-theta_offset[0])]]
        facets.append(front_face)
        facetFlags.append(boundaryTags['obstacle'])
    elif (theta_offset[1]-theta_offset[0]) == 1: #start of body is a single point
        i=0; j=0
        vertices.append([x[i,j],y[i,j],z[i,j]])
        vertexFlags.append(boundaryTags['obstacle'])
        for j in range(theta_offset[i+2]-theta_offset[i+1]): #connect all of next ring of points to start
            if vN(i+1,j+1) != vN(i+1,j):
	    	facets.append([[vN(i,j),vN(i+1,j),vN(i+1,j+1)]])
		facetFlags.append(boundaryTags['obstacle'])
            
    for i in range(1,nx-1):
        for j in range(theta_offset[i+1]-theta_offset[i]):
            #if i == nx-2:
            #   import pdb
	    #	pdb.set_trace()
            vertices.append([x[i,j],y[i,j],z[i,j]])
            vertexFlags.append(boundaryTags['obstacle'])
            #
            if vN(i,j+1) != vN(i,j):
	    	facets.append([[vN(i,j),vN(i+1,j),vN(i,j+1)]])
		facetFlags.append(boundaryTags['obstacle'])
	    if vN(i+1,j) != vN(i+1,j+1):
    	        facets.append([[vN(i+1,j),vN(i+1,j+1),vN(i,j+1)]])
		facetFlags.append(boundaryTags['obstacle'])
    #
    #include last set of points regardless
    for j in range(theta_offset[nx]-theta_offset[nx-1]):
        vertices.append([x[nx-1,j],y[nx-1,j],z[nx-1,j]])
        vertexFlags.append(boundaryTags['obstacle'])
    #
    if include_front_and_back >= 2:
        for j in range(theta_offset[nx]-theta_offset[nx-1]):
            vertices.append([x[nx-1,j],y[nx-1,j],z[nx-1,j]])
            vertexFlags.append(boundaryTags['obstacle'])
	back_face = [[vN(nx-1,j) for j in range(theta_offset[nx]-theta_offset[nx-1])]]
	facets.append(back_face)
	facetFlags.append(boundaryTags['obstacle'])
    
    domain = proteus.Domain.PiecewiseLinearComplexDomain(vertices=vertices,
                                                         vertexFlags=vertexFlags,
                                                         facets=facets,
                                                         facetFlags=facetFlags,
                                                         regions=regions,
                                                         regionFlags=regionFlags,
                                                         holes=holes)
    #go ahead and add a boundary tags member 
    domain.boundaryTags = boundaryTags

    return domain

def build_2d_domain_from_axisymmetric_points(x,y,x_ll,L,regions=None,regionFlags=None,
                                             has_duplicate_endpoints=True,name='axi'):
    """
    basic code for building domain from point set generated as regular grid in x,y with x
    as central axis
    """
    from math import sqrt,pow,pi    
    import numpy
    nx = x.shape[0];
    assert 2 == x.shape[1], "assumes only 2 points in theta"
    
    assert y.shape[0] == nx; 
    assert y.shape[1] == x.shape[1] ; 
    #
    boundaryTags = { 'bottom': 1, 'right':2, 'left':3, 'top':4, 'obstacle':5}
    #build poly representation
    #bounding box
    vertices = [[x_ll[0],x_ll[1],x_ll[2]],#0
                [x_ll[0]+L[0],x_ll[1],x_ll[2]],#1
                [x_ll[0]+L[0],x_ll[1]+L[1],x_ll[2]],#2
                [x_ll[0],x_ll[1]+L[1],x_ll[2]]]#3
              
    vertexFlags=[boundaryTags['left'],
                 boundaryTags['right'],
                 boundaryTags['right'],
                 boundaryTags['left']]
    
    segments = [[0,1],
                [1,2],
                [2,3],
                [3,0]]
    segmentFlags = [boundaryTags['bottom'],
                    boundaryTags['right'],
                    boundaryTags['top'],
                    boundaryTags['left']]

    if regions == None:
	    regions=[[x_ll[0]+0.001*L[0],x_ll[1]+0.001*L[1]]]
    if regionFlags == None:
	    regionFlags=[1.0]
    holes=[[x_ll[0]+0.5*L[0],x_ll[1]+0.5*L[1]]]
    #
    offset = 4; obstacle_start=offset
    vertices.append([x[0,0],y[0,0]])
    vertexFlags.append(boundaryTags['obstacle'])
    #bottom
    for i in range(nx-1):
        vertices.append([x[i+1,0],y[i+1,0]])
        vertexFlags.append(boundaryTags['obstacle'])
        segments.append([offset,offset+1])
        segmentFlags.append(boundaryTags['obstacle'])
        offset += 1
    #top
    start = nx; end = 0
    if has_duplicate_endpoints:
        start = nx-1; end = 1
    for i in range(start,end,-1):
        vertices.append([x[i-1,1],y[i-1,1]])
        vertexFlags.append(boundaryTags['obstacle'])
        segments.append([offset,offset+1])
        segmentFlags.append(boundaryTags['obstacle'])
        offset += 1
    segments.append([offset-1,obstacle_start])
    segmentFlags.append(boundaryTags['obstacle'])
    domain = proteus.Domain.PlanarStraightLineGraphDomain(vertices=vertices,
                                                          vertexFlags=vertexFlags,
                                                          segments=segments,
                                                          segmentFlags=segmentFlags,
                                                          regions=regions,
                                                          regionFlags=regionFlags,
                                                          holes=holes)
    #go ahead and add a boundary tags member 
    domain.boundaryTags = boundaryTags

    return domain

def write_csv_file(x,y,z,name='xyz'):
    fout = open(name+'.csv','w')
    fout.write('#x,y,z,r\n')
    nx=x.shape[0]; nth = x.shape[1]
    for i in range(nx):
        for j in range(nth):
            fout.write('%12.5e, %12.5e, %12.5e, %12.5e \n' % (x[i,j],y[i,j],z[i,j],(y[i,j]**2 + z[i,j]**2)))
    fout.close()

def darpa2gen(nx,ntheta,pad_x=4., pad_r_fact=4.,length_conv=1.0):
    """
    Version of original darpa2gen tha builds points in 3d using ntheta points to 
      discretize y,z plane in polar coordinates
    Note, last point in \theta is identified with first

    Original documentation:

    THIS PROGRAM CONTAINS FOLLOWING EQUATIONS FOR GENERATING
     OFFSETS IN FEET FOR DARPA2 MODEL WITH (FULL/MODEL) SCALE RATIO =24.

   INCLUDED ARE: 
     BOW EQ.	FOR	0.0 FT <- X <- 3.333333 FT, 
     PARALLEL MID-BODY EQ. FOR 3.333333 FT <- X <- 10.645833 FT, 
     AFTERBODY EQ.	FOR 10.645833 FT <- X <- 13.979167 FT, 
     AFTERBODY CAP EQ.	FOR 13-979167 FT <- X <- 14.291667 FT.
   AS SET UP HERE, OFFSETS ARE COMPUTED EVERY 0.1 FT. 
    (EXCEPT IN FIRST 0.5 FT, WHERE THEY ARE EVERY 6.01 FT)


    """
    from math import sqrt,pow,pi
    
    x = numpy.zeros((nx,ntheta),'d'); y = numpy.zeros((nx,ntheta),'d'); z = numpy.zeros((nx,ntheta),'d')
    dtheta = 2.0*pi/float(ntheta)
    theta = numpy.arange(ntheta,dtype='d')
    theta *= dtheta

    #constants
    rmax = 0.8333333
    xb   = 3.333333
    xm   = 10.645833
    xa   = 13.979167
    xc   = 14.291667
    cb1  = 1.126395191
    cb2  = 0.442874707
    cb3  = 1.0/2.1
    rh   = 0.1175
    k0   = 10.0
    k1   = 44.6244
    #bounding box info
    x_ll = [-pad_x*0.5,-rmax - 0.5*pad_r_fact,-rmax -0.5*pad_r_fact] #lower left for bounding box
    L = [pad_x+xc,2.0*rmax + pad_r_fact, 2.0*rmax + pad_r_fact] #domain box

    
    #
    xx = -0.01
    dx = 0.01
    i = 0

    
    while (i < nx and xx < xc):
        np = i
        xx += dx
        if (xx >= 0.5): dx = 0.1
        if (xx >= xa): dx = 0.01
        if (xx < xb): #otherwise skip to 200
            #bow equation
            a = 0.3*xx - 1.0
            a3= a*a*a
            a4= a3*a
            b = 1.2*xx + 1.0
            r = cb1*xx*a4 + cb2*xx*xx*a3 + 1.0 - a4*b
            r = rmax*pow(r,cb3)
            x[i].fill(xx)
            discretize_yz_plane(y[i],z[i],r,theta)
        else: #goto 200
            if (xx < xm): #otherwise skip to 400
                #parallel mid-body equation
                x[i].fill(xx)
                discretize_yz_plane(y[i],z[i],rmax,theta)
            else: #goto 400
                if (xx < xa): #otherwise goto 600
                    #afterbody equation
                    xi = (13.979167 - xx)/3.333333
                    c1 = rh*rh
                    xipow = xi*xi
                    c2 = rh*k0*xipow                  
                    xipow *= xi #3
                    c3 = (20.0 - 20.0*rh*rh - 4.0*rh*k0 - 0.333333*k1)*xipow
                    xipow *= xi #4
                    c4 = (-45.0 + 45.0*rh*rh + 6.0*rh*k0 + k1)*xipow
                    xipow *= xi #5
                    c5 = (36.0  - 36.0*rh*rh - 4.0*rh*k0 - k1)*xipow
                    xipow *= xi #6
                    c6 = (-10.0 + 10.0*rh*rh +     rh*k0 + 0.333333*k1)*xipow
                    r  = rmax*sqrt((c1+c2+c3+c4+c5+c6))
                    x[i].fill(xx)
                    discretize_yz_plane(y[i],z[i],r,theta)

                else: #goto 600
                    if (xx < xc): #otherwise goto 1100
                        #afterbody cap equation
                        r = 1.0 - (3.2*xx - 44.733333)*(3.2*xx - 44.733333)
                        assert r >= 0.0, "negative square root in afterbody cap equation"
                        r = rh*rmax*sqrt(r)
                        x[i].fill(xx)
                        discretize_yz_plane(y[i],z[i],r,theta)
                    else:#1100
                        x[np].fill(xc)
                        y[np].fill(0.0)
                        z[np].fill(0.0)
                    #end 1100 block
                #end 600 block
            #end 400 block
        #end 200 block
        i += 1
    #end loop 
    theta_offset = numpy.zeros((nx+1,),'i')
    theta_offset[0]= 0
    theta_offset[1]= 1
    for i in range(1,np):
        theta_offset[i+1]=theta_offset[i]+ntheta
    theta_offset[np+1]= 1+theta_offset[np]

    #convert length units potentially
    x *= length_conv; y *= length_conv; z *= length_conv
    for i in range(3):
	    x_ll[i] *= length_conv; L[i] *= length_conv 
    return x,y,z,theta_offset,np+1,x_ll,L
#end darpagen2

def darpa2gen_orig(npoints):
    """
    THIS PROGRAM CONTAINS FOLLOWING EQUATIONS FOR GENERATING
     OFFSETS IN FEET FOR DARPA2 MODEL WITH (FULL/MODEL) SCALE RATIO =24.

   INCLUDED ARE: 
     BOW EQ.	FOR	0.0 FT <- X <- 3.333333 FT, 
     PARALLEL MID-BODY EQ. FOR 3.333333 FT <- X <- 10.645833 FT, 
     AFTERBODY EQ.	FOR 10.645833 FT <- X <- 13.979167 FT, 
     AFTERBODY CAP EQ.	FOR 13-979167 FT <- X <- 14.291667 FT.
   AS SET UP HERE, OFFSETS ARE COMPUTED EVERY 0.1 FT. 
    (EXCEPT IN FIRST 0.5 FT, WHERE THEY ARE EVERY 6.01 FT)

    """
    from math import sqrt,pow
    import numpy
    x = numpy.zeros((npoints,),'d'); y = numpy.zeros((npoints,),'d')
    #constants
    rmax = 0.8333333
    xb   = 3.333333
    xm   = 10.645833
    xa   = 13.979167
    xc   = 14.291667
    cb1  = 1.126395191
    cb2  = 0.442874707
    cb3  = 1.0/2.1
    rh   = 0.1175
    k0   = 10.0
    k1   = 44.6244
    #
    xx = -0.01
    dx = 0.01
    i = 0
    while (i < npoints and xx < xc):
        np = i
        xx += dx
        if (xx >= 0.5): dx = 0.1
        if (xx >= xa): dx = 0.01
        if (xx < xb): #otherwise skip to 200
            #bow equation
            a = 0.3*xx - 1.0
            a3= a*a*a
            a4= a3*a
            b = 1.2*xx + 1.0
            r = cb1*xx*a4 + cb2*xx*xx*a3 + 1.0 - a4*b
            r = rmax*pow(r,cb3)
            x[i] = xx
            y[i] = r
        else: #goto 200
            if (xx < xm): #otherwise skip to 400
                #parallel mid-body equation
                x[i]=xx
                y[i]=rmax
            else: #goto 400
                if (xx < xa): #otherwise goto 600
                    #afterbody equation
                    xi = (13.979167 - xx)/3.333333
                    c1 = rh*rh
                    xipow = xi*xi
                    c2 = rh*k0*xipow                  
                    xipow *= xi #3
                    c3 = (20.0 - 20.0*rh*rh - 4.0*rh*k0 - 0.333333*k1)*xipow
                    xipow *= xi #4
                    c4 = (-45.0 + 45.0*rh*rh + 6.0*rh*k0 + k1)*xipow
                    xipow *= xi #5
                    c5 = (36.0  - 36.0*rh*rh - 4.0*rh*k0 - k1)*xipow
                    xipow *= xi #6
                    c6 = (-10.0 + 10.0*rh*rh +     rh*k0 + 0.333333*k1)*xipow
                    r  = rmax*sqrt((c1+c2+c3+c4+c5+c6))
                    x[i] = xx
                    y[i] = r
                else: #goto 600
                    if (xx < xc): #otherwise goto 1100
                        #afterbody cap equation
                        r = 1.0 - (3.2*xx - 44.733333)*(3.2*xx - 44.733333)
                        assert r >= 0.0, "negative square root in afterbody cap equation"
                        r = rh*rmax*sqrt(r)
                        x[i] = xx
                        y[i] = r
                    else:#1100
                        x[np] = xc
                        y[np] = 0.0
                    #end 1100 block
                #end 600 block
            #end 400 block
        #end 200 block
        i += 1
    #end loop 
    return x,y,np+1
#end darpagen2


if __name__ == '__main__':

    nx = 300
    try_cylinder = False
    try_new_darpa= False
    try_darpa_2d = True
    if try_cylinder:
        nx=11;ntheta=8
        x,y,z,domain,x_ll,L =build_cylinder(nx,ntheta)
	domain.writePLY("cyl")
	domain.writePoly("cyl")
 
        write_csv_file(x,y,z,'cyl')
    elif try_new_darpa:
        ntheta = 8
        x,y,z,theta_offset,np,x_ll,L = darpa2gen(nx,ntheta,pad_x=10.0, pad_r_fact=8.)
        write_csv_file(x[:np],y[:np],z[:np],'darpa2')
        domain = build_domain_from_axisymmetric_points(x[:np,:],y[:np,:],z[:np,:],x_ll,L,include_front_and_back=0,theta_offset_user=theta_offset[:np+1],name='darpa2')
	domain.writePLY('darpa2')
	domain.writePoly('darpa2')
	domain.writeGeo('darpa2')

    elif try_darpa_2d:
        ntheta = 2
        x,y,z,theta_offset,np,x_ll,L = darpa2gen(nx,ntheta,pad_x=10.0, pad_r_fact=8.)
        write_csv_file(x[:np],y[:np],z[:np],'darpa2_2d')
        domain = build_2d_domain_from_axisymmetric_points(x[:np,:],y[:np,:],x_ll,L,name='darpa2_2d')
	domain.writePoly('darpa2_2d')

    else:
        x,y,np = darpa2gen_orig(nx)

        fout = open('darpa2.dat','w')
        for i in range(np):
            fout.write("%12.5e %12.5e \n" % (x[i],y[i]))

        #
        fout.close()
        import matplotlib
        from matplotlib import pylab

        fig = pylab.figure(1)
        pylab.plot(x[:np],y[:np])
        fig.hold('on')
        y *= -1.0
        pylab.plot(x[:np],y[:np])
        pylab.xlabel('x [ft]'); pylab.ylabel('y [ft]')
        pylab.title('DARPA2 body')
        pylab.axes().set_aspect('equal','datalim')
        pylab.savefig('darpa2.png')
        pylab.show()
