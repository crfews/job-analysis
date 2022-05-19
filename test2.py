import jobanalysis
import pandas as pd

# create sample list of logistics jobs
url_list = [
    'https://www.linkedin.com/jobs/view/3063429466',
    'https://www.linkedin.com/jobs/view/3019370404',
    'https://www.linkedin.com/jobs/view/2829993099',
    'https://www.linkedin.com/jobs/view/3074129179',
    'https://www.linkedin.com/jobs/view/2828387493',
    'https://www.linkedin.com/jobs/view/3075098988',
    'https://www.linkedin.com/jobs/view/3068137055',
    'https://www.linkedin.com/jobs/view/3072626331',
    'https://www.linkedin.com/jobs/view/3074267030'
]

jobs = jobanalysis.Cloud_Job_Analysis(url_list) # create cloud object

jobs.evaluate(createimg=False,pos=['ADJ','ADV','NOUN'])

job_data = jobs.job_data

jobs.make_cloud(saveplot=True,title='logistics')

print(job_data)
job_data.to_excel('logistics_job_data.xlsx')
