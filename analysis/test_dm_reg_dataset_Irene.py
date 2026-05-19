from ehrql import days
from datetime import date
from dm_reg_dataset_Irene import dataset 

index_date = "2024-03-31"

#assign dm_code and dm_resolved_code
dm_code = "111552007"
dm_resolved_code = "315051004"


#define cases that are expected and not expected in the data based on teh rules in task 1
test_data = {
# not expected: registration date out of range
1:{
    "patients": {"date_of_birth": date(1970,1,1)},
    "practice_registrations": [{
        "start_date": (index_date + days(20)),
        "end_date": (index_date + days(200))
        }],
        "clinical_events": [
            {"date": (index_date + days(50)), "snomedct_code": dm_code}
        ], 
        "expected_in_population": False
}, 
# not expected: has no diabetes diagnosis in patient record
2: {
    "patients": {"date_of_birth": date(1970,1,1)},
    "practice_registrations": [{
        "start_date": (index_date - days(500)),
        "end_date": (index_date + days(200))
        }],
        "clinical_events": [], 
        "expected_in_population": False
},
# not expected: is under 17
3: {
        "patients": {"date_of_birth": date(2021, 1, 1)},
        "practice_registrations": [{
            "start_date": (index_date - days(200)), 
            "end_date": (index_date + days(100))}],
        "clinical_events": [],
        "expected_in_population": False
    },

# not expected: diabetes diagnosis out of date range
4:{
    "patients": {"date_of_birth": date(1970,1,1)},
    "practice_registrations": [{
        "start_date": (index_date - days(800)),
        "end_date": (index_date + days(200))}],
        "clinical_events": [
            {"date": (index_date + days(100)), "snomedct_code": dm_code}
        ], 
        "expected_in_population": False
} , 
# not expected: dm resolved date is after dm diagnosis
5:{
    "patients": {"date_of_birth": date(1970,1,1)},
    "practice_registrations": [{
        "start_date": (index_date - days(800)),
        "end_date": (index_date + days(200))}],
        "clinical_events": [
            {"date": (index_date - days(100)), "snomedct_code": dm_code}, 
            {"date": (index_date - days(30)), "snomedct_code": dm_resolved_code}, 
        ], 
        "expected_in_population": False
},
# expected: all rules are met, with missing dm_resolved date 
6:{
    "patients": {"date_of_birth": date(1970,1,1)},
    "practice_registrations": [{
        "start_date": (index_date - days(800)),
        "end_date": (index_date + days(200))}],
        "clinical_events": [
            {"date": (index_date - days(100)), "snomedct_code": dm_code}
        ], 
        "expected_in_population": True, 
        "expected_columns": {
            "pat_age": 54,
            "dmlat_dat": (index_date - days(100)),
            "dmres_dat": None
        }
},
# expected: all rules met, with last dm_resolved date < last dem diagnosis date
7:{
    "patients": {"date_of_birth": date(1970,1,1)},
    "practice_registrations": [{
        "start_date": (index_date - days(800)),
        "end_date": (index_date + days(200))}],
        "clinical_events": [
            {"date": (index_date - days(100)), "snomedct_code": dm_code},
            {"date": (index_date - days(200)), "snomedct_code": dm_resolved_code}
        ], 
        "expected_in_population": True, 
        "expected_columns": {
            "pat_age": 54,
            "dmlat_dat": (index_date - days(100)),
            "dmres_dat": (index_date - days(200))
        }
}
}