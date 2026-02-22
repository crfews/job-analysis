# job-analysis

This code contains a class that is able to scrape LinkedIn job listings that are accepting active applications and graphing the most common words associated with them/

## How to Install
1. Navigate to the main page and click code.
2. Clone the repository in your terminal. 
```git clone https://github.com/crfews/job-analysis.git```
3. Create a virtual environment in the directory e.g. ```python -m venv venv``` and run activate (Windows:```.\venv\Scripts\activate``` Linux:```source venv/bin/activate```
5. Install required packages using ```pip install requirements.txt```
6. Run ```python -m spacy download en_core_web_sm```

## Examples
Make sure to install the list of libraries used before running `test.py` or `test2.py`. These test files test the output for data science and logistics job listings, respectively.

## Note
The code will not function if the linked job listing is no longer accepting applications or is otherwise invalid. If the former case is true, use a link that is open for applicants.

## Libraries used
- Beautiful Soup
- Matplotlib
- Pandas
- Requests
- Spacy
- TextBlob
- Wordcloud
