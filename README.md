# Analysis of Traffic Crash Data Using FARS Datasets

## Contributors

## Summary

## Data Profile
Our project uses three datasets from the Fatality Analysis System (FARS): ACC_AUX, PER_AUX, and VEH_AUX. These three datasets all relate to fatal traffic crashes in the United States, but each one looks at a different level of detail. Together they will allow us to see a more complete picture of what occurs during a crash.

The ACC_AUX dataset has information at the crash-level. Each row is there to represent a single crash and has general details about the location and time of the crash. This dataset is critical because it serves as the base dataset for this project. 

The PER_AUX dataset contains information at the person-level. Every row is there to represent a person involved in a crash like the passenger or driver. Because in some cases multiple people can be involved in a crash, there are multiple rows that have the same ST_CASE value. This dataset gives us a better understanding of how many individuals were involved and provides more details about individuals in the crash.

The VEH_AUX dataset contains vehicle-level data. Each row represents a vehicle that was involved in a crash. This is similar to the person dataset because multiple vehicles can be a part of one crash. This dataset gives an additional layer of detail by showing us how many vehicles were involved.

These three datasets are connected using the ST_CASE, which is the unique crash ID. This allows it to be possible to combine the datasets later. The raw data was stored as a zip file in the data/raw folder, and all the cleaned and processed files are saved in the data/processed folder. 
## Data Quality
At first glance at the raw dataset, there were multiple issues that needed to be fixed before the data was usable. The first problem that was noticed was that the column names were not consistent. Multiple column names had an extra space or were formatted in a different way, which could create problems when trying to combine the datasets. If you do not have consistent column names it becomes much harder to match the same fields across datasets, which has the possibility to cause errors during the merge.

Another major problem was with the ST_CASE column. This was identified as the most important column because it is used to connect all three of the datasets. There was values that were not stored as numbers, and same values that were not there at all. If this column is not clean, the dataset would not merge correctly, which would give us wrong final results. Because ST_CASE was the main identifier for every crash, issues within this column would directly affect the entire project. 

There was also duplicate rows in the dataset. Keeping these duplicate rows would have led to incorrect counts and make it seem like there are more crashes, people, or vehicles then there really is. Those rows would also affect analysis that was done later and make the results less reliable. Removing these duplicates was necessary to make sure every record represented the real and unique data. Missing values was also a problem across different columns. While not all of the missing values needed to be removed, it was very crucial that the key fields like ST_CASE were valid. Any row that was missing a usable crash ID could not be connected to other datasets and therefore could not be used in the final dataset. 

Another issue was incorrect data types. Some values that should have been numbers were actually stored as text, which would create serious problems when trying to perform grouping or counting operations. Since our project needs to count people and vehicles per crash, these data type issues had to be fixed. There was also some cases where records could not be matched across the datasets because of missing or invalid ST_CASE values. Those records had to be removed because they could not be reliably used in the integration process.

In addition to those issues, the structure of the datasets also had some issues. The ACC_AUX dataset is organized at the crash-level, while PER_AUX and the VEH_AUX datasets are organized at the person and vehicle-levels. This means that a singular crash could have multiple related rows in the other datasets. Because of this, it would not be possible to directly merge all three of the datasets without first checking to make sure the data is properly prepared. If this was not handled correctly it can cause duplicate information or incorrect totals in the final dataset. 

Another issue was checking to make sure the data was usable after cleaning. Any type of issues even small problems, like an extra space in columns names or incorrect data types, could create errors in the code or lead to incorrect results. This little issues might not seem that important upon first look, but later on the have the ability to create bigger problems in the overall process. Because of this is was extremely important to fully review the data and fix all these issues early on. Another need was to balance cleaning the data with keeping enough useful information. While some information needed to be removed like rows with missing or invalid ST_CASE values, removing too much of the data could reduce the amount of information that would be used for analysis. This was important so we could only remove records that could not be used and keep as much useful data as possible.

Overall, all these issues show that data quality is not just about trying to fix obvious problems. It also involves checking to make sure that the data is consistent, usable, and structured in a way that supports the overall purpose of this project. Taking the time to address these issues allowed me to make sure that the final dataset would be accurate, reliable, and ready for analysis.
## Data Cleaning

## Findings

## Future Work

## Challenges

## Reproducing

## References
