## Overview
The goal of our project is to study the factors that might affect car accidents and insurance claims. Accidents can happen for many different reasons, and insurance companies try to understand that so they can estimate risk. By searching through the data about vehicles, drivers, and crashes, we can find patterns that might help explain why accidents happened and how they can relate to insurance claims.

In this project, we are going to use two datasets. The first dataset was found from the insuranceData package. This package has datasets that are normally used for risk analysis and insurance. This dataset has important information about insurance claims and vehicle characteristics. The second dataset is from the Fatality Analysis Reporting System (FARS). This dataset was made by the National Highway Traffic Saftey Administration and has detailed information about fatal motor vehicle crashes in the United States of America. 

Our approach will have mutliple steps to follow. First, we will collect the two datasets and look over how the data is organized. Second, we will explore the data and search for missing values or any other cleaning issues. Third, we will focus on variables related to vehicles and drivers to explore potential patterns in the data. Lastly, we will summarze our results using simple analysis and visualization. The goal of this project is to get a better understanding of how vehicle and driver characteristics relate to accident outcomes and insurance risk. 

## DataSets

## Dataset 1: insuranceData Dataset
Source: https://cran.r-project.org/web/packages/insuranceData/index.html

Description: Our first dataset comes from insuranceData package. This package is available to access on the CRAN website and is normally used for insurance research and teaching. This dataset has information that is related to insurance claims and risk factors. Some important variables describe vehicle characteristics, policy exposure, and other factors that might influence insurance claims. This dataset was organized in a table format, which makes it a lot easier to work with for easy analysis while using Python.  
## Dataset 2: Fatality Analysis Reporting System (FARS)
Source: https://www.nhtsa.gov/file-downloads?p=nhtsa/downloads/FARS/2023/National/

Description: Our second dataset comes from the Fatality Analysis Reporting System (FARS). This dataset was made by the National Highway Traffic Safety Administration and has detailed information about fatal motor vehicle crashes in the United States of America. This dataset has multiple tables that show different parts of each crash. The tables have information about things like the accident itself, the vehicles involved, and the people who were in the crash. In the project on main focus will be on the vehicle dataset, becasue it has information about vehicle characteristics and crash involvement. This dataset is in CSV format, which means it is also easier to work with and analyze with Python. 

## Data Integration
Even though these datasets are not from the same sources, they both have important information that is related to vehicles and drivers. They are both two pieces for one puzzle; the insurance dataset has information about insurance claims and vehicle characteristics, while the FARS has all of the crash data. By using these variables together, we can find possible patterns between vehicle characteristics, crash involvement, and insurance risk.  

## Timeline
Week 1 - Data Collection: Collect the insuranceData and FARS datasets. We will also read the documentation to understand what variables are in each dataset.
Responsible: Marco and Ellen
Week 2 - Explore the Data: Look through the datasets to understand the variables and search for missing values or any other data problems. 
Responsible: Marco



## Team 
*Marco Soto: Data Preprocessing and Integration*
- Download, organize, and document the FARS crash dataset and insurancerating dataset.
- Assess completeness, consistency, and quality issues and document all cleaning steps.
- Design and implement methods to combine FARS crash data with insurancerating variables.
- Document integration schema, mapping between datasets, and any assumptions made during integration.

*Ellen Harris: Data Analysis and Reproducibility*
- Develop predictive models to address the research question
- Generate visualizations and summarize numeric findings of integrated datasets
- Create workflow scripts to ensure end-to-end reproducibility from data acquisition to final results.

## Research or Business Question(s)
*Research Question:* How can historical crash data (from the NHTSA FARS dataset) be integrated with insurance rating variables (from the insurancerating dataset) to improve predictive models for auto insurance risk and pricing?

This project investigates how historical crash data from the NHTSA FARS dataset can be combined with insurance rating variables from the insurancerating dataset to improve predictive models for auto insurance risk. Specifically, we aim to identify the crash and policyholder factors that most strongly influence claim frequency and severity. The goal is to develop insights that can enhance insurance pricing accuracy and support more effective risk assessment strategies. For insurance pricing models, GLMs (Poisson, Negative Binomial, Tweedie) are standard in practice, while tree-based methods (Random Forest, GBM) can capture complex patterns from crash and rating data. Often, a combination of models is used: GLMs for interpretability and tree-based models for predictive power.


## Constraints

Our analysis is constrained by several factors inherent in the datasets and the scope of the project. The FARS dataset captures only fatal crashes in the United States, which means non-fatal or minor incidents are not represented. Additionally, certain variables, such as alcohol involvement, seatbelt usage, or driver impairment, may be incomplete or inconsistently reported across states and years. The insurancerating dataset may also have missing entries for key variables like policyholder demographics, vehicle type, or coverage details, limiting the completeness and precision of any predictive models.

Integrating these datasets poses additional challenges. There is no direct linkage between individual crash records in FARS and insurance policy records, so any analysis combining the datasets must rely on aggregated or proxy-level matching. Differences in coding schemes, data formats, and variable definitions further complicate the integration process. Large dataset sizes and the need for extensive preprocessing or feature engineering may introduce computational limitations, requiring careful planning and efficient workflow design to ensure reproducibility.

Finally, there are important ethical and legal considerations. Both datasets contain sensitive information about individuals, including demographic and vehicle data, which must be handled responsibly. Predictive modeling for insurance risk also raises potential ethical concerns, such as inadvertently introducing bias against certain demographic groups or regions. These limitations, along with temporal and geographic constraints, missing data, and modeling challenges, may affect the generalizability, accuracy, and fairness of our findings. Careful documentation and transparency in all data handling and analysis steps are critical to mitigating these risks.

