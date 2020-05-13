from steem import Steem
from pick import pick
import pprint
import json

s = Steem()

query = {
        "limit":100, #number of posts
        "tag":"python" #tag of posts
        }
    #post list for selected query
posts = s.get_discussions_by_created(query)

title = 'Please choose post: '
options = []
#posts list options
string = ""
i =0
for post in posts:
    options.append(post["author"]+'/'+post["permlink"])

    details = s.get_content(post["author"],post["permlink"])

    # text_file = open('steem_posts.txt','wt')
    # n = text_file.write(str(details))
    # text_file.close()

    
    string += json.dumps(details,indent=4)
    string += '\n\n'
    # print(string)
    


    # pprint.pprint(details)
    # pprint.pprint("Selected: ")
    print('Post '+str(i)+' details collected!')
    i+=1
print("Dumping into text file ... ")    
text_file = open('steem_posts2.txt','wt')
n = text_file.write(string)
text_file.close()
print("Scraping Complete!")
# get index and selected filter name
# option, index = pick(options, title)
