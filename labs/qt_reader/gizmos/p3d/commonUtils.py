from pandac.PandaModules import Mat4
            
            
def GetTrsMatrices( xform ):
    
    """
    Return translation, rotation and scale matrices back for the specified
    transform.
    """
    
    # Get translation and rotation matrices
    rotMat = Mat4()
    xform.getQuat().extractToMatrix( rotMat )
    transMat = Mat4().translateMat( xform.getPos() )
    
    # More care must be taken to get the scale matrix as simply calling
    # Mat4().scaleMat( xform.getScale() ) won't account for shearing or other
    # weird scaling. To get this matrix simply remove the translation and
    # rotation components from the xform.
    invRotMat = Mat4()
    invRotMat.invertFrom( rotMat )
    invTransMat = Mat4()
    invTransMat.invertFrom( transMat )
    scaleMat = xform.getMat() * invTransMat * invRotMat
    
    return transMat, rotMat, scaleMat