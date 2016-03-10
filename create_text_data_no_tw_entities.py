#!/usr/bin/env python2

"""Dump 1 million tweets (raw text) to a file from mongo.  So they
can be read line by line without needing to involve mongo"""


import codecs
from pymongo import MongoClient
import re


__author__ = 'Eric Lind'


COLLECTIONS = ['twitter1_bad_entities', 'twitter2']
TW_ENT_PATTERN = re.compile(r"(?:\A|\s)(?:@|#)\w+", re.U)
URL_PATTERN = re.compile(r"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)", re.U)


# Get connection
conn = MongoClient()
db = conn['synapsify']


# Get cursors and write the file
with codecs.open('tweets_no_tw_ents.txt', mode='a+', encoding='utf-8') as _f:
    total = 0

    for c in COLLECTIONS:
        cursor = db[c].find({}, projection={'text': True}).limit(505000)  # Add a few extra

        for tw in cursor:
            if 'text' in tw:
                if total % 10000 == 0:
                    print "On tweet %s" % total

                # Remove newlines
                txt = tw['text'].replace('\n', ' ')
                txt = TW_ENT_PATTERN.sub(' ', txt)
                txt = URL_PATTERN.sub(' ', txt)
                txt = txt.strip()

                # Write to file
                if txt:
                    _f.write(txt + '\n')

                total += 1


print "DONE"

