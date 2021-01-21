# !pip install hazm

import re, hazm, nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

nltk.download("wordnet")
nltk.download("stopwords")


class Preprocess:
    def __init__(self, data):
        is_fa = data["language"] == "fa"
        fa_data = data[is_fa]
        self.fa_data = self.clean_fa(fa_data)

        is_en = data["language"] == "en"
        en_data = data[is_en]
        self.en_data = self.clean_en(en_data)

    def clean_fa(self, data):
        data.text = self.fa_normalize(data.text)
        data.text = self.tokenizer(data.text)

        stemmer = hazm.Stemmer()
        lemmatizer = hazm.Lemmatizer()
        stopwords = hazm.stopwords_list()
        alphabet = set(list("آابپتثجچحخدذرزژسشصضطظعغفقکگلم‌ن‌وهی"))

        data.text = data.apply(
            lambda row: self.stemLemmaStopWord(
                stemmer, lemmatizer, stopwords, alphabet, row.text
            ),
            axis=1,
        )
        return data

    def clean_en(self, data):
        data.text = self.normalize(data.text)
        data.text = self.tokenizer(data.text)

        stemmer = PorterStemmer()
        lemmatizer = WordNetLemmatizer()
        stopwords = set(stopwords.words("english"))
        alphabet = set(list("abcdefghijklmnopqrstuvwxyz"))

        data.text = data.apply(
            lambda row: self.stemLemmaStopWord(
                stemmer, lemmatizer, stopwords, alphabet, row.text
            ),
            axis=1,
        )
        return data

    def tokenizer(self, text):
        text = text.str.split(" ")
        return text

    def stemLemmaStopWord(self, stemmer, lemmatizer, stopwords, alphabet, tokens):
        final_tokens = []
        for token in tokens:
            stemmed_token = stemmer.stem(lemmatizer.lemmatize(token))
            if "#" in stemmed_token:
                stemmed_token = stemmed_token.split("#")[0]
            if (
                token not in stopwords
                and stemmed_token not in stopwords
                and not token == ""
                and stemmed_token not in alphabet
            ):
                final_tokens.append(stemmed_token)
        return final_tokens

    def fa_normalize(self, text):
        text = text.replace(to_replace=r"[ئيی]", value="ی", regex=True)
        text = text.replace(to_replace=r"[ك]", value="ک", regex=True)
        text = text.replace(to_replace=r"[ؤ]", value="و", regex=True)
        text = text.replace(to_replace=r"[ة]", value="ه", regex=True)
        text = text.replace(to_replace=r"[إأآا]", value="ا", regex=True)
        text = text.replace(
            to_replace=r"[^آابپتثجچحخدذرزژسشصضطظعغفقکگلم‌ن‌وهی]", value=" ", regex=True
        )
        text = text.replace(to_replace=r"(.)\1+", value=r"\1", regex=True)
        text = text.replace(to_replace=r"[^\S\n\t]+", value=" ", regex=True)
        return text

    def en_normalize(self, text):
        text = text.replace(to_replace=r"@([A-Za-z0-9_]+)", value="", regex=True)
        text = text.replace(to_replace=r"http([^\s\\]+)", value="", regex=True)
        text = text.str.lower()
        text = text.replace(to_replace=r"[^a-z]", value=" ", regex=True)
        text = text.replace(to_replace=r"(.)\1+", value=r"\1", regex=True)
        text = text.replace(to_replace=r"[^\S\n\t]+", value=" ", regex=True)
        return text

