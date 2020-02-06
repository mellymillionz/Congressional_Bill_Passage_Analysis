import spacy
from spacy.lang.en import English
from spacy.lang.en import en_core_web_sm
import string
import re

# Create our list of stopwords

class Tokenizer:

    def __init__(self):

        self.nlp = spacy.load('en_core_web_sm')

        self.nlp.Defaults.stop_words |= {"bill","amend", "purpose", "united", "state", "states", "secretary", "act", "federal", "provide"}

        self.replace_with_space = re.compile('[/(){}\[\]\|@,;]')

        self.just_words = re.compile('[^a-zA-Z\s]')

        # Create our list of punctuation marks
        self.punctuations = string.punctuation

        self.stop_words = spacy.lang.en.stop_words.STOP_WORDS


    def tokenizer(self, text):
        
        #lowercase everything
        lower_text = text.lower()
        
        #remove punctuation
    #     no_pun_text = lower_text.translate(str.maketrans('', '', string.punctuation))
        
        #get rid of weird characters
        text = self.replace_with_space.sub('',lower_text)
        
        #remove numbers
        just_words_text = self.just_words.sub('', text)
        
        #add spacy tokenizer
        mytokens = self.nlp(just_words_text, disable=['parser', 'ner'])
    #     print(mytokens)
        
        #for POS tagging
    #     mytokens = [word for word in mytokens if (word.pos_ == 'NOUN') or (word.pos_ == 'VERB') or (word.pos_ == 'ADJ') or (word.pos_ == 'ADV')]
        
        #lemmatize
        mytokens = [word.lemma_.strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens ]
        
        #MAP SPECIFIC WORDS to others (veteran from veterans)

        #add stopwords
        mytokens = [word for word in mytokens if word not in self.stop_words and word not in self.punctuations]
        
        return mytokens
    
