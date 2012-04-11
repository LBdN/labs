from reader import MetaReader, Reader

def io_readers():
    r = [IOReader()]
    return r

class IOReader(Reader):
    def __init__(self, *args):
        Reader.__init__(self, *args)
        self.io_listener = None

    def match(self, obj):
        return True

    def _read(self, source, ctx):
        if not self.io_listener:
            self.io_listener = IOListener(self.meta)
        #==
        if not source.parents:
            self.meta.root = source
            return source.children, ctx
        #==
        source.locked, ll = False, source.locked
        source.register(self.io_listener)
        source.locked = ll
        if source.rvalue().is_union() :
            rvalue = source.rvalue().children[0]
        else :
            rvalue = source.rvalue()
        #==
        if rvalue.is_container():
            return rvalue.children, ctx
        else:
            return None, None

class IOListener(object):
    def __init__(self, meta):
        self.meta = meta

    def tr_delete(self, transaction):
        self.meta.changed()

    def tr_replace(self, transaction):
        #print "here %s" %transaction
        self.meta.changed()

    def tr_change_type(self, transaction):
        if transaction.target.rvalue().is_container():
            new_val = transaction.target.rvalue().children[0].children
        else:
            new_val = transaction.target.rvalue()
        self.meta.read_all([(new_val, {})])
        self.meta.changed()

    def tr_append(self, transaction):
        new_val = transaction.target.rvalue().children[-1]
        self.meta.read_all([(new_val, {})])
        self.meta.changed()

    def tr_remove(self, transaction):
        pass

class IOMetaReader(MetaReader):
    def __init__(self, readers, filepath):
        MetaReader.__init__(self, readers)
        self.filepath = filepath
        self.root     = None
        self.dirty    = True

    def changed(self):
        self.dirty = True

    def write(self):
        if not self.dirty:
            return
        if not self.root:
            return
        _str = to_json(self.root)
        #print "%s writing" %_str
        print "writing" 
        f = open(self.filepath, "w")
        f.write(_str)
        #==
        self.dirty    = False

def to_json(obj):
    import json
    k, v = _to_json(obj)
    return json.dumps(v, indent=4)

def _to_json(obj):
    if not obj.parents:
        k = 'root'
        v = {}
        for c in obj.children:
            k2, v2 = _to_json(c)
            v[k2] = v2
        return k, v
    #==
    k = obj.as_key()
    if obj.rvalue().is_list():
        v = {}
        v['_type'] = 'multilist' if obj.rvalue().is_multi_list() else 'list'
    elif obj.rvalue().is_union():
        v = {}
        v['_type'] = 'union'
        v['_active_type'] = str(obj.rvalue().children[0].rtype)
        if obj.rvalue().is_container():
            for c in obj.rvalue().children[0].children:
                k2, v2 = _to_json(c)
                v[k2] = v2
        else:
            v['_value'] = obj.get_value()
        return k, v
    elif obj.rvalue().is_container():
        v = {}
        v['_type'] = str(obj.rvalue().rtype)
    else:
        v = obj.get_value()
    #==
    for c in obj.rvalue().children:
        k2, v2 = _to_json(c)
        v[k2] = v2
    #==
    return k, v
