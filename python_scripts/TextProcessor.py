import re
import nltk


class TextProcessor:
    
    def __init__(self, string):
        self.string = string
        self.pstring = []
        self.cstring = None
        self.tstring = []
        
    def remove_emojis(self):
        emoj = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002500-\U00002BEF"  # chinese char
            u"\U00002702-\U000027B0"
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            u"\U0001f926-\U0001f937"
            u"\U00010000-\U0010ffff"
            u"\u2640-\u2642" 
            u"\u2600-\u2B55"
            u"\u200d"
            u"\u23cf"
            u"\u23e9"
            u"\u231a"
            u"\ufe0f"  # dingbats
            u"\u3030"
            u"\u203c"
            "]+", re.UNICODE)
        self.cstring = re.sub(emoj, '', self.string)
        return self

    def split_sentences(self):
        self.tstring = nltk.sent_tokenize(self.cstring)
        return self
    
    def cut_outliers(self):
        for s in self.tstring:
            if(s != None):
                if(len(s) > 4):
                    self.pstring.append(s)

    def process_text(self):
        self.remove_emojis().split_sentences().cut_outliers()
        return self.pstring
