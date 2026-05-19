from ehrql import INTERVAL, create_measures, months, case, when, show
from ehrql.tables.core import practice_registrations, patients, clinical_events
from codelists_import import *

measures = create_measures()


#Events up to end of month interval
events_in_interval = clinical_events.where(clinical_events.date <= INTERVAL.end_date)


# patient registration up to end of interval (exclude those whose registration ended before interval end-date)
has_registration = (
    practice_registrations
    .where(practice_registrations.start_date <= INTERVAL.end_date)
    .except_where(practice_registrations.end_date < INTERVAL.end_date)
    .exists_for_patient()
)


# Has unresolved diabetes diagnosis at the end of month interval
latest_disgnosis_date = (
    events_in_interval
    .where(events_in_interval.snomedct_code.is_in(dm_cod))
    .sort_by(events_in_interval.date)
    .last_for_patient()
    .date
)

latest_resolved_date = (
    events_in_interval
    .where(events_in_interval.snomedct_code.is_in(dmres_cod))
    .sort_by(events_in_interval.date)
    .last_for_patient()
    .date
)

has_unresolved_diagnosis = latest_disgnosis_date.is_not_null() & (
    latest_resolved_date.is_null()
    | (latest_disgnosis_date > latest_resolved_date)
)

# is 17 years at end of interval 
aged_17_or_more = patients.age_on(INTERVAL.end_date) >= 17

#is alive at end of interval
is_alive = patients.is_alive_on(INTERVAL.end_date)


# DM017 registration eligibility in interval;
dm017_reg = ( 
    aged_17_or_more & is_alive & has_registration & has_unresolved_diagnosis
    )

# sex variable for patients
has_recorded_sex = patients.sex.is_not_null()

# age variable for patients
age = patients.age_on(INTERVAL.start_date)
age_band = case(
    when((age >= 0) & (age < 20)).then("0-19"),
    when((age >= 20) & (age < 40)).then("20-39"),
    when((age >= 40) & (age < 60)).then("40-59"),
    when((age >= 60) & (age < 80)).then("60-79"),
    when(age >= 80).then("80+"),
)

# Measures
# Proportion of patients on dm017_reg each month by sex
measures.define_measure(
    name = "dm017_register_by_sex",
    numerator = dm017_reg,
    denominator = dm017_reg & has_recorded_sex,
    group_by = {"sex": patients.sex},
    intervals= months(12).starting_on("2024-01-01"),
)

# Proportion patients on dm017_reg each month by age
measures.define_measure(
    name="dm017_register_by_age",
    numerator=dm017_reg,
    denominator=dm017_reg,
    group_by={"age_band": age_band},
    intervals=months(12).starting_on("2024-01-01"),
)

# Prevalence: % of dm017_reg patients out of population (>=17, alive & registered)
measures.define_measure(
    name="dm017_register_prevalence",
    numerator=dm017_reg,
    denominator=aged_17_or_more & is_alive & has_registration,
    intervals=months(12).starting_on("2024-01-01"),
)