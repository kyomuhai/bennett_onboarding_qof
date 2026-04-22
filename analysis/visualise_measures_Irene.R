 # to run R: opensafely exec r R

#load packages
library("tidyverse")
library("here")
library("readr")
library("scales")
library("patchwork")


#create a directory for the visualizations:
dir.create(here("output", "figures"), recursive = TRUE)


# read compressed CSV output from ehrql
dm_measure_age_group <- read_csv("output/dm017/dm017_register_by_age.csv.gz")
dm_measure_age_group

dm_measure_sex <- read_csv("output/dm017/dm017_register_by_sex.csv.gz")
dm_measure_sex

dm_measure_prevalence <- read_csv("output/dm017/dm017_register_prevalence.csv.gz")
dm_measure_prevalence

####
#### Age plot**********************************************
####
#check min and max for y-axis
max(dm_measure_age_group$numerator)
min(dm_measure_age_group$numerator)
table(dm_measure_age_group$interval_start)

age_plot <- ggplot(dm_measure_age_group, aes(interval_start, numerator, color = age_band)) +
geom_line() +
geom_point() +
scale_x_date(
  date_breaks = "1 month",
  labels = label_date_short()
) +
scale_y_continuous(
  limits=(c(10,220))
) +
labs(
  x = " ",
  y = "Count",
  title = "Diabetes Mellitus Register by Age, (DM017)"
) +
theme_light()
ggsave("output/figures/age_plot.png", age_plot)


#sense checks
dm_measure_age_group_80plus <- dm_measure_age_group %>%
  filter(age_band == "80+")
  dm_measure_age_group_80plus


####
#### Sex plot**********************************************
####
#check min and max for y-axis
max(dm_measure_sex$numerator)
min(dm_measure_sex$numerator)

sex_plot <- ggplot(dm_measure_sex, aes(interval_start, numerator, color = sex)) +
geom_line() +
geom_point() +
scale_x_date(
  date_breaks = "1 month",
  labels = label_date_short()
) +
scale_y_continuous(
  limits=(c(10,220))
) +
labs(
  x = " ",
  y = "Count",
  title = "Diabetes Mellitus Register by Sex, (DM017)"
) +
theme_classic()
ggsave("output/figures/sex_plot.png", sex_plot)

#sense checks
dm_measure_sex_female <- dm_measure_sex %>%
  filter(sex == "female")
 dm_measure_sex_female
nrow(dm_measure_sex_female)


####
#### Sex plot**********************************************
####
dm_measure_prevalence
prev_plot <- ggplot(dm_measure_prevalence, aes(interval_start, ratio)) +
geom_line() +
geom_point() +
scale_x_date(
  date_breaks = "1 month",
  labels = label_date_short()
) +
scale_y_continuous(
  limits=(c(0,1)),
  labels = percent_format(accuracy = 1)
) +
labs(
  x = " ",
  y = "Prevalence",
  title = "Diabetes Mellitus Register Prevalence, (DM017/Total Population)"
) +
theme_light()
ggsave("output/figures/prev_plot.png", prev_plot)



# Combine plots
measures_plot <- (age_plot / sex_plot / prev_plot) +
    plot_annotation(tag_levels = 'A')

ggsave("output/figures/combined_plot.png", measures_plot)
