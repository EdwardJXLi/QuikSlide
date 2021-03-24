import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from rake_nltk import Rake

from flask import jsonify

import requests
import os
import uuid
import re

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from serpapi import GoogleSearch

from app.process.slides import Slides

class Process:
    def __init__(self, text): 
        self.text = ''.join([' ' if c in ('\n', '\r', '\t') else c for c in text.encode("ascii", "ignore").decode()])
        raise NotImplementedError("Fill In The Azure Credentials Here!!!")
        ta_credential = AzureKeyCredential(None)  # FILL THIS IN!!!
        text_analytics_client = TextAnalyticsClient(endpoint="https://quickslide-textanalytics.cognitiveservices.azure.com/",  credential=ta_credential)
        self.azureClient = text_analytics_client
    
    def summarize(self, TOLERANCE=1.1):
        stop_words = set(stopwords.words("english"))
        words = word_tokenize(self.text)
        word_freq = dict()

        for word in words:
            word = word.lower()
            if not word in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        sentences = sent_tokenize(self.text)
        sent_value = dict()

        for sentence in sentences:
            for word in word_tokenize(sentence):
                if word in word_freq:
                    sent_value[sentence] = sent_value.get(sentence, 0) + word_freq[word]
        
        val_tot = sum(sent_value.values())
        average = val_tot / len(sent_value)
        
        summary = [sentence for sentence in sentences if sent_value.get(sentence, 0) > (TOLERANCE * average)]
        return summary

    #def tokenize(self, text=None, LIMIT=10):
    def tokenize_old(self, text=None, LIMIT=10):
        stop_words = set(stopwords.words("english"))
        words = word_tokenize(self.text)
        word_freq = dict()

        for word in words:
            word = word.lower()
            if not word in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1

        if text is None:
            text = self.text
        r = Rake()
        r.extract_keywords_from_text(text)
        tk = dict()

        for kw in r.get_ranked_phrases():
            val = 0
            for word in word_tokenize(kw):
                if word in word_freq:
                    val += word_freq[word]
            tk[kw] = val // len(word_tokenize(kw))

        return [''.join([c for c in kw if c.isalnum() or c == ' ']) for kw in sorted(tk, key=tk.get, reverse=True)][:LIMIT]

    def tokenize(self, text=None, LIMIT=10):
        try:
            if not text:
                text = self.text

            documents = [text]
            response = self.azureClient.extract_key_phrases(documents=documents)[0]

            if not response.is_error:
                return response.key_phrases[:LIMIT]
                # stop_words = set(stopwords.words("english"))
                # words = word_tokenize(self.text)
                # word_freq = dict()
                # tk = dict()

                # for word in words:
                #     word = word.lower()
                #     if not word in stop_words:
                #         word_freq[word] = word_freq.get(word, 0) + 1

                # for kw in response.key_phrases[:LIMIT]:
                #     val = 0
                #     for word in word_tokenize(kw):
                #         if word in word_freq:
                #             val += word_freq[word]
                #     tk[kw] = val // len(word_tokenize(kw))

                # return [''.join([c for c in kw if c.isalnum() or c == ' ']) for kw in sorted(tk, key=tk.get, reverse=True)]
            else:
                raise Exception(response.id, response.error)

        except Exception as err:
            raise Exception("Encountered exception. {}".format(err))

    def get_image(self, keyword):
        for _ in range(5):
            try:
                print("RUNNING SEARCH " + keyword)
                raise NotImplementedError("Fill In The SerpAPI Credentials Here!!!")
                params = {
                    'q' : keyword,
                    'tbm': 'isch',
                    'ijn': 0,
                    'api_key': None
                }
                search = GoogleSearch(params)
                results = search.get_dict()
                images_results = results['images_results']
                # print(results)
                if len(results['images_results']) > 0:
                    print(f"SEARCH: {keyword} | NUMRES: {len(results['images_results'])} | RET: {results['images_results'][0]['original']}")
                    return results['images_results'][0]['original']
                else:
                    return None

                # print("RUNNING SEARCH " + keyword)
                # raise NotImplementedError("Fill In The Bing Credentials Here!!!")
                # subscription_key = None
                # search_url = "https://api.bing.microsoft.com/v7.0/images/search"
                # search_term = keyword
                # headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
                # params  = {"q": search_term, "license": "any", "imageType": "photo"}
                # response = requests.get(search_url, headers=headers, params=params)
                # response.raise_for_status()
                # search_results = response.json()
                # if len(search_results["value"]) != 0:
                #     print(f"SEARCH: {keyword} | NUMRES: {len(search_results['value'])} | RET: {search_results['value'][0]['contentUrl']}")
                #     if search_results["value"][0]["contentUrl"] == "https://www.goodfreephotos.com/albums/people/barack-obama-portrait-photo.jpg":
                #         print("pass")
                #         return None
                #     return search_results["value"][0]["contentUrl"]
                # else:
                #     return None
            except requests.exceptions.ConnectionError:
                print("FAIL TRYING AGAIN")
        raise Exception("Connection Failed :(")
    
    def process(self, email, name, slide_title, CHAR_LIMIT=512):
        summary = self.summarize()
        slides = Slides()
        if slide_title is None:
            keywords = self.tokenize_old(' '.join(re.split(r'(?<=[.:;])\s', self.text)[:2]))
            slide_title = keywords[0].title()
            slides.create(slide_title)
        else:
            slides.create(slide_title.title())
        slides.share(email)

        self.name = slide_title
        self.link = "https://docs.google.com/presentation/d/%s/" % slides.id

        req = [
            {
                'insertText': {
                    'objectId': 'i0',
                    'insertionIndex': 0,
                    'text': slide_title
                }
            },
            {
                'insertText': {
                    'objectId': 'i1',
                    'insertionIndex': 0,
                    'text': name.title()
                }
            },
        ]
        
        pt350 = {
            'magnitude': 350,
            'unit': 'PT'
        }
        emu4M = {
            'magnitude': 4000000,
            'unit': 'EMU'
        }

        v = set()
        pages = 0
        EXIT = 0

        # for i in range(0, len(summary), 3):
        #     points = summary[i:i + 3]
        while summary:
            pages += 1
            if pages > 100:
                raise Exception()
            
            points = []
            count = len(summary[0])
            points.append(summary.pop(0))

            while summary:
                if count + len(summary[0]) < CHAR_LIMIT:
                    EXIT += 1
                    if EXIT > 100:
                        raise Exception()
                    count += len(summary[0])
                    points.append(summary.pop(0))
                else:
                    break

            kwd = self.tokenize(' '.join(points))

            for t in kwd:
                if t not in v:
                    title = t.title()
                    image_q = title.strip().lower()
                    if slide_title.lower() not in image_q:
                        image_q += " " + slide_title.lower()
                    image = self.get_image(image_q)
                    # image = None
                    v.add(title)
                    break
            else:
                title = '[ADD TITLE]'
                image = None

            if not image:
                # raise NotImplementedError("TODO")
                image = "https://via.placeholder.com/360x360"
            
            page_id = str(uuid.uuid4())
            unique_image_id = str(uuid.uuid4())
            layout = 'TITLE_AND_TWO_COLUMNS'

            title_id = page_id + "__title"
            col_1 = page_id + "__col1"
            col_2 = page_id + "__col2"

            req += list(reversed([
                {
                    'createSlide': {
                        'objectId': page_id,
                        'insertionIndex': 1, 
                        'slideLayoutReference': {
                            'predefinedLayout': layout
                        },
                        "placeholderIdMappings": [
                            {
                                "objectId": title_id,
                                "layoutPlaceholder": {
                                    'type' : 'TITLE',
                                    'index': 0
                                },
                            },
                            {
                                "objectId": col_1,
                                "layoutPlaceholder": {
                                    'type' : 'BODY',
                                    'index': 0
                                },
                            },
                            {
                                "objectId": col_2,
                                "layoutPlaceholder": {
                                    'type' : 'BODY',
                                    'index': 1
                                }
                            }
                        ]
                    }
                },
                {
                    'insertText': {
                        'objectId': title_id,
                        'insertionIndex': 0,
                        'text': title
                    }
                },
                {
                    'insertText': {
                        'objectId': col_1,
                        'insertionIndex': 0,
                        'text': '\t\n'.join([point[:-1] for point in points])
                    }
                },
                {
                    'createParagraphBullets': {
                        'objectId': col_1,
                        'textRange': {
                            'type': 'ALL'
                        },
                        'bulletPreset' : 'BULLET_ARROW_DIAMOND_DISC'
                    }
                },
                {
                    'insertText': {
                        'objectId': col_2,
                        'insertionIndex': 0,
                        'text': unique_image_id
                    }
                },
                {
                    "replaceAllShapesWithImage": {
                        "imageReplaceMethod": "CENTER_INSIDE",
                        "pageObjectIds": [
                            page_id
                        ],
                        "containsText": {
                            "text": unique_image_id,
                            "matchCase": False
                        },
                        "imageUrl": image
                    }
                }

            ]))

        # print(list(reversed(req)))
        slides.update(list(reversed(req)))
