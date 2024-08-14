import matplotlib.pyplot as plt
import numpy as np

#pre game odds
preGameOdds = [['Aaron Nesmith', 14.5], ['Alperen Sengun', 23.5], ['Andrew Nembhard', 10.5], ['Dillon Brooks', 13.5], ['Jabari Smith Jr.', 11.5], ['Jalen Green', 20.5], ['Myles Turner', 14.5], ['Pascal Siakam', 21.5], ['Tyrese Haliburton', 14.5]]
HTOdds = [['Aaron Nesmith', 16.5], ['Alperen Sengun', 16.5], ['Andrew Nembhard', 18.5], ['Dillon Brooks', 14.5], ['Jabari Smith Jr.', 8.5], ['Jalen Green', 26.5], ['Myles Turner', 14.5], ['Pascal Siakam', 20.5], ['Tyrese Haliburton', 19.5]]
gameDiff = [['Aaron Nesmith', 12], ['Alperen Sengun', -4], ['Andrew Nembhard', -2], ['Dillon Brooks', 1], ['Jabari Smith Jr.', 17], ['Jalen Green', 3], ['Myles Turner', -7], ['Pascal Siakam', 0], ['Tyrese Haliburton', 15]]
endPoints = [['Aaron Nesmith', 13], ['Alperen Sengun', 17], ['Andrew Nembhard', 17], ['Dillon Brooks', 16], ['Jabari Smith Jr.', 6], ['Jalen Green', 29], ['Myles Turner', 12], ['Pascal Siakam', 19], ['Tyrese Haliburton', 15]]
y = [endPoints[i][1] for i in range(len(endPoints) - 5)]
data = []
for i in range (len(preGameOdds)-5):
    data.append([preGameOdds[i][1], HTOdds[i][1], (abs(gameDiff[i][1])), 1])
pred = [0 for i in range(len(data[0]))]    
def der(xArr, yArr, predVar):
    
    cost = [0 for j in range(len(predVar))]
    for j in range(len(cost)):
        for i in range(len(xArr)):
            cost[j]+= (np.dot(predVar,xArr[i]) - yArr[i])*xArr[i][j]
        cost[j]/=(len(xArr))
    return cost




def findBestFit(predVar, xArr, yArr, r):
    x1 = 10
    x2 = 100
    z1 = 10
    z2 = 100
    temp = [0 for i in range(len(predVar))]
    while (x1 - x2 > r or x2 - x1 > r or z1 - z2 > r or z2 - z1 > r):
        for i in range(len(predVar)):
            temp[i] = predVar[i]-r*der(xArr, yArr, predVar)[i]
            
        x1 = predVar[2]
        z1 = predVar[1]
        predVar = temp.copy()
        x2 = predVar[2]
        z2 = predVar[1]

    
        
  
    
    return predVar



params = findBestFit(pred, data, y,0.001)
print(params)
print(data)
print(y)
#y2s = [(params[0]*x + params[1]) for x in xs]
'''
plt.plot(xs, ys, 'ro')
plt.plot(xs, y2s)
plt.title('Plot of points')
plt.show()
'''