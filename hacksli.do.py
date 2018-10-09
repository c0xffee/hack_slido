import requests
import multiprocessing as mp
import time
import json
import datetime
from datetime import timezone, timedelta	
from bs4 import BeautifulSoup


#THE FUNCTION HIT THE LIKE BUTTON FOR YOU SO I CALLED IT SHOWTIME(IT'S THE MOST IMPORTANT PART OF THIS ATTACK!!?)
#IT TRY TO GET A ALL NEW ACESS_TOKEN FROM SERVER TO BECOME A NEW ANONYMOUS USER
#THE REASON WHY WE NEED TO CAMOUFLAGE A ALL NEW ANONYMOUS USER IS A ANONYMOUS USER CAN ONLY HIT THE LIKE BUTTON ONCE
#SO WE HAVE TO DO THAT SO MUCH TIMES TO REACH OUR GOAL(THE NUMBER OF LIKE WE WANT)
def showtime(uuid, question_id):
  authurl = 'https://app2.sli.do/api/v0.5/events/%s/auth'%uuid    #GET ACESS_TOKEN
  s = requests.Session()     #START WITH A ALL NEW SESSION BECAUSE WE WANT TO GET A ALL NEW IDENTITY
  res = s.post(authurl)
  tmp = res.text.split(',')
  #print(tmp)
  access_token = tmp[0].split('"')[-2]  #GET ACESS_TOKEN FROM RESPONSE DATA
  event_id = tmp[1].split(':')[-1]      #GET EVENT_ID FROM RESPONSE DATA
  #print('access_token:%s'%access_token)
  #print('event_id:%s'%event_id)
  like = 'https://app2.sli.do/api/v0.5/events/%s/questions/%s/like'%(event_id, question_id)
  #print(like)
  s.headers.update({'Authorization': 'Bearer %s'%access_token})
  res = s.post(like)
  #print(res.text)
  print('         %s   hit a like button on   %s   question'%(access_token, event_id))
  
  
#CONVERT DATE(+0) TO YOUR LOCAL TIMEZONE
def datesTW(date):
  date = '%s+0000'%date.split('.')[0]
  gmtf = '%Y-%m-%dT%H:%M:%S%z'
  date = datetime.datetime.strptime(date, gmtf)
  #############################################
  #2 get the utc offset by (now local hour - now utc +0 hour == offset == local utc)
  u = int(datetime.datetime.utcnow().strftime('%H'))
  n = int(datetime.datetime.now().strftime('%H'))
  offset = n-u
  #############################################
  utc = timezone(datetime.timedelta(hours=offset))
  date = date.astimezone(utc)
  date = date.strftime('%b %d, %Y %H:%M:%S')
  
  return date
  
def width(sth):
##get the width of string. Because a chinese char use 2 space and english char use 1.
  n = 0
  for c in sth:
    if '\u4e00' <= c <= '\u9fa5':
      ##chinese char unicode range
      n += 2
    else:
      n += 1
  return n
	
	
def getprofileapha(name):
  
  if '\u4e00' <= name[0] <= '\u9fa5':
    ##search for the first chinese char's turn to english and get the first aphabet.
    u = 'https://pinyin.thl.tw/converter?s=%s'%name[0]
    res = requests.get(u)
    soup = BeautifulSoup(res.text, 'html.parser')
    p = soup.find_all('td')[2].text.replace(' ', '').replace('\n', '')[0]
  else:
    p = name[0]  
  return p	  
	
	
	
if __name__ == '__main__':

  
  #id = 'aj4ibexu'
  id = input('\ncopy your room url here : ').split('/')
  id = id[id.index('event')+1]

  #TO GET UUID 
  #ID NEEDED
  url = 'https://app2.sli.do/api/v0.5/events?hash=%s'%id
  s = requests.Session()      #A NEW SESSION
  res = s.get(url)
  tmp = res.text.split(',')
  uuid = [i.split('"') for i in tmp if 'uuid' in i][0][-2]        #GET UUID FROM RESPONSE DATA
  
  #TO GET ACESS_TOKEN(BEARER TYPE) AND EVENT_ID
  #THE REQUEST NEED UUID
  authurl = 'https://app2.sli.do/api/v0.5/events/%s/auth'%uuid
  res = s.post(authurl)#POST METHOD
  tmp = res.text.split(',')
  access_token = tmp[0].split('"')[-2]  #GET ACESS_TOKEN FROM RESPONSE DATA
  event_id = tmp[1].split(':')[-1]      #GET EVENT_ID FROM RESPONSE DATA
  
  #TO GET THE ALL QUESTIONS INFORMATION IN THIS ROOM
  #WE NEED EVENT_ID AND THE BEARER TYPE ACESS_TOKEN TO PASS VERIFICATION BY ANONYMOUS IDENTITY
  url = 'https://app2.sli.do/api/v0.5/events/%s/questions?path=/questions'%event_id
  s.headers.update({'Authorization': 'Bearer %s'%access_token})
  res = s.get(url).text
  sth = json.loads(res)                 #PROCESS JSON TYPE OF RESPONSE DATA
  #print(li[0])
  #print('#############')
  
  
  #PICK UP ALL THE DATA FROM PRESPONSE AND MAKE A QUESTIONS BOX THAT CONTAINT ALL THE QUESTION'S INFORMATIONS
  qbox = []   #QUESTIONS BOX
  c = 0
  for i in sth:
    qbox.append([])
    if i['author'] != {}:
      qbox[c].append(i['author']['name'])
    else:
      qbox[c].append('Anonymous')
    qbox[c].append(i['text'])
    qbox[c].append(i['event_question_id'])
    qbox[c].append(i['is_public'])
    qbox[c].append(i['is_answered'])
    qbox[c].append(i['is_highlighted'])
    qbox[c].append(datesTW(i['date_created']))  #TO GET THE DATE
    qbox[c].append(i['score'])
    c += 1
	
  qbox.sort(key=lambda x:x[-1], reverse=True)
  #print(qbox)
  
  #THE DATA TYPE OF QUESTION IN QBOX
  #q = [name, text, q_id, is_pub, is_ans, is_high, date, score]
  #       0     1     2      3       4       5       6     7
  
  
  #SORT OUT ALL THE QUESTION'S AND PRINT THEM IN A GOOD LOOK WAY(ASCII ART) LIKE THE SLI.DO'S OFFICIAL VERSION
  #SO YOU CAN USE SLI.DO IN YOUR TERMINAL, THAT'S SO FUN WHEN YOU TAKE PART IN A LECTURE
  padding = 100      #WIDTH OF THE QUESTION BOX
  head = '           %s '%('_'*padding)
  print('\n\n')
  print('             room_ID : %s'%id)
  print(head)
  for q in qbox:
    profile = '          |  .-.%s|\n          | ( %s ) %s%sLike <%d>%s|\n          |  \'-\'  %s%s|\n          |%s|\n'%(' '*(padding-5), getprofileapha(q[0][0].upper()), q[0], ' '*((padding-19)-width(q[0])-width(str(q[7]))), q[7], ' '*5, q[6], ' '*((padding-7)-width(q[6])), ' '*padding)
    content = '          |  %s%s%s%s%s|\n'%(q[1], ' '*((padding-2-10-width(q[1])-width(str(q[2])))), 'Q_ID : ', q[2], ' '*(3))
    tail = '          |%s|'%('_'*padding)
    print('%s%s%s'%(profile, content, tail))
  print('\n\n')
  question_id = input('question_ID:')  #CHOOSE A QUESTION_ID YOU LIKE
  num = int(input('like:'))            #INPUT HOW MANY LIKES YOU WANT TO MAKE YOUR QUESTION ON THE TOP

  #MULTIPROCESSING , USE ALL THE CORES YOU HAVE TO MAKE PROCESS OF HACK MORE EFFICINECY AND FAST(DEFAULT IS 8 CORES)
  mp.freeze_support()
  pool = mp.Pool(8)
  
  print('\n\ninfo:\n')
  beg = time.time()
  for i in range(num):
    pool.apply_async(showtime, args=(uuid,question_id))

  pool.close()
  pool.join()
  
  print('\ncost_time : %s s'%str(time.time()-beg)[:5 ])
  print('\n=============================finished hit the like %d times============================='%num)
#id = input('Event_ID:')
#https://app2.sli.do/api/v0.5/events/606989/questions?path=%2Fquestions


