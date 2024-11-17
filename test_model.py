import requests
url = "http://127.0.0.1:8000/predict"
test_data = {
 "loan_id": 'JPH2T4UBXC',
 "age": 28,
 "income": 92535,
 "loan_amount": 175581,
 "credit_score": 321,
 "months_employed": 13,
 "num_credit_lines": 2,
 "interest_rate": 24.36,
 "loan_term": 12,
 "dtiratio": 0.66,
 "education": "High School",
 "employment_type": "Self-employed",
 "marital_status": "Married",
 "has_mortgage": "No",
 "has_dependents": "Yes",
 "loan_purpose": "Education",
 "has_co_signer": "Yes",
 "income_to_loan_ratio": 0.5270217164727391,
 "empl_sta": 0.4642857142857143,
 "loan_pay_to_inc_ratio": 0.1581212514183822,
 "credit_util_ratio": 87790.5,
 "credit_age_factor": 14.0,
 "interest_payment_burden": 42771.5316,
 "income_to_interest_ratio": 3798.645320197045,
 "credit_income_inter": 29703735,
 "high_dti_flag": False,
 "marital_status_dependents": "Married_Yes",
 "employment_type_loan_purpose": "Self-employed_Education"
 }

# Send POST request to FastAPI
response = requests.post(url, json=test_data)

# Check if the request was successful
if response.status_code == 200:
    print("Prediction result:", response.json())
else:
    print(f"Request failed with status code {response.status_code}")
    print("Error:", response.text)
