import os
import uuid

import requests
import json


def test_grammar():
    # BASE_URL = os.getenv('BASE_URL')
    # assert BASE_URL is not None

    res = requests.get('http://35.239.61.25:5000/grammar?uuid=c2881c71-d4f5-40b1-b83f-da2426fd5067')
    actual=json.loads(res.text)

    grammar1={"message": "Put a space after the comma, but not before the comma", "shortMessage": "", "replacements": [{"value": ","}], "offset": 9, "length": 2, "context": {"text": "And first , I have to reply to the older charges an...", "offset": 9, "length": 2}, "sentence": "And first , I have to reply to the older charges and to my first accusers , and then I will go to the later ones .", "type": {"typeName": "Other"}, "rule": {"id": "COMMA_PARENTHESIS_WHITESPACE", "description": "Use of whitespace before comma and before/after parentheses", "issueType": "whitespace", "category": {"id": "TYPOGRAPHY", "name": "Typography"}}}
    grammar2={"message": "Put a space after the comma, but not before the comma", "shortMessage": "", "replacements": [{"value": ","}], "offset": 73, "length": 2, "context": {"text": "...e older charges and to my first accusers , and then I will go to the later ones . ...", "offset": 43, "length": 2}, "sentence": "And first , I have to reply to the older charges and to my first accusers , and then I will go to the later ones .", "type": {"typeName": "Other"}, "rule": {"id": "COMMA_PARENTHESIS_WHITESPACE", "description": "Use of whitespace before comma and before/after parentheses", "issueType": "whitespace", "category": {"id": "TYPOGRAPHY", "name": "Typography"}}}
    
    assert grammar1 in actual
    assert grammar1 in actual
    
test_grammar()

def test_search():
    # BASE_URL = os.getenv('BASE_URL')
    # assert BASE_URL is not None

    res = requests.get('http://35.239.61.25:5000/search?text=google')
    actual=json.loads(res.text)

    search1={"_index": "ocr_texts", "_type": "_doc", "_id": "QtXXSnYBTdRn14gy_Djb", "_score": 1.0, "_source": {"uuid": "32c3cf5d-c6e6-4e8e-9c26-9ac68a0ad5a0", "ocr_text": "1. API interfaces : Flask to provide an API interface to the front - end , Cloud Storage  API , Cloud Vision API , grammarbot API - We will be developing a Flask API for data transfer and communication . Apart from this , we will be making use of several GCP APIs for making use of Google's services programmatically .  \n\n2. Storage Services : Google Cloud Storage for image storage - The image of the  handwritten document uploaded by the users will be stored using Cloud Storage . This will also allow users to keep a digital history of their documents .  \n\n3. Databases : Elasticsearch for indexing the extracted text data to provide search  feature - This elasticsearch instance will be deployed on GCP . We're making use of Elasticsearch instead of some other cloud database services since Elasticsearch provides extremely fast keyword based search .  \n\n4. Message Queues : Kafka to act as a queue for search queries - all search  queries will be first enqueued into Kafka and then dequeue one by one as the results obtained from Elasticsearch are returned to the front - end .  \n\n5. Containers , VMs : All components of our pipeline such as Flask service ,  Elasticsearch , Message Queues etc. , will be run as containers with Kubernetes as our orchestration platform - We'll be relying on GCP's GKE service for deploying a Kubernetes cluster . All components of the project will be dockerized and deployed on the cluster .  \n\n"}}
    search2={"_index": "ocr_texts", "_type": "_doc", "_id": "Q9XZSnYBTdRn14gymjif", "_score": 1.0, "_source": {"uuid": "abc03bb3-1e10-43e5-9998-3c43d8ec7071", "ocr_text": "Google Cloud  \n\nPlatform  \n\n"}}
    
    assert search1 in actual
    assert search2 in actual
    
test_search()


def test_search_empty():
    # BASE_URL = os.getenv('BASE_URL')
    # assert BASE_URL is not None

    res = requests.get('http://35.239.61.25:5000/search?text=')
    actual=json.loads(res.text)

    expected = [{"_index": "ocr_texts", "_type": "_doc", "_id": "QdXXSnYBTdRn14gyITgA", "_score": 1.0, "_source": {"uuid": "c2881c71-d4f5-40b1-b83f-da2426fd5067", "ocr_text": "And first , I have to reply to the older charges and to my first accusers , and then I will go to the later ones . For I have had many accusers , who accused me of old , and their false charges have continued during many years ; and I am more afraid of them than of Anytus and his associates , who are dangerous , too , in their own way . But far more dangerous are these , who began when you were children , and took possession of your minds with their falsehoods , telling of one Socrates , a wise man , who speculated about the heaven above , and searched into the earth beneath , and made the worse appear the better cause . These are the accusers whom I dread ; for they are the circulators of this rumor , and their hearers are too apt to fancy that speculators of this sort do not believe in the gods . And they are many , and their charges against me are of ancient date , and they made them in days when you were impressible - in childhood , or perhaps in youth - and the cause when heard went by default , for there was none to answer . And , hardest of all , their names I do not know and cannot tell ; unless in the chance of a comic poet . But the main body of  \n\n"}}, {"_index": "ocr_texts", "_type": "_doc", "_id": "QtXXSnYBTdRn14gy_Djb", "_score": 1.0, "_source": {"uuid": "32c3cf5d-c6e6-4e8e-9c26-9ac68a0ad5a0", "ocr_text": "1. API interfaces : Flask to provide an API interface to the front - end , Cloud Storage  API , Cloud Vision API , grammarbot API - We will be developing a Flask API for data transfer and communication . Apart from this , we will be making use of several GCP APIs for making use of Google's services programmatically .  \n\n2. Storage Services : Google Cloud Storage for image storage - The image of the  handwritten document uploaded by the users will be stored using Cloud Storage . This will also allow users to keep a digital history of their documents .  \n\n3. Databases : Elasticsearch for indexing the extracted text data to provide search  feature - This elasticsearch instance will be deployed on GCP . We're making use of Elasticsearch instead of some other cloud database services since Elasticsearch provides extremely fast keyword based search .  \n\n4. Message Queues : Kafka to act as a queue for search queries - all search  queries will be first enqueued into Kafka and then dequeue one by one as the results obtained from Elasticsearch are returned to the front - end .  \n\n5. Containers , VMs : All components of our pipeline such as Flask service ,  Elasticsearch , Message Queues etc. , will be run as containers with Kubernetes as our orchestration platform - We'll be relying on GCP's GKE service for deploying a Kubernetes cluster . All components of the project will be dockerized and deployed on the cluster .  \n\n"}}, {"_index": "ocr_texts", "_type": "_doc", "_id": "Q9XZSnYBTdRn14gymjif", "_score": 1.0, "_source": {"uuid": "abc03bb3-1e10-43e5-9998-3c43d8ec7071", "ocr_text": "Google Cloud  \n\nPlatform  \n\n"}}, {"_index": "ocr_texts", "_type": "_doc", "_id": "RNXgSnYBTdRn14gyFzga", "_score": 1.0, "_source": {"uuid": "6af7cd49-9600-4f5c-a773-025dfa6b43c0", "ocr_text": "Planet POF  \n\nCHAPTER ONE  THE EVE OF THE WAR No one would have believed in the last years of the incercely but this world was being watched keenly and closely by intelligences greater than man's and yet as mental as his contras men besied themelves about their various concerns they were scrutinised and studied . perhaps almost as namonly as a man with a mimos might line the transient creatures the swaandiply is a drop of water . With infinite complacency men went and freever this globe about their little liars , Seres in their curance of their empire over matter . It is possible that the infusoria under the microscope do the same . No one gave a thought to the  \n\n"}}, {"_index": "ocr_texts", "_type": "_doc", "_id": "RdXlSnYBTdRn14gyuzj1", "_score": 1.0, "_source": {"uuid": "0ac34e3a-c02f-4fa1-b548-94a31b022f83", "ocr_text": "Google Cloud  \n\nPlatform  \n\n"}}, {"_index": "ocr_texts", "_type": "_doc", "_id": "RtUfS3YBTdRn14gyZDiI", "_score": 1.0, "_source": {"uuid": "8b12960e-cfd3-4421-8a2e-a416f3135917", "ocr_text": "THIS IS AN EXAMPLE OF MY ACTUAL HAND WRITING . I PRINT THIS WAY . BECAUSE M\u0173 CURSIVE IS VIRTUALLY UNREADABLE .  \n\nAND THIS IS AN EXAMPLE OF MY CUSTOM COMPUTER FONT NOT MUCH MORE READABLE THAN MY HANDWRITING , BUT WAY FASTER AND EASIER TO EDIT . PRETTY COOL , RIGHT ?  \n\n"}}, {"_index": "ocr_texts", "_type": "_doc", "_id": "R9UiS3YBTdRn14gyBDhw", "_score": 1.0, "_source": {"uuid": "ae7c8475-d45a-42e0-9682-24fcc18ad1e3", "ocr_text": "My favorite movie is the Notebook I'm So this movie \u00f1 times and the 5 time cryed for the beautiful history this movie and the titanic .  are my favorite because are very romantic , and teach that the love is perfect and when any person love to other person every is possible is not in portant of the family don't like the Irelation , the film the Notebook \" teachine that the true love is possible I have  other category to movie that I like is commedy because ore funny and more the movies to ny octors favorites : Ryan Goggly Adam Samko , leonardo Dicrapio , Jennifer Aniston , Angelina Jolie And brat Pitt . All lomous actors of my favorites move .  \n\n"}}, {"_index": "ocr_texts", "_type": "_doc", "_id": "SNUjS3YBTdRn14gyTziz", "_score": 1.0, "_source": {"uuid": "bba23537-9f0d-4b9f-acd1-caa079842daa", "ocr_text": "Date : 31. Oct.2019  \n\naw  \n\n\u0441 causes of \uc544  \n\nink . pen  \n\nan  \n\nDear Diary This is a test to see if the ink  impression on the other side the page . as what I am  what I am using is I feel if one has to make his hes handwriting look beautiful , use an ink pen . or it can also be used if one wants to improve ones handwriting . I My only fear is , what if  day water gets chilled oves my book ( ope its a worst cast scenario )  memories would actually get washed away  \n\nall m \u043c  \n\n.  \n\n"}}]
    
    assert len(expected) == len(actual)
    
test_search_empty()



