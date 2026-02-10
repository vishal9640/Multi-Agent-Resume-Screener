import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

#Now we are generating the data using the following line:
np.random .seed(42)

#Creating a DataFrame with random data
df = pd.DataFrame({
    #Choosing 'area_sqft' between 500 and 3500 sqft for 500 samples
  'area_sqft' : np.random.randint(500, 3500, 500),
  #Bedrooms between 1 and 4
  'bedrooms' : np.random.randint(1, 5, 500),
  #Metro access score between 0.5 and 10.  
  #Here we round it to one decimal place for better readability. Beacuse metro access scores are often represented in such a manner, where it have .
  'Metro_Access_Score' : np.round(np.random.uniform(0.5, 10, 500), 1),
  #Floor number between 1 and 20
  'floor_number' : np.random.randint(1, 21, 500),
  #Age of the byilding between 1 and 25 years
  'age_of_building' : np.random.randint(1, 26, 500),
})

#Lets define how well factors will effect the rent
base_rent = 2000
rent_per_sqft = 15
rent_per_bedroom = 3000
rent_per_each_floor=300
rent_reduction_per_km = 200   #Rent reduction per km from metro. getting fartherto metro increases rent
rent_reduction_per_year = 300 # Rent reduction per year of building age

#y=mx+b , mx+c, wx+a
#Calulating using the formula. to get the rent which is the value of Y
df['rent'] = (base_rent 
              + rent_per_sqft * df['area_sqft'] 
              + rent_per_bedroom * df['bedrooms']
              + rent_per_each_floor * df['floor_number']
              - rent_reduction_per_km * df['Metro_Access_Score']
              - rent_reduction_per_year * df['age_of_building']
              )

print(df.head())
X= df[['area_sqft']]
y= df['rent']

#Splitting the data into training and testing sets. With 80% for training and 20% for testing
X_train , X_test, y_train,y_test = train_test_split(X,y,test_size=0.2, random_state=42)

#Creating the Linear Regression model
model = LinearRegression()

#Training the model using the training data here X_train and y_train. The regular X and y are not used for training directly.
model.fit(X_train,y_train)

#Predicting the rent for the test data
y_pred = model.predict(X_test)

#Print the output along with the df head
print("\n Simple Linear Regression Model :")
print(f"\n Rent={model.coef_[0]:.0f} * Area + {model.intercept_:.0f}") #Here y=mx+c format is used where m is coef_ and c is intercept_

#Calculating accuracy metrics
r2_simple = r2_score(y_test, y_pred)
mse_simple = mean_squared_error(y_test, y_pred)
mae_simple = mean_absolute_error(y_test, y_pred)
print(f"\n R² Score: {r2_simple:.4f} (closer to 1.0 = better)")
print(f" Mean Squared Error: ${mse_simple:,.0f}")
print(f" Mean Absolute Error: ${mae_simple:,.0f}")

#Plotting the actual vs predicted rents
plt.scatter(X_test['area_sqft'], y_test, alpha=0.5, label='Actual Rent')
X_test_sorted = X_test.sort_values('area_sqft')
plt.plot(X_test_sorted['area_sqft'], model.predict(X_test_sorted), color='red', label='Predicted Rent')
plt.xlabel('Area (sqft)')
plt.ylabel('Rent ($)') 
plt.title('Actual vs Predicted Rent based on Area')
plt.legend() #Legend to differentiate actual and predicted rents
plt.grid(True, alpha=0.3)
plt.savefig('Comparision_Linear.png',dpi=150, bbox_inches='tight')
plt.show()


#Creating a multiliner model
X = df[['area_sqft', 'bedrooms', 'Metro_Access_Score', 'floor_number', 'age_of_building']]

#The output which we want to predict
y = df['rent']

#Spliiting the data into training and testing sets. With 80% for training and 20% for testing
X_test_multi , X_train_multi, y_test_multi,y_train_multi = train_test_split(X,y,test_size=0.2, random_state=42)

#Creating the model
model_multi = LinearRegression()

#Train the model with the available data
model_multi.fit(X_train_multi,y_train_multi)

#Now we need to predict the rent for the test data
y_pred_multi = model_multi.predict(X_test_multi)

#print the values in the terminal 
print(f"\n Multiple Linear Regression Model :")
print(f"\n Rent = {model_multi.intercept_:.0f} ")
for feature, coef in zip(X.columns, model_multi.coef_):
    print(f"     + ({coef:.0f} * {feature})")

#Calculating accuracy metrics
r2_multi = r2_score(y_test_multi, y_pred_multi)
mse_multi = mean_squared_error(y_test_multi, y_pred_multi)
mae_multi = mean_absolute_error(y_test_multi, y_pred_multi)
print(f"\n R² Score: {r2_multi:.4f} (closer to 1.0 = better)")
print(f" Mean Squared Error: ${mse_multi:,.0f}")
print(f" Mean Absolute Error: ${mae_multi:,.0f}")

#Comparison
print(f"\n========== MODEL COMPARISON ==========")
print(f"Simple Linear Regression R²: {r2_simple:.4f}")
print(f"Multiple Linear Regression R²: {r2_multi:.4f}")
print(f"\nImprovement: {(r2_multi - r2_simple):.4f} ({((r2_multi - r2_simple)/r2_simple)*100:.1f}% better)")
    
    
#Ploting evrtything
plt.scatter(y_test_multi, y_pred_multi, alpha=0.5, label='Predictions')

#Drawing a red dashed diagonal line from (min, min) to (max, max) representing perfect predictions
#Points closer to this line indicate better model accuracy
plt.plot([y_test_multi.min(), y_test_multi.max()], [y_test_multi.min(), y_test_multi.max()], 'r--', label='Perfect Prediction') 
plt.xlabel('Actual Rent ($)')
plt.ylabel('Predicted Rent ($)')
plt.title(f"Multiple Linear Regression: Actual vs Predicted Rent (R²={r2_multi:.4f})")
plt.legend() #Legend to differentiate actual and predicted rents
plt.grid(True, alpha=0.3)
plt.savefig('Comparision_multi.png',dpi=150, bbox_inches='tight')
plt.show()

#Polynomial Regression 
#y=mx+b our target is to draw a curved line. 
#y= prediction value

#Rent= a + b * Area + c * Area^2

#Here we are adding a new feature Area^2 to the existing feature Area

#Why we are squaring the area because we want to capture non-linear relationships between area and rent. 

#By adding the square the values will get increased exponentially which the graph will show a curve instead of a straight line.

# By using the degree we can control the curvature of the line.
#Degree 1: Rent = a(Intercept) + b(m) * Area (X)-> straight line
#Degree 2: Rent = a + b * Area + c * Area^2 -> One nice curved line
#Degree 3: Rent = a + b * Area + c * Area^2 + d * Area^2 -> More complex curve with more bends like S shaped curve



    
    
    
    