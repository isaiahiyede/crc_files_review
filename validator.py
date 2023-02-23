import json
import re

# validator to use
# to be reworked.............
# def validator_to_use(file_type,data_file):
#     pattern = "[ _]"
#     file_type_name = re.sub(pattern, "", file_type.lower())
#     return_obj = f'{file_type_name(file_type,data_file)}'
#     return eval(return_obj)

# field must return value
def isTrue():
    return True

# validation for individual borrower
def individualborrower(file_type,data_file):
    # check validation rules
    # 1 rule: specify count of columns
    # 2 rule: customerID not null and 20 characters in all
    # 3 rule: set branchcode to '001' is if null
    # 4 rule: firstname not null
    # 5 rule: last name not null
    # 6 rule: middle name optional but if provided more than 2 characters and less than 20 characters in length without space
    # 7 rule: date of birth not null and format should be 'DD/MM/YYY'
    # 8 rule: National Identity Number optional but if provided more than 2 characters and less than 20 characters in length without space
    # 9 rule: Drivers License No optional but if provided more than 2 characters and less than 20 characters in length without space
    # 10 rule: BVN mandatory and must be 11 chracters in length
    
    # 11 rule: Passport No optional but if provided more than 2 characters and less than 20 characters in length without space
    # 12 rule: Gender not null ("male","female","m","f")
    # 13 rule: Nationality not null ("Nigeria","NG")
    # 14 rule: Marital Status not null ("single","married","divorced","widow","widower")
    # 15 rule: Mobile number not null - must not have special characters
    # 16 rule: Primary Address Line 1 mandatory but more than 2 characters and less than or equal to 100 characters in length
    # 17 rule: Primary Address Line 2 not mandatory but if provided must be more than 2 characters and less or equal to 100 characters in length
    # 18 rule: Primary city/LGA mandatory but more than 2 characters and less than or equal to 100 characters in length
    # 19 rule: Primary State mandatory but more than 2 characters and less than or equal to 15 characters in length
    # 20 rule: Primary Country mandatory but more than 2 characters and less than or equal to 15 characters in length
    
    # 21 rule: Employment Status mandatory ("employed","unemployed","self employed")
    # 22 rule: Occupation mandatory but more than 2 characters and less than or equal to 15 characters in length
    # 23 rule: Business Category mandatory
    # 24 rule: Business Sector mandatory
    # 25 rule: Borrower Type mandatory
    
    # 26 rule: Other ID not mandatory but more than 2 characters and less than or equal to 100 characters in length if provided
    # 27 rule: Tax ID not mandatory but more than 2 characters and less than or equal to 100 characters in length if provided
    # 28 rule: Picture File Path not mandatory but more than 2 characters and less than or equal to 100 characters in length if provided
    # 29 rule: E-mail address not mandatory but more than 2 characters and less than or equal to 100 characters in length if provided
    # 30 rule: Employer Name not mandatory but more than 2 characters and less than or equal to 100 characters in length if provided
    # 31 rule: Employer Address Line 1 not mandatory but more than 2 characters and less than or equal to 100 characters in length if provided
    # 32 rule: Employer Address Line 2 not mandatory but more than 2 characters and less than or equal to 100 characters in length if provided
    # 33 rule: Employer City not mandatory but more than 2 characters and less than or equal to 100 characters in length if provided
    # 34 rule: Employer State not mandatory but more than 2 characters and less than or equal to 100 characters in length if provided
    # 35 rule: Employer Country not mandatory but more than 2 characters and less than or equal to 100 characters in length if provided
    # 36 rule: Title not mandatory but more than 2 characters and less than or equal to 100 characters in length if provided
    # 37 rule: Place of Birth not mandatory but more than 2 characters and less than or equal to 100 characters in length if provided
    # 38 rule: Work phone not mandatory but more than 2 characters and less than or equal to 100 characters in length if provided
    # 39 rule: Home phone not mandatory but more than 2 characters and less than or equal to 100 characters in length if provided
    # 40 rule: Secondary Address Line 1 not mandatory but more than 2 characters and less than or equal to 100 characters in length if provided
    # 41 rule: Secondary Address Line 1 not mandatory but more than 2 characters and less than or equal to 100 characters in length if provided
    # 42 rule: Secondary Address City/LGA not mandatory but more than 2 characters and less than or equal to 100 characters in length if provided
    # 43 rule: Secondary Address State not mandatory but more than 2 characters and less than or equal to 100 characters in length if provided
    # 44 rule: Secondary Address Country not mandatory but more than 2 characters and less than or equal to 100 characters in length if provided
    # 45 rule: Spouse's Surname not mandatory but more than 2 characters and less than or equal to 100 characters in length if provided
    # 46 rule: Spouse's First name not mandatory but more than 2 characters and less than or equal to 100 characters in length if provided
    # 47 rule: Spouse's Middle name not mandatory but more than 2 characters and less than or equal to 100 characters in length if provided
    return True

# validation for Credit Information
def creditinformation(file_type,data_file):
    return True

# validation for Corporate Borrower Information
def corporateborrowerinformation(file_type,data_file):
    return True

# validation for Guarantor Information
def guarantorinformation(file_type,data_file):
    return True

# validation for Principal Template
def principaltemplate(file_type,data_file):
    return True