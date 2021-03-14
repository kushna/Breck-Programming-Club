#!/usr/bin/env
#M3 Scheduler, Question 2
#Ben Kroul, February 27
#Scheduler assumes no pauses in 16-hour workday
# just internet event to internet event
# normally randomizes time spent doing something
# randomizes order of events

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

'''
Basically a natural histogram

Possible change would be to create a day list that has all the timestamps
Then iterate through each timestamp and get the total bandwidth being used
    during each interval where a new activity is present
Then use this to make a list of [bandwidth,time]
Then at end sort list by bandwidth, add up bandwidths' times (multiple lst[x][0]s)
    and get final list, cumulative time at each bandwidth
Then would just sort list by bandwidth
To find percent, add up all lst[x][1]s to get total time
Then add up all lst[x][1]s until reaches bandwidth to get time%
--> could also just convert list into [bandwidth,timestamp] (timestamp is end of event)
    bandwidth-->% = timestamp/total time
    %-->bandwith = totaltime*%=timestamp, look for 1st instance of lst[x][1]>=timestamp
https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.bar.html
make bar graph with x=lst[x][0], height=lst[x][1]
'''

#------Changeable Variables-----#
#0=toddler, 1=kids, 2=undergrad, 3=teacher, 4=other parent, 5=grandma
#list of peoples age ranges in household
alst=[2,2,2]
labellst=[['Toddler','Kid','Undergrad','Teacher Parent','Other Parent','Grandma'][a] for a in alst]+['Combined']

#use data from table D4 (T) or ignore it (F)
D4=False

#schedules online class at the beginning of the day for everone
#therefore, online class overlaps
correlatedclass=True

#randomize bandwidth usage per activity instead of set value
randomizebandwidth=True

#1/degree = increments the bandwidth can be, so 1 is rounded to nearest whole number, 4 to nerest quarter, etc.
degree=4 #or instead could fix in post when sorting bandwidths into groups by bandwidth??

#number of days to simulate (1,000 - 10,000 usually)
numberofdays=10000

#-----Internet Activities & Data----#
#the first section of this list is the left table taken from source D4
#the second bit of this list is estimated values we used for each person
#since values in D4 were given in weeks, we converted our estimated values
#to weeks; basically a table
#columns = age ranges; rows = activity
meanlst=[[12.00,7.60,11.35,23.80,40.02,50.60], #tv
         [2.72,4.18,3.63,1.73,0.47,0.17], #tv connected game console
         [7.72,4.52,6.95,6.87,4.95,3.20], #tv connected internet device
         [0,0,3.97,4.77,5.03,3.17], #internet on computer
         [0,0,1.73,1.28,1.07,0.50], #video on computer
         [15,35,29.48,30.12,25.23,19.12], #total app on smartphone
         [3,8,3.03,2.28,1.38,0.97], #video focused app on smartphone
         [0.5,1.5,1.62,0.85,0.60,0.42], #audio on smartphone
         [15,10,5.07,7.13,7.27,7.97], #total app on tablet
         [3,2,0.98,1.07,0.85,0.65], #video focused app on tablet
         [0.1,0.2,0.20,0.22,0.17,0.10], # audio on tablet
         #end of D4 data, start of custom data
         [14,8,8,0,5,4], #online gaming (3) [toddler, kids, undergrad, teacher, other parent, grandma]
         [0,0.5,1,0.5,0.5,0], #large downloads (50)
         [2.05,0,28,34.51,34.51,22.68], #homework (1)
         [6.95,22.5,14,12.67,12.67,2.17], #streaming video (5)
         [6,10,14,0,0,0], #social media (1)
         [2.95,3,14,3.64,3.64,1.54], #random internet stuff (3)
         [15,21,28,28,11.2,0]] #online class (4)

#describes the activity; only called when printing a schedule
descriptions=['TV','TV Game Console','Smart TV','Computer Browsing','Computer Video',
              'Smartphone App','Smartphone Video','Smartphone Audio','Tablet App','Tablet Video','Tablet Audio',
              'Online Gaming','Large Downloads','Homework','Streaming Video','Social Media',
              'Internet Browsing','Online Class']

#Mbps used for each category
usage=[0,3,5,1,4,1,4,1,1,4,1,3,50,1,5,1,3,4]
if not D4: usage[0:11]=[0,0,0,0,0,0,0,0,0,0,0] #inhibits D4 data

#divide data from times in weeks to daily times
for i in range(len(meanlst)):
    for _ in range(len(meanlst[i])): meanlst[i][_]=meanlst[i][_]/7

#combines three lists into list of possible activies
#(ignores activities with usage 0)
#thingstodo[things][info]([meanlstcolumn])
thingstodo=[[meanlst[_],usage[_],descriptions[_]] for _ in range(len(usage)) if usage[_]!=0]

if correlatedclass: #remove online class: (which is last column)
    onlineclass=thingstodo.pop(len(thingstodo)-1)

#-------Run Simulation------#

#list of ceiling bandwidths per person + total
lst=[ [] for _ in range(len(alst)+1)]

#lst[person(+combined)]

for z in range(numberofdays): #simulate multiple days
    if z==0: continue
    #print status updates every 10%
    for i in range(1,11):
        if z==np.floor(numberofdays*i/10)-1: print(' - '+str(i*10)+'% done - \n')

    #make a list that holds the daily schedules for each person
    #schedule[person][event][info]
    schedule=[ [] for _ in range(len(alst)) ]

    #assign schedules to each person, randomizing order of events and events themselves
    for a in range(len(alst)):
        #---------Random 1: Shuffles Order of Events------#
        np.random.shuffle(thingstodo)

        if correlatedclass: #insert online class as first thing in schedule
            thingstodo.insert(0,onlineclass)

        for thing in thingstodo: #make a schedule for each person with timestamp from agelst; randomize bandwidth; 
            if thing[0][alst[a]]==0: continue #person doesn't do activity in day (based on average time)
            if randomizebandwidth: #----Random 2: Bandwidth Used in Each Event-----#
                bandwidth=round((thing[1]+np.random.randn()*thing[1]/8)*degree)/degree
            else: bandwidth=thing[1]
            #------Random 3: Times Spent in Each Event-------#
            time=thing[0][alst[a]]+np.random.randn()*thing[0][alst[a]]/4 #timestamp
            description=thing[2]
            schedule[a].append([time,bandwidth,description])

        #remove online class so the schedule can be shuffled again
        if correlatedclass: thingstodo.pop(0)

    if z==0: #print the first schedule to see if thing is working
        print('Schedule for day '+str(z)+'\ndescription of activity : time activity takes (hrs) | bandwidth used (Mbps)')
        for a in range(len(schedule)):
            print('\n'+labellst[a]+"'s schedule: ")
            for event in schedule[a]:
                print('\t'+event[2]+': '+str(round(event[0],2))+' | '+str(round(event[1],2)))
    '''could make graph of schedule, kinda like on veracross type beat with rectangles in matplotlib'''

    #---Simulate Each Day----#
    currentmaxbandwidth=[0]*(len(alst)+1)
    time=float(0) #time starts at zero

    #get individual stuff and create schedule w timestamps instead of time
    tschedule=[ [] for _ in range(len(alst)) ]
    #tschedule[person][event][info], info=[bandwidth,timestamp]
    
    for a in range(len(alst)):
        timestamp=0
        for event in schedule[a]:
            time=event[0] #time spent doing event
            timestamp+=time #time when event ends
            bandwidth=event[1] #bandwidth used for event
            lst[a].append([bandwidth,time]) #add to individual list
            tschedule[a].append([bandwidth,timestamp]) #
        
    #order timestamp schedule by timestamp into a singular list of events that occur in order
    timestamplst=sorted([event[1] for person in tschedule for event in person])
    #timestamplst[event]
    
    #when all actions end
    maxtime=timestamplst[len(timestamplst)-1]

    if z==0:
        print('tschedule')
        print(tschedule)
        print('\nschedule',schedule,'\n')
        print('timestamplst:')
        print(timestamplst)
        print('maxtime:',maxtime)
    #----Household Bandwidth Usage Over Day-----#   
    nexttimestamp=timestamp=0; nexttimes=[0]*len(alst)
    while timestamp<maxtime:
        timestamp=nexttimestamp
        if len(timestamplst)>0: nexttimestamp=timestamplst.pop(0)
        
        #get next timestamp for each person so we know which thing we're in
        for a in range(len(alst)):
            for e in tschedule[a]:
                if e[1]>timestamp: break
            nexttimes[a]=e[1]

        #get currentbandwidth by adding up bandwidths that are used on the interval from timestamp to nexttimestamp
        bandwidth=0
        if z==0:
            print('current t=',timestamp)
            print('next t=',nexttimestamp)
            print(nexttimes)
        msg=[]
        for a in range(len(alst)):
            msg.append('p:'+str(a))
            for event in tschedule[a]:
                if timestamp<event[1]<=nexttimes[a]:
                    bandwidth+=event[0]
                    msg.append('b:'+str(bandwidth))
                    break
        if z==0: print('\t'+'    '.join(msg))
        #now have current bandwidth over interval
        time=nexttimestamp-timestamp
        if time!=0: lst[len(alst)].append([bandwidth,time])
    if z==0: print('\n\n'.join([str(i) for i in lst]))

#------Sort Lst by Bandwidth------#
print('Now Sorting List...')
print('\n#terms in list before simplifying = '+str(sum([len(a)*2 for a in lstlst])))
print('    #different bandwidths for each =  '+', '.join([str(len(a)) for a in lstlst]))
if numberofdays<20: print('\n\n'.join([str(i) for i in lst])+'\n\n'+'Sorted and Added List:\n\n')
lstlst=lst.copy() #unchanging list
#sort each person (and combined) in lst by bandwidth (to get bandwidths next to each other)
for a in range(len(alst)+1):
    lst[a]=sorted(lst[a], key=lambda x: x[0])
    for e in range(len(lstlst[a])):
        #print('len(lst['+str(a)+'])='+str(len(lst[a])))
        if e>=len(lst[a])-1: break #only access up to last term in editable list
        while lst[a][e][0]==lst[a][e+1][0]: #could do within for random bandwidths (<1/degree)---------------
            lst[a][e][1]+=lst[a][e+1][1] #add times
            del lst[a][e+1] #remove term that just got added
            if e>=len(lst[a])-1: break #only access up to last term in editable list
if numberofdays<20:
    print('Original List:\n')
    print('\n\n'.join([str(i) for i in lst]))

#-----Get Lst Statistics-----# (lengths,#hours,mean,stdv)
lengths=[len(a) for a in lst]; totallength=sum(lengths)
print('\n#terms in list after simplifying = '+str(totallength*2))
print('    #different bandwidths for each =  '+', '.join([str(i) for i in lengths])+'\n\n')
#list of total hours in each list, weighted average, & stdv
totaltime=[]; meanlst=[]; stdlst=[]
for a in range(len(lst)):
    totaltime.append(sum([b[1] for b in lst[a]])) #get total hours
    meanlst.append(sum([b[0]*b[1] for b in lst[a]])/totaltime[a]) #weighted average = sum of bandwidth*time all divided by total time
    stdlst.append(np.std([b[0]*b[1]/totaltime[a] for b in lst[a]])) #standard deviation of list of weighted averages
    
    print(labellst[a]+' total hours = '+str(totaltime[a]))
    print(' '*len(labellst[a])+' mean bandwidth = '+str(meanlst[a]))
    print(' '*len(labellst[a])+' stdv of bandwidths = '+str(stdlst[a]))
    if a==len(alst)-1: print(str(len(alst))+' person total hours = '+str(sum(totaltime[0:len(alst)])))
    

#-----Print Values----#
def getBandwidth(percent,a): #get bandwidth from percent
    timepercent=percent/100*totaltime[a]
    timestamp=0
    for i in lst[a]:
        timestamp+=i[1]
        if timestamp>=timepercent: break
    return i[0] #return bandwidth

def getTime(percent,a): #get bandwidth from percent
    timepercent=percent/100*totaltime[a]
    timestamp=0
    for i in lst[a]:
        timestamp+=i[1]
        if timestamp>=timepercent: break
    return i[1] #return time

def getPercent(bandwidth,a):
    if bandwidth>=lst[a][len(lst[a]-1)][0]: #greater than or equal to maximum bandwidth
        time=totaltime[a]
    else:
        time=0
        for i in lst[a]:
            time+=i[1] #add time
            if bandwidth>i[0]: continue
            break
    return 100*time/totaltime[a]

colorlst=['blue','red','green','pink','orange','purple','brown'][0:len(alst)]+['black']
legend_elements=[Line2D([0], [0], marker='o', color='w', markerfacecolor=colorlst[a], label=labellst[a]) for a in range(len(alst)+1)]

t=input('\nSimulation complete. You can:\n'+
        ' - Get bandwidth needed to cover certain % of household internet usage:\n'+
        '    >>> input a percent or multiple percents separated by commas\n'+
        ' - Show bar graphs showing the time spent at each bandwidth usage\n'+
        "    >>> 'all' or 'total' to show all bar graphs, other characters to show only a few"+
        ' - Graph percent of internet usage met over bandwidth supplied (answer to problem)\n'+
        '    >>> press enter\n\n>>> ').lower().strip()

percentlst=[90,99,100]
for percent in percentlst: print(str(percent)+'%: '+', '.join([str(getBandwidth(percent,a)) for a in range(len(alst)+1)]))
while t!='e' and t!='exit': #able to keep printing percents
    try: #----Input a single percent----#
            percent=float(t) if 0<float(t)<100 else 100
            if percent not in percentlst:
                percentlst.append(percent) #selected percent
                print(str(percent)+'%: '+str(getValue(percent,len(alst))))
            else: print("Input a comma to print current percents")
    except:
        if ',' in t: #list of percents
            if t!=',':percentlst=[]
            t=t.split(',')
            for i in t: #add percents to percentlst
                i=i.strip()
                try:
                    percent=float(i) if 0<float(i)<100 else 100
                    if percent not in percentlst: percentlst.append(percent)
                except: pass
            print(', '.join(labellst)) #print percentlst
            for percent in percentlst:
                print(str(percent)+'%: '+', '.join([str(getBandwidth(percent,a)) for a in range(len(alst)+1)]))
        elif 'bar' in t or 'graph' in t: #----Graph all Bar Graphs----#
            #graph bar graph of time spent at each bandwidth over indiviual and combined
            if len(alst)>1:
                for a in range(len(alst)+1): #individual bar graphs
                    plt.clf()
                    plt.title(labellst[a]+' Time at Each Bandwidth')
                    plt.ylabel('Time Spent (hrs) Over '+str(numberofdays)+' Days')
                    plt.xlabel('Bandwidth (mbps)')
                    plt.bar(x=[i[0] for i in lst[a]], height=[i[1] for i in lst[a]],color=colorlst[a])
                    for p in percentlst: #add lines to show where percents are
                        value=getBandwidth(p,a)
                        height=getTime(p,a)
                        plt.axvline(x=value,linestyle='--',c=colorlst[a])
                        plt.text(value,height,str(p)+'%: '+str(round(value,2)),va='top')
                    plt.savefig('scheduler_bar_'+str(a)+'.png',dpi=400.0,bbox_inches='tight')
                    plt.show()
            plt.clf() #combined bar graph
            plt.title('Household Times at Each Bandwidth')
            plt.ylabel('Time Spent (hrs) Over '+str(numberofdays)+' Days')
            plt.xlabel('Bandwidth (mbps)')
            for a in range(len(alst)+1):
                plt.bar(x=[i[0] for i in lst[a]], height=[i[1] for i in lst[a]],color=colorlst[a],label=labellst[a])
            plt.legend()
            plt.savefig('scheduler_bar_household.png',dpi=400.0,bbox_inches='tight')
            plt.show()
        elif t!='': #----Only Show Important Bar Graphs----#
            plt.clf(); a=len(alst) #combined bar graph
            plt.title(labellst[a]+' Time at Each Bandwidth')
            plt.ylabel('Time Spent (hrs) Over '+str(numberofdays)+' Days')
            plt.xlabel('Bandwidth (mbps)')
            plt.bar(x=[i[0] for i in lst[a]], height=[i[1] for i in lst[a]],color=colorlst[a])
            for p in percentlst: #add lines to show where percents are
                value=getBandwidth(p,a)
                height=getTime(p,a)
                plt.axvline(x=value,linestyle='--',c=colorlst[a])
                plt.text(value,height,str(p)+'%: '+str(round(value,2)),va='top')
            plt.savefig('scheduler_bar_'+str(a)+'.png',dpi=400.0,bbox_inches='tight')
            plt.show()
            if len(alst)>1: #bar graph with combined and individual stuff
                plt.clf()
                plt.title('Household Times at Each Bandwidth')
                plt.ylabel('Time Spent (hrs) Over '+str(numberofdays)+' Days')
                plt.xlabel('Bandwidth (mbps)')
                for a in range(len(alst)+1):
                    plt.bar(x=[i[0] for i in lst[a]], height=[i[1] for i in lst[a]],color=colorlst[a],label=labellst[a])
                plt.legend()
                plt.savefig('scheduler_bar_household.png',dpi=400.0,bbox_inches='tight')
                plt.show()
        else: #------Graph Percent Covered over Bandwidth (Answers Question Directly)-----#
            plt.clf()
            increment=0.01 #percentincrement (1=1%)
            y=[i*increment for i in range(1,int(np.ceil(100/increment))+1)]
            for a in range(len(alst)+1):
                x=[getBandwidth(p,a) for p in y]
                plt.plot(x, y, c=colorlst[a])
            plt.title('Percent of Required Bandwidth Covered at Each Bandwidth Speed')
            plt.yticks([i for i in range(0,105,5)])
            plt.ylabel('Percent Coverage')
            plt.xlabel('Bandwidth')
            plt.legend(handles=legend_elements)
            plt.savefig('scheduler_percent.png',dpi=400.0,bbox_inches='tight')
            for p in percentlst: #add lines to show where percents are
                value=getBandwidth(p,a)
                plt.axvline(x=value,linestyle='--',ymin=5/110,ymax=(p+5)/110,c='black')
                plt.text(value,p,str(p)+'%: '+str(round(value,2)),va='top')
            plt.show()
    
    t=input('>>> ').lower().strip()

