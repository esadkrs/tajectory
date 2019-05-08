import pandas as pd
import datetime as dt
import csv
import math
import numpy as np
filename= "Trajectory_output_withQWarningN.csv"
output = 'aubonpain2w.csv'

def getDistance(x1,x2,y1,y2):
	dist = math.sqrt( (float(x1)-float(x2))**2+ (float(y1)-float(y2))**2 )
	return dist

def getTTC(leader,follower,length,distance):
	TTC = (distance-length) / (follower-leader)
	return TTC


#dictionary to hold the output
escobar = {}
# Read a CSV file

df = pd.read_csv(filename)
# Unique Bus List
df1 = df.apply(pd.to_numeric, args=('n/a',))

#timestep = df[(df['time'] > 292) & (df['time'] <= 293)]

#timestep = 293.5




uTimeList = df["time"].unique()

varLen = len(uTimeList)

oList = []
oList.append(["time","leader","follower","ttc","lane"])

for k in range(varLen):
	subdf = df[df["time"]== uTimeList[k]]
	subdf =  subdf.sort(["y"],ascending=[False]).reset_index(drop=True)
	#"y" degerleri uzerinden subDf reverse order yapilmasi lazim asc desc
	laneList = subdf["lane"].unique()
	#print laneList
	for lane in laneList:
		subdf = subdf[subdf["lane"]== lane].reset_index(drop=True)

		uCarList = subdf["ID"].unique()

		# Length of the rows in the Unique Bus List
		varLen = len(uCarList)

		if varLen >1 :
		# First for loop for each bus ID
			for i in range(varLen-1):
				l = uCarList[i] # leader depending on y value
				f = uCarList[i+1] # follower
				#print l,f
				rDist = getDistance(subdf["x"][i],subdf["x"][i+1],subdf["y"][i],subdf["y"][i+1])
				ttc = getTTC(subdf["speed.mph"][i]*1.47,subdf["speed.mph"][i+1]*1.47,20,rDist)
				if ttc<= 1.5 and ttc>0:
					#print uTimeList[k],l,f,ttc # timestamp
					tempO = [uTimeList[k],l,f,ttc,lane]
					oList.append(tempO)
				


escobar2 = sorted(escobar.items())




with open(output, "wb") as f:
    writer = csv.writer(f)
    writer.writerows(oList)
print '__________________________'
print 'Completed.'
print '__________________________'




