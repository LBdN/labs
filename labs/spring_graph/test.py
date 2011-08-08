def tarjan(root, graph):
    nb_parents = {}
    for el in graph.nodes():
        nb_parents[el] = len(graph.successors(el))
    #=    
    all_roots = [[root]]
    task_list = []
    while all_roots:
        roots = all_roots.pop(0)
        task_list.append(roots)
        new_roots = []
        for root in roots:
            for node in graph.predecessors(root):
                nb_parents[node] = nb_parents[node] - 1
                if nb_parents[node] == 0:
                    new_roots.append(node)
        if new_roots:
            all_roots.append(new_roots)
    return task_list

def positionning(graph):
    for i, n in enumerate(tarjan(graph.nodes[0], graph.G)): 
        for i2, e in enumerate(n) :
            e.x.x = i * 70 + i2
            e.x.y = ((i2-len(n)/2) * 70) +150
            #===
            #parents = graph.G.successors(e)
            #if parents:
                #pos = parents[0].x
                #e.x.y += pos.y
            #e.x.y += 150 
class Grid(object):
    def __init__(self, case_size):
        self.case_size = case_size
        self.taken = set([])

    def case_from_pos(self, x, y):
        x = int(x) / self.case_size[0]
        y = int(y) / self.case_size[1]
        return x, y

    def pos_from_case(self, case):
        x = (case[0] + 0.5) * self.case_size[0]
        y = (case[1] + 0.5) * self.case_size[1]
        return x, y

    def free_case_on_col(self, case):
        i = 0
        ncase = case[0],case[1]
        while ncase in self.taken:
            ncase = case[0], case[1] + i
            if i > 0 : i = -i
            else     : i = -(i-1)
        return ncase

    def mark(self, case):
        self.taken.add(case)





def positionning4(graph):
    partial_order = tarjan(graph.nodes[0], graph.G)
    grid          = Grid((100,70))
    for i, group in enumerate(partial_order[:-1]):
        for node in group:
            good_nodes = set(partial_order[i+1]) & set(graph.G.predecessors(node))
            gg = sorted([(g, len(graph.G.successors(g))) for g in good_nodes])
            good_nodes = [g for g,nb in gg]
            for j, n in enumerate(good_nodes):
                x = (i+1) * 100  
                y = ((j-len(good_nodes)/2) * 70) + node.x.y  
                case = grid.case_from_pos(x,y)
                fcase = grid.free_case_on_col(case)
                grid.mark(fcase)
                x, y = grid.pos_from_case(fcase)
                n.x.x = x
                n.x.y = y
                #n.x.x = (i+1) * 70 
                #n.x.y = ((j-len(good_nodes)/2) * 70) + node.x.y  

def move_down(graph):
    for n in graph.nodes:
        n.x.y +=100

def move_up(graph):
    for n in graph.nodes:
        n.x.y -=100

def positionning2(graph):
    for n in graph.nodes:
        children = graph.G.predecessors(n)
        for i, c in enumerate(children):
            c.x.y = n.x.y + (i-len(children)/2) * 50
            
def positionning3(graph):
    for n in graph.nodes:
        parents = graph.G.successors(n)
        if parents:
            y  = sum((p.x.y for p in parents)) / len(parents)
            n.x.y = y + (i-len(children)/2) * 50
