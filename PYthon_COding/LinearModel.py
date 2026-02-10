#step1: Importing Libraries
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression

#step2: Data

house_size= [500,700,800,1000,1200,1500,1800,2000,2200,2500,3000]
rent= [8000,10000,12000,15000,18000,20000,23000,25000,27000,30000,35000]

#step3: convert the data into numpy arrays to reshape them

x= np.array(house_size).reshape(-1,1)
y= np.array(rent)

#step4: create a model and then train it

model= LinearRegression()
model.fit(x,y)

#step5: make predictions
new_house_size=1200
predicted_rent= model.predict([[new_house_size]])
print(f"House Size: {new_house_size} sq ft - Predicted Rent: {predicted_rent[0]:.0f}") #here predicted_rent is an array which gives the first number of elements

#step6: visualize the results Preparation
plt.figure(figsize=(10,6)) #Here the figsize is in pixels of 10,6
plt.scatter(house_size, rent, color='blue', s=100, label='Actual Data') #Here the scatter plot is used to plot the actual data points on the graph Preparation and here s is the siz e of the points in pixels.
plt.plot(house_size, model.predict(x), color='red', linewidth=2, label='Linear Regression Line') #Here the plot function is used to plot the regression line on the graph Preparation and here linewidth is the thickness of the line in pixels.
plt.scatter(new_house_size, predicted_rent, color='green', s=200, marker='*', label='Predicted Rent') #Here the scatter plot is used to plot the predicted rent point on the graph Preparation and here s is the size of the point in pixels.

#here marker is the shape of the point where it can be used for pointing the points on a line.
plt.xlabel('House Size in sq ft', fontsize=12) #Here the xlabel function is used to label the x-axis of the graph.
plt.ylabel('Rent in INR', fontsize=12) #Here the ylabel function is used to label the y-axis of the graph.
plt.title('House Size vs Rent Prediction using Linear Regression', fontsize=14)
plt.legend() #Here the legend function is used to show the labels of the points and lines on the graph.
plt.grid(True, alpha=0.3) #Here the grid function is used to show the grid lines on the graph and here alpha is the transparency of the grid lines.
plt.savefig('linear_regression_house_rent.png',dpi=150, bbox_inches='tight') #Here the savefig function is used to save the graph as an image file.
plt.show() #Here the show function is used to display the graph.

print("\nLinear Regression model visualization saved as 'linear_regression_house_rent.png'")