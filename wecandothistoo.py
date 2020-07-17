import praw
import re
from datetime import datetime
import jsonpickle

reddit = praw.Reddit(                   #random user to access r/all
    client_id='xxxxxx',
    client_secret ="xxxxxx",
    username="xxxxxx",
    password="xxxxxx",
    user_agent="WeCanDoThisToo"
)

reddit2 = praw.Reddit(                #user that has acces to r/wecandothistoo and can remove/add contributers
    client_id='xxxxxx',
    client_secret ="xxxxxx",
    username="xxxxxx",
    password="xxxxxx",
    user_agent="WeCanDoThisToo2"
)
class WCDT2user:                    #custom class to save users
    def __init__(self, username, timejoined, lastaction, status):
        self.username =  username
        self.timejoined = timejoined
        self.lastaction=lastaction
        self.status=status

    def __str__(self):
        return f'({self.user})'
    
    def __repr__(self):
        return f'({self.user})'
     
allpossibleusers = set();      #set to contain all users that could be added
i=0;
j=0;
k=0;

file3 = open("fallenusers.txt", "r+")  #loading list of all fallen users to check that we dont add a user that already got removed
fallenusers_pickled=""
for line in file1:
    fallenusers_pickled=fallenusers_pickled+line
file3.close()           
fallenusers_all=jsonpickle.decode(fallenusers_pickled)

for submission in reddit.subreddit("all").hot(limit=10):   #search all comments of the top 10 threads on r/all
    submission.comments.replace_more(limit=None)
    i=i+1;
    print("Submissions: "+str(i))
    print(len(allpossibleusers))
    if len(allpossibleusers)>1000:  #stop at 1000 possible users (only to speed up testing right now)
        break
    for comment in submission.comments.list():
        add=True
        k=k+1;
        j=j+1;
        print("Users: "+str(j))
        for fallen in fallenusers_all: #check if users was already removed
            if fallen.username=comment.author:
                add=False
        if add:
            allpossibleusers.add(comment.author)
        
print(allpossibleusers)
print(len(allpossibleusers))

import time
import random

nowtime=time.time() #time to check account age, lastaction and such

userstoadd=random.sample(allpossibleusers,100)
userstoadd_new=userstoadd.copy()
gonecount=0
not_finished=True
n=0
print(len(userstoadd))
print(userstoadd)

while not_finished:
    n=n+1
    print("try: "+str(n))
    gonecount=0
    for redditor in userstoadd:
        if (redditor.comment_karma+redditor.link_karma)<100:
            print("USER GONE KARMA")
            userstoadd_new.remove(redditor)
            gonecount=gonecount+1
        elif redditor.created_utc>(nowtime-31622400):
            userstoadd_new.remove(redditor)
            print("USER GONE AGE")
            gonecount=gonecount+1
    if len(userstoadd_new)==100:
        not_finished=False
    print("removed users: "+str(gonecount))
    userstoadd_new_new=random.sample(allpossibleusers,gonecount)
    userstoadd_new=userstoadd_new+userstoadd_new_new
    userstoadd=userstoadd_new.copy()
    print(len(userstoadd))

print(len(userstoadd))
print(userstoadd)

now = datetime.now()
    
dt_string = now.strftime("%Y.%m.%d")
WCDT2userstoadd = set();

for x in userstoadd:                 #transfer usertoadd to a set in our custom class
    usertoadd=WCDT2user(x.name,nowtime,nowtime,"new")
    WCDT2userstoadd.add(usertoadd)
    
with open(dt_string+" - new users.txt", "w") as f:
    f.write(jsonpickle.encode(WCDT2userstoadd))
f.closed

file1 = open("allusers.txt", "r+")  
allusers_pickled=""
for line in file1:
    allusers_pickled=allusers_pickled+line
file1.close()
             
file2 = open("lasttime.txt, "r+")  
lasttime_pickled=""
for line in file1:
    lasttime_pickled=lasttime_pickled+line
file2.close()
                          
allusers=jsonpickle.decode(allusers_pickled)
lasttime=jsonpickle.decode(lasttime_pickled)
senior_lasttime=lasttime-((nowtime-lasttime)*5)
             
for x in WCDT2userstoadd:
    allusers.add(x)
             
for user in allusers:
    if user.status=="new" and nowtime-user.timejoined>(8*604800):
             user.status="senior"
                    
             
activeusers = set()
for submission in reddit2.subreddit("WeCanDoThisToo").new(limit=1000):        #check activity of users
    if submission.created_utc<(nowtime-15552000)
        break
    if submission.created_utc>(nowtime-lasttime):   #add to list of active users if submission was between now and last sweep
        activeusers.add(submission.author)
    submission.comments.replace_more(limit=None)
    if submission.comments.list():
        for comment in submission.comments.list()
            if comment.created_utc>(nowtime-lasttime): #add to list of active users if comment was between now and last sweep
                activeusers.add(comment.author)
            
for activeuser in activeusers:
    for user in allusers:
        if activeruser.name==user.name:
            user.lastaction=nowtime
            #update lastaction of active users to current time
             
 fallenusers = set()
             
allusers_new=allusers.copy()        
for user in allusers:
    if user.status=="new" and lasttime=user.lastaction:
             allusers_new.remove(user)
             fallenusers.add(user)
    if user.status=="senior" and senior_lasttime>user.lastaction:
             allusers_new.remove(user)
             fallenusers.add(user)
            
with open("allusers.txt", "w") as f:
    f.write(jsonpickle.encode(allusers_new))
f.closed
             
with open(dt_string+"allusers.txt", "w") as f:
    f.write(jsonpickle.encode(allusers_new))
f.closed
             
with open(dt_string+"fallenusers.txt", "w") as f:
    f.write(jsonpickle.encode(fallenusers))
f.closed
            
             
for fallenuser in fallenusers:
             fallenusers_all.add(fallenuser)
                  
with open("fallenusers.txt", "w") as f:
    f.write(jsonpickle.encode(fallenusers_all))
f.closed

with open("lasttime.txt", "w") as f:
    f.write(jsonpickle.encode(nowtime))
f.closed
             
for fallenuser in fallenusers:
    reddit2.subreddit('wecandothistoo').contributor.remove(fallenuser.username)
for WCDT2usertoadd in WCDT2userstoadd:
    reddit2.subreddit('wecandothistoo').contributor.add(WCDT2usertoadd.username)

#TODO generate post
