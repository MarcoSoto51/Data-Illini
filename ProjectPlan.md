## Overview
The overall goal of this project is to analyze factors contributing to fatal crashes in the United States in 2023 and identify patterns associated with crash severity. We aim to understand how driver characteristics, environmental conditions, vehicle types, and roadway features influence fatal crash outcomes. The planned approach involves integrating the FARS 2023 National Auxiliary dataset, which provides detailed crash-level information, with a complementary dataset containing vehicle or state-level traffic statistics. By linking these datasets via common identifiers such as crash ID, state, and vehicle type, we will perform descriptive and inferential analyses. The main steps include: 1) data cleaning and preprocessing, 2) exploratory data analysis to identify trends and correlations, 3) statistical modeling (e.g. logistic regression) to quantify risk factors for fatal crashes, and 4) visualization of key findings to support evidence-based insights. Ultimately, we aim to provide actionable recommendations for traffic safety interventions and predictive insights to identify high risk scenarios.


## Research or Business Question(s)
*Research Questions:* 
- Which driver, vehicle, and environmental factors are most strongly associated with fatal crashes in 2023?
- Can we predict the likelihood of a fatal crash given a combination of driver, vehicle, and environmental variables?

This project seeks to answer several research questions. First, which driver, vehicle, and environmental factors are most strongly associated with fatal crashes in 2023? Second, how do fatal crash patterns vary across geographic regions, time of day, and road types? Third, what is the impact of seat belt use, alcohol, or other impairments on fatality outcomes? Finally, can we predict the likelihood of a fatal crash given a combination of driver, vehicle, and environmental variables? These questions aim to identify actionable insights that can improve traffic safety and guide policy interventions.


## Datasets: Fatality Analysis Reporting System (FARS) Auxiliary Datasets
Source: https://www.nhtsa.gov/file-downloads?p=nhtsa/downloads/FARS/2023/National/

Description: Datasets detailed crash-level data including driver demographics, crash circumstances, vehicle types, and outcomes. The source provides three datasets: ACC_AUX, PER_AUX, and VEH_AUX. These three datasets provide information on the accident, persons involved, and vehicle information for crashes in 2023. Datasets will be joined using the ST_CASE key. This is a provided key to join the datasets for analysis.
  

## Timeline
Week 1 - Data Collection: Collect the FARS datasets. We will also read the documentation to understand what variables are in each dataset.
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
- Download, organize, and document the FARS datasets.
- Assess completeness, consistency, and quality issues and document all cleaning steps.
- Design and implement methods to combine insurancerating variables.
- Document integration schema, mapping between datasets, and any assumptions made during integration.

*Ellen Harris: Data Analysis and Reproducibility*
- Develop predictive models to address the research question
- Generate visualizations and summarize numeric findings of integrated datasets
- Create workflow scripts to ensure end-to-end reproducibility from data acquisition to final results.


## Constraints

The project faces several limitations due to the nature of the FARS auxiliary datasets. Some variables may have missing or incomplete values, particularly for less frequently reported factors such as drug involvement or specific vehicle features. Differences in coding conventions across the three datasets may introduce challenges when merging data, especially for variables that appear in multiple files. Spatial granularity is often limited to the state or county level, which may prevent detailed local-level analysis. Temporal coverage is restricted to crashes that occurred in 2023, limiting the ability to analyze long-term trends. Additionally, the datasets rely on reported crash data, which may contain reporting errors or inconsistencies, and certain sensitive information is masked or unavailable due to privacy restrictions, limiting detailed demographic or location-specific analyses. Some of the procided documentation links no longer work, and the DOI link points to a secure ArcGIS feature service, so you cannot fetch the data dictionary directly without access credentials, even though it is listed as available for public use. 


## Gaps
Several gaps remain that may require additional input or supplementary data. Exposure-related information, such as vehicle miles traveled or traffic volume for specific roadway types, is not fully captured in the auxiliary files, which limits risk-adjusted comparisons across locations or vehicle types. Some variables, such as driver distraction or precise roadway conditions, may be inconsistently reported or unavailable, reducing the granularity of causal analysis. Verification of variable coding across the three datasets is needed to ensure accurate integration and analysis. Finally, additional geospatial or temporal data could enhance the project’s ability to identify patterns at a more localized or time-specific level.

