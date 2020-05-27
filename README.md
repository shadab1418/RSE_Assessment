# RSE Assessment

## Data files

You are provided with 3 files which are described below. These are located in the `test_data` directory in this repository. The first two files contain simulated data based on a real data set.

Use these files and your choice of Python or R to answer the Assessment Questions below 

### File 1: Patient demographics (patients.txt)
| Field | Description | Data Type
|-|-|-|
| unique_id	| Unique patient ID	| Number |
| date_of_birth	| Date of birth | Date (in d/m/y format) |
| gender | Gender of patient | List (1=Female, 2=Male) |
| date_extracted | Date extracted from medical system | Date (in Y-m-d format) |

### File 2: Linked clinical data (clinical_data.txt)
| Field | Description | Data Type
|-|-|-|
| unique_id	| Unique patient ID | Number |
| read_code	| READ version 3 code | List (links to clinical concept terms) |
| date_recorded	| Date recorded	| Date (in m/d/y format) | 

### File 3: Clinical concept terms* (read_codes.txt)
| Field | Description | Data Type
|-|-|-|
| read_code	| READ version 3 code | Character
| description | Description of clinical concept	| Character

<verbatim>* this file contains a subset of the complete READ code set</verbatim>

## Assessment questions
It should take between 30 minutes and an hour to answer the questions. 

Please document your code files with question numbers so we can refer back to them. 

To share your results please create your own github repository containing your generated data and code files, then share this with **@rcfree**.

1.	How many male patients are present in the patient demographics?

2.	How many patients were extracted after 01/01/2015 

3.	Calculate the age in years of patients (using patient date of birth and today’s date) and determine the min, max, median and interquartile range.

4.	What percentage of patients have linked clinical data?

5.	Produce a CSV file named `num_clin_data_records.csv` with the headings `patient_id` and `num_records` containing the number of clinical data records present per linked patient which were recorded after 12/03/1980. 

6.	Using the files provided work out:
    1. How many females have diabetes mellitus
    2. How many patients >50 years old have had at least one Acute myocardial infarction
    3. How many patients have had at least 2 courses of amoxiciilin