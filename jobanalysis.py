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
        self.nouns_list = []  # (noun, count) tuples
        self.verbs_list = []  # (verb, count) tuples
        self.adverbs_list = []  # (adverb, count) tuples
        self.polarity_list = []  # polarity of job description
        self.subjectivity_list = []  # subjectivity of job description
        self.all_nouns = Counter() # count of all nouns in the dataset
        self.all_verbs = Counter() # count of all verbs in the dataset
        self.all_adverbs = Counter() # count of all adverbs in the dataset
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
        headers = {'user-agent':'Mozilla/5.0 (X11; CrOS x86_64 14469.41.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.57 Safari/537.36',
                   'referer':'https://www.google.com'}
        page = requests.get(url,headers=headers)
        html = page.text
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

    def create_graph_words(self, doc, title, company, saveimg=False, **kwargs):
        """
        The function takes a job description from LinkedIn 
        and plots the frequency of the 25 most common nouns, verbs and adverbs.
        If saveimg is true, it will also save a png of the plot created.
        in: information from process and boolean to create image
        currently kwargs must be "NOUN","ADV","VERB"
        out: tuples of (common word, count)
        """

        for key in kwargs: # loop through strings in kwargs
            if key == "NOUN":
                # list each noun
                nouns = [token.lemma_ for token in doc if token.pos_ == "NOUN"]
                noun_freq = Counter(nouns) # create a counter object counting all nouns in the text 
                self.all_nouns.update(noun_freq) # update the dataset list of all nouns
                common_nouns = noun_freq.most_common(25) # only take the 25 most common nouns 
                noun_list, noun_occurrence = zip(*common_nouns) # zips the most common nouns in the dataset
                self.all_words.update(noun_freq) # updates list of all words

                
            if key == "ADV":
                adverbs = [token.lemma_ for token in doc if token.pos_ == "ADV"]
                adverb_freq = Counter(adverbs)
                self.all_adverbs.update(adverb_freq)
                common_adverbs = adverb_freq.most_common(25)
                adverb_list, adverb_occurrence = zip(*common_adverbs)
                self.all_words.update(adverb_freq) # updates list of all words
            
            if key == "VERB":
                verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]
                verb_freq = Counter(verbs)
                self.all_verbs.update(verb_freq)
                common_verbs = verb_freq.most_common(25)
                verb_list, verb_occurrence = zip(*common_verbs)
                self.all_words.update(verb_freq) # updates list of all words
        

        ## subplots are used for each class of nouns
        
        if len(kwargs) > 2:

            fig, axs = plt.subplots(1, 3, sharex=False, figsize=(16, 6))

            axs[0].bar(x=adverb_list,
                       height=adverb_occurrence,
                       width=0.8,
                       edgecolor='#E6E6E6',
                       color=['teal', 'mediumorchid']) # creates first plot of adverbs
            axs[1].bar(x=noun_list,
                       height=noun_occurrence,
                       width=0.8,
                       edgecolor='#E6E6E6',
                       color=['tomato', 'steelblue']) # creates second plot of adverbs
            axs[2].bar(x=verb_list,
                       height=verb_occurrence,
                       width=0.8,
                       edgecolor='#E6E6E6',
                       color=['slateblue', 'lightsalmon']) # creates third plot of verbs

            for label in axs[0].get_xticklabels():
                label.set_rotation(45)
                label.set_ha('right')

            for label in axs[1].get_xticklabels():
                label.set_rotation(45)
                label.set_ha('right')

            for label in axs[2].get_xticklabels():
                label.set_rotation(45)
                label.set_ha('right')

            axs[0].set_title('Adverbs')
            axs[1].set_title('Nouns')
            axs[2].set_title('Verbs')

            fig.suptitle(f'{title} @ {company}')
            fig.tight_layout()

            if saveimg:
                plt.savefig(f'job at {company}.png', facecolor='lightgrey')
            else:
                plt.show() # shows plots if not displayed

        return common_adverbs, common_nouns, common_verbs
    
    def make_cloud(self):
        wordcloud = WordCloud(background_color="white", width=800,height=400)
        wordcloud.generate_from_frequencies(self.all_words)
        plt.figure( figsize=(20,10) )
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.savefig('frequent word cloud.png')
        plt.show()
        return None

    def evaluate(self, createimg=False,**kwargs):
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

                self.adverbs_list[len(self.adverbs_list):], self.nouns_list[
                    len(self.nouns_list
                        ):], self.verbs_list[len(self.verbs_list):] = tuple(
                            zip(
                                self.create_graph_words(
                                    content, title, company, createimg,**kwargs))) # populate dataset lists with values counted; pass kwargs in here

                #self.adverbs_list.append(adverbs)
                #self.nouns_list.append(nouns)
                #self.verbs_list.append(verbs)

            except AttributeError:
                print(f'The link {link} appears to not be working. The job listing may be down or the link may be invalid')

        zipped_data = zip(self.links, self.title_list, self.company_list,
                          self.raw_list, self.content_list, self.polarity_list,
                          self.subjectivity_list, self.adverbs_list,
                          self.nouns_list, self.verbs_list)
        self.job_data = pd.DataFrame(list(zipped_data),
                                     columns=[
                                         'Link', 'Job Title', 'Company',
                                         'Raw Text', 'Soup', 'Polarity',
                                         'Subjectivity', 'Adverbs', 'Nouns',
                                         'Verbs'
                                     ])
        return None
