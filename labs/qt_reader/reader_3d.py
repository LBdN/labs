import p_base
from reader import Reader, MetaReader
from pandac.PandaModules import Vec4

class Mesh(Reader):
    _type = p_base.Node


    def _read(self, node, ctx):
        mesh_node = node['mesh']
        am   = MeshView(self.meta.panda, mesh_node)
        node.locked, ll = False, node.locked
        node.register(am)
        node.locked = ll
        Wrapper(mesh_node['path'], am.notify_path)
        for idx, c in enumerate(mesh_node['position'].children[0].children):
            Wrapper(c, am.notify_pos, {'idx':idx})
        for idx, c in enumerate(mesh_node['rotation'].children[0].children):
            Wrapper(c, am.notify_rot, {'idx':idx})
        for idx, c in enumerate(mesh_node['scale'].children[0].children):
            Wrapper(c, am.notify_scale, {'idx':idx})
        #==
        #return node, ctx
        return None, None

class Selection(Reader):
    def match(self, obj):
        if not obj.is_name():
            return False
        return obj.rvalue().is_list() and isinstance(obj.parents[0].get_value(), p_base.Selection)

    def _read(self, node, ctx):
        selectionCol = SelectionColorizer(node)
        node.locked, ll = False, node.locked
        node.register(selectionCol)
        node.locked = ll
        self.meta.panda.nodePicker.selectionCol = selectionCol
        return node, ctx

class SelectionColorizer(object):
    def __init__(self, source):
        self.source = source
        self.pos  = []
        self.npos = []

    def replace_nodes(self, nodes):
        print "nodes %s, %s" %(nodes, map(type, nodes))
        nn   = [] 
        for n in nodes:
            po= n.getPythonTag("mesh_view")
            assert_(po)
            self.npos.append(po)
            nn.append(po.source.get_value())
        #==
        l = self.source.listeners
        for listener in l:
            self.source.listeners = [listener]
            self.source.replace(nn, self)
            for p in nodes:
                assert_(p.getPythonTag( "mesh_view" ))
        #==
        self.source.listeners = l
        self.source.replace(nn, self)
        for p in nodes:
            assert_(p.getPythonTag( "mesh_view" ))
        #==
        self.pos = self.npos
        self.npos = []
        #==
        for p in nodes:
            assert_(p.getPythonTag( "mesh_view" ))

    def clear_nodes(self):
        self.source.replace([], self)
        self.pos = []

    def tr_append(self, tr):
        new_wrapped_item = tr.target.rvalue().children[-1]
        for po in self.pos:
            if po.source is new_wrapped_item:
                if po.mesh:
                    self.colorize(po.mesh)

    def tr_replace(self, tr):
        for po in self.pos:
            self.uncolorize(po.mesh)
        #==
        for i in self.npos:
            self.colorize(i.mesh)
        #==
        for p in self.pos:
            assert_(p.mesh.getPythonTag( "mesh_view" ))
        for p in self.npos:
            assert_(p.mesh.getPythonTag( "mesh_view" ))

    def tr_remove(self, tr):
        return

    def colorize(self, t):
        t.setColorScale( Vec4(1, 0, 0, 1))

    def uncolorize(self, t):
        t.setColorScale( Vec4(1))

class MatchAll(Reader):
    def __init__(self):
        self.mesh_listener = None

    def match(self, source):
        return True

    def _read(self, source, ctx):
        if not self.mesh_listener:
            self.mesh_listener = MeshListener(self.meta)
        if not source.parents:
            return source.children, ctx
        #==
        source.locked, ll = False, source.locked
        source.register(self.mesh_listener)
        source.locked = ll
        #==
        if source.rvalue().is_union() :
            rvalue = source.rvalue().children[0]
        else :
            rvalue = source.rvalue()
        #==
        if rvalue.is_container():
            return rvalue.children, ctx
        else:
            return None, None

class MeshListener(object):
    def __init__(self, meta):
        self.meta = meta

    def tr_change_type(self, transaction):
        print "TR_CHANGETYPE" * 20
        if isinstance(transaction.new, p_base.Node):
            new_wrapped_val = transaction.target.rvalue().children[0]
            self.meta.read_all([(new_wrapped_val, {})])

    def tr_append(self, transaction):
        print "TR_APPEND" * 20
        if isinstance(transaction.new, p_base.Node):
            new_wrapped_val = transaction.target.rvalue().children[-1]
            self.meta.read_all([(new_wrapped_val, {})], seen=set([]))

    def tr_replace(self, transaction):
        print "TR_REPLACE" * 20
        #if isinstance(transaction.new, p_base.Selection):
            #new_wrapped_val = transaction.target.rvalue().children
            #self.meta.read_all([(new_wrapped_val, {})])
        pass

    def tr_remove(self, transaction):
        print "TR_REMOVE" * 20
        pass

    def tr_delete(self, transaction):
        print "TR_DELETE" * 20
        pass

class MeshView(object):
    def __init__(self, loader, source):
        self.loader = loader
        self.source = source
        self.mesh   = None
        print "MeshView %s" %self.source

    def translate(self, vector):
        print "translate"
        if not self.mesh:
            pass
        new_pos = self.mesh.getPos() + vector
        self.source['position'][0].replace(new_pos[0], self)
        self.source['position'][1].replace(new_pos[1], self)
        self.source['position'][2].replace(new_pos[2], self)

    #==
    def __del__(self):
        assert_ ( False )

    def scale(self, vector):
        if not self.mesh:
            pass
        new_pos = self.mesh.getScale()
        ##==
        new_pos[0] = vector[0] * new_pos[0]
        new_pos[1] = vector[1] * new_pos[1]
        new_pos[2] = vector[2] * new_pos[2]
        #new_pos = vector
        #==
        self.source['scale'][0].replace(new_pos[0], self)
        self.source['scale'][1].replace(new_pos[1], self)
        self.source['scale'][2].replace(new_pos[2], self)


    def tr_delete(self, transaction):
        print "DELETE" * 50
        self.mesh.clearPythonTag( 'mesh_view' )
        self.mesh.removeNode()

    def tr_replace(self, transaction):
        print "REPLACE" * 50
        pass

    #==

    def notify_path(self, transaction, d=None):
        if self.mesh:
            scale = self.mesh.getScale()
            pos   = self.mesh.getPos()
            self.mesh.clearPythonTag( 'mesh_view' )
            self.mesh.removeNode()
        #==
        new_mesh = self.loader.load(transaction.new)
        if self.mesh:
            new_mesh.setScale(scale)
            new_mesh.setPos(pos)
        #==
        self.mesh = new_mesh
        self.mesh.setPythonTag( 'mesh_view', self )
        #==
        assert self.mesh.getPythonTag('mesh_view')

    def notify_scale(self, transaction, d=None):
        if not self.mesh:
            pass
        scale = self.mesh.getScale()
        scale[d['idx']] = transaction.new
        self.mesh.setScale(scale)

    def notify_pos(self, transaction, d=None):
        if not self.mesh:
            pass
        pos = self.mesh.getPos()
        pos[d['idx']] = transaction.new
        self.mesh.setPos(pos)

    def notify_rot(self, transaction, d=None):
        if not self.mesh:
            pass
        pos = self.mesh.getHpr()
        pos[d['idx']] = transaction.new
        self.mesh.setHpr(pos)

class Wrapper(object):
    def __init__(self, node, func, _dict=None):
        node.locked, ll = False, node.locked
        node.register(self)
        node.locked = ll
        self.func  = func
        self._dict = _dict

    def tr_replace(self, transaction):
        self.func(transaction, d=self._dict)

def get_3d_readers():
    r = [Mesh(), Selection(), MatchAll()]
    return r

class ThreeDMetaReader(MetaReader):
    def __init__(self, readers, panda):
        MetaReader.__init__(self, readers)
        self.panda = panda
