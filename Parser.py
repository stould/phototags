import json

token =  "CAACEdEose0cBACOfZAOdlkn06Ls8TU9NQSZBb3MxRj3pAjSssODY0El7ygKexnkCIgf5QFlYORoONxJMtK0XmgBotJusl42GZBYZB9K2ysZBnq0tUoYag8IK57N3rlR0ki2USxUWSMERyoSjijVgqkFN9CKZCOVAM7eOOJbUUi9ZCJZCaPiBGWCleYu9RyZCntZA6aGvPupETYUcBQAQAZCI2BlnPDtV5WMyZAAZD"
url = "graph.facebook.com"
id = "me"

def readCommentary(data, tags):
        m = len(data.comments)
        for j in range(m):
                msg = data.comments[j]
        found = 0
        sz = len(data.comments[j])
        for k in range(sz):
            sz2 = len(data.comments[j].data)
            for l in range(sz2):
                msg = data.comments[j].data[l].message
                for index in range(len(tags)):
                    if(msg.find(tags[index])):
                        return 1
        return 0

def readDescription(data, tags):
        for i in range (len(tags)):
                if data.name.find(tags[i]):
                        return 1
        return 0


def parse(data, tags):
    obj = json.loads(data)
    n = len(obj['data'])
    ans = []
    for i in range(n):
        # Seeking for comments who have 'tags' inside
        if(readCommentary(obj['data'][i], tags)):
            link = obj['data'][i].link
            source = obj['data'][i].source
            v = {"link": link, "source": source}
            ans.append(v)
                # Seeking for image descriptions who have 'tags' inside
        if(readDescription(obj['data'][i], tags)):
            link = obj['data'][i].link
            source = obj['data'][i].source
            v = {"link": link, "source": source}
            ans.append(v)
    return json.dumps(ans)
