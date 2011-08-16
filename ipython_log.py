# IPython log file

get_ipython().show_usage()
get_ipython().magic(u"logstart")
import labs.vector.test_gamr7_lib as tv
get_ipython().magic(u"edit labs.vector.test_gamr7_lib ")
get_ipython().magic(u"edit ./labs/vector/test_gamr7_lib.py")
import labs.vector.test_gamr7_lib as tv
get_ipython().magic(u"edit ./labs/vector/test_gamr7_lib.py")
import labs.vector.test_gamr7_lib as tv
import labs.layers_array.test as t
map(t.from_vertex, tv.iter_generate_poly_grid(10,10,10))
reduce( t.add_layers, map(t.from_vertex, tv.iter_generate_poly_grid(10,10,10)))
bbig = reduce( t.add_layers, map(t.from_vertex, tv.iter_generate_poly_grid(10,10,10)))
get_ipython().magic(u"pylab")
plot(*tv.separate_coord(bbig.vtx))
get_ipython().magic(u"edit t")
plot(*tv.separate_coord(bbig.as_vtx()))
bbig.idx
import numpy
numpy.array(bbig.idx)
nidx = numpy.array(bbig.idx)
nvtx = numpy.array(bbig.vtx)
nvtx[nidx]
bbig.pol
bbig.p
numpy.array(bbig.p)
npol = numpy.array(bbig.p)
bbig.l
numpy.array(bbig.l)
nl = numpy.array(bbig.l)
npol[1]
nidx[npol[1]]
nidx[npol[1:]]
nidx[npol[1][0]:npol[1][1]]
nvtx[nidx[npol[1][0]:npol[1][1]]]
type(nvtx[nidx[npol[1][0]:npol[1][1]]])
plot(nvtx[nidx[npol[1][0]:npol[1][1]]])
nvtx1 = nvtx[nidx[npol[1][0]:npol[1][1]]])
nvtx1 = nvtx[nidx[npol[1][0]:npol[1][1]]]
nvtx1[:,1]
plot(nvtx1[:,0], nvtx1[:,1])
get_ipython().system(u"ls -F --color ")
get_ipython().system(u"cat ipython_log.py")
