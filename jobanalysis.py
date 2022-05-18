from collections import Counter  # allows us to count the frequency of nouns as they appear
import requests  # allows us to get HTML requests and scrape web pages
import spacy  # NLP library
from bs4 import BeautifulSoup  # counting words
from textblob import TextBlob  # sentiment analysis
import matplotlib.pyplot as plt  # creating plots of the frequent words
import pandas as pd  # for creating a dataframe object that organizes and consolidates the data for easy access
import matplotlib.cm as cm # for plotting cloud
from matplotlib import rcParams # for plotting cloud
from wordcloud import WordCloud, STOPWORDS # for creating word clouds

class Job_Analysis():
    """
    This class was written to analyze a list of URLs from LinkedIn job descriptions to
    count the most common words in the job description.
    """

    def __init__(self, url_list):
        self.links = url_list  # list of links in prescribed format
        self.raw_list = []  # scraped html content
        self.content_list = []  # content without html code
        self.title_list = []  # job titles listed
        self.company_list = []  # companies listed
        self.words_list = [] # list of words
        self.polarity_list = []  # polarity of job description
        self.subjectivity_list = []  # subjectivity of job description

        self.all_words = Counter() # count of all "common" words in the dataset
        self.job_data = pd.DataFrame(
        )  # all data collected, organized, and stored
        return None

    def process(self, url):
        """
        the following code accesses the website at the link and 
        extracts job information
        in: string of link to webpage
        out: raw text, processed text, job title, company
        """
        headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0',
                   'referer':'https://www.google.com'}
        page = requests.get(url,headers=headers,timeout=10.00)
        html = page.text
        page.close()
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('h1').string
        company = soup.find(
            'a', class_='topcard__org-name-link topcard__flavor--black-link'
        ).string.replace("\\n", "").strip()
        content = soup.find(
            'div',
            class_=
            'show-more-less-html__markup show-more-less-html__markup--clamp-after-5'
        )
        body_string = ''
        for x in iter(content.stripped_strings):
            body_string = body_string + x.lower()
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(body_string)
        return body_string, doc, title, company

    def create_graph_words(self, doc, title, company, saveimg=False, pos=['ADV','NOUN','VERB'],**kwargs):
        """
        The function takes a job description from LinkedIn 
        and plots the frequency of the 25 most common nouns, verbs and adverbs.
        If saveimg is true, it will also save a png of the plot created.
        in: information from process and boolean to create image
        currently kwargs must be "NOUN","ADV","VERB"
        out: tuples of (common word, count)
        """
        common_df = pd.DataFrame() # dataframe for word types
        ind = 0
        fig, axs = plt.subplots(1, len(pos), sharex=False, figsize=(16, 6))
        for wordtype in pos: # loop through strings in kwargs
            if wordtype == "ADJ" or wordtype == "ADV" or wordtype == "NOUN" or wordtype == "PRON" or wordtype == "PROPN" or wordtype == "VERB":
                # list each noun
                words = [token.lemma_ for token in doc if token.pos_ == wordtype]
                word_freq = Counter(words) # create a counter object counting all words of the part of speech in the text 
                common_words = word_freq.most_common(25) # only take the 25 most common nouns 
                word_list, word_occurrence = zip(*common_words) # zips the most common nouns in the dataset
                self.all_words.update(word_freq) # updates list of all words

                add = pd.DataFrame(common_words)
                common_df = pd.concat([common_df, add],axis=1)



            ## subplots are used for each class of nouns
        
            axs[ind].bar(x=word_list,
                       height=word_occurrence,
                       width=0.8,
                       edgecolor='#E6E6E6',
                       color=['slateblue', 'lightsalmon']) # creates third plot of verbs
            
            for label in axs[ind].get_xticklabels():
                label.set_rotation(45)
                label.set_ha('right')

            axs[ind].set_title(wordtype)
            
            ind += 1


        fig.suptitle(f'{title} @ {company}')
        fig.tight_layout()

        if saveimg:
            plt.savefig(f'job at {company}.png', facecolor='lightgrey')
        else:
            plt.show() # shows plots if not displayed

        return sorted(word_freq, key=word_freq.get, reverse=True)

    def evaluate(self, createimg=False,pos=['ADV','NOUN','VERB'],**kwargs):
        """
        This function evaluates all the links and individually graphs
        the most common words in the job description. There is also an optional
        boolean argument to save the images plotted by the graph.
        in: optional boolean to create image, false by default, and strings of the parts of speech:
        "ADV" "NOUN" "VERB"
        out: none
        """
        for link in self.links:
            # If the url no longer works due to the job listing
            # not accepting more applications, the user is notified
            # of the broken link and the loop continues.
            try:
                raw, content, title, company = self.process(link)

                self.raw_list.append(raw)
                self.content_list.append(content)
                self.title_list.append(title)
                self.company_list.append(company)
                self.polarity_list.append(TextBlob(raw).polarity)
                self.subjectivity_list.append(TextBlob(raw).subjectivity)

                self.words_list[len(self.words_list):] = [self.create_graph_words(
                                    content, title, company, createimg,pos,**kwargs)] # populate dataset lists with values counted; pass kwargs in here

            except AttributeError:
                print(f'The link {link} appears to not be working. The job listing may be down or the link may be invalid')

        zipped_data = zip(self.links, self.title_list, self.company_list,
                          self.raw_list, self.content_list, self.polarity_list,
                          self.subjectivity_list, self.words_list)
        self.job_data = pd.DataFrame(list(zipped_data),
                                     columns=[
                                         'Link', 'Job Title', 'Company',
                                         'Raw Text', 'Soup', 'Polarity',
                                         'Subjectivity', 'Words'
                                     ])
        return None

### Class that extends Job_Analysis, and has creating word cloud feature
class Cloud_Job_Analysis(Job_Analysis):
    def __init__(self, url_list):
        super().__init__(url_list) # calls super constructor

    ### Creates word cloud from the collected words in Job_Analysis class
    def make_cloud(self,saveplot=False):
        """
        in: optional saveplot boolean that saves if true
        out: none
        """
        wordcloud = WordCloud(background_color="white", width=800,height=400)
        wordcloud.generate_from_frequencies(self.all_words)
        plt.figure( figsize=(20,10) )
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        if saveplot:
            plt.savefig('frequent word cloud.png')
        else:
            plt.show()
        return None
