
import streamlit as st
import joblib
import pandas as pd
from pathlib import Path

# --------------------------------
# 1. Streamlit application
# --------------------------------

st.set_page_config(
    page_title="Car Price Prediction",
    page_icon="🚗",
    layout="centered"
)

st.title("🚗 Car Price Prediction App")
st.write("Enter the car details to predict its selling price.")

# --------------------------------
# 2. Load model and scaler
# --------------------------------

BASE_DIR = Path(__file__).resolve().parent

model_path = BASE_DIR / "cars24_model.joblib"
scaler_path = BASE_DIR / "scaler.pkl"

if not model_path.exists():
    st.error(f"Model file not found: {model_path}")
    st.stop()

if not scaler_path.exists():
    st.error(f"Scaler file not found: {scaler_path}")
    st.stop()

try:
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)

except Exception as e:
    st.error(f"Error loading model or scaler: {e}")
    st.stop()

st.success("Model and scaler loaded successfully!")

# --------------------------------
# 3. Input features
# --------------------------------

year = st.slider(
    "Manufacturing Year",
    min_value=1990,
    max_value=2023,
    value=2015,
    step=1
)

seller_type = st.selectbox(
    "Seller Type",
    ["Dealer", "Individual", "Trustmark Dealer"]
)

km_driven = st.number_input(
    "Kilometers Driven",
    min_value=0,
    max_value=1000000,
    value=50000,
    step=5000
)

mileage = st.number_input(
    "Mileage (kmpl)",
    min_value=0.0,
    max_value=18.0,
    value=15.0,
    step=0.5
)

max_power = st.number_input(
    "Max Power (bhp)",
    min_value=0.0,
    max_value=300.0,
    value=150.0,
    step=5.0
)

col1, col2 = st.columns(2)

with col1:
    fuel_type = st.selectbox(
        "Fuel Type",
        ["Diesel", "Petrol", "CNG", "LPG", "Electric"]
    )

    engine = st.number_input(
        "Engine (cc)",
        min_value=500,
        max_value=5000,
        value=1500,
        step=100
    )

with col2:
    transmission_type = st.selectbox(
        "Transmission Type",
        ["Manual", "Automatic"]
    )

    seats = st.number_input(
        "Seats",
        min_value=2,
        max_value=10,
        value=5,
        step=1
    )

# --------------------------------
# 4. Define training feature order
# --------------------------------

feature_columns = [
    'year',
    'km_driven',
    'mileage',
    'engine',
    'max_power',
    'age',
    'Individual',
    'Trustmark Dealer',
    'Diesel',
    'Electric',
    'LPG',
    'Petrol',
    'Manual',
    '5',
    '>5'
]

# --------------------------------
# 5. Model prediction function
# --------------------------------

def model_pred(
    year,
    seller_type,
    km_driven,
    fuel_type,
    transmission_type,
    mileage,
    engine,
    max_power,
    seats
):

    # Calculate car age
    age = 2023 - year

    # Create all 15 input features
    input_data = {
        'year': float(year),
        'km_driven': float(km_driven),
        'mileage': float(mileage),
        'engine': float(engine),
        'max_power': float(max_power),
        'age': float(age),

        # Seller type encoding
        'Individual': int(seller_type == 'Individual'),
        'Trustmark Dealer': int(
            seller_type == 'Trustmark Dealer'
        ),

        # Fuel type encoding
        'Diesel': int(fuel_type == 'Diesel'),
        'Electric': int(fuel_type == 'Electric'),
        'LPG': int(fuel_type == 'LPG'),
        'Petrol': int(fuel_type == 'Petrol'),

        # Transmission encoding
        'Manual': int(transmission_type == 'Manual'),

        # Seats encoding
        '5': int(seats == 5),
        '>5': int(seats > 5)
    }

    # Convert dictionary into DataFrame
    data = pd.DataFrame(
        [input_data],
        columns=feature_columns
    )

    # Match the exact scaler training column order,
    # if the scaler contains feature names
    if hasattr(scaler, "feature_names_in_"):

        expected_columns = list(scaler.feature_names_in_)

        missing_columns = set(expected_columns) - set(data.columns)

        if missing_columns:
            raise ValueError(
                f"Missing training features: {missing_columns}"
            )

        data = data[expected_columns]

    # Verify feature count
    if data.shape[1] != scaler.n_features_in_:
        raise ValueError(
            f"Expected {scaler.n_features_in_} features, "
            f"but received {data.shape[1]} features."
        )

    # Scale input features
    data_scaled = scaler.transform(data)

    # Predict selling price
    prediction = model.predict(data_scaled)

    return round(float(prediction[0]), 2)


# --------------------------------
# 6. Predict button
# --------------------------------

if st.button("Predict Car Price", type="primary"):

    try:

        price = model_pred(
            year,
            seller_type,
            km_driven,
            fuel_type,
            transmission_type,
            mileage,
            engine,
            max_power,
            seats
        )

        st.success(
            f"Predicted Car Price: ₹ {price} Lakhs (approx.)"
        )

    except Exception as e:

        st.error(f"Prediction Error: {e}")

else:

    st.info(
        "Click the Predict Car Price button "
        "after entering all the car details."
    )


















































































































#import streamlit as st
#import pickle
#import joblib

#st.title("Car Price Prediction App")

#encode_dict = {
    #"fuel_type": {"Diesel": 1, "Petrol": 2, "CNG": 3, "LPG": 4, "Electric": 5},
    #"transmission_type": {"Manual": 1, "Automatic": 2},
    #"seller_type": {"Dealer": 1, "Individual": 2, "Trustmark Dealer": 3},
#}

#model = joblib.load('cars24_model.joblib')
#scaler = joblib.load('scaler.pkl')

#year = st.slider("Manufacturing Year", min_value=1990, max_value=2023, value=2015, step=1)

#seller_type = st.selectbox("Seller Type",
                          #["Dealer", "Individual", "Trustmark Dealer"])

#km_driven = st.number_input("Kilometers Driven",
                            #min_value=0, max_value=1000000,
                            #value=50000, step=5000)

#mileage = st.number_input("Mileage (kmpl)",
                          #min_value=0.0, max_value=18.0,
                          #value=15.0, step=0.5)

#max_power = st.number_input("Max Power (bhp)",
                           #min_value=0.0, max_value=300.0,
                           #value=150.0, step=5.0)

#col1, col2 = st.columns(2)

#fuel_type = col1.selectbox("Fuel Type",
                           #["Diesel", "Petrol", "CNG", "LPG", "Electric"])

#engine = col2.number_input("Engine (cc)",
                           #min_value=500, max_value=5000,
                           #value=1500, step=100)

#transmission_type = st.selectbox("Transmission Type",
                                 #["Manual", "Automatic"])

#seats = st.number_input("Seats",
                        #min_value=2, max_value=10,
                        #value=5, step=1)

#import pandas as pd

# Define feature columns in the exact training order
#feature_columns = [
    #'year',
    #'km_driven',
    #'mileage',
    #'engine',
    #'max_power',
    #'age',
    #'Individual',
    #'Trustmark Dealer',
    #'Diesel',
    #'Electric',
    #'LPG',
    #'Petrol',
    #'Manual',
    #'5',
    #'>5'
#]


#def model_pred(
    #year, seller_type, km_driven, fuel_type,
    #transmission_type, mileage, engine, max_power, seats
#):

    # Calculate car age (dataset uses 2023 as reference year)
    #age = 2023 - year

    # Convert categorical inputs into one-hot encoded features
    #data = pd.DataFrame([{
        #'year': float(year),
        #'km_driven': float(km_driven),
        #'mileage': float(mileage),
        #'engine': float(engine),
        #'max_power': float(max_power),
        #'age': float(age),

        # Seller type encoding
        #'Individual': 1 if seller_type == 'Individual' else 0,
        #'Trustmark Dealer': 1 if seller_type == 'Trustmark Dealer' else 0,

        # Fuel type encoding
        #'Diesel': 1 if fuel_type == 'Diesel' else 0,
        #'Electric': 1 if fuel_type == 'Electric' else 0,
        #'LPG': 1 if fuel_type == 'LPG' else 0,
        #'Petrol': 1 if fuel_type == 'Petrol' else 0,

        # Transmission encoding
        #'Manual': 1 if transmission_type == 'Manual' else 0,

        # Seats encoding
        #'5': 1 if seats == 5 else 0,
        #'>5': 1 if seats > 5 else 0

    #}], columns=feature_columns)

    # Scale the 15 features
    #data_scaled = scaler.transform(data)

    # Predict car price
    #prediction = model.predict(data_scaled)

    #return round(float(prediction[0]), 2)


# Predict button
#if st.button("Predict"):

    #price = model_pred(
        #year,
        #seller_type,
        #km_driven,
        #fuel_type,
        #transmission_type,
        #mileage,
        #engine,
        #max_power,
        #seats
    #)

    #st.write(f"**Predicted Car Price: {price} Lakhs (approx.)**")

#else:
    #st.write("Click the **Predict** button once you've entered all the details.")