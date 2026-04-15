from ehrql import codelist_from_csv

# import codelists from csv ---
dm_cod = codelist_from_csv(
  "codelists/nhsd-primary-care-domain-refsets-dm_cod.csv" ,
  column="code"
)

dmres_cod = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-dmres_cod.csv",
    column = "code"
)
