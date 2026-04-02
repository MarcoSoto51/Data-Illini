## Overview
The goal of this project is to analyze how legal representation and demographic factors influence insurance claim payout severity. Using the AutoBi and AutoClaims datasets from the CRAN insuranceData package, we explore patterns in claim amounts across different genders, ages, and attorney involvement. The project follows a structured workflow: first, we clean and preprocess the data, addressing missing values and outliers; next, we summarize claim patterns using aggregation and visualizations; finally, we model relationships between demographics, attorney involvement, and payout severity using Generalized Linear Models (GLMs). By systematically combining descriptive and inferential analysis, this project aims to provide insights into which factors are associated with higher or lower claim payouts, supporting more informed risk assessment in auto insurance.


## Research or Business Question(s)
*Research Question:* "Does legal representation or demographic factors predict claim payout severity across claim types?"

The AutoBi dataset provides detailed information on reported losses, including policyholder age, gender, and attorney involvement, while AutoClaims contains paid claim amounts and associated vehicle information. We will first clean and standardize the demographic and claim variables to handle missing or inconsistent entries, and cap outliers to reduce distortion from extreme values. Aggregation and normalization by gender and attorney status will allow us to compare reported versus paid claims systematically. Statistical modeling, specifically Generalized Linear Models (GLMs) with a Gamma distribution and log link, will be applied to quantify the effects of demographic factors and attorney involvement on claim severity. Visualizations, including histograms, boxplots, and normalized bar charts, will further illustrate patterns and differences across claim types. Together, these analyses will provide evidence on whether demographic characteristics or legal representation significantly predict the severity of insurance claim payouts, enabling a clearer understanding of risk factors in insurance claims.


## Datasets: insuranceData Dataset
Source: https://cran.r-project.org/web/packages/insuranceData/index.html

Description: Both our datasets comes from insuranceData package. This package is available to access on the CRAN website and is normally used for insurance research and teaching. This data source has information that is related to insurance claims and risk factors. Some important variables describe vehicle characteristics, policy exposure, and other factors that might influence insurance claims. The two datasets we will be joining are the AutoBi and the AutoClaims datasets. 

Aggregated comparison will be made by combining the two datasets. AutoBi has individual-level auto bodily injury claims with variables like attorney representation (ATTORNEY), claimant sex (CLMSEX), marital status, seatbelt use, claimant age (CLMAGE), and total loss (LOSS). AutoClaims adds state-level context with claim class and amount paid. They will be integrated conceptually by demographic attributes (gender, age) to build a combined severity model.  

## Timeline
Week 1 - Data Collection: Collect the insuranceData datasets. We will also read the documentation to understand what variables are in each dataset.
Responsible: Marco and Ellen

Week 2 - Explore the Data: Look through the datasets to understand the variables and search for missing values or any other data problems. 
Responsible: Marco

Week 3 - Clean the Data: Clean the datasets by fixing any formatting issues and select the most useful variables for this project.
Responsible: Ellen

Week 4 - Integrate the Data: Work together to find out how the datasets relate and connect the information together for further analysis.
Responsible: Ellen and Marco

Week 5 - Analyze the Data: Create visualizations to show patterns related to vehicles, crashes, and insurance risk.
Responsible: Marco and Ellen

Week 6 - Finalize: Organize the GitHub repository and finish the documentation for the final project.
Responsible: Marco and Ellen

## Team 
*Marco Soto: Data Preprocessing and Integration*
- Download, organize, and document the insurancerating datasets.
- Assess completeness, consistency, and quality issues and document all cleaning steps.
- Design and implement methods to combine insurancerating variables.
- Document integration schema, mapping between datasets, and any assumptions made during integration.

*Ellen Harris: Data Analysis and Reproducibility*
- Develop predictive models to address the research question
- Generate visualizations and summarize numeric findings of integrated datasets
- Create workflow scripts to ensure end-to-end reproducibility from data acquisition to final results.


## Constraints

Our analysis is limited to the AutoBi and AutoClaims datasets from the CRAN insuranceData package. These datasets only include policyholder demographics, attorney involvement, and claim amounts. Non-fatal accident information or other factors influencing claim severity, such as vehicle damage details, driving history, or environmental conditions, are not included. Additionally, the datasets may contain missing values or inconsistencies in gender or age fields, which requires cleaning and may reduce sample size. Outlier capping is used to mitigate extreme claim values, but this may slightly distort the impact of very high claims.

Another limitation is that the data are cross-sectional and do not track multiple claims from the same policyholder over time. This prevents modeling longitudinal effects or repeated claim behavior. The datasets also lack geographic identifiers or other context that might influence claim severity, so conclusions are limited to patterns observable from the provided variables. Lastly, while GLMs can quantify relationships between attorney involvement, demographics, and payouts, other unobserved factors may influence claims, so results should be interpreted as indicative rather than causal.


## Gaps
While the AutoBi and AutoClaims datasets provide rich information on claims, demographics, and attorney involvement, there are several gaps. First, the datasets do not include policy-level details such as coverage limits, deductible amounts, or driving history, which could affect payout severity. Second, information on claim type or cause of loss is limited, restricting the ability to differentiate patterns across specific claim categories. Finally, external validation with real-world insurance or crash data is not included, which limits the generalizability of findings beyond these datasets.

