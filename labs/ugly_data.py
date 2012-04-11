
#data = GraphData()#test data
##dummy node
#data.nodePath = render.attachNewNode("Graph")

##lines definition (strip is defined by two lines)
#for x, y in [(0,0), (2,0), (6,0), (8,0), (3,-2), (5,-2)]:
    #data.lines.append(GraphCoordinate2D(x,y))

#def strip_append(p1, p2, data):
    ##strip definition
    #st = StripData()
    #st.p1 = p1
    #st.p2 = p2
    #a = data.lines[st.p2].x - data.lines[st.p1].x
    #b = data.lines[st.p2].y - data.lines[st.p1].y
    #l = sqrt(a*a + b*b)
    #st.data.append(GraphCoordinate2D(0.0*l,1))
    #st.data.append(GraphCoordinate2D(0.3*l,0.5))
    #st.data.append(GraphCoordinate2D(0.7*l,0.3))
    #st.data.append(GraphCoordinate2D(1.0*l,0.7))
    #data.strips.append(st)

#strip_append(0,1)
#strip_append(1,2)
#strip_append(2,3)
#strip_append(1,4)
#strip_append(4,5)
#strip_append(5,2)


#colors = [VBase4(0,1,0,1),VBase4(0,0,1,1),VBase4(1,1,0,1),VBase4(1,0,1,1),VBase4(0,1,1,1),VBase4(1,1,1,1)]
#for i in range(len(data.strips)):
    #data.graphs.append(SubGraph(data, i, data.nodePath, scale = data.scale, colGraph = colors[i], colAxes = colors[col]*-1.6))
