#!/usr/bin/env python
# coding: utf-8

# In[1]:


import praw
import re
from datetime import datetime
import jsonpickle

reddit = praw.Reddit(                   #random user to access r/all
    client_id='******',
    client_secret ="******",
    username="******",
    password="******",
    user_agent="WeCanDoThisToo"
)

reddit2 = praw.Reddit(                #user that has acces to r/wecandothistoo and can remove/add contributers
    client_id='******',
    client_secret ="******",
    username="******",
    password="******",
    user_agent="WeCanDoThisToo2"
)
class WCDT2user:                    #custom class to save users
    def __init__(self, username, timejoined, lastaction, status,number):
        self.username =  username
        self.timejoined = timejoined
        self.lastaction=lastaction
        self.status=status
        self.number=number

    def __str__(self):
        return f'({self.user})'
    
    def __repr__(self):
        return f'({self.user})'


# In[12]:


allpossibleusers = set();      #set to contain all users that could be added
i=0;
j=0;
k=0;
#print("hello")

file3 = open("fallenusers.txt", "r+")  #loading list of all fallen users to check that we dont add a user that already got removed
fallenusers_pickled=""
for line in file3:
    fallenusers_pickled=fallenusers_pickled+line
file3.close()           
fallenusers_all=jsonpickle.decode(fallenusers_pickled)

file3 = open("allusers.txt", "r+")  #loading list of all fallen users to check that we dont add a user thats already in
allusersold_pickled=""
for line in file3:
    allusersold_pickled=allusersold_pickled+line
file3.close()           
allusersold=jsonpickle.decode(allusersold_pickled)

#print("ullo")

for submission in reddit.subreddit("all").hot(limit=10):   #search all comments of the top 10 threads on r/all
    #print("hallo?")
    submission.comments.replace_more(limit=1)
    #print("hallo!")
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
        if comment.author is None:
            add=False
        if add:
            for fallen in fallenusers_all: #check if users was already removed
                if fallen.username==comment.author.name:
                    add=False
        if add:
            for userino in allusersold: #check if users was already removed
                if userino.username==comment.author.name:
                    add=False
        if add and comment.author:
            allpossibleusers.add(comment.author)
        
print(allpossibleusers)
print(len(allpossibleusers))


# In[13]:


import time
import random

nowtime=time.time() #time to check account age, lastaction and such
wanted_count=100

userstoadd=random.sample(allpossibleusers,wanted_count)
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
    if len(userstoadd_new)==wanted_count:
        not_finished=False
    print("removed users: "+str(gonecount))
    userstoadd_new_new=random.sample(allpossibleusers,gonecount)
    userstoadd_new=userstoadd_new+userstoadd_new_new
    userstoadd=userstoadd_new.copy()
    print(len(userstoadd))

print(len(userstoadd))
print(userstoadd)


# In[14]:


now = datetime.now()
    
dt_string = now.strftime("%Y-%m-%d")
WCDT2userstoadd = [];

for x in userstoadd:                 #transfer usertoadd to a list in our custom class
    usertoadd=WCDT2user(x.name,nowtime,nowtime,"new",0)
    WCDT2userstoadd.append(usertoadd)
    
with open(dt_string+" - new users.txt", "w") as f:
    f.write(jsonpickle.encode(WCDT2userstoadd))
f.closed


# In[15]:


file1 = open("allusers.txt", "r+")  #import list of all current users
allusers_pickled=""
for line in file1:
    allusers_pickled=allusers_pickled+line
file1.close()
allusers=jsonpickle.decode(allusers_pickled)
           
file2 = open("lasttime.txt", "r+") #import time of last sweep
lasttime_pickled=""
for line in file2:
    lasttime_pickled=lasttime_pickled+line
file2.close()                      
lasttime=jsonpickle.decode(lasttime_pickled)

senior_lasttime=lasttime-(604800*5)
             
for user in allusers:            #give older users senior status
    if user.status=="new" and nowtime-user.timejoined>(8*604800):
             user.status="senior"
                    


# In[16]:


activeusers = []
for submission in reddit2.subreddit("WeCanDoThisToo").new(limit=1000):        #check activity of users
    if submission.created_utc<(nowtime-15552000):
        break
    if submission.created_utc>(nowtime-lasttime):   #add to list of active users if submission was between now and last sweep
        activeusers.append(submission.author)
    submission.comments.replace_more(limit=None)
    if submission.comments.list():
        for comment in submission.comments.list():
            if comment.created_utc>(nowtime-lasttime): #add to list of active users if comment was between now and last sweep
                activeusers.append(comment.author)
            
for activeuser in activeusers:
    for user in allusers:
        if activeuser.name==user.username:
            user.lastaction=nowtime
            break
            #update lastaction of active users to current time
            
for x in WCDT2userstoadd:       #add new users to list of all users
    allusers.append(x)


# In[17]:


fallenusers = []
             
allusers_new=allusers.copy()        #remove fallen users from list
for user in allusers:
    if user.status=="new" and lasttime==user.lastaction:
             allusers_new.remove(user)
             fallenusers.append(user)
    if user.status=="senior" and senior_lasttime>user.lastaction:
             allusers_new.remove(user)
             fallenusers.append(user)               
usercount=2
for user in allusers_new:
    if user.status!="permanent":
        user.number=usercount
        usercount=usercount+1

with open("allusers.txt", "w") as f: #export new list of all users
    f.write(jsonpickle.encode(allusers_new))
f.closed
             
with open(dt_string+" - allusers.txt", "w") as f: #export new list of all users with current date for logging
    f.write(jsonpickle.encode(allusers_new))
f.closed
             
with open(dt_string+" - fallenusers.txt", "w") as f: #export list of fallen users with current date for logging
    f.write(jsonpickle.encode(fallenusers))
f.closed
            
             
for fallenuser in fallenusers:
             fallenusers_all.append(fallenuser)
                  
with open("fallenusers.txt", "w") as f: #export new list of all fallen users 
    f.write(jsonpickle.encode(fallenusers_all))
f.closed

with open("lasttime.txt", "w") as f: #export new time of sweep
    f.write(jsonpickle.encode(nowtime))
f.closed


# In[ ]:


for fallenuser in fallenusers: #remove fallen users from sub
    reddit2.subreddit('wecandothistoo').contributor.remove(fallenuser.username)
for WCDT2usertoadd in WCDT2userstoadd: #add new users to sub
    reddit2.subreddit('wecandothistoo').contributor.add(WCDT2usertoadd.username)


# In[18]:


title=dt_string+" - Bot Recap"
selftext=""
selftext=selftext+"# Users removed"
selftext=selftext+"\n"
selftext=selftext+"\n"
for fallenuser in fallenusers:
    selftext=selftext+"- \#"+str(fallenuser.number)+" /u/"+fallenuser.username+"\n"
selftext=selftext+"\n"
selftext=selftext+"\n"
selftext=selftext+"# New Users"
selftext=selftext+"\n"
selftext=selftext+"\n"
for newuser in WCDT2userstoadd:
    selftext=selftext+"- \#"+str(newuser.number)+" /u/"+newuser.username+"\n"
#submission2=subreddit2.submit(title=title, selftext=selftext)
print(selftext)




