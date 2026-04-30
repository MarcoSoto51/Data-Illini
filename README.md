# Analysis of Traffic Crash Data Using FARS Datasets

## Contributors

## Summary

## Data Profile
Our project uses three datasets from the Fatality Analysis System (FARS): ACC_AUX, PER_AUX, and VEH_AUX. These three datasets all relate to fatal traffic crashes in the United States, but each one looks at a different level of detail. Together, they will allow us to see a more complete picture of what occurs during a crash. 

The ACC_AUX dataset has information at the crash level. Each row is there to represent a single crash and has general details about the location and time of the crash. This dataset is critical because it serves as the base dataset for this project.  

The PER_AUX dataset contains information at the person level. Every row is there to represent a person involved in a crash, like the passenger or driver. Because in some cases multiple people can be involved in a crash, there are multiple rows that have the same ST_CASE value. This dataset gives us a better understanding of how many individuals were involved and provides more details about individuals in the crash. 

The VEH_AUX dataset contains vehicle-level data. Each row represents a vehicle that was involved in a crash. This is similar to the person dataset because multiple vehicles can be a part of one crash. This dataset gives an additional layer of detail by showing us how many vehicles were involved.

These three datasets are connected using the ST_CASE, which is the unique crash ID. This allows it to be possible to combine the datasets later. The raw data was stored as a zip file in the data/raw folder, and all the cleaned and processed files are saved in the data/processed folder. 
## Data Quality
At first glance, the raw dataset had multiple issues that needed to be fixed before the data was usable. The first problem that was noticed was that the column names were not consistent. Multiple column names had an extra space or were formatted in a different ways, which could create problems when trying to combine the datasets. If you do not have consistent column names, it becomes much harder to match the same fields across datasets, which has the possibility of causing errors during the merge. 

Another major problem was with the ST_CASE column. This was identified as the most important column because it is used to connect all three of the datasets. There was values that were not stored as numbers, and the same values that were not there at all. If this column is not clean, the dataset would not merge correctly, which would give us wrong final results. Because ST_CASE was the main identifier for every crash, issues within this column would directly affect the entire project.  

There were also duplicate rows in the dataset. Keeping these duplicate rows would have led to incorrect counts and made it seem like there are more crashes, people, or vehicles then there really are. Those rows would also affect the analysis that was done later and make the results less reliable. Removing these duplicates was necessary to make sure every record represented the real and unique data. Missing values were also a problem across different columns. While not all of the missing values needed to be removed, it was very crucial that the key fields like ST_CASE were valid. Any row that was missing a usable crash ID could not be connected to other datasets and, therefore, could not be used in the final dataset.

Another issue was incorrect data types. Some values that should have been numbers were actually stored as text, which would create serious problems when trying to perform grouping or counting operations. Since our project needs to count people and vehicles per crash, these data type issues had to be fixed. There was also some cases where records could not be matched across the datasets because of missing or invalid ST_CASE values. Those records had to be removed because they could not be reliably used in the integration process. 

In addition to those issues, the structure of the datasets also had some issues. The ACC_AUX dataset is organized at the crash-level, while PER_AUX and the VEH_AUX datasets are organized at the person and vehicle-levels. This means that a singular crash could have multiple related rows in the other datasets. Because of this, it would not be possible to directly merge all three of the datasets without first checking to make sure the data is properly prepared. If this was not handled correctly, it could cause duplicate information or incorrect totals in the final dataset.  

Another issue was checking to make sure the data was usable after cleaning. Any type of issue, even small problems, like an extra space in column names or incorrect data types, could create errors in the code or lead to incorrect results. These little issues might not seem that important upon first look, but later on, they have the ability to create bigger problems in the overall process. Because of this is was extremely important to fully review the data and fix all these issues early on. Another need was to balance cleaning the data with keeping enough useful information. While some information needed to be removed, like rows with missing or invalid ST_CASE values, removing too much of the data could reduce the amount of information that would be used for analysis. This was important so we could only remove records that could not be used and keep as much useful data as possible. 

Overall, all these issues show that data quality is not just about trying to fix obvious problems. It also involves checking to make sure that the data is consistent, usable, and structured in a way that supports the overall purpose of this project. Taking the time to address these issues allowed me to make sure that the final dataset would be accurate, reliable, and ready for analysis. 
## Data Cleaning
To correct all the issues that were found in the raw datasets, several cleaning steps were performed using a Python script. These steps were based on the problems I identified earlier in the data quality section, and they were necessary to make sure they could correctly be merged and used for later analysis. 

The first step was to clean the column names. Many column names had an extra space or inconsistent formatting, which could create problems when trying to match the columns across datasets. To correct this issue, all the column names were stripped of any extra spaces and then converted to uppercase. This allowed the datasets to be consistent and easier to work with, especially while merging.  

The next step was to remove the duplicate rows from each dataset. This step directly corrected the issue of repeated records that could have caused incorrect counts. If the duplicates were to remain in the data, it would make it look like there were more crashes, people, or vehicles then there actually was. Getting rid of these duplicates made sure that each row represented unique information and improved the overall accuracy of the dataset. 

The next step was to clean the ST_CASE column. This column is the key value used to connect all three of the datasets, so it had to be consistent and valid. I started by converting all the ST_CASE values to a numeric format. Any values that could not be converted or were missing were removed from the dataset. Next, the column was converted to integers to make sure there was perfect consistency across all datasets. Fixing this issue was particularly important because any issues in ST_CASE would prevent the dataset from being merged correctly and cleanly. Any rows that had invalid or missing ST_CASE values were also removed. Those rows would not be able to link to the other datasets, so keeping them would not be doing any benefit to the final dataset.  

In addition to cleaning the datasets, another step had to happen to prepare the data for merging. Since the PER_AUX and VEH_AUX datasets are at the person and vehicle levels, they have multiple rows for each crash. To deal with this, both of the datasets were grouped by the ST_CASE to gather a count of how many people and vehicles were involved in each crash. This made summary datasets that could be merged together with the crash-level dataset without making any duplicate rows. This was important because it dealt with the structural differences between the datasets. Without grouping and merging the datasets directly would have given results with repeated crash records and incorrect totals. Because we summarized the data first, the final dataset remained at the crash level while still having useful information about people and vehicles. 

All of these cleaning steps were done in a single Python script, which makes the process reproducible. That means that my steps could be done again if needed, and the results would remain the same. The cleaned datasets and summary files were saved in the data/processed folder so they could be used for in the next stage of our project.  

Overall, every cleaning step directly addressed the specific problem that was found in the data. Cleaning column names fixed formatting problems, removing duplicates improved accuracy, fixing ST_CASE allowed for proper connection between the datasets, and grouping the data dealt with the structural differences. These important steps allow for the data to be more reliable and ready for integration and analysis. 
## Data Integration
After the datasets were cleaned, it was time to combine them into a single dataset that could be used for analysis. This project used three datasets: ACC_AUX, PER_AUX, and VEH_AUX. Even though these datasets are related, they are still structured differently, so they could not be straight-up merged without causing any errors. 

The ACC_AUX dataset is at the crash level, and each row represents one crash. The PER_AUX dataset is at the person level, and the VEH_AUX dataset is at the vehicle level. This is important because it shows how a single crash can contain multiple rows in the person and vehicle datasets. If we were to try to merge directly, duplicates would be created for the crash records and have incorrect totals. To correct this problem, the PER_AUX and VEH_AUX were first grouped by the ST_CASE column. This allowed for the data to be summarized by counting exactly how many individuals took part in every crash. Once the grouping was finished, each crash had a single row in these summary datasets. This step allowed it to be possible to actually combine them correctly with the crash-level data.  

The ST_CASE column was the key to connecting all three of the datasets. This column is a unique crash ID, so it was the correct way to link these datasets together. Next, the summarized person and vehicle datasets were merged with the ACC_AUX dataset using the ST_CASE. Then a left join was used so that all the crash records would still be there, even if there were not any matching rows in the other datasets. Once the merging was completed, any values that were missing in the person or vehicle count columns were substituted with zero. This ensured that for every crash, it had a valid value for the number of individuals and vehicles involved. 

We were then left with the final results of this process, which was a single dataset where every row represents one crash. This dataset still had the original crash information, but also had the number of individuals and vehicles involved. This final dataset is saved as fars_integrated_crash_level.csv. 

Overall, these steps used for the integration process made it possible to combine the three datasets with different structures into one clean dataset. Grouping all the data before merging stopped any duplication problems, and using ST_CASE made sure that all the records were linked correctly. This creates a dataset that is accurate and ready to use for analysis.  
## Findings

## Future Work

## Challenges

## Reproducing
To reproduce our project would need to clone the GitHub repository to your own local machine. This project was done using Python 3 and requires the pandas library for data processing. Before trying to reproduce, double-check that you have Python installed and that pandas are available in your environment before trying to run any scripts.

All the input data that is needed for this project is included in the repository. The raw dataset, FARS2023NationalAuxiliaryCSV.zip, is easy to locate in the data/raw folder. In this file, you will find the ACC_AUX, PER_AUX, and VEH_AUX datasets, which were used throughout the project. There are no additional downloads needed since all the data is already provided in the correct location. After you have gathered the data in the data/raw folder, the workflow can be run using the scripts in the given scripts directory. For the easiest way to reproduce the full pipeline is to run the run_all.sh script, which executes all the needed steps from data cleaning and integration to analysis and visualization. You can do this by running this command: 
```
bash scripts/run_all.sh
```
Once the script is run, it will automatically install the required dependencies, verify the raw data files, run the cleaning and integration process using the scripts/integrate.py, and then will run the analysis and visualization script. The now cleaned and integrated data will be saved in the data/processed folder, and results from analysis will be saved in the results/figures and results/tables folders after you run the full workflow. Because all of our scripts, data, and outputs are included in the repository or created from the workflow, any user could follow the exact steps and be able to fully reproduce this project, starting from the raw data to the final results, without having to modify any code.  
## References
