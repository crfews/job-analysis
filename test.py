import jobanalysis
import pandas as pd

# create sample list of data science jobs
url_list = [
    'https://www.linkedin.com/jobs/view/4374021430/',
    'https://www.linkedin.com/jobs/view/4373080915/',
    'https://www.linkedin.com/jobs/view/4323533943/'
]

jobs = jobanalysis.Cloud_Job_Analysis(url_list) # create cloud object

jobs.evaluate(createimg=False,pos=['ADV','NOUN','VERB'])

job_data = jobs.job_data

jobs.make_cloud(saveplot=True,title='entry level data scientists')

job_data.to_excel('data_science.xlsx')
