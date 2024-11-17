from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np

# FastAPI app
app = FastAPI()


# Define the input data model for 20 features
class InputData(BaseModel):
    loan_id: str
    age: int
    income: int 
    loan_amount: int
    credit_score: int 
    months_employed: int
    num_credit_lines: int 
    interest_rate: float 
    loan_term: int
    dtiratio: float
    education: str      
    employment_type: str
    marital_status: str    
    has_mortgage: str
    has_dependents: str
    loan_purpose: str
    has_co_signer: str
    income_to_loan_ratio: float        
    empl_sta: float     
    loan_pay_to_inc_ratio: float
    credit_util_ratio: float
    credit_age_factor: float
    interest_payment_burden: float
    income_to_interest_ratio: float
    credit_income_inter: int
    high_dti_flag: bool         
    marital_status_dependents: str
    employment_type_loan_purpose: str

# Load the model and DictVectorizer from the saved file (once when the app starts)
with open("modelxgb_i=93.bin", 'rb') as f_in:
    dv, model = pickle.load(f_in)

# Define an endpoint for prediction
@app.post("/predict")
def predict(data: InputData):
    # Convert input data to dictionary for DictVectorizer
    data_dict = data.dict()  # Convert to dictionary for DictVectorizer

    # Transform input data using DictVectorizer
    transformed_data = dv.transform([data_dict])
    # Specify the columns you want to keep
    selected_features = ['months_employed', 'credit_score', 'age', 'interest_rate',
       'credit_age_factor', 'dtiratio', 'interest_payment_burden',
       'income_to_interest_ratio', 'credit_income_inter',
       'income_to_loan_ratio', 'loan_pay_to_inc_ratio', 'loan_amount',
       'empl_sta', 'credit_util_ratio', 'income', 'has_co_signer=No',
       'employment_type=Full-time', 'loan_term',
       'employment_type=Unemployed', 'has_dependents=No']  # Example: Select feature1 and feature3

    feature_names = dv.get_feature_names_out()
   

    # Get indices of selected features
    selected_indices = [np.where(feature_names == feature)[0][0] for feature in selected_features]

    # Extract the specific columns
    filtered_data = transformed_data[:, selected_indices]

    #filtered_data = dict((k, transformed_data[k]) for k in selected_features if k in transformed_data)
 

    # Make prediction using the model
    prediction = model.predict_proba(filtered_data)[:,1]
    y_decision = (prediction > 0.5).astype(int).tolist()

    return {"prediction": y_decision}

# If running with Uvicorn (use this in terminal):
# uvicorn app:app --reload