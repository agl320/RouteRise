import osmnx as ox 
import geopandas as gpd 
import matplotlib.pyplot as plt
from IPython.display import display
from collections import deque

# marginOfErrorDist, targetDistance, xCoord, yCoord, targetElevation, marginOfErrorEl
"""
@api_params

perhaps make targetElevation optional ( can be null )
"""
marginOfErrorDist = 100
targetDistance = 200
xCoord = -122.8927259
yCoord = 49.2317256
targetElevation = 500
marginOfErrorEl = 100


"""
extra_params
"""
debug = False
debugShowNames = False
debugShowIDs = True


def calcDistance(routeArr):
    lengthTotal = 0
    for i in range(len(routeArr)-1):
        lengthTotal = lengthTotal + edges["length"][routeArr[i],routeArr[i+1],0]
        
    return lengthTotal
    
# def createHighlight(startNodeID, endNodeID):
#     plt.plot(getCoordinates(startNodeID)["x"],getCoordinates(startNodeID)["y"], marker="o")
#     plt.plot(getCoordinates(endNodeID)["x"],getCoordinates(endNodeID)["y"],"g", marker="o")
    
# def createPoint(NodeID):
#     plt.plot(getCoordinates(NodeID)["x"],getCoordinates(NodeID)["y"], "o", marker="o")
        
# {nodeX: {nodeA: {}, nodeB: {}, nodeC: {}}, nodeY: {}}

def getNeighboursIDS(nextNodeID):
   return edges["osmid"][nextNodeID, :, 0].keys().values
    
# def bfs_with_path(start, target):
#   queue = deque([(start, [start])])
#   visited = set()

#   while queue:
#     current, path = queue.popleft()
#     if current == target:
#         return path 
    
#     if current not in visited:
#         visited.add(current)

#         for neighbor in getNeighboursIDS(current):
#           if neighbor not in visited:
#               queue.append((neighbor, path + [neighbor]))

#   return None

def find_all_paths(start):
    all_paths = []
    queue = deque([(start, [start])])
    visited = set()

    while queue:
        current, path = queue.popleft()
        all_paths.append(path)
        if current not in visited:
            visited.add(current)
            try: 
                for neighbor in getNeighboursIDS(current):
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor]))
            except:
                continue

    # now all we have to do is go through all_paths and find the first 5 paths that satisfy the condition on the desired
    # maybe we can do +/-0.5km, rarely do I think we will find 5 paths that are exactly the desired
    return all_paths

  
# area = ox.geocode_to_gdf()
# graph = ox.graph_from_address("9087 Briar road, Burnaby, BC, Canada", dist=1000)
graph = ox.graph_from_point((yCoord, xCoord), dist=1000, dist_type='bbox')

# fig, ax = ox.plot_graph(graph, node_size=1, show=False, close=True)

# Retrieve nodes and edges
nodes, edges = ox.graph_to_gdfs(graph)
nodes.head()

# STARTS HERE

# Get nearest edge, then get the nearest node on the edge via euclidian distance
startNodeID = ox.nearest_nodes(graph, xCoord, yCoord, return_dist=False)
routeArr = []
# dist1 = ox.distance.euclidean(xCoord, yCoord, nodes.loc[11246885219]["y"], nodes.loc[11246885219]["x"])
# dist2 = ox.distance.euclidean(xCoord, yCoord, nodes.loc[11246885219]["y"], nodes.loc[11246885219]["x"])
# if dist1 >= dist2:
#    # pick node1
# else:
#    # pick node2

# startNodeID = 415845427

for route in find_all_paths(startNodeID):
    routeDist = calcDistance(route)
    if targetDistance - marginOfErrorDist < calcDistance(route) < targetDistance + marginOfErrorDist:
        routeArr.append(route)

# startNodeIDArr = [startNodeID]

# for j in range(len(startNodeIDArr)):
#   for i, neighbourNodeID in enumerate(edges["osmid"][startNodeIDArr[j], :, 0].keys().values):
#       routeArr.append(ox.routing.shortest_path(graph, startNodeIDArr[j], neighbourNodeID))

if(len(routeArr) <= 0):
    fig, ax = ox.plot_graph(graph, node_size=0.5, show=False, close=False, edge_linewidth=0.5)
else:
    if(len(routeArr) == 1):
        fig, ax = ox.plot.plot_graph_route(graph, routeArr[0], show=False, close=False, node_size=0.5, edge_linewidth=0.5, route_linewidth=1, route_color="y", route_alpha=0.3, orig_dest_size=5)
    else:
        fig, ax = ox.plot.plot_graph_routes(graph, routeArr, show=False, close=False, node_size=0.5, edge_linewidth=0.5, route_linewidths=1, route_colors="y", route_alpha=0.3, orig_dest_size=5) 
  
    # for i,node in enumerate(nodes):
    #   # c = edges.iloc[i]["geometry"].centroid
    #   # text=edges.iloc[i]["osmid"]
    #   # ax.annotate(text, (c.x, c.y), c='w')
    #   plt.plot(nodes.iloc[i]['geometry'].centroid.x, nodes.iloc[i]['geometry'].centroid.y, "o", marker="o")
    #   # print(nodes.iloc[i]['osmid'])
    #   # print(nodes.iloc[i]['geometry'].centroid)

    
    # for nodeID in routeArr:
    #   # text=str(node)
    #   # ax.annotate(text, (getCoordinates(node)["x"],getCoordinates(node)["y"]), c='w')
    #   # plt.plot(nodes.loc[nodeID]["x"],nodes.loc[nodeID]["y"], marker="o")
    #   # plt.text(, str(node))
    #   display(nodes.loc[nodeID]["x"])
      
    # plt.plot(nodes.loc[1014695502]["x"],nodes.loc[1014695502]["y"], marker="o", c="y")
    # plt.plot(xCoord,yCoord, marker="o", c="b")
    
    # Display address names on map
    if debug == True:
        for _, edge in ox.graph_to_gdfs(graph, nodes=False).fillna('').iterrows():            
            c = edge['geometry'].centroid
            if debugShowNames == True:
                text = str(edge['name'])
                ax.annotate(text, (c.x, c.y), c='w', fontsize=5)
            elif debugShowIDs == True:
                text = str(edge['osmid'])
                ax.annotate(text, (c.x, c.y), c='w', fontsize=5)
            # elif debugShowCoords == True:
            #     text = str(nodes.loc[11246885219]["y"], nodes.loc[11246885219]["x"])
            #     ax.annotate(text, (c.x, c.y), c='w', fontsize=5)

display(routeArr)

# draw start node
plt.plot(xCoord,yCoord, marker="o", c="c", markersize=3)

finalRoutes = []
for i, route in enumerate(routeArr):
    coordArr = []
    for j in route:
        coordArr.append([nodes.loc[j]["x"], nodes.loc[j]["y"]])

    finalRoutes.append([coordArr,calcDistance(route)])
    
display(finalRoutes)
display(len(finalRoutes))

"""
Output format

finalRoutes = [ [ [[X1, Y1], [X2, Y2]] , distance ] ]
numRoutes = len(finalRoutes)

"""


# calcDistance(routeArr[0])

# must find edges that have a u-val of starting node
# for a given node
    # for each possible path
    # draw path

# display(edges["osmid"][7483134363, :, 0])


plt.show()