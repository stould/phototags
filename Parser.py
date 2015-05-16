import json

def readCommentary(data, tags):
        m = len(data['comments']['data'])
        for i in range(m):
                try:
                        msg = data['comments']['data'][i]['message']
                except:
                        return False;
                for j in tags:
                    if msg.find(j) != -1:
                            return True
        return False
                

def readDescription(data, tags):
        try:
                for i in tags:
                        if data['name'] and data['name'].find(i) != -1:
                                return 1
        except:
                return 0
    

def parse(data, tags):
    obj = json.loads(data)
    n = len(obj['data'])
    ans = []
    for i in range(n):
        # Seeking for comments who have 'tags' inside
        if readCommentary(obj['data'][i], tags):
            link = obj['data'][i]['link']
            source = obj['data'][i]['source']
            v = {"link": link, "source": source}
            ans.append(v)
            # Seeking for image descriptions who have 'tags' inside
            return json.dumps(ans)
"""        if readDescription(obj['data'][i], tags):
            link = obj['data'][i]['link']
            source = obj['data'][i]['source']
            v = {"link": link, "source": source}
            ans.append(v)
"""

