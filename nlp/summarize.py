# nlp_utils/summarize.py
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from nltk.tokenize import sent_tokenize

def extractive_summarization(text, method='textrank', sentences_count=3):
    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = TextRankSummarizer() if method == 'textrank' else LsaSummarizer()
        summary = summarizer(parser.document, sentences_count)
        return ' '.join([str(s) for s in summary])
    except:
        return ' '.join(sent_tokenize(text)[:3])
