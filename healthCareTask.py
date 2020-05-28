# -*- coding: utf-8 -*-
"""
Created on Wed May 27 19:07:06 2020

@author: z02511mm
"""
import pandas as pd
from datetime import datetime
from datetime import date
from scipy.stats import iqr

# Reading files
read_codes = pd.read_csv('test_data/read_codes.txt', skiprows=[0], sep="\t",header=None)
read_codes.columns = ["read_code", "description"]

clinical_data = pd.read_csv('test_data/clinical_data.txt', skiprows=[0], sep="\t",header=None)
clinical_data.columns = ["date_recorded", "patient_id", "read_code"]

patients = pd.read_csv('test_data/patients.txt', skiprows=[0], sep="\t",header=None)
patients.columns = ["date_extracted", "date_of_birth", "full_name", "gender", "id"]

# Ques 1
count_male = patients.loc[patients.gender == 2, "gender"].count()
print ("Number of male patient " + str(count_male))

# Ques 2
pt_date_extracted = patients.loc[patients.date_extracted > "2015-01-01", "date_extracted"].count()
print("Patient extracted after 01/01/2015 " + str(pt_date_extracted))
               
# Ques 3
def calculate_age(born):
    born = datetime.strptime(born, "%d/%m/%Y").date()
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
patients['age'] = patients['date_of_birth'].apply(calculate_age)
print("Min Age " + str(patients['age'].min()))
print("Max Age " + str(patients['age'].max()))
print("Median Age " + str(patients['age'].median()))
#print("25% " + str(patients['age'].quantile(0.25)))
#print("75% " + str(patients['age'].quantile(0.75)))
print("Inter Quartile Range of Age " + str(iqr(patients['age'])))

# Ques 4
count = 0
for i in range(len(patients)):
    #print(patients.loc[i, "id"])
    if patients.loc[i, "id"] in clinical_data["patient_id"].values:
        count = count + 1

print("Percentage of linked patient " + str(round(count*100/patients["id"].count(),2)) + " %")

# Ques 5

pt_date_recorded = clinical_data[clinical_data["date_recorded"] > "02/03/1980"]
freq3 = pt_date_recorded["patient_id"].value_counts().to_frame()
freq3.columns = ["num_records"]
freq3["patient_id"] = freq3.index
freq3 = freq3[['patient_id', 'num_records']]

freq3.to_csv('num_clin_data_records.csv', index=False)

# Ques 6 (i)

#c_index = read_codes.index[read_codes['description'] == "Diabetes mellitus"].tolist()[0]
#r_code = read_codes.loc[c_index, "read_code"]

code_table = read_codes.loc[read_codes.description.str.contains("mellitus", na=False)]

female = patients[patients.gender == 1]
female_linked = pd.DataFrame(columns = ["date_recorded", "patient_id", "read_code"])
d_female_linked = pd.DataFrame(columns = ["date_recorded", "patient_id", "read_code"])


for ind in female.index: 
     #print(female['id'][ind]) 
     if female['id'][ind] in clinical_data["patient_id"].values:
        f_linked = clinical_data.loc[clinical_data["patient_id"] == female['id'][ind]  ]
        female_linked = female_linked.append(f_linked)
#print("No. of females with diabetes " + str(female_linked[female_linked.read_code == r_code]["read_code"].count()))

for ind in code_table.index: 
     #print(code_table['read_code'][ind]) 
     d_female_linked_data= female_linked[female_linked.read_code == code_table['read_code'][ind]]
     d_female_linked = d_female_linked.append(d_female_linked_data)
  
female_mellitus = d_female_linked["patient_id"].value_counts()
print("Females with diabetes mellitus " + str(female_mellitus.size) )
    
# Ques 6 (ii)

m_code_table = read_codes.loc[read_codes.description.str.contains("myocardial infarction", na=False)]
pat_over_fifty = patients[patients.age > 50]
pat_over_fifty_linked = pd.DataFrame(columns = ["date_recorded", "patient_id", "read_code"])
m_pat_over_fifty_linked = pd.DataFrame(columns = ["date_recorded", "patient_id", "read_code"])

#c_index = read_codes.index[read_codes['description'] == "Acute myocardial infarction"].tolist()[0]
#r_code = read_codes.loc[c_index, "read_code"]

for ind in pat_over_fifty.index: 
     #print(female['id'][ind]) 
     if pat_over_fifty['id'][ind] in clinical_data["patient_id"].values:
        ytr = clinical_data.loc[clinical_data["patient_id"] == pat_over_fifty['id'][ind]  ]
        pat_over_fifty_linked = pat_over_fifty_linked.append(ytr)

for ind in m_code_table.index: 
     #print(m_code_table['read_code'][ind]) 
     m_pat_over_fifty_linked_data= pat_over_fifty_linked[pat_over_fifty_linked.read_code == m_code_table['read_code'][ind]]
     m_pat_over_fifty_linked = m_pat_over_fifty_linked.append(m_pat_over_fifty_linked_data)



print("No. of patients with Acute myocardial infarction " + str(m_pat_over_fifty_linked["read_code"].size))


# Ques 6 (iii)



# for ind in patients.index: 
#      #print(female['id'][ind]) 
#      if patients['id'][ind] in clinical_data["patient_id"].values:
#         ytr = clinical_data.loc[clinical_data["patient_id"] == patients['id'][ind]  ]
#         patients_linked = patients_linked.append(ytr)

patients_linked = pd.DataFrame(columns = ["date_recorded", "patient_id", "read_code"])
p_code_table = read_codes.loc[read_codes.description.str.contains("Amoxicillin", na=False)]

#c_index1 = read_codes.index[read_codes['description'] == "Amoxicillin 250mg capsule"].tolist()[0]
#c_index2 = read_codes.index[read_codes['description'] == "Amoxicillin 500mg capsule"].tolist()[0]
#r_code1 = read_codes.loc[c_index1, "read_code"]
#r_code2 = read_codes.loc[c_index2, "read_code"]

#record1 = clinical_data[clinical_data.read_code == r_code1]
#record2 = clinical_data[clinical_data.read_code == r_code2]

for ind in p_code_table.index: 
     #print(p_code_table['read_code'][ind]) 
     d_patients_linked= clinical_data[clinical_data.read_code == p_code_table['read_code'][ind]]
     patients_linked = patients_linked.append(d_patients_linked)

group_count = patients_linked["patient_id"].value_counts()
#freq1 = record1["patient_id"].value_counts()
#freq2 = record2["patient_id"].value_counts()

print("Number of patients taking atleast 2 doses of Amoxicillin " + str(group_count.where(group_count>=2).count()))










