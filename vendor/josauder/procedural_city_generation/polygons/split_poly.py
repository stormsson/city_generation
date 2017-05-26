from procedural_city_generation.polygons.Polygon2D import *
from procedural_city_generation.additional_stuff.Singleton import Singleton
singleton=Singleton("polygons")

def split_poly(poly, eps=10**-5):
        """Split polygon into two parts"""

        if poly.area < singleton.split_poly_min_area:
            #Polygon2D is too small
            return False

        for split_edge in sorted(poly.edges, key=lambda x: -x.length):
            if split_edge.length < singleton.split_poly_min_length:
                #Edge is too small for splitting
                return False

            new_edges = [[], []]

            #Find points where line starting from split point intersects other edges,
            #allocate new edges to two different lists using switch variable
            #if more than one intersection is found or resulting polygons are not
            #connected to street, try again with different edge

            #Find point at approximate half of split edge
            split_point = split_edge[0] + split_edge.dir_vector*np.random.uniform(0.5-singleton.split_poly_half_tolerance, 0.5+singleton.split_poly_half_tolerance)

            #Switch variable determines which list in new edges is appended to
            switch = True

            total_cuts = 0

            for other in poly.edges:
                if other is split_edge:
                    #Append two parts of split edge
                    new_edges[switch].append(Edge(split_edge[0], split_point, split_edge.bordering_road))
                    switch = not switch
                    new_edges[switch].append(Edge(split_point, split_edge[1], split_edge.bordering_road))
                else:
                    this_cuts = False
                    try:
                        x = np.linalg.solve(np.array([split_edge.n, -other.dir_vector]).T, other[0] - split_point)
                        if eps < x[0] and 0 + eps < x[1] < 1 - eps:
                            this_cuts = True
                            total_cuts += 1
                            new_point = split_point + x[0]*split_edge.n
                    except np.linalg.LinAlgError:
                        pass

                    if total_cuts  <= 1:
                        if not this_cuts:
                            #No intersection found, append other edge as it is
                            new_edges[switch].append(other)
                        else:
                            #Intersection found, append resulting edges
                            new_edges[switch].append(Edge(other[0], new_point, bordering_road=other.bordering_road))
                            new_edges[switch].append(Edge(new_point, split_point, bordering_road=False))
                            switch = not switch
                            new_edges[switch].append(Edge(split_point, new_point, bordering_road=False))
                            new_edges[switch].append(Edge(new_point, other[1], bordering_road=other.bordering_road))
                    else:
                        #More than one intersection found
                        break
            else:
                #Only one intersection found
                for edge_set in new_edges:
                    #Check if resulting polygon would be connected to road
                    if all(not edge.bordering_road for edge in edge_set):
                        break
                else:
                    return Polygon2D(new_edges[0], poly_type="lot"), Polygon2D(new_edges[1], poly_type="lot")
        else:
            #Not possible to split polygon
            return False

if __name__ == "__main__":

    import matplotlib.pyplot as plt
    p = [np.array(x) for x in [[0, 0], [0, 1], [1, 0.8], [1, 0]]]
    p = Polygon2D(p)
    split_poly(p)
    p.selfplot()
    plt.show()
