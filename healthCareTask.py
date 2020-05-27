# -*- coding: utf-8 -*-
"""
Created on Wed May 27 19:07:06 2020

@author: z02511mm
"""
import pandas as pd
from datetime import datetime
from datetime import date


read_codes = pd.read_csv('test_data/read_codes.txt', skiprows=[0], sep="\t",header=None)
read_codes.columns = ["read_code", "description"]

clinical_data = pd.read_csv('test_data/clinical_data.txt', skiprows=[0], sep="\t",header=None)
clinical_data.columns = ["date_recorded", "patient_id", "read_code"]

patients = pd.read_csv('test_data/patients.txt', skiprows=[0], sep="\t",header=None)
patients.columns = ["date_extracted", "date_of_birth", "full_name", "gender", "id"]


count_male = patients.loc[patients.gender == 2, "gender"].count()
print ("Number of male patient " + str(count_male))
pt_date_extracted = patients.loc[patients.date_extracted > "2015-01-01", "date_extracted"].count()
print("Patient extracted after 01/01/2015 " + str(pt_date_extracted))
               

def calculate_age(born):
    born = datetime.strptime(born, "%d/%m/%Y").date()
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
patients['age'] = patients['date_of_birth'].apply(calculate_age)
print("Min " + str(patients['age'].min()))
print("Max " + str(patients['age'].max()))
print("Median " + str(patients['age'].median()))
print("25% " + str(patients['age'].quantile(0.25)))
print("75% " + str(patients['age'].quantile(0.75)))

count = 0
for i in range(len(patients)):
    #print(patients.loc[i, "id"])
    if patients.loc[i, "id"] in clinical_data["patient_id"].values:
        count = count + 1

print("Percentage of linked patient " + str(round(count*100/patients["id"].count(),2)))

c_index = read_codes.index[read_codes['description'] == "Diabetes mellitus"].tolist()[0]
r_code = read_codes.loc[c_index, "read_code"]

female = patients[patients.gender == 1]
female_linked = pd.DataFrame(columns = ["date_recorded", "patient_id", "read_code"])


for ind in female.index: 
     #print(female['id'][ind]) 
     if female['id'][ind] in clinical_data["patient_id"].values:
        ytr = clinical_data.loc[clinical_data["patient_id"] == female['id'][ind]  ]
        female_linked = female_linked.append(ytr)
print("No. of females with diabetes " + str(female_linked[female_linked.read_code == r_code]["read_code"].count()))

    

pat_over_fifty = patients[patients.age > 50]
pat_over_fifty_linked = pd.DataFrame(columns = ["date_recorded", "patient_id", "read_code"])

c_index = read_codes.index[read_codes['description'] == "Acute myocardial infarction"].tolist()[0]
r_code = read_codes.loc[c_index, "read_code"]

for ind in pat_over_fifty.index: 
     #print(female['id'][ind]) 
     if pat_over_fifty['id'][ind] in clinical_data["patient_id"].values:
        ytr = clinical_data.loc[clinical_data["patient_id"] == pat_over_fifty['id'][ind]  ]
        pat_over_fifty_linked = pat_over_fifty_linked.append(ytr)

print("No. of patients with Acute myocardial infarction " + str(pat_over_fifty_linked[pat_over_fifty_linked.read_code == r_code]["read_code"].count()))

#Acute myocardial infarction




