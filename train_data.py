from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Load engineered dataset
df = pd.read_csv("sensor_data_features.csv")

# Define features (X) and target (y) - Example: Predicting Temperature
X = df.drop(columns=['temperature'])  # Features
y = df['temperature']  # Target variable

# Split into training & testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate performance
mse = mean_squared_error(y_test, y_pred)
print(f"Model Mean Squared Error: {mse}")

# Save trained model
import joblib
joblib.dump(model, "sensor_model.pkl")
print("Model training complete. Saved as sensor_model.pkl.")