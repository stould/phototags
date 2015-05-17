#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

LIM = 500


def threadTag(tag):
    return tag.lower()


def readCommentary(data, tags):
    if not 'comments' in data:
        return False
    n = len(tags)
    m = len(data['comments']['data'])

    seen = set()

    for i in range(m):
        msg = ''
        try:
            msg = data['comments']['data'][i]['message']
        except:
            continue
        for j in tags:
            if msg.lower().find(j.lower()) != -1:
                seen.add(j.lower())
    return seen


def readDescription(data, tags):
    if not 'name' in data:
        return False
    seen = set()
    for i in tags:
        if not 'name' in data:
            continue
        if data['name'].lower().find(i.lower()) != -1:
            seen.add(i.lower())
    return seen


def readTaggedNames(data, tags):
    if not 'tags' in data:
        return set()
    n = len(data['tags']['data'])
    seen = set()
    for i in range(n):
        name = data['tags']['data'][i]['name']
        for j in range(len(tags)):
            if name.lower().find(tags[j].lower()) != -1:
                seen.add(tags[j].lower())
    return seen


def seekImage(data, DIFF):
    n = len(data)
    for i in range(n):
        height = data[i]['height']
        width = data[i]['width']
        source = data[i]['source']
        if abs(LIM - height) <= DIFF and abs(LIM - width) <= DIFF:
            return source
    return None


# binary search the images to get the nearest to 500x500

def binarySearchImage(obj, i):
    lo = 0
    hi = 500
    small = 99999
    bestImage = None
    while lo <= hi:
        mid = (lo + hi) // 2
        seeked = seekImage(obj['data'][i]['images'], mid)
        if seeked != None:
            if mid < small:
                small = mid
                bestImage = seeked
            hi = mid - 1
        else:
            lo = mid + 1
    return bestImage


def parse(data, tags):
    obj = json.loads(data)
    n = len(obj['data'])
    ans = []
    for i in range(n):

        # Seeking for comments who have 'tags' inside

        seen = set()
        seen = seen + readCommentary(obj['data'][i], tags)
        seen = seen + readDescription(obj['data'][i], tags)
        seen = seen + readTaggedNames(obj['data'][i], tags)

        if len(seen) == len(tags):
            link = obj['data'][i]['link']
            v = {'link': link, 'source': binarySearchImage(obj, i),
                 'type': 'tagged in photo'}
            ans.append(v)
    return ans



			
