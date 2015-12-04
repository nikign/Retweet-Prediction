import snap

g = snap.LoadEdgeList(snap.PNGraph, "edge_list.csv", 0, 1)
print g.GetEdges()