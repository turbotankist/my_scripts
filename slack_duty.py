from slackclient import SlackClient
from datetime import datetime, date, timedelta
import time, re, calendar, os, sys
import numpy as np


def Shift_missed(dayz):
	"""Shift days with missed duties (Deprecated)"""

	if os.path.isfile("missed.dat"):
		MISSED = np.loadtxt("missed.dat", dtype=str, comments="#", delimiter=",", unpack=False)
	else:
		MISSED = []
	print(MISSED)
	for day in MISSED:
		if len(day.split()) > 1:
			print(day.split()[1],", Thank you!")
		else:
			dayz-=1

	return dayz

def Days_count(startday,today,HOLIDAYS):
	"""Shift days for holidays"""
	dayz = np.busday_count(startday,today)

	for hday in HOLIDAYS:
		if startday < hday < today:
			dayz-=1
	#dayz = Shift_missed(dayz)
	return dayz


def get_duty(Crew, when=0):
	"""Calculate who is duty today"""

	STARTDAY = date(2018, 5, 19)
	TODAY = date.today() + timedelta(when)
	HOLIDAYS = [ date(2018, 2, 23), date(2018, 3, 8), date(2018, 3, 9), date(2018, 4, 30),
	             date(2018, 5, 1), date(2018, 5, 2), date(2018, 5, 9),
	             date(2018, 6, 12), date(2018, 11, 5)]
	DAYS = Days_count(STARTDAY,TODAY,HOLIDAYS)

	USER = "Nobody"
	if TODAY.weekday() < 5 and TODAY not in HOLIDAYS:
		USER = Crew[DAYS % len(Crew)]
	
	return USER

def Dirty_duty(dytyman, usr_dic, msg_list=[]):

	KEYWORDS=["дома","приболел","не будет","9-40"]

	Message = True
	if msg_list:
		for msg in msg_list:
			if msg['user'] == dytyman:
				for kw in KEYWORDS:
					if kw in msg['text']:
						print(msg,"\n\n")
						Message = "Seems like %s is away" % usr_dic[dytyman][1]
						break
				Message = False
				break
	else: 
		print("Can't load timing...")
		return False
	if Message and msg_list: Message = "Seems like %s is away" % usr_dic[dytyman][1]

	return Message

def next_week(Crew, usr_dic):
	"""Show duty list on next days"""
	try:
		FD = int(os.environ["DUTY_DAYS"])
	except:
		FD = 14
	week = []
	DAY = date.today()
	WD = "> *duty list:  in A304 room  |  in A421 room*\n"
	
	for i in range(FD):
		if DAY.weekday() < 5:
			week.append((str(DAY.day)+' '+calendar.day_name[DAY.weekday()], get_duty(Crew[0]['users'],i), get_duty(Crew[1]['users'],i)))
		DAY += timedelta(days=1)

	for d in week:
		WD = WD + '*'+d[0]+'*' + ':  ' + usr_dic[d[1]][1]+' |  '+ usr_dic[d[2]][1] +"\n"

	print(WD)
	return WD


def Send_slack(text):
	### Send to Slack ###

	try:
		token = os.environ["SLACK_API_TOKEN"]
	except:
		token = "xoxb-********"

	try:
		Channel = os.environ["SLACK_CHANNEL"]
	except: 
		Channel = "#general"
	sc = SlackClient(token)

	sc.api_call(
	  "chat.postMessage",
	  channel=Channel,
	  as_user=True,
	  link_names=True,
	  mrkdwn=True,
	  text=text
	  	)

def main():

	token = "xoxp-****"

	channel_id = ["dsgdf","ST0Q"]

	sc = SlackClient(token)
	ts = time.time() - 43200
	msg_hist = sc.api_call("channels.history", channel="8484", oldest=ts)
	msg_hist = msg_hist['messages']
	usr_list = sc.api_call("users.list")

	usr_dic = {'Nobody':["Nobody","Nobody"]}
	for usr in usr_list['members']:
		usr_dic[ usr['id'] ] = [usr['name'], usr['profile']['real_name']]

	grp_list = []
	USER_304 = {}
	USER_421 = {}
	
	for chid in channel_id:
		grp_list.append( sc.api_call("usergroups.users.list",usergroup=chid) )
	
	

	# print(usr_list)
	# print(msg_hist)
	# print(sc.api_call("usergroups.list"))

	USER_304 = get_duty(grp_list[0]['users'])
	USER_421 = get_duty(grp_list[1]['users'])


	print("@%s is on duty today in office 304!\n@%s is on duty today in office 421!\n" % (usr_dic[USER_304][0],usr_dic[USER_421][0]))

	# Send_slack(next_week(grp_list, usr_dic))
	if len(sys.argv)>1:
		if sys.argv[1] == 'list': 
			Send_slack(next_week(grp_list, usr_dic))
	else: 
		print(sys.argv)
		Send_slack( "@%s is on duty today in office 304!\n@%s is on duty today in office 421!\n:blin: Have a good time\n" 
						% (usr_dic[USER_304][0],usr_dic[USER_421][0]) )

		if msg_hist:
			dd = Dirty_duty(USER_304,usr_dic,msg_hist)
			
			if dd:
				print(dd)
				Send_slack(dd)
				
			dd = Dirty_duty(USER_421,usr_dic,msg_hist)
			if dd:	
				Send_slack(dd)
				print(dd)
		else: print("no timing")


if __name__ == "__main__":
    main()