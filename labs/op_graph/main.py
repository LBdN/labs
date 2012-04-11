from labs.data_structure.tree import Node

def Slot(name, type):
    si = SlotInfo(name, type)
    n  = Node(data = si)
    return n

class SlotInfo(object):
    def __init__(self, type, name):
        self.type = type
        self.name = name
        self.content = content

def Operation(uuid, callable, params):
    oi = OperationInfo(uuid, callable, params)
    n  = Node(data = oi)
    return n

class OperationInfo(object):
    def __init__(self, uuid, callable, params):
        self.uuid = uuid
        self.callable = callable
        self.params = params


class OpFunc(object):
    def __init__(self, callable, params, ins, outs, prepass=None):
        self.callable = callable
        self.params   = params
        self.ins      = ins
        self.outs     = outs
        self.prepass  = None

    def __call__(state):
        target_list = [state[k] for k in op.in_ptrs]
        if self.prepass:
            target_list = self.prepass(target_list)
        #==
        result = self.callable(target_list)
        #==
        for k in op.out_ptrs:
            state[k].append(result[k])
        return state

def node_to_OpFunc(node, context):
    static_params = node.data.params.resolve_context(context)
    if not node.parents:
        in_ptrs = ['base']
    else:
        in_ptrs = []
        for in_slot in node.parents:
            key = node.data.uuid+':'+in_slot.data.name
            in_ptrs.append(key)
    #==
    if not node.children:
        out_ptrs = ['out']
    else:
        out_ptrs = []
        for out_slot in node.children:
            for in_slot in out_slot.children:
                node = in_slot.children[0]
                k = node.data.uuid+':'+in_slot.data.name
                out_ptrs.append(k)
    #==
    return OpFunc(node.data.callable, static_params, in_ptrs, out_ptrs)


def exec_OpFunc(state, opfuncs):
    for op in opfuncs:
        state = op(state)
        #==
    return state


#class Params(object):
    #def resolve_context(self, context):



