def traverse(dart, dimensions, func, ffrom):
    cdef int i
    traversed_dart = set([dart])
    stack = [dart]
    while stack:
        current_dart = stack.pop()
        func(current_dart)
        for i in dimensions:
            other_dart = current_dart.alphas[i]
            if not other_dart in traversed_dart:
                traversed_dart.add(other_dart)
                stack.append(other_dart)
    #print len(traversed_dart), dimensions, ffrom
