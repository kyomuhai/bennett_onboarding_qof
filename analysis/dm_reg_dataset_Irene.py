from ehrql import create_dataset, show
from ehrql.tables.tpp import patients, practice_registrations, clinical_events, medications
from codelists_import import dm_cod, dmres_cod


index_date = "2024-03-31"


#patient registered on index date
has_registration = (
    practice_registrations
    .exists_for_patient_on(index_date)
)
#show(has_registration)


###
# Define Rule 1 ---
###

# a) Patient has diabetes diagnosis in the patient record 
# up to and including the achievement date

#identify prior clinical events up to index date

prior_clinical_events = (
    clinical_events.where(clinical_events.date <= index_date)
)

latest_diagnosis_date = (
    prior_clinical_events
    .where(prior_clinical_events.snomedct_code.is_in(dm_cod))
    .sort_by(prior_clinical_events.date)
    .last_for_patient()
    .date
)

#show(latest_diagnosis_date, dm_reg_r1_a)
# b) Latest diabetes diagnosis is not followed 
# by a diabetes resolved code.
latest_resloved_date = (
    prior_clinical_events
    .where(prior_clinical_events.snomedct_code.is_in(dmres_cod))
    .sort_by(prior_clinical_events.date)
    .last_for_patient()
    .date
)

dm_reg_r1 = ( 
    latest_diagnosis_date.is_not_null() 
    & (latest_resloved_date.is_null() 
       | (latest_diagnosis_date > latest_resloved_date))
    )

#show(latest_diagnosis_date, dm_reg_r1_a, latest_resloved_date, dm_reg_r1_b)


###
# Define Rule 2 ---
###

# a) Reject patients passed to this rule who are aged under 17 years old 
# on the achievement date. Select the remaining patients
dm_reg_r2_a = (
    patients.age_on(index_date) >= 17
)

#b) patient is alive

dm_reg_r2_b = patients.is_alive_on(index_date)
# combine rule 2: has registration, is 17 and over, is alive
dm_reg_r2 = has_registration & dm_reg_r2_a & dm_reg_r2_b


###
# Create dataset based on rule 1 & 2---
###

dataset = create_dataset()
dataset.define_population(dm_reg_r1 & dm_reg_r2)

###
# define dataset columns---
###

dataset.dmlat_dat = latest_diagnosis_date
dataset.dmres_dat = latest_resloved_date
dataset.pat_age = patients.age_on(index_date)

show(dataset)

