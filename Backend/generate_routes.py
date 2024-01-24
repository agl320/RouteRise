import osmnx as ox 
import geopandas as gpd 
import matplotlib.pyplot as plt
from IPython.display import display
from collections import deque
import random

# marginOfErrorDist, targetDistance, xCoord, yCoord, targetElevation, marginOfErrorEl

class GenerateRoutes():

    """
    Object that generates and stores routes.

    Parameters:

    xCoord (numeric): starting x coordinate 
    yCoord (numeric): starting y coordinate
    targetDistance (numeric): desired run distance in metres
    marginOfErrorDist (numeric): margin of error for distance (+-)
    targetElevation (numeric): target elevation net difference of run
    marginOfErrorEl (numeric): margin of error for elevation (+-)
    searchDist (numeric): mapping distance for routes (should at least be >= targetDistance)
    networkType (string): defines types of routes mapped ("all_private", "all", "bike", "drive", "drive_service", "walk")
    closeGraph (boolean): for displaying matplotlib graph for debugging

    """
    def __init__(self, xCoord, yCoord, targetDistance, marginOfErrorDist, targetElevation = 500, marginOfErrorEl = 100, searchDist = 1000, networkType = "all_private", closeGraph = False):

        self.xCoord = xCoord 
        self.yCoord = yCoord

        self.targetDistance = targetDistance 
        self.marginOfErrorDist = marginOfErrorDist
     
        self.targetElevation = targetElevation 
        self.marginOfErrorEl = marginOfErrorEl

        """
        internal_debug_params
        """
        debug = False
        debugShowNames = False
        debugShowIDs = True

          
        # area = ox.geocode_to_gdf()
        self.graph = ox.graph_from_point((self.yCoord, self.xCoord), dist=searchDist, dist_type='bbox', network_type=networkType)

        # fig, ax = ox.plot_graph(graph, node_size=1, show=False, close=True)

        # Retrieve nodes and edges
        self.nodes, self.edges = ox.graph_to_gdfs(self.graph)
        self.nodes.head()

        # STARTS HERE

        startNodeID = ox.nearest_nodes(self.graph, self.xCoord, self.yCoord, return_dist=False)
        routeArr = []
        # dist1 = ox.distance.euclidean(xCoord, yCoord, nodes.loc[11246885219]["y"], nodes.loc[11246885219]["x"])
        # dist2 = ox.distance.euclidean(xCoord, yCoord, nodes.loc[11246885219]["y"], nodes.loc[11246885219]["x"])
        # if dist1 >= dist2:
        #    # pick node1
        # else:
        #    # pick node2

        # startNodeID = 415845427

        for route in self.find_all_paths(startNodeID):
            if targetDistance - marginOfErrorDist < self.calcDistance(route) < targetDistance + marginOfErrorDist:
                routeArr.append(route)

        # startNodeIDArr = [startNodeID]

        # for j in range(len(startNodeIDArr)):
        #   for i, neighbourNodeID in enumerate(edges["osmid"][startNodeIDArr[j], :, 0].keys().values):
        #       routeArr.append(ox.routing.shortest_path(graph, startNodeIDArr[j], neighbourNodeID))

        # PLOT HIDE
        # if(len(routeArr) <= 0):
        #     fig, ax = ox.plot_graph(self.graph, node_size=0.5, show=False, close=False, edge_linewidth=0.5)
        # else:
        #     if(len(routeArr) == 1):
        #         fig, ax = ox.plot.plot_graph_route(self.graph, routeArr[0], show=False, close=closeGraph, node_size=0.5, edge_linewidth=0.5, route_linewidth=1, route_color="y", route_alpha=0.3, orig_dest_size=5)
        #     else:
        #         fig, ax = ox.plot.plot_graph_routes(self.graph, routeArr, show=False, close=closeGraph, node_size=0.5, edge_linewidth=0.5, route_linewidths=1, route_colors="y", route_alpha=0.3, orig_dest_size=5) 
        
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
            
            # PLOT HIDE
            # Display address names on map
            # if debug == True:
            #     for _, edge in ox.graph_to_gdfs(self.graph, nodes=False).fillna('').iterrows():            
            #         c = edge['geometry'].centroid
            #         if debugShowNames == True:
            #             text = str(edge['name'])
            #             ax.annotate(text, (c.x, c.y), c='w', fontsize=5)
            #         elif debugShowIDs == True:
            #             text = str(edge['osmid'])
            #             ax.annotate(text, (c.x, c.y), c='w', fontsize=5)
                    # elif debugShowCoords == True:
                    #     text = str(nodes.loc[11246885219]["y"], nodes.loc[11246885219]["x"])
                    #     ax.annotate(text, (c.x, c.y), c='w', fontsize=5)

        # display(routeArr)

        # PLOT HIDE
        # draw start node
        # plt.plot(self.xCoord,self.yCoord, marker="o", c="c", markersize=3)
        # plt.plot(self.nodes.loc[startNodeID]["x"],self.nodes.loc[startNodeID]["y"], marker="o", c="c")

        self.finalRoutes = []
        for i, route in enumerate(routeArr):
            coordArr = []
            for j in route:
                coordArr.append([self.nodes.loc[j]["x"], self.nodes.loc[j]["y"]])

            self.finalRoutes.append([coordArr,self.calcDistance(route)])
            
        # display(self.finalRoutes)
        # display(len(self.finalRoutes))

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

        if not closeGraph:
            plt.show()
        
    
    def getFinalRoutes(self):
        return {"routes": self.finalRoutes, "numberOfRoutes": len(self.finalRoutes)}

    def getFinalRoutes(self, numberOfRoutes):
        if numberOfRoutes >= len(self.finalRoutes):
            self.getFinalRoutes()
        else:
            return {"routes": random.sample(self.finalRoutes, numberOfRoutes), "numberOfRoutes": numberOfRoutes}

    def calcDistance(self, routeArr):
        lengthTotal = 0
        for i in range(len(routeArr)-1):
            lengthTotal = lengthTotal + self.edges["length"][routeArr[i],routeArr[i+1],0]
            
        return lengthTotal
    
    def calcCalories(self, avgRunSpeed=8):
        """
        avgRunSpeed 
            float (km/hr)
        """

        pass

    
    def calcCarbonEm(self):
        """
        To have the best chance of avoiding a 2℃ rise in 
        global temperatures, the average global carbon footprint 
        per year needs to drop to under 2 tons by 2050.
        """
        pass


        
    # def createHighlight(startNodeID, endNodeID):
    #     plt.plot(getCoordinates(startNodeID)["x"],getCoordinates(startNodeID)["y"], marker="o")
    #     plt.plot(getCoordinates(endNodeID)["x"],getCoordinates(endNodeID)["y"],"g", marker="o")
        
    # def createPoint(NodeID):
    #     plt.plot(getCoordinates(NodeID)["x"],getCoordinates(NodeID)["y"], "o", marker="o")
            
    # {nodeX: {nodeA: {}, nodeB: {}, nodeC: {}}, nodeY: {}}

    def getNeighboursIDS(self, nextNodeID):
        return self.edges["osmid"][nextNodeID, :, 0].keys().values
        
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

    def find_all_paths(self, start):
        all_paths = []
        queue = deque([(start, [start])])
        visited = set()

        while queue:
            current, path = queue.popleft()
            all_paths.append(path)
            if current not in visited:
                visited.add(current)
                try: 
                    for neighbor in self.getNeighboursIDS(current):
                        if neighbor not in visited:
                            queue.append((neighbor, path + [neighbor]))
                except:
                    continue

        # now all we have to do is go through all_paths and find the first 5 paths that satisfy the condition on the desired
        # maybe we can do +/-0.5km, rarely do I think we will find 5 paths that are exactly the desired
        return all_paths

  