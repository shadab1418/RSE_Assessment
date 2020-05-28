# -*- coding: utf-8 -*-
"""
Created on Wed May 27 19:07:06 2020

@author: z02511mm
"""
import pandas as pd
from datetime import datetime
from datetime import date
from scipy.stats import iqr

# Reading data files
read_codes = pd.read_csv('test_data/read_codes.txt', skiprows=[0], sep="\t",header=None)
read_codes.columns = ["read_code", "description"]

clinical_data = pd.read_csv('test_data/clinical_data.txt', skiprows=[0], sep="\t",header=None)
clinical_data.columns = ["date_recorded", "patient_id", "read_code"]

patients = pd.read_csv('test_data/patients.txt', skiprows=[0], sep="\t",header=None)
patients.columns = ["date_extracted", "date_of_birth", "full_name", "gender", "id"]

# Ques 1
#Num of male patients
count_male = patients.loc[patients.gender == 2, "gender"].count()
print ("Number of male patient - " + str(count_male))

# Ques 2
#Patient extracted after 2015-01-01
pt_date_extracted = patients.loc[patients.date_extracted > "2015-01-01", "date_extracted"].count()
print("Patient extracted after 01/01/2015 - " + str(pt_date_extracted))
               
# Ques 3

#calculate age of patients
def calculate_age(born):
    born = datetime.strptime(born, "%d/%m/%Y").date()
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

patients['age'] = patients['date_of_birth'].apply(calculate_age)

print("Min Age - " + str(patients['age'].min()))
print("Max Age - " + str(patients['age'].max()))
print("Median Age - " + str(patients['age'].median()))
print("Inter Quartile Range of Age - " + str(iqr(patients['age'])))

# Ques 4
#percentage of linked patient
count = 0
for i in range(len(patients)):
    #print(patients.loc[i, "id"])
    if patients.loc[i, "id"] in clinical_data["patient_id"].values:
        count = count + 1

print("Percentage of linked patient - " + str(round(count*100/patients["id"].count(),2)) + " %")

# Ques 5

#patients with date recorded after 02/03/1980
pt_date_recorded = clinical_data[clinical_data["date_recorded"] > "02/03/1980"]
pat_count = pt_date_recorded["patient_id"].value_counts().to_frame()
pat_count.columns = ["num_records"]
pat_count["patient_id"] = pat_count.index
pat_count = pat_count[['patient_id', 'num_records']]

#write to csv file
pat_count.to_csv('num_clin_data_records.csv', index=False)

# Ques 6 (i)
#There were multiple diabetes millitus, The question does not specify which one so i have checked all occurances

code_table = read_codes.loc[read_codes.description.str.contains("mellitus", na=False)]

# female patients
female = patients[patients.gender == 1]
female_linked = pd.DataFrame(columns = ["date_recorded", "patient_id", "read_code"])
d_female_linked = pd.DataFrame(columns = ["date_recorded", "patient_id", "read_code"])

#female linked patients
for ind in female.index: 
     #print(female['id'][ind]) 
     if female['id'][ind] in clinical_data["patient_id"].values:
        f_linked = clinical_data.loc[clinical_data["patient_id"] == female['id'][ind]  ]
        female_linked = female_linked.append(f_linked)
        
#find female linked patients with diabetes millitus
for ind in code_table.index: 
     #print(code_table['read_code'][ind]) 
     d_female_linked_data= female_linked[female_linked.read_code == code_table['read_code'][ind]]
     d_female_linked = d_female_linked.append(d_female_linked_data)
  
female_mellitus = d_female_linked["patient_id"].value_counts()
print("Females with diabetes mellitus - " + str(female_mellitus.size) )
    
# Ques 6 (ii)
#There were multiple myocardial infarction.The question does not specify which one so i have checked all occurances

m_code_table = read_codes.loc[read_codes.description.str.contains("myocardial infarction", na=False)]

#patients over fifty
pat_over_fifty = patients[patients.age > 50]
pat_over_fifty_linked = pd.DataFrame(columns = ["date_recorded", "patient_id", "read_code"])
m_pat_over_fifty_linked = pd.DataFrame(columns = ["date_recorded", "patient_id", "read_code"])

#linked patients over fifty
for ind in pat_over_fifty.index: 
     #print(female['id'][ind]) 
     if pat_over_fifty['id'][ind] in clinical_data["patient_id"].values:
        ytr = clinical_data.loc[clinical_data["patient_id"] == pat_over_fifty['id'][ind]  ]
        pat_over_fifty_linked = pat_over_fifty_linked.append(ytr)
        
#find linked patients over fifty with myocardial infarction
for ind in m_code_table.index: 
     #print(m_code_table['read_code'][ind]) 
     m_pat_over_fifty_linked_data= pat_over_fifty_linked[pat_over_fifty_linked.read_code == m_code_table['read_code'][ind]]
     m_pat_over_fifty_linked = m_pat_over_fifty_linked.append(m_pat_over_fifty_linked_data)

print("No. of patients with Acute myocardial infarction - " + str(m_pat_over_fifty_linked["read_code"].size))


# Ques 6 (iii)

#Amoxicillin code
p_code_table = read_codes.loc[read_codes.description.str.contains("Amoxicillin", na=False)]

patients_linked = pd.DataFrame(columns = ["date_recorded", "patient_id", "read_code"])

#find patients taking Amoxicillin
for ind in p_code_table.index: 
     #print(p_code_table['read_code'][ind]) 
     d_patients_linked= clinical_data[clinical_data.read_code == p_code_table['read_code'][ind]]
     patients_linked = patients_linked.append(d_patients_linked)

group_count = patients_linked["patient_id"].value_counts()
#find patients taking at least 2 or more doses of Amoxcillin
print("Number of patients taking atleast 2 doses of Amoxicillin - " + str(group_count.where(group_count>=2).count()))










