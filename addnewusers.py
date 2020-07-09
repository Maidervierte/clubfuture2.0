import praw
import re
import time
import random

reddit = praw.Reddit(
    client_id='*******',
    client_secret ="*******",
    username="*******",
    password="*******",
    user_agent="*******"
)

allusers = set();
i=0;
j=0;
#k=0;

for submission in reddit.subreddit("all").hot(limit=10):
    submission.comments.replace_more(limit=None)
    i=i+1;
    print("Submissions: "+str(i))
    k=0;
    print(len(allusers))
    for comment in submission.comments.list():
        #k=k+1;
        j=j+1;
        print("Users: "+str(j))
        allusers.add(comment.author)
        #if k==1000:
            #break
        
print(allusers)
print(len(allusers))

nowtime=time.time()

userstoadd=random.sample(allusers,100)
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
    userstoadd_new_new=random.sample(allusers,gonecount)
    userstoadd_new=userstoadd_new+userstoadd_new_new
    userstoadd=userstoadd_new.copy()
    print(len(userstoadd))

print(len(userstoadd))
print(userstoadd)
