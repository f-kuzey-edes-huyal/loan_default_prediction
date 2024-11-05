[dataset](https://www.kaggle.com/datasets/nikhil1e9/loan-default/data)

[article](https://pdf.sciencedirectassets.com/777796/1-s2.0-S2666764923X00046/1-s2.0-S2666764923000218/main.pdf?X-Amz-Security-Token=IQoJb3JpZ2luX2VjEH0aCXVzLWVhc3QtMSJHMEUCIQCo6yLxh1kIlxWFSvB9px9u5uqlT4RYSP6k2hxcdnbbZAIgTfmpKBzb92IOQkHcPhk0Kza9COFHXl4EOp3AQqeH71AquwUI9f%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAFGgwwNTkwMDM1NDY4NjUiDOnhNFzfhUUEM0PzYSqPBb0BgBY6ApBwOMKGu%2FoglJeZOllfV%2B2L0iWrcZgwi%2BzEq%2FCTDOSufc8%2FkuymU4SBb2TWbMKmOueYy0QR27Hw%2BDi8RW%2B%2BfYIHPaa7Y0UkjnV7sGynOgmOBTE%2ByCb7LF8f3MrAa%2F300exgB%2BRCpmtIXQ3xj1PVqTZIj9TcD1tiQg3wCGHmsj1DbtJremXvRFEcdVQDiLzUXD%2BgtOAOaIEKS0fPKe%2Fde5Vy6VJjlMDIphQSNrXS3T2I8zU1SjRCEmlQ%2Bipw7c0vaKqmUxxl6%2FGF1HMgFfGzKVnIxwM7Ymyp6vRLyKAWm9UdhShKKt8LVggfwgwM74g08WeuWSCJLzHgks9mjUFkem2nstR1sSHrIRW3jUrKifdoerjVYt3vWiCngKgT%2F3OznPKtls2AZWwzKlh1anvAsWK9qf7Flk85T1ZsQza7k5WdvfHNXh6BaribFAU4PDceHPnN4actrSwp6vjXzN8JOIKQJK%2FSyMq2zIZEMPrZuiMxXQZoQAQMMHRu9Luz1hDZpBmczMwrtWY0VakhoOQO36HjC0ejvnD7kuaOw1XWTE%2BHAM64PXEGC2iV8g103MBeGgEjy2Zv2KpaRxI5Du39LfQAnv4CZqZSeqCKNMJOy7juOIBvY5zMx5q3xryCB7KPdo0I6gqduksvdLNheKkT1BV4DD0oakt%2BLdTCgqvf5GC1Uz0IQk7ApEW3lJ%2FNzBw2VU4ysb9d%2BcWgkspkyPAGe%2B91vnz7dn49oZ7EneZrNsy8ecD8UJjWuJTQ%2FFg59KyeFBIQl7W2sVNesR2LaKol7Tu2Ig5AUd1dZGSRfNwkg1uxvdyiLwZfPIunszjBkJ%2B5VCTuAWYIYMOiJgbzOVODK9x3xT9jLSuvKSgwmdOkuQY6sQHh1IOueMR52IAUPtfcJtlV5HJnHkANAJMpviWszQmW0ieWBjGCmv5iTgWM7E%2FPE14d%2FxAP%2BgXY6ANLGUuMn9Q%2Fh%2FCm26xdPj%2BjP7SX2l1BCgmdB4rGflo7X0zftWo6uOYWMkEfifV8taLWbFIRMfryBDfoR%2BDJY91GFpLKn8eiLLjiyS5xFix2kKqzfBTApcAXyoLIzB9oDynv5nIomfWFjDoinEVTmWXvgQg%2B3wLdpOU%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20241104T203311Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAQ3PHCVTYUHTFC7EU%2F20241104%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=059fb38754ae008207a16ca37d36a23103922d977761b7161bf034fffea1cbf1&hash=4957cf8a41f93fc0a5dafef931b8f417a33d6bcf5536a901ba1aaa6cc49f58ba&host=68042c943591013ac2b2430a89b270f6af2c76d8dfd086a07176afe7c76c2c61&pii=S2666764923000218&tid=spdf-1097699e-a6c1-4c73-9610-0e8815b7cad8&sid=a3db921a664a9149979b718598636f6d2efegxrqb&type=client&tsoh=d3d3LnNjaWVuY2VkaXJlY3QuY29t&ua=12105f020b5056540505&rr=8dd760ac5e05d406&cc=tr)



[sample project](https://www.analyticsvidhya.com/blog/2022/04/predicting-possible-loan-default-using-machine-learning/)


# Problem Definition


We may need to apply for a loan to make our dreams a reality, such as purchasing a home, starting our dream job, buying a car, or covering our education costs. When applying for a loan, it is important for the relevant bank or company to accurately assess whether we are eligible to repay the borrowed money. If an organization selects a person who is unable to pay back the loan, they will incur a loss. Conversely, if they mistakenly identify a qualified individual as a defaulter, they risk losing that customer. With this project, I aim to construct a pipeline that will determine whether a customer will default on their loan.



### Loan Default Data Overview

This table provides an overview of the key attributes used in a [loan default prediction dataset](https://www.kaggle.com/datasets/nikhil1e9/loan-default/data), including a brief description and example values for each feature. These attributes offer insights into various aspects of a borrower's financial profile, loan specifics, and personal information, which are essential for assessing the likelihood of loan default.

- **Loan Information**: Attributes like `LoanID`, `LoanAmount`, `LoanTerm`, `InterestRate`, and `LoanPurpose` provide details about the loan, such as its amount, duration, purpose, and interest rate.
- **Borrower Financial Profile**: Attributes such as `Income`, `CreditScore`, `NumCreditLines`, and `DTIRatio` reflect the borrower’s financial health, including their income level, credit score, number of credit lines, and debt-to-income ratio.
- **Personal Information**: Features like `Age`, `MaritalStatus`, `Education`, `EmploymentType`, and `MonthsEmployed` give additional context about the borrower's background, employment stability, and household characteristics.
- **Additional Risk Indicators**: Fields like `HasMortgage`, `HasDependents`, and `HasCoSigner` indicate additional financial obligations or support, which may impact the borrower’s repayment capacity.

The last column, **`Default`**, is the target variable indicating whether the borrower defaulted on the loan (1 for defaulted, 0 for not defaulted). This label serves as the output for training predictive models to forecast default risk based on the borrower and loan features.

| Attribute         | Description                                                   | Example Values            |
|:------------------|:--------------------------------------------------------------|---------------------------|
| LoanID            | A unique identifier for each loan                             | VFVJ0MCK4P                |
| NumCreditLines    | Number of open credit lines the borrower has                  | 5                         |
| MaritalStatus     | Marital status of the borrower                                | Single, Married           |
| Age               | The age of the borrower                                       | 48                        |
| InterestRate      | Annual interest rate of the loan                              | 15.29                     |
| HasMortgage       | Indicates if the borrower has an existing mortgage            | Yes, No                   |
| Income            | The annual income of the borrowerr                            | 118989                    |
| LoanTerm          | Duration of the loan in months                                | 60                        |
| HasDependents     | Indicates if the borrower has dependents                      | Yes, No                   |
| LoanAmount        | The amount of money being borrowed                            | 230883                    |
| DTIRatio          | Debt-to-Income ratio of the borrower                          | 0.76                      |
| LoanPurpose       | Purpose of the loan                                           | Auto, Home, Business      |
| CreditScore       | Credit score of the borrower                                  | 695                       |
| Education         | Education level of the borrower                               | High School, Bachelor's   |
| HasCoSigner       | Indicates if there is a co-signer on the loan                 | Yes, No                   |
| MonthsEmployed    | Number of months the borrower has been employed               | 59                        |
| EmploymentType    | Type of employment (e.g., full-time, part-time, self-employed)| Full-time                 |
| __Default__       | Target variable indicating if the borrower defaulted          | 1 (Yes), 0 (No)           |

### Additional Features through Feature Engineering

[Prediction of loan default based on multi-model fusion](https://www.sciencedirect.com/science/article/pii/S1877050922000953)

" In this paper, we construct a new feature 'installment_feat' based on two features of the
original dataset, installment (the amount of monthly installment of the loan) and annual_inc (annual income).
A larger value of 'installment_feat' means the greater the pressure on the lender to repay the debt and the
greater the probability of default."

```installment_fea  = (12* installment)/(annual_inc)```

We don't have a specific installment feature, but we can approximate one by:

```installment = (12*(LoanAmount/LoanTerm))/Income```



### Key Performance Indicators (KPI)
