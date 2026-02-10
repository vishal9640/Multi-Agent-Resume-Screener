import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.preprocessing import PolynomialFeatures
#Generating the data 
np.random.seed(42)
df = pd.DataFrame({
    'area_sqft': np.random.randint(500, 3500, 500),
    'bedrooms': np.random.randint(1,5,500),
    'distance_to_metro_km': np.round(np.random.uniform(0.5,10,500),1),
    'floor_number': np.random.randint(1,21,500),
    'age_of_building': np.random.randint(1,26,500),
})

# We define the features which effected the rent
Base_rent = 2000
rent_per_sqft = 15
rent_per_sqft_sqaured = 0.02 #This is for polynomial features
rent_per_bedroom = 1000
reduction_per_km = 200
reduction_per_year = 300
increase_per_floor = 300

#Calculating rent with the curved relationship by sqauring

df['rent'] = (Base_rent
              +rent_per_sqft *df['area_sqft']
              +rent_per_bedroom *df['bedrooms']
              +increase_per_floor *df['floor_number']
              -reduction_per_km *df['distance_to_metro_km']
              -reduction_per_year *df['age_of_building']
              +rent_per_sqft_sqaured * (df['area_sqft'] **2) #To keep the polynomial feature
)
print(df.head())

#Now we are preapring the data to train for linear model 
X = df['area_sqft'].values.reshape(-1,1)
y=df['rent'].values

#Now we are splitting the data into training and tetsting sets 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#We need to create the linear model 
model_linear = LinearRegression()
model_linear.fit(X_train, y_train)

#Predicting the rent using the test data 
y_pred_linear = model_linear.predict(X_test)

print("\n Linear Regressuion Predictions:")
print(f"Rent = {model_linear.coef_[0]:.2f} * Area_sqft + {model_linear.intercept_:.2f}")
print ("\n Linear Regression Model Performance:")
r2_linear = r2_score(y_test, y_pred_linear)
print(f"R-squared: {r2_linear:.4f}")


#Now we are preparing the data for polynomial regression
poly = PolynomialFeatures(degree=2, include_bias=False) #Here degree=2 means we are using square features

#Data prep to transform the data according to polynomial features
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)

# CEreating the polynomial regression model
poly_model = LinearRegression()
poly_model .fit(X_train_poly, y_train)

# We can print output in the terminal to see how the features are transformed
print("\n Polynomial Features:")
print(f"Original : Area = {X_train[0][0]}")
print(f"After : Area = {X_train_poly[0][0]:.0f}, Area^2 = {X_train_poly[0][1]:.0f}")

#Predict the data from the model 
y_pred_poly = poly_model.predict(X_test_poly)

#output the results 
print("\n Polynomial Regression Predictions:")
print(f"Rent= {poly_model.coef_[0]:.0f} * Area + {poly_model.coef_[1]:.0f} * Area^2 + {poly_model.intercept_:.0f}")

#Comparing the model 
#Linear Vs Polynomial
X_plot = np.linspace(X.min(), X.max(), 100).reshape(-1,1) # Here we are creating 100 points between min and max for smooth curve
X_plot_poly = poly.transform(X_plot) # Here we are transforming the data for polynomial features

#plotting the both models 
plt.figure(figsize=(10,6))

#mention the data points 
plt.scatter(X,y, alpha=0.3, label= "Actual Rent Data")

#Linear regression scatter
plt.plot(X_plot, model_linear.predict(X_plot), color='red', label='Linear Regression', linewidth=2)

#Polynomial regression scatter
plt.plot(X_plot, poly_model.predict(X_plot_poly), color='green', label='Polynomial Regression (Degree 2)', linewidth=2)

plt.xlabel('Area (sqft)')
plt.ylabel('Rent')
plt.title('Linear vs Polynomial Regression')
plt.legend()
plt.show()

#Accuracy metrics for Linear and polynomial regression
r2_linear = r2_score(y_test, y_pred_linear)
print("\n Linear Regression Model Performance:")
r2_poly = r2_score(y_test, y_pred_poly)
print("\n Polynomial Regression Model Performance:")
print("\n Accuracy Metrics:")
print(f"Linear Regression R²: {r2_linear:.4f}")
print(f"Polynomial Regression R²: {r2_poly:.4f}")
print(f"\n Improvement: {(r2_poly - r2_linear):.4f} ({((r2_poly - r2_linear)/r2_linear)*100:.1f}% better)")