from matplotlib import colors
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
# Sample data for multiple linear regression
common_interest =[2,3,5,6,7,8,6,5,8,7]
response_time=[3,4,6,5,7,8,5,9,4,6]
age_compartibility= [4,5,7,8,6,9,5,4,1,8]

#I want to predict the match score of each couple outof 100
match_score = [50, 60, 70, 65, 80, 90, 75, 85, 88, 92]

#prepare the model
X= np.array([common_interest, response_time, age_compartibility]).T #Here the .T is used to transpose the array. Why ? Because sklearn expects the features to be in columns.
y= np.array(match_score)#Here the target variable is a 1D array. So we are not using .T

#y=mx+b(linear) y=m1*x1+m2*x2+m3*x3+.....+b(multiple linear)
print("Our features (X):")
print("Interest | Response Time | Age Compatibility")
print(X)
print(f"\nShape: {X.shape}-> 10 samples, 3 features\n") #Here we have 8 samples and 3 features. By the help of shape we can confirm that our data is in the correct format.
#(10,3)

#Creating the model
model = LinearRegression()
model.fit(X,y)

print(f"\n ------what model has leanred!------")
print(f"Coefficients: {model.coef_.round(2)}") #Here Coefficients are the weights assigned to each feature. We are rounding the coefficients to 2 decimal places for better readability.
print(f"-> coefficients Common interests contributes: {model.coef_[0]:.2f}points per unit")
print(f"-> coefficients Response time contributes: {model.coef_[1]:.2f}points per unit")
print(f"-> coefficients Age compatibility contributes: {model.coef_[2]:.2f}points per unit")

#predict for a new match #y=w1x1+w2x2+w3x3+b -> y=wx+b

new_match = [[7,8,6]] #7 common interests, 8 response time, 6 age compatibility. Here the new match data is in the correct format (1 sample, 3 features) in 2d format.
predicted_score = model.predict(new_match)

#print the prediction 

print("\n ------- New match predictions -------")
print(f"Common Interests: 7/10")
print(f"Response Time: 8/10")
print(f"Age Compatibility: 6/10")
print(f"Predicted Match Score: {predicted_score[0]:.1f}/100")

#Visualizing the results
fig, axis = plt.subplots(1,3, figsize=(15,5)) #Here the subplots function is used to create multiple plots (3 plots )in a single figure.
#here the subplots are we need 3 colums with 3 images in the sigle image.

features= [common_interest, response_time, age_compartibility]
names= ['Common Interests', 'Response Time', 'Age Compatibility']
colors_list= ['r','g','b'] 

for i, (feature, name, color) in enumerate(zip(features, names, colors_list)):
    axis[i].scatter(X[:, i], match_score, color=color, s=100, alpha=0.7)
    axis[i].set_xlabel(name, fontsize=11)
    axis[i].set_ylabel('Match Score', fontsize=11)
    axis[i].set_title(f"{name} Vs Match Score", fontsize=12)
    axis[i].grid(True, alpha=0.3) # Here the grid function is used to add grid lines to the plot for better readability.
#Here aplha is used to set the transparency of the grid lines.

plt.suptitle("Multiple Linear Regression: Features vs Match Score", fontsize=14, fontweight='bold')
plt.tight_layout(rect=[0, 0.03, 1, 0.95]) #Here the tight_layout function is used to adjust the spacing between subplots to prevent overlap.
plt.savefig("multiple_linear_regression_match_score.png",dpi=150, bbox_inches='tight') 
plt.show()
print("Graph is saved ")