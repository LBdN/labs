from direct.showbase.DirectObject import DirectObject


class Object( DirectObject ):
    
    def __init__( self, name, camera=None, rootNp=None ):
        DirectObject.__init__( self )
        
        self.name = name
        self.camera = camera
        self.rootNp = rootNp
        
        self.__task = None
        
        # Default camera to base camera if None is specified
        if self.camera is None:
            self.camera = base.camera
            
        # Default root node to render if None is specified
        if self.rootNp is None:
            self.rootNp = render
        
    def UpdateTask( self, task ):
        pass
        
    def Start( self ):
        
        """Start the object's task if it hasn't been already."""
        
        if self.__task not in taskMgr.getAllTasks():
            self.__task = taskMgr.add( self.UpdateTask, '%sUpdateTask' % self.name )
            
    def Stop( self ):

        """Remove the object's task from the task manager."""
        
        if self.__task in taskMgr.getAllTasks():
            taskMgr.remove( self.__task )
            self.__task = None
            
    def IsRunning( self ):
        
        """
        Return True if the object's task can be found in the task manager,
        False otherwise.
        """
        
        return self.__task in taskMgr.getAllTasks()
        
