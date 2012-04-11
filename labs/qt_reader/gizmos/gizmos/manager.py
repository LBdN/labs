from direct.showbase.DirectObject import DirectObject

class Manager( DirectObject ):

    def __init__( self , gizmos = None):
        DirectObject.__init__( self )
        self.__gizmos      = gizmos if gizmos else {}
        self.__active = None
        #==
        self.accept( 'space', self.toggle_mode )
        self.accept( '+'    , self.set_size , [2] )
        self.accept( '-'    , self.set_size , [0.5] )
        self.accept( 'q'    , self.set_active, [None] )
        self.accept( 'w'    , self.set_active, ['pos'] )
        self.accept( 'e'    , self.set_active, ['rot'] )
        self.accept( 'r'    , self.set_active, ['scl'] )

    def __iter__(self):
        return iter(self.__gizmos.values())

    def __getitem__(self, key):
        return self.__gizmos[key]

    def toggle_mode( self ):
        """Toggle all gizmos local mode on or off."""
        value = self['pos']
        for gizmo in self:
            gizmo.local = not value
        self.__active.Refresh()


    def get_active( self ):
        """Return the active gizmo."""
        return self.__active

    def set_active( self, name ):
        """
        Stops the currently active gizmo then finds the specified gizmo by
        name and starts it.
        """
        print "HERE"
        # Stop the active gizmo
        if self.__active is not None:
            self.__active.Stop()
        # Get the gizmo by name and start it if it is a valid gizmo
        self.__active = self.__gizmos.get(name)
        print self.__active, name
        if self.__active is not None:
            self.__active.Start()

    active = property(fget=get_active, fset=set_active)

    def set_size( self, factor ):
        """Resize the gizmo by a factor."""
        for gizmo in self:
            gizmo.SetSize( factor )

    def AttachNodePaths( self, nodePaths ):
        """Attach a node path to be transformed by the gizmos."""
        for gizmo in self:
            gizmo.AttachNodePaths( nodePaths )
