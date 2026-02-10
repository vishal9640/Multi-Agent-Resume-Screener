#Impoerted all the necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

#Now i am going to create a sample dataset or else loading a dataset
df= pd.read_csv('D:\Machine Learning\PYthon_COding\Housing.csv') 

#Here the dataset contains some categorical variables which need to be converted into numerical format for the model to understand yes=1 and no=0. 
binary_cols=['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea']
df[binary_cols] = df[binary_cols].apply(lambda x:x.map({'yes':1, 'no':0}))

#Here we are using the get_dummies function to convert the categorical variable 'furnishingstatus' into numerical format.
df = pd.get_dummies(df, columns=['furnishingstatus'], drop_first=False, dtype=int)

#Apply log transformation to reduce skewness in price and area
df['price_log'] = np.log(df['price'])
df['area_log'] = np.log(df['area'])

print(df.head()) #Which displays the first 5 rows of the dataset
print(df.info()) #Which displays the information about the dataset

# Set display options to show all columns
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
print(df.describe()) #Which displays the statistical summary of the dataset

#Preparing the features and target variable
X = df.drop(['price', 'price_log','area','hotwaterheating'], axis=1) #Dropping the original price column and using the log transformed price as target variable
y= df['price_log']
print("X shape:", X.shape)
print("y shape:", y.shape)
print("\n Features (X) columns:")
print(X.columns)

#Now splitting the data into training and testing sets
X_train, X_test, y_train, y_test= train_test_split(X,y, test_size=0.2, random_state=42)

#Creating and training the model
model= LinearRegression()
model.fit(X_train, y_train)

#Predicting the prices using the test data
y_pred= model.predict(X_test)

#Evaluating the model
print("\n Linear Regression Model Performance (log-Scale):")
r2= r2_score(y_test, y_pred)
mse_log= mean_squared_error(y_test, y_pred) 
rmse_log = np.sqrt(mse_log)
print(f"R-squared: {r2:.4f}")
print(f"Mean Squared Error: {mse_log:.4f}")

#To convert the log transformed prices back to original prices we need to apply exponential function
y_test_price = np.exp(y_test)
y_price_pred = np.exp(y_pred)
mse_price = mean_squared_error(y_test_price, y_price_pred)
rmse_price = np.sqrt(mse_price)

print("\nPerformance in original price scale:")
print(f"MSE (price): {mse_price:.2f}")
print(f"RMSE (price): {rmse_price:.2f}")

# Final predicted prices (original scale)
price_pred = y_price_pred

#Visualizing the residuals
residuals = y_test - y_pred
plt.hist(residuals, bins=30)
plt.title("Residuals (log scale)")
plt.show()

plt.figure(figsize=(8,6))
plt.scatter(y_test_price, y_price_pred, alpha=0.7)
plt.plot([y_test_price.min(), y_test_price.max()], [y_test_price.min(), y_test_price.max()], 'r--', lw=2)
plt.xlabel("Area")
plt.ylabel("Price")
plt.title("Area vs Price")
plt.legend() #Legend to differentiate actual and predicted rents
plt.grid(True, alpha=0.3)
plt.savefig('LinearRegression.png',dpi=150, bbox_inches='tight')
plt.show()


#Multi Linear Regression model 
X= df[['area', 'bedrooms', 'bathrooms', 'stories', 'mainroad', 'guestroom', 'basement', 'airconditioning', 'prefarea',
       'furnishingstatus_furnished', 'furnishingstatus_semi-furnished', 'furnishingstatus_unfurnished']]
y= df['price_log']

#Splitting the data into training and testing sets
X_train_multi, X_test_multi, y_train_multi, y_test_multi = train_test_split(X, y, test_size=0.2, random_state=42)

#Creating and training the model
model_multi = LinearRegression()
model_multi.fit(X_train_multi, y_train_multi)

#Predicting the prices using the test data
y_predict_multi = model_multi.predict(X_test_multi)

#print the values in the terminal 
print(f"\n Multiple Linear Regression Model :")
print(f"\n Rent = {model_multi.intercept_:.4f} ")
 
for feature, coef in zip(X.columns, model_multi.coef_):
    print(f"    + ({coef:.4f} * {feature})")
    
r2_multi = r2_score(y_test_multi, y_predict_multi)
mse_multi = mean_squared_error(y_test_multi, y_predict_multi)
mae_multi = mean_absolute_error(y_test_multi, y_predict_multi)
print(f"\n R² Score: {r2_multi:.4f} (closer to 1.0 = better)")
print(f" Mean Squared Error: ${mse_multi:,.0f}")
print(f" Mean Absolute Error: ${mae_multi:,.0f}")

#Comparison
print(f"\n========== MODEL COMPARISON ==========")
print(f"Simple Linear Regression R²: {r2:.4f}")
print(f"Multiple Linear Regression R²: {r2_multi:.4f}")
print(f"\nImprovement: {(r2_multi - r2):.4f} ({((r2_multi - r2)/r2)*100:.1f}% better)")

plt.scatter(y_test_multi, y_predict_multi, alpha=0.5, label='Predicted Price')
plt.plot([y_test_multi.min(), y_test_multi.max()], [y_test_multi.min(), y_test_multi.max()], 'r--', lw=2)
plt.xlabel('Actual Rent ($)')
plt.ylabel('Predicted Rent ($)')
plt.title(f"Multiple Linear Regression: Actual vs Predicted Rent (R²={r2_multi:.4f})")
plt.legend() #Legend to differentiate actual and predicted rents
plt.grid(True, alpha=0.3)
plt.savefig('MultipleLinearRegression.png',dpi=150, bbox_inches='tight')
plt.show()



