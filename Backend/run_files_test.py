import generate_routes

targetDistance = 200
marginOfErrorDist = 100

xCoord = -123.16
yCoord = 49.26

targetElevation = 500
marginOfErrorEl = 100

searchDist = 500

test = generate_routes.GenerateRoutes(xCoord = xCoord,
    yCoord = yCoord, 
    marginOfErrorDist = marginOfErrorDist,
    targetDistance = targetDistance,
    targetElevation = targetElevation,
    marginOfErrorEl = marginOfErrorEl,
    searchDist = searchDist,
    networkType="all_private",
    closeGraph=False)

# gets random sample of specified amount
result1 = test.getFinalRoutes(5)
result2 = test.getFinalRoutes(10)

print(result1)
