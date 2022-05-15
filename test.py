import jobanalysis

# create sample list of jobs
url_list = [
    'https://www.linkedin.com/jobs/view/2959124718',
    'https://www.linkedin.com/jobs/view/3030646645',
    'https://www.linkedin.com/jobs/view/3023688838',
    'https://www.linkedin.com/jobs/view/3042583942',
    'https://www.linkedin.com/jobs/view/3042428478',
    'https://www.linkedin.com/jobs/view/3036847597',
    'https://www.linkedin.com/jobs/view/3041899464',
    'https://www.linkedin.com/jobs/view/3044949120',
    'https://www.linkedin.com/jobs/view/3039549560'
]

jobs = jobanalysis.Cloud_Job_Analysis(url_list) # create cloud object

obj = jobs.evaluate(createimg=False,pos=['ADV','NOUN','VERB'])

jobs.make_cloud()

