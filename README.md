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

## Data Cleaning

## Findings

## Future Work

## Challenges

## Reproducing

## References
