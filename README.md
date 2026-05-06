---
editor_options: 
  markdown: 
    wrap: 72
---

# Analysis of Traffic Crash Data Using FARS Datasets

## Contributors

-   Ellen Harris (ellen4)
-   Marco Soto (masoto2)

## Summary

This project presents a comprehensive analysis of traffic crash fatality
data using three datasets from the Fatality Analysis Reporting System
(FARS): ACC_AUX, PER_AUX, and VEH_AUX. FARS, maintained by the National
Highway Traffic Safety Administration (NHTSA), provides detailed records
of all motor vehicle crashes in the United States that result in at
least one fatality. The primary motivation for this analysis is the
persistent public health burden of traffic fatalities as crashes remain
one of the leading causes of preventable death in the U.S. and the need
to identify actionable, data driven insights that can guide safety
interventions and policy decisions.

The project began with data cleaning and integration across the three
FARS auxiliary files, which capture crash-level, person-level, and
vehicle-level attributes respectively. These were merged into a unified
analytical dataset to enable cross domain analysis. The resulting
dataset covers **37,769 fatal crashes** in 2023, representing **41,025
total fatalities** and an average of 1.09 fatalities per crash. Of
these, **2,641 crashes (7.0%)** involved multiple fatalities,
representing the most severe outcomes and a key target for predictive
modeling.

Exploratory analysis revealed several notable patterns. A majority of
fatal crashes (**54.2%**) occurred at night, and **58.0%** occurred on
weekends, consistent with prior research linking reduced visibility and
increased recreational driving to elevated crash risk. Geographically,
urban areas accounted for a larger share of crashes (22,516 vs. 15,064
in rural areas), though rural crashes are often associated with higher
severity due to longer emergency response times and higher speeds.

Impairment factors were prominent across the dataset. Alcohol
involvement was present in **8,019 crashes**, representing over half of
crashes where impairment status was known. Speeding was implicated in
**28.2%** of all fatal crashes (10,657 incidents), making it the single
most common contributing behavior. Distracted driving and drowsy
driving, though less frequent at 3,024 and 568 crashes respectively,
represent categories likely undercounted due to reporting limitations.
Vulnerable road users such as pedestrians (7,323 crashes), motorcyclists
(6,274), and pedalcyclists (1,173), collectively accounted for roughly
39% of fatal crash involvements, underscoring the outsized risk faced by
non-occupant road users.

Road geometry also played a role as **roadway departures** were the most
common crash type (17,542 crashes), while intersections and interstate
highways accounted for 9,781 and 4,692 crashes respectively.

To address the predictive research question, a Logistic Regression model
was trained to classify crashes as single- vs. multi-fatality events.
The model achieved a **ROC-AUC of 0.691**, indicating moderate
discriminative ability given the class imbalance (only 7%
multi-fatality). Among the strongest positive predictors were
**wrong-way driving** (OR = 1.21), **speeding** (OR = 1.19), and **young
driver age (15–19)** (OR = 1.12). Notably, crashes involving
**pedestrians** (OR = 0.55), **motorcyclists** (OR = 0.70), and
**pedalcyclists** (OR = 0.74) were associated with *lower* odds of
multi-fatality outcomes, reflecting that these crashes, while fatal,
typically involve a single vulnerable individual rather than multiple
vehicle occupants.

Taken together, these findings highlight speeding, alcohol, nighttime
conditions, and roadway departures as priority targets for traffic
safety intervention, while the predictive model demonstrates the
feasibility of using crash-level features to identify high risk
scenarios before or immediately after a crash occurs.

## Data Profile

Our project uses three datasets from the Fatality Analysis System
(FARS): ACC_AUX, PER_AUX, and VEH_AUX. These three datasets all relate
to fatal traffic crashes in the United States, but each one looks at a
different level of detail. Together, they will allow us to see a more
complete picture of what occurs during a crash.

The ACC_AUX file is a structured dataset that has information at the
crash level. Each row is there to represent a single crash and has
general details about the location and time of the crash. This dataset
is critical because it serves as the base dataset for this project.

The PER_AUX file is a structured dataset that contains information at
the person level. Every row is there to represent a person involved in a
crash, like the passenger or driver. Because in some cases multiple
people can be involved in a crash, there are multiple rows that have the
same ST_CASE value. This dataset gives us a better understanding of how
many individuals were involved and provides more details about
individuals in the crash.

The VEH_AUX file is a structured dataset that contains vehicle-level
data. Each row represents a vehicle that was involved in a crash. This
is similar to the person dataset because multiple vehicles can be a part
of one crash. This dataset gives an additional layer of detail by
showing us how many vehicles were involved.

These three datasets are connected using the ST_CASE, which is the
unique crash ID. This allows it to be possible to combine the datasets
later. The raw data was stored as a zip file in the data/raw folder, and
all the cleaned and processed files are saved in the data/processed
folder.

The FARS dataset is a publicly available federal dataset maintained by
the National Highway Traffic Safety Administration and published under
the U.S. Department of Transportation's open data policy. As a
government-produced dataset funded by taxpayers and released for public
research use, there are no licensing restrictions on its use for
academic analysis. No data use agreement, institutional review board
approval, or special access credentials were required to download or
analyze the 2023 national files. However, the absence of formal legal
restrictions does not eliminate the need for ethical consideration in
how the data is used, interpreted, and communicated.

Although FARS is a public dataset, it contains detailed records of real
fatal crashes involving real people who died on U.S. roads. Each record
corresponds to an actual fatality, and the dataset includes variables
such as state, county, crash date and time, road type, and demographic
attributes of the persons involved. While the dataset does not include
direct identifiers such as names or social security numbers, the
combination of geographic, time, and demographic variables could in
principle allow a determined user to re-identify individuals involved in
specific crashes, particularly in low population rural areas where a
fatal crash on a specific date and road type may be uniquely
identifiable through public records or news reporting.

Crash data analysis carries a risk of stigmatizing particular groups if
findings are reported without appropriate context. For example, findings
that younger drivers (ages 15 to 24) or older drivers (65+) are
disproportionately involved in fatal crashes could be used to support
discriminatory licensing policies if presented without acknowledging the
role of exposure, infrastructure design, and socioeconomic factors.
Similarly, the strong association between alcohol involvement and fatal
crashes reflects a well documented behavioral pattern, but framing this
purely as an individual failing ignores systemic factors such as lack of
public transit, inadequate enforcement, and the marketing practices of
the alcohol industry. Throughout this project, care was taken to present
findings descriptively and to note the limitations of attributing
causality to any single variable.

The FARS dataset is well suited to the research questions guiding this
project. FARS provides complete national coverage without the sampling
bias that would affect a survey-based dataset. The crash-level,
person-level, and vehicle-level structure of the auxiliary files
directly supports analysis of driver, vehicle, and environmental factors
simultaneously, which is central to our research questions. The binary
and categorical variables available in FARS, covering impairment, road
type, time of day, geography, and crash type, map cleanly onto the
predictive modeling framework used to address the question of whether
fatality likelihood can be estimated from observable crash
characteristics. The primary limitation is that FARS captures only
crashes that resulted in at least one fatality, meaning it cannot be
used to study the broader universe of non-fatal crashes or to estimate
absolute crash risk without denominators such as vehicle miles traveled.

## Data Quality

At first glance, the raw dataset had multiple issues that needed to be
fixed before the data was usable. The first problem that was noticed was
that the column names were not consistent. Multiple column names had an
extra space or were formatted in a different ways, which could create
problems when trying to combine the datasets. If you do not have
consistent column names, it becomes much harder to match the same fields
across datasets, which has the possibility of causing errors during the
merge.

Another major problem was with the ST_CASE column. This was identified
as the most important column because it is used to connect all three of
the datasets. There was values that were not stored as numbers, and the
same values that were not there at all. If this column is not clean, the
dataset would not merge correctly, which would give us wrong final
results. Because ST_CASE was the main identifier for every crash, issues
within this column would directly affect the entire project.

There were also duplicate rows in the dataset. Keeping these duplicate
rows would have led to incorrect counts and made it seem like there are
more crashes, people, or vehicles then there really are. Those rows
would also affect the analysis that was done later and make the results
less reliable. Removing these duplicates was necessary to make sure
every record represented the real and unique data. Missing values were
also a problem across different columns. While not all of the missing
values needed to be removed, it was very crucial that the key fields
like ST_CASE were valid. Any row that was missing a usable crash ID
could not be connected to other datasets and, therefore, could not be
used in the final dataset.

Another issue was incorrect data types. Some values that should have
been numbers were actually stored as text, which would create serious
problems when trying to perform grouping or counting operations. Since
our project needs to count people and vehicles per crash, these data
type issues had to be fixed. There was also some cases where records
could not be matched across the datasets because of missing or invalid
ST_CASE values. Those records had to be removed because they could not
be reliably used in the integration process.

In addition to those issues, the structure of the datasets also had some
issues. The ACC_AUX dataset is organized at the crash-level, while
PER_AUX and the VEH_AUX datasets are organized at the person and
vehicle-levels. This means that a singular crash could have multiple
related rows in the other datasets. Because of this, it would not be
possible to directly merge all three of the datasets without first
checking to make sure the data is properly prepared. If this was not
handled correctly, it could cause duplicate information or incorrect
totals in the final dataset.

Another issue was checking to make sure the data was usable after
cleaning. Any type of issue, even small problems, like an extra space in
column names or incorrect data types, could create errors in the code or
lead to incorrect results. Another need was to balance cleaning the data
with keeping enough useful information. While some information needed to
be removed, like rows with missing or invalid ST_CASE values, removing
too much of the data could reduce the amount of information that would
be used for analysis. This was important so we could only remove records
that could not be used and keep as much useful data as possible.

All these issues show that data quality is not just about trying to fix
obvious problems. It also involves checking to make sure that the data
is consistent, usable, and structured in a way that supports the overall
purpose of this project. Taking the time to address these issues allowed
me to make sure that the final dataset would be accurate, reliable, and
ready for analysis.

## Data Cleaning

To correct all the issues that were found in the raw datasets, several
cleaning steps were performed using a Python script. These steps were
based on the problems identified earlier in the data quality section,
and they were necessary to make sure they could correctly be merged and
used for later analysis.

The first step was to clean the column names. Many column names had an
extra space or inconsistent formatting, which could create problems when
trying to match the columns across datasets. To correct this issue, all
the column names were stripped of any extra spaces and then converted to
uppercase. This allowed the datasets to be consistent and easier to work
with, especially while merging.

The next step was to remove the duplicate rows from each dataset. This
step directly corrected the issue of repeated records that could have
caused incorrect counts. If the duplicates were to remain in the data,
it would make it look like there were more crashes, people, or vehicles
then there actually was. Getting rid of these duplicates made sure that
each row represented unique information and improved the overall
accuracy of the dataset.

The next step was to clean the ST_CASE column. This column is the key
value used to connect all three of the datasets, so it had to be
consistent and valid. I started by converting all the ST_CASE values to
a numeric format. Any values that could not be converted or were missing
were removed from the dataset. Next, the column was converted to
integers to make sure there was perfect consistency across all datasets.
Fixing this issue was particularly important because any issues in
ST_CASE would prevent the dataset from being merged correctly and
cleanly. Any rows that had invalid or missing ST_CASE values were also
removed. Those rows would not be able to link to the other datasets, so
keeping them would not be doing any benefit to the final dataset.

Since the PER_AUX and VEH_AUX datasets are at the person and vehicle
levels, they have multiple rows for each crash. To deal with this, both
of the datasets were grouped by the ST_CASE to gather a count of how
many people and vehicles were involved in each crash. This made summary
datasets that could be merged together with the crash-level dataset
without making any duplicate rows. This was important because it dealt
with the structural differences between the datasets. Without grouping
and merging the datasets directly would have given results with repeated
crash records and incorrect totals. Because we summarized the data
first, the final dataset remained at the crash level while still having
useful information about people and vehicles.

All of these cleaning steps were done in a single Python script, which
makes the process reproducible. That means that my steps could be done
again if needed, and the results would remain the same. The cleaned
datasets and summary files were saved in the data/processed folder so
they could be used for in the next stage of our project.

Every cleaning step directly addressed the specific problem that was
found in the data. Cleaning column names fixed formatting problems,
removing duplicates improved accuracy, fixing ST_CASE allowed for proper
connection between the datasets, and grouping the data dealt with the
structural differences. These important steps allow for the data to be
more reliable and ready for integration and analysis.

After the datasets were cleaned, it was time to combine them into a
single dataset that could be used for analysis. The ACC_AUX dataset is
at the crash level, and each row represents one crash. The PER_AUX
dataset is at the person level, and the VEH_AUX dataset is at the
vehicle level.The PER_AUX and VEH_AUX were first grouped by the ST_CASE
column. This allowed for the data to be summarized by counting exactly
how many individuals took part in every crash. Once the grouping was
finished, each crash had a single row in these summary datasets. This
step allowed it to be possible to actually combine them correctly with
the crash-level data.

Next, the summarized person and vehicle datasets were merged with the
ACC_AUX dataset using the ST_CASE. Then a left join was used so that all
the crash records would still be there, even if there were not any
matching rows in the other datasets. Once the merging was completed, any
values that were missing in the person or vehicle count columns were
substituted with zero. This ensured that for every crash, it had a valid
value for the number of individuals and vehicles involved.

We were then left with the final results of this process, which was a
single dataset where every row represents one crash. This dataset still
had the original crash information, but also had the number of
individuals and vehicles involved. This final dataset is saved as
fars_integrated_crash_level.csv.

These steps used for the integration process made it possible to combine
the three datasets with different structures into one clean dataset.
Grouping all the data before merging stopped any duplication problems,
and using ST_CASE made sure that all the records were linked correctly.
This creates a dataset that is accurate and ready to use for analysis.

## Findings

Findings Analysis of 37,769 fatal crashes and 41,025 total fatalities
from the 2023 FARS dataset revealed consistent and interpretable
patterns across time, geographic, behavioral, and demographic
dimensions.

*Fatality Distribution:* The overwhelming majority of fatal crashes,
35,128 (93.0%), involved a single fatality, while 2,641 crashes (7.0%)
produced multiple fatalities. The rural vs. urban breakdown of this
distribution was largely similar in shape, though rural crashes showed a
slightly higher proportion of multi-fatality outcomes, consistent with
higher travel speeds and longer emergency response times in non-urban
areas.

*Geographic Patterns:* The West North Central region recorded the
highest number of fatal crashes (7,737), followed by the East South
Central (6,340) and Pacific (5,112) regions. At the state level, Texas
(approximately 3,870), California (approximately 3,810), and Florida
(approximately 3,150) were the top three states by fatal crash count, a
pattern driven by a combination of large population, high vehicle miles
traveled, and road network scale. Together, these three states accounted
for a disproportionate share of national fatalities.

*Time Patterns:* More than half of all fatal crashes (54.5%) occurred at
night, and 58.1% occurred during the extended weekend period (Friday 6
PM through Sunday 11:59 PM). This clustering underscores the role of
reduced visibility, fatigue, and higher rates of alcohol use during off
hours in elevating crash risk.

*Road Type and Environment:* Principal arterials were the most dangerous
road class by count (11,318 crashes), followed by minor arterials
(8,665) and major collectors (7,370). Interstates accounted for 4,692
crashes. Notably, the vast majority of crashes, 28,023, occurred under
clear weather conditions, reinforcing that adverse weather alone is not
the primary driver of fatal outcomes as driver behavior and
infrastructure play larger roles.

*Impairment and Risky Behaviors:* Among crashes where BAC status was
known, 55% involved alcohol, making it the most prevalent impairment
factor. Speeding was the single most common behavioral risk factor,
present in 28.2% of all fatal crashes. Distracted driving (8.0%) and
hit-and-run incidents (7.5%) were also notable, while wrong-way driving
(3.3%) and drowsy driving (1.5%), though less frequent, were among the
strongest predictors of multi-fatality outcomes in the regression model.

*Vulnerable Road Users:* Pedestrians were involved in 7,323 fatal
crashes, motorcyclists in 6,274, and pedalcyclists in 1,173. This
breakdown revealed pedestrian crashes were far more concentrated in
urban areas (\~27% of urban crashes), while motorcyclist and large truck
involvement were more evenly distributed, with large trucks more
prevalent in rural crashes (\~18%).

*Driver Age:* Older drivers (65+) were involved in the highest absolute
count of fatal crashes (7,826, or 20.7%), and their crashes were heavily
concentrated in daytime hours (\~32% of daytime crashes). Teen drivers
(15-19) and young adults (21-24) showed elevated nighttime involvement
rates relative to their daytime share, consistent with risk taking
behavior and inexperience.

*Predictive Modeling:* The Random Forest feature importance analysis
identified pedestrian involvement (0.149) and motorcycle involvement
(0.094) as the top two features for predicting multi-fatality crashes,
followed by speeding (0.068) and roadway departure (0.065). The model
achieved an AUC of 0.674. The Logistic Regression model (AUC = 0.691)
confirmed that wrong way driving (OR = 1.21) and speeding (OR = 1.19)
were the strongest positive predictors of multi-fatality outcomes, while
pedestrian (OR = 0.55) and motorcycle involvement (OR = 0.70) were
negatively associated, reflecting that these crashes, though fatal,
typically involve a single victim. The correlation matrix further showed
that roadway departure had strong negative correlations with pedestrian
(0.38) and intersection involvement (0.38), suggesting these represent
distinct crash typologies with different causal structures.

## Future Work

*Lessons Learned*

This project provided several important methodological and substantive
lessons about working with large-scale administrative crash data. The
first and most time-consuming challenge was data integration. The three
FARS auxiliary files (ACC_AUX, PER_AUX, and VEH_AUX) each capture
different units of analysis: crashes, persons, and vehicles. Merging
these correctly required careful attention to key variables and
aggregation logic, as a naive join would produce duplicate rows or
misjoin person- and vehicle-level characteristics to the wrong crash.
This reinforced the importance of understanding each dataset before
attempting any integration.

A second lesson involved the handling of missing and unknown values.
FARS uses coded values to distinguish between "unknown," "not reported,"
and "not applicable," and treating these interchangeably would introduce
systematic bias. For example, the alcohol involvement rate changes
substantially depending on whether unknown BAC cases are included or
excluded. We chose to exclude unknowns when computing rates, but this
decision itself introduces a form of selection bias if unknown BAC is
not missing at random. Future analyses should more carefully model the
missingness mechanism, potentially using multiple imputation for
variables like BAC and impairment status.

The class imbalance in the predictive modeling task was a third key
challenge. Multi-fatality crashes represent only 7% of the dataset,
which caused both the Random Forest and Logistic Regression models to
struggle with recall on the minority class. While the Logistic
Regression achieved reasonable recall for multi-fatality crashes (0.73),
it did so at the cost of very low precision (0.11), meaning the majority
of its positive predictions were false positives. This tradeoff is
inherent to imbalanced classification and should be addressed explicitly
in future modeling efforts. This project underscored the difference
between statistical association and causal inference. The odds ratios
and feature importances identify variables correlated with
multi-fatality outcomes, but they cannot establish causation. For
example, the negative association between pedestrian involvement and
multi-fatality crashes does not mean pedestrians are a protective
factor. It reflects a structural feature of crash types.

*Future Work*

Several directions could meaningfully extend and improve this analysis.
One direction is expanding the feature set. The current model relies on
a relatively small set of binary indicators derived from the FARS
auxiliary files. Incorporating additional variables from the full FARS
dataset, such as road surface condition, lighting condition, vehicle
type, restraint use, and driver license status, could improve predictive
performance and provide richer insight into crash severity. Weather data
from external sources could also be merged at the crash level to better
characterize environmental conditions.

Geographic modeling represents another promising extension. The current
analysis treats geography as a categorical variable (state or NHTSA
region), but crash risk has meaningful spatial structure that aggregate
comparisons cannot capture. Future work could use spatial clustering
methods or geographically weighted regression to identify local hotspots
and assess whether the predictors of multi-fatality crashes vary by
region. Linking crash locations to road network attributes, such as
speed limits, lane count, and median presence, would allow for
infrastructure-level analysis that is currently missing.

Longitudinal analysis is another option for future work. The current
project focuses exclusively on 2023 data, which limits the ability to
assess trends over time. Extending the analysis to cover multiple years
of FARS data would allow for examination of whether crash rates,
impairment patterns, or vulnerable user involvement have changed in
response to policy interventions such as increased DUI enforcement,
speed camera deployment, or infrastructure improvements. This would also
allow for interrupted time series analysis around specific policy
changes.

Finally, future work should more explicitly engage with policy
translation. The findings here, particularly around speeding, alcohol,
nighttime driving, and vulnerable road users, align with well
established risk factors in the traffic safety literature. However,
translating statistical findings into actionable recommendations
requires engagement with the specific policy levers available to
federal, state, and local agencies. Future analyses could incorporate
cost-benefit frameworks to prioritize interventions, or partner with
transportation agencies to validate findings against locally collected
data. Connecting crash severity predictions to emergency response
planning, for example by identifying corridors where multi-fatality
crashes are most likely and ensuring appropriate EMS resources are
positioned nearby, represents one concrete application where this type
of model could have real-world impact.

This project established a solid analytical foundation using 2023 FARS
data, but the complexity of traffic crash causation means there is
substantial room to deepen both the modeling and the interpretive work.
Addressing class imbalance, expanding features, incorporating spatial
structure, and situating findings within a longitudinal and
policy-relevant framework would all meaningfully advance the goals of
this research.

## Challenges

*Data Integration and Schema Complexity:* The most significant technical
challenge in this project was the integration of three separate FARS
auxiliary files, each operating at a different unit of analysis. The
ACC_AUX file records one row per crash, while PER_AUX records one row
per person involved and VEH_AUX records one row per vehicle. Merging
these files into a single dataset required careful aggregation of
person- and vehicle-level attributes up to the crash level before any
join could be performed. For variables like driver age group, this meant
creating binary flags that indicated whether any driver in the crash
belonged to a given age category, rather than simply joining on a single
value. Getting this logic right was iterative and required repeated
validation checks to confirm that crash counts remained consistent
across merges and that no duplicate rows were introduced.

*Handling Missing and Coded Unknown Values:* FARS data uses a complex
coding scheme in which different numeric values distinguish between "not
applicable," "unknown," and "not reported" for many variables. This
distinction matters analytically as a crash with unknown BAC is
fundamentally different from one where BAC was tested and found to be
zero, but both could be coded as non-alcohol-involved if unknowns are
not handled carefully. Deciding how to treat these cases required
variable-by-variable judgment calls, and different choices produced
meaningfully different rates for key indicators like alcohol
involvement. There was no universally correct approach, and the need to
document and justify each decision added substantial overhead to the
cleaning process.

*Class Imbalance in Predictive Modeling:* Building a model to predict
multi-fatality crashes was complicated by the severe imbalance in the
target variable: only 7% of crashes in the dataset involved multiple
fatalities. Both models trained during this project, the Random Forest
and the Logistic Regression, struggled with this imbalance in different
ways. The Random Forest tended to under predict the minority class,
while the Logistic Regression achieved better recall at the cost of very
poor precision. Selecting the right evaluation metric was itself a
challenge, since overall accuracy is a misleading measure when one class
dominates. Navigating these tradeoffs without the benefit of resampling
techniques or cost-sensitive learning meant accepting meaningful
limitations in model performance.

*Interpreting Feature Directionality:* A recurring interpretive
challenge was making sense of features that were negatively associated
with multi-fatality outcomes, particularly pedestrian and motorcycle
involvement. At first glance, a negative odds ratio for pedestrian
involvement seems counterintuitive given that pedestrians are among the
most vulnerable road users. Understanding that this reflects crash
typology rather than a protective effect required careful reasoning
about what the model was actually predicting and what the reference
category implied. Distinguishing between statistical association and
causal interpretation was a constant discipline throughout the analysis,
and communicating these nuances clearly in the findings required
deliberate framing to avoid misleading conclusions.

## Reproducing

To reproduce our project, you would first need to clone the GitHub
repository to your own local machine. This project was done using Python
3. Before trying to reproduce, double-check that you have the correct
version of Python installed on your local system.

All the input data that is needed for this project is included in the
repository. The raw datasets, FARS2023NationalAuxiliaryCSV.zip, is easy
to locate in the data/raw folder. In this file, you will find the
ACC_AUX, PER_AUX, and VEH_AUX datasets, which were used throughout the
project. There are no additional downloads needed since all the data is
already provided in the correct location. Make sure you are in the
project root directory for the steps below.

Before trying to run the workflow, you must install the required
dependencies by running:

```         
pip install -r requirements.txt
```

The three FARS datasets are stored in a zip file. You can manually unzip
them, or run the following command:

```         
unzip data/raw/FARS2023NationalAuxiliaryCSV.zip -d data/raw/FARS2023NationalCSV
```

Once everything is set up, the workflow can be run by using the scripts
in the given scripts directory. For the easiest way to reproduce the
full pipeline is to run the run_all.sh script, which does all the needed
steps for each part, like data cleaning, integration, analysis, and
visualization.

You can complete this by running this command:

```         
bash scripts/run_all.sh 
```

Once the script is run, it will automatically install the required
dependencies, verify the raw data files, run the cleaning and
integration process using the scripts/integrate.py, and then will run
the analysis and visualization script. The cleaned and integrated data
will be saved in the data/processed folder, and any analysis of outputs
will be generated by the workflow. Because all of our scripts, data, and
outputs are included in the repository or created from the workflow, any
user could follow the exact steps and be able to fully reproduce this
project, starting from the raw data to the final results, without having
to modify any code.

## References

National Highway Traffic Safety Administration. (2024). *FARS 2023
national data files* [Data set]. U.S. Department of Transportation.
<https://www.nhtsa.gov/research-data/fatality-analysis-reporting-system-fars>

National Highway Traffic Safety Administration. (2024). *Fatality
Analysis Reporting System (FARS) 2023 auxiliary files: ACC_AUX, PER_AUX,
VEH_AUX* [Data set]. U.S. Department of Transportation.
<https://www.nhtsa.gov/file-downloads?p=nhtsa/downloads/FARS/2023/National/>
