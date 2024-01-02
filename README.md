# Pattern-Recognition-in-Microbiomes

This repository aims to develop a web application to process and build a machine-learning model to geographically classify organisms at a taxonomical level. 

# Pre-requisites
Before running this app, make sure to install the required modules. Navigate to the requirements.txt file and run the code below in your suitable terminal environment

```
pip install -r requirements.txt
```
or 
```
python -m pip install -r requirements.txt
```

After completing the above step, the user can download the other files and execute the command below to host the web app locally

```
python streamlit run app.py
```
Make sure the path is referenced properly.

# Decription
The coded app contains four sections. Some sections are yet to be completed and hence warned about.
- Upload
- Profiling (incomplete)
- Modeling
- Download (incomplete)

## Upload 
This section is designed to process and model our dataset. Please ensure that you upload the OTUs, taxonomic, and metadata tables. Ensure that all columns in the sampled tables are named correctly. Use a single space (' ') as the separator for the OTUs and tax files, and use a tab space ('\t') for the metadata.

Choose the appropriate taxonomical hierarchy for classification for both the index and the target variable. This final processed dataset will be saved either on your local disk or on the server for subsequent sections. It can only be modified by pressing the merge button

## Profiling
This section is planned to showcase a small EDA on the dataset the final processed dataset.

## Modeling
In this section, the user is provided with the option to choose either 
- To build a classification model of choice 
- Compare all the classification models build around the default tuning parameters.

This is built with the idea that the user might want to identify the best modeling algorithm suitable for the dataset and later choose to examine that model's performance in the previous section.

## Download
This section is designed to allow users to download the chosen model for the analysis (with default parameters), which can later be appropriately tuned by the user
