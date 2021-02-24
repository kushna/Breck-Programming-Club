#Ben Kroul
#Jan 29 2021 - Feb 16
#Programming Club Meeting #6 Project
#esketit
#connect 4

import sys, random, time

#---------Definitions---------#
'''debug 0=regular gameplay, 1=important stuff, 2=everything'''
debug=0
delay=True
animation=True
#debug=1; delay=animation=False #editing mode

columnbreak='|' #what separates terms in connect 4 board
speed=0.15 #animation speed (0.1-0.5)
width=60 #screen width (works best 60-80)

specifications=True #do specifications?
justreplay=False #play dual computer game but skip to replay?
skip=False #skip game and go directly to end?

#-Constants-#
b=[' ']*42 #game board
a=[' ']*14 #animation board
e=keepgamemode=automatic=False #exit; specifications thing; automatic dual comp
piece=name1=x='X'; name2=y='O'
msg0=msg=''; before=['']*10; after=['']*10 #reset messages and sides of screen
move=numwins=numlosses=numties=0; gamenum=1 #keeps track of game

#-Mini Functions-#
s = lambda number : '' if number==1 else 's' #plural or singular number
on = lambda boolean : 'on' if boolean else 'off' #for turning variables on/off
slst = lambda lst : [str(i) for i in lst] #turns a list into list of strings

#-Functions-#
def centerLine(line,lwidth=0,bothsides=False): #center a line on screen
    if lwidth==0: lwidth=width
    if len(line)>lwidth: line=line[0:lwidth] #if line longer than line, cut line
    w=lwidth-len(line)
    centeredline=' '*(w//2)+line #add spaces to center line
    if bothsides:
        if w%2!=0: w+=1
        centeredline+=' '*(w//2) #add spaces after line
    return(centeredline)

def resetBoard(): #reset the connect 4 board
    b[0:len(b)]=' '*len(b)
    a[0:len(a)//2]=' '*(len(a)//2)
    a[len(a)//2:len(a)]='_'*(len(a)//2)

def printBoard(inGame=True,_=0):
    c=columnbreak
    lines=['  '+a[0]+' '+a[1]+' '+a[2]+' '+a[3]+' '+a[4]+' '+a[5]+' '+a[6]+'  ',
           ' .'+a[7]+'_'+a[8]+'_'+a[9]+'_'+a[10]+'_'+a[11]+'_'+a[12]+'_'+a[13]+'. ',
           ' |'+b[0]+c+b[1]+c+b[2]+c+b[3]+c+b[4]+c+b[5]+c+b[6]+'| ',
           ' |'+b[7]+c+b[8]+c+b[9]+c+b[10]+c+b[11]+c+b[12]+c+b[13]+'| ',
           ' |'+b[14]+c+b[15]+c+b[16]+c+b[17]+c+b[18]+c+b[19]+c+b[20]+'| ',
           ' |'+b[21]+c+b[22]+c+b[23]+c+b[24]+c+b[25]+c+b[26]+c+b[27]+'| ',
           ' |'+b[28]+c+b[29]+c+b[30]+c+b[31]+c+b[32]+c+b[33]+c+b[34]+'| ',
           ' |'+b[35]+c+b[36]+c+b[37]+c+b[38]+c+b[39]+c+b[40]+c+b[41]+'| ',
           ' |–––––––––––––| ',
           '_|_           _|_']
    if _==1:
        lines=['  a0 a1 a2 a3 a4 a5 a6  ',
               ' .a7_a8_a9_10_11_12_13. ',
               ' |b0'+c+'b1'+c+'b2'+c+'b3'+c+'b4'+c+'b5'+c+'b6| ',
               ' |b7'+c+'b8'+c+'b9'+c+'10'+c+'11'+c+'12'+c+'13| ',
               ' |14'+c+'15'+c+'16'+c+'17'+c+'18'+c+'19'+c+'20| ',
               ' |21'+c+'22'+c+'23'+c+'24'+c+'25'+c+'26'+c+'27| ',
               ' |28'+c+'29'+c+'30'+c+'31'+c+'32'+c+'33'+c+'34| ',
               ' |35'+c+'36'+c+'37'+c+'38'+c+'39'+c+'40'+c+'41| ',
               ' |––––––––––––––––––––| ',
               '_|_                  _|_']
    if _==2:
        lines=['–'*(width-2),
               '',
               'This is the window size!! ('+str(width)+')',
               '',
               'Increase the text size',
               "to whatever's comfortable",
               '',
               'Then resize your terminal window to',
               "the top and right of this box, and",
               "you're ready to play!",
               '',
               "Input enter at ':' below once ready -->"]
        for i in range(len(lines)): #make a box around the screen
            lines[i]='|'+centerLine(lines[i],width-2,True)+'|'
    elif inGame: #add title, information, and messages to game board
        global title,name; l=la=0
        for i in lines: 
            if len(i)>l: l=len(i) #longest line length
        for i in after: #get length of longest line in after
            if len(i)>la: la=len(i)
        lines.append(centerLine(msg0,l,True)) #add msg0 to bottom
        #format first line
        w=(width-len(lines[0]))//2 #space available to left side of board
        if w<len(name): name=name[0:w]
        lines[0]=name+' '*(w-len(name))+lines[0]
        w=width-len(lines[0]) #space available to right side of board
        if w<len(title): title=title[0:w]
        lines[0]+=' '*(w-len(title))+title
        #format rest of lines
        for i in range(1,len(lines)): #add before & after to each line
            w=(width-len(lines[i]))//2 #add before, left
            if w<(len(before[i-1])+1): before[i-1]=before[i-1][0:w-1]
            lines[i]=' '+before[i-1]+' '*(w-len(before[i-1])-1)+lines[i]
            w=width-len(lines[i]); l=la #add after, right
            if w<(len(after[i-1])+1):
                after[i-1]=after[i-1][0:w-1]
                l=len(after[i-1])
            lines[i]+=' '*(w-l-1)+after[i-1]+' '
        lines.insert(0,'') #add line above (for printing space)
        lines.append(centerLine(msg)) #add message below
        if len(msg)>width: lines.append(centerLine(msg[width:])) #add additional line for longer messages
    else: lines=[centerLine(lines[i]) for i in range(len(lines))] #center plain old board
    print('\n'.join(lines)) #print lines

def saveMove(move,piece): #adds move to movelst
    opp=x if piece==y else y #opposite piece
    movetype=0 #determine 'highlight status' of move
    if debug==2: print(' – assigning movetype to move '+str(move)+' – ')
    if ptItr(move,piece): movetype=6     #made 4-in-row
    elif ptItr(move,opp): movetype=5     #blocked 4-in-row
    elif ptItr(move,piece,2): movetype=4 #made 3-in-row
    elif ptItr(move,opp,2): movetype=3   #blocked 3-in-row
    elif ptItr(move,piece,1): movetype=2 #made 2-in-row
    elif ptItr(move,opp,1): movetype=1   #blocked 2-in-row
    movelst.append([move,piece,movetype])

def replay(movetypelst=[6,5],pre=-1):
    global b,before,after,animation,movelst,screenlst,msg,title,name
    b=[' ']*42; before=[' ']*10; after=[' ']*10 #start of board
    screenlst=[[' ']*42]
    tanimation=animation; animation=True #change animation back to what it was after replay
    n=6 #number of screens in row
    for i in range(len(movelst)): #screenlst = all the screens in game
        if len(movelst[i])==3: #if [move,'piece',movetype]
            getPos(movelst[i][0])
            b[pos]=movelst[i][1] #place move in screen
        else: b=movelst[i].copy() # copy edit screen
        screenlst.append(b.copy()) #add new screen to screenlst
    if debug>0:
        print('Printing all '+str(len(screenlst))+' screens, '+str(n)+' in each row')
        print('Under each screen is next move (column-piece-movetype')
        for i in range(0,len(screenlst),n): #print n screens in a row
            print('Screen '+str(i)+'-'+str(i+n-1)+':')
            for c in range(0,len(screenlst[i]),7): #prints 1 line for each row in screen
                print('|'+'| |'.join( #connects the row of all n screens
                    [''.join(screenlst[i+_][c:c+7]) #gets row of each screen
                     for _ in range(n) if (i+_)<len(screenlst)]) #if screen exists
                      +'|')
            lst_=[]
            for _ in range(n):
                if (i+_)<len(movelst):
                    lst_.append('-'.join(slst(movelst[i+_])) if len(movelst[i+_])==3 else 'edits')
            print('  '+'     '.join(lst_))
    highlights=[]; movesmatched=[] #integer values of which screens to print
    #if move matches desired movetype, add move and premoves to highlight
    for i in range(len(movelst)): #iterate through all moves made
        for movetype in movetypelst: #determine which screens to replay
            p=0 if pre==-1 else pre
            #if movetype>4 and pre==-1: p=1
            #look for all instances of movetype
            if len(movelst[i])==3: #doesnt look at edit screens
                if movelst[i][2]==movetype: #if move is movetype
                    [highlights.append(i-_) for _ in range(p+1) if i-_>=0] #add up premoves
                    movesmatched.append(i)
                    break #only find one matching move per move in movelst
    if debug>0: print('\nhighlights:\n'+', '.join(slst(movesmatched)))
    if debug==2: print('highlights + pre:\n'+', '.join(slst(highlights)))
    res=[] #removes duplicates in highlights (from pre stuff overlapping)
    [res.append(x) for x in highlights if x not in res]; res.sort()
    highlights=res
    t=''
    if debug>0:
        print('highlights + pre post-sort:\n'+', '.join(slst(highlights)))
        t=input(':')
    mvtplst=['moved','blocked 2-in-row','made 2-in-row','blocked 3-in-row',
             'made 3-in-row','blocked 4-in-row','won!']
    title='Connect 4™ Replayer®'
    name='Replaying game '+str(gamenum)
    if 'e' not in t:
        for i in range(len(highlights)):
            d=1.5 #time delay between screen prints
            s=highlights[i]
            b=screenlst[s].copy()
            if s in movesmatched: #if one of the matches
                msg=movelst[s][1]+' '+mvtplst[movelst[s][2]]+' '+str(movelst[s][0])
                d+=1.5
            elif i+1<len(highlights): #search for next match (if not last thing)
                for _ in range(i+1,len(highlights)-1): #up to last term
                    s_=highlights[_]
                    if s_ in movesmatched:
                        msg=movelst[s_][1]+' '+mvtplst[movelst[s_][2]]+' '+str(movelst[s_][0])
                        break
            if len(movelst[s])==3: addMove(movelst[s][0],movelst[s][1]) #if not edit screen, animation
            else: b=screenlst[s+1].copy()
            printBoard()
            time.sleep(d)
    animation=tanimation

def addMove(move,piece): #adds move to column in board
    x=-1; y=move-8
    if animation:
        time.sleep(speed)
        a[move-1]=piece
        printBoard()
        time.sleep(speed)
        a[move-1]=' '
        a[move+6]=piece
        printBoard()
        time.sleep(speed)
        a[move+6]='_'
    for i in range(move-1,len(b)-7+move,7): #iterates down column
        if b[i]==' ': #if space is empty, add piece
            x+=1; y=i
            b[i]=piece
            if i-7>=0: b[i-7]=' ' #clear space above
            if animation: printBoard(); time.sleep(speed)
        else: break
    global pos,row
    row=x; pos=y

def getPos(move): #gets row (-1,0,1,2,3,4,5) and pos (-7 to 41)
    x=-1; y=move-8
    for i in range(move-1,len(b)-7+move,7): #iterates down column
        if b[i]==' ': x+=1; y+=7
        else: break
    global pos,row
    row=x; pos=y

def ptItr(move,piece,number=3,after=False): #checks for n-in-row from move position
    #after means addMove is used, so shouldn't check for pos and row again
    if not after: getPos(move)
    p=pos #pos (-7 to 41)
    r=row #row (-1,0,1,2,3,4,5)
    c=move-1 #column (0-6)
    lst=[]; directions=[]
    for _ in range(4): #checks: | , – , / , \
        v=w=0; dirlst=[]
        if pos<0: break #doesn't check full things
        for i in range(1,number+1):
            if _==0 and r<=5-i: #check i below
                if b[p+7*i]==piece: v+=1; dirlst.append('↓')
                else: break
            if _==1 and c>=i: #check i left
                if b[p-i]==piece: v+=1; dirlst.append('←')
                else: break
            if _==2 and c>=i and r<=5-i: #check i bot left
                if b[p+6*i]==piece: v+=1; dirlst.append('↙')
                else: break
            if _==3 and c>=i and r>=i: #check i top left
                if b[p-8*i]==piece: v+=1; dirlst.append('↖')
                else: break
        for i in range(1,number+1-v): 
            if _==0 and r>=i: #check i above
                if b[p-7*i]==piece: v+=1; dirlst.append('↑')
                else: break
            if _==1 and c<=6-i: #check i right
                if b[p+i]==piece: v+=1; dirlst.append('→')
                else: break
            if _==2 and c<=6-i and r>=i: #check i top right
                if b[p-6*i]==piece: v+=1; dirlst.append('↗')
                else: break
            if _==3 and c<=6-i and r<=5-i: #check i bot right
                if b[p+8*i]==piece: v+=1; dirlst.append('↘')
                else: break
        for i in dirlst: lst.append(i) #transfer 1-direction moves to all moves seen
        if v>=number: #find more than 1 n-in-rows for a single move
            res=[]; [res.append(x) for x in dirlst if x not in res]
            directions.append(''.join(res))
    direction='/'.join(directions) #lists if theres more than one direciton found
    if len(lst)>0 and debug==2: #only prints if there is adjacent piece
        print('Checking '+piece+' '+str(number+1)+'-in-a-row, move '+str(move)+': '+', '.join(lst))
    if len(direction)>0: #if found a match
        if debug>0: print('    '+piece+' made '+str(number)+'-in-a-row, '+direction+' from move '+str(move))
        ptItrLst.append(piece+', '+str(number+1)+'-peat, '+direction+', '+str(move))
        return True #found it
    else: return False

#------------Intro------------#
if not skip and not justreplay:
    resetBoard()
    print('\n\n'+centerLine('Welcome to Connect 4™!'))
    if delay: time.sleep(2)
    printBoard(False)
    print("\nHow to play:\n    1. Type after ':' at the bottom of the screen"+
          "\n    2. Input a column 1-7, then press enter\n    3. Get 4 in a row!!"+
          "\n    4. (Input 'help' during the game for help)")
    if delay: time.sleep(3)
    t=input("\n\nPractice by typing an input after the ':' now\n:")
    if t!='skip':
        print('\nNice!')
        if delay: time.sleep(2)
        printBoard(False,2)
        t=input(':')
        print(centerLine("Now that you're ready to play,")+'\n'+
              centerLine("let's start with some specifications")+'\n')
        if delay: time.sleep(2)
    if justreplay or t=='skip': #use 'skip' to computer ai 4 v computer ai 4
        specifications=False; automatic=True; gamemode=3
        ailvl=[4,4]; name1='Computer 1'; name2='Computer 2'

#play multiple games of connect 4 in a row
while not skip:
    ptItrLst=[]; moveslst=[]
    #-------Specifications--------#
    if specifications:
        #select gamemode
        while not keepgamemode: #1-player, 2-player, or dueling computers
            numwins=numlosses=numties=0 #choosing a new gamemode = new chain of games
            t=input('Single-player, 2-player, or dueling computers?\n:').lower().strip()
            if '1' in t or t=='singleplayer' or t=='single-player' or t=='one' or t=='computer' or t=='s' or (t=='' and not delay):
                gamemode=1
                name1='Player'; name2='Computer'
                break
            if '2' in t or t=='multiplayer' or t=='two' or t=='m':
                gamemode=2
                name1='Player 1'; name2='Player 2'
                t=input(name1+' name?\n:') #select names for two-player
                if t!='': name1=t
                t=input(name2+' name?\n:')
                if t!='': name2=t
                break
            if '0' in t or '3' in t or 'ai' in t or 'computer' in t:
                gamemode=3
                name1='Computer 1'; name2='Computer 2'
                break
            if t=='exit' or t=='end': e=True
        ailvl=[] #select computer(s) skill level
        while gamemode!=2 and not e:
            name=name1 if gamemode==3 and len(ailvl)==0 else name2
            t=input(name+' skill level? (1-4) easiest to hardest\n:').lower().strip()
            if t.isdigit():
                if 0<int(t)<5: ailvl.append(int(t))
                else: continue
            elif 'eas' in t: ailvl.append(1)
            elif 'har' in t or (not delay and t==''): ailvl.append(4) #default
            elif t=='exit' or t=='end' or t=='stop': e=True
            else: continue
            if gamemode==1 or len(ailvl)==2: break #only asign twice for gamemode==3
        if gamemode==3 and not e: #add lvl to name if 2 computers
            name1='Comp 1 [lvl '+str(ailvl[0])+']'
            name2='Comp 2 [lvl '+str(ailvl[1])+']'
        piecelist=['O','X','#','+','•'] #select pieces
        strlst=[name1.lower(),name2.lower()]; i=0
        while not e:
            print('Select '+strlst[i]+"'s piece (1-5) -")
            str1=''
            for _ in range(len(piecelist)): str1+='\t'+str(_+1)+': '+piecelist[_]
            print(str1) #print available pieces
            t=input(':').lower().strip()
            if gamemode!=2 and t=='': #defaults pieces 
                x=piecelist[0] #player/computer 1 get O
                y=piecelist[ailvl[(gamemode-1)//2]] #computer/computer 2 gets X,#,*,+
                break
            for _ in range(len(piecelist)): #pieces --> number
                if t.upper()==piecelist[_]: t=str(_+1)
            if t.isdigit():
                if 0<int(t)<=len(piecelist): 
                    if i==0: #set x & from piecelist
                        x=piecelist.pop(int(t)-1)
                        i+=1
                    else: #sets y if x='O' & gamemode=2 on second pass
                        y=piecelist[int(t)-1]
                        break
                    if int(t)!=1: #automatically set y to 'O'
                        y=piecelist[0]
                        break
                    elif gamemode!=2: #set computer/computer 2 to ailevel
                        y=piecelist[ailvl[(gamemode-1)//2]-1]
                        break
            if t=='*': #idk why but you can use * as a piece too
                if i==0:
                    x=t
                    y=piecelist[0]
                else: y=t #x is already 'O'
                break
            if t=='exit' or t=='end' or t=='stop': e=True
    print(name1+' is '+x+' and '+name2+' is '+y)
    if delay: time.sleep(1)
    
    #--------Play Connect 4--------#
    resetBoard()
    if ailvl==[]: ailvl=[0]
    piece=y if ailvl[0]==4 and gamemode==1 else x #who goes first
    win=msg0=msg=''; title='Connect 4™'; before=['']*10; after=['']*10
    movelst=[]
    replaydebug=debug
    if justreplay: automatic=True; debug=0
    while not e: #play game, repeats for each move by player or computer
        #get name
        name=name1+"'s turn:" if piece==x else name2+"'s turn:"
        if piece==y and gamemode==1: name='Computer [lvl '+str(ailvl[0])+']:'
        if delay: time.sleep(1)
        if not justreplay: printBoard()
        msg0=msg=''; before=['']*10; after=['']*10 #reset screen
        g=0 #number of non-inputs in a row
        #-----Player Moves-----#
        while gamemode!=1 or piece==x: #player input
            if automatic and gamemode==3: break #automatic is automatic
            t=input(':').lower().strip()
            if t=='' and gamemode==3: break #can quickly cycle thru computers
            if e: #exit confirmation
                if t=='y' or t=='exit' or 'ye' in t: break
                else: e=False
            if 'debug' in t or 'animation' in t or 'delay' in t or 'automatic' in t:
                t=t.replace(' ','').split(','); msglst=[]
                for i in t:
                    if i=='debug' or i=='animation' or i=='delay' or (i=='automatic' and gamemode==3):
                        exec(i+'=False if '+i+'==True else True') if eval('isinstance('+i+', bool)') else exec(i+'+=1 if '+i+'!=2 else -2')
                        msglst.append(i+' is now '+str(eval(i))) 
                    elif i!='': msglst.append(i+' is not a changeable variable')
                msg='--- '+'; '.join(msglst)+' ---'
            elif t=='exit':
                msg='You sure you want to exit?'
                e=True
            elif 'copy' in t: #print current board
                print("b=['"+"','".join(b)+"']")
                time.sleep(5)
            elif t=='help' or t=='show' or 'num' in t: #add column numbers to top of board
                a[0:7]=[str(i) for i in range(1,8)]
                a[8:14]=' '*7
                if gamemode!=3: msg="Pick a column 1-7"
                before=['','','',"'edit'","'animation'","'debug'","'delay'",'','','']
            elif t.isdigit() and gamemode!=3: #place a move
                if 0<int(t)<8: 
                    move=int(t)
                    if b[move-1]==' ': break
                    msg='That column is full already.'
                else: msg="Pick a column 1-7. Type 'help' for more"
            #----Edit Screen----#
            elif t=='edit':
                editslst=[]; g=0 #keep track of edits
                title='Connect 4™ Editor®'
                msg="Welcome to the editor! Type 'help' for more info"
                while 1:
                    name='Current piece: '+piece
                    if 'var' in t: printBoard(True,1)
                    else: printBoard();
                    msg=msg0=''; before=['']*10; after=['']*10 #reset screen info
                    tt=input(':').strip()
                    t=tt.lower()
                    if t=='exit': break
                    if t=='':
                        g+=1
                        if g==1: msg="--- Type 'help' for help ---"
                        else: msg="--- you have left the editor ---"; break
                    elif t=='switch':
                        if debug==2: #switch from debug mode do gameplay mode
                            debug=0; animation=delay=True
                            msg='--- Now in regular gameplay mode ---'
                        else:
                            debug+=1; animation=delay=False
                            msg='--- Now in debug '+str(debug)+' mode ---'
                    elif 'debug' in t or 'animation' in t or 'delay' in t or 'automatic' in t:
                        t=t.replace(' ','').split(','); msglst=[]
                        for i in t:
                            if i=='debug' or i=='animation' or i=='delay' or (i=='automatic' and gamemode==3):
                                exec(i+'=False if '+i+'==True else True') if eval('isinstance('+i+', bool)') else exec(i+'+=1 if '+i+'!=2 else -2')
                                msglst.append(i+' is now '+str(eval(i))) 
                            elif i!='': msglst.append(i+' is not a changeable variable')
                        msg='--- '+'; '.join(msglst)+' ---'
                    elif t=='x': piece=x
                    elif t=='y': piece=y
                    elif 'copy' in t: print("b=['"+"','".join(b)+"']"); time.sleep(5)
                    elif t=='help' or t=='h':
                        before=['','Editor Info:','','This lets you','edit the board!','',"'var'iable list","'help'","'exit'","'switch' mxodes"]
                        after=['','Editor Commands:    ','','x = '+x+', y = '+y,'add move: _','clear column: c_',"'clear' screen",'u or undo','find, find_','findnext']
                        msg0='+ any commands'
                    elif 'var2' in t or 'expla' in t:
                        before=['Variables 2','','animation spots','board spots','select piece','column character','','resets spots','','']
                        after=['','screen width','animation speed','do animations','debug msg lvl','have pauses',"winstate ('',T,F)",'1=p-c; 2=p-p; 3=c-c','[c1 ailvl, c2 ailvl]','']
                    elif 'var' in t:
                        before=['Useful Variables','',"a[_]=''","b[_]=''","piece=''","columnbreak='"+columnbreak+"'",'','resetBoard()','for a[] & b[]','']
                        after=['','width='+str(width),'speed='+str(speed),'animation='+str(animation),'debug='+str(debug),'delay='+str(delay),'win='+str(win),'gamemode='+str(gamemode),'ailvl='+','.join(slst(ailvl)),'']
                        msg="--- Input 'var2' to show variable info ---"
                    elif t.startswith('c'): #clear
                        if len(t)==2: #column clear
                            if t[1].isdigit():
                                if 0<int(t[1])<8: #move fits in board
                                    lastclear=[]
                                    for i in range(int(t[1])-1,len(b)-7+int(t[1]),7):
                                        lastclear.append(b[i])
                                        b[i]=' '
                                editslst.append([int(t[1]),lastclear]) #[edit1,edit2,...,[1,[' ',' ',' ',' ',' ',' ','x']]]
                                msg='--- Column '+t[1]+' succesfully cleared ---'
                        elif t=='c' or t=='clear': #clear entire board
                            lastclear=[]
                            for i in range(len(b)):
                                lastclear.append(b[i])
                                b[i]=' '
                            editslst.append([lastclear]) #[edit1,edit2,...,[[literally the entire board]]]
                            msg='--- Entire board succesfully cleared ---'
                    elif t.isdigit(): #add move directly w number
                        if 0<int(t)<8: #move fits in board
                            if b[int(t)-1]==' ': #move is open
                                addMove(int(t),piece)
                                editslst.append([pos])
                                msg='--- '+piece+' added to column '+t+' ---'
                    elif t.startswith('a') and len(t)==2: #add move
                        if t[1].isdigit():
                            if 0<int(t[1])<8: #move fits in board
                                if b[int(t[1])-1]==' ': #move is open
                                    addMove(int(t[1]),piece)
                                    editslst.append([pos]) #[edit1,edit2,...,[37]]
                                    msg='--- '+piece+' added to column '+t[1]+' ---'
                    elif t=='u' or t=='undo': #undo last edit
                        if len(editslst)!=0:
                            lastedit=editslst.pop(len(editslst)-1) #pops out last term in editslst
                            if len(lastedit)==1:
                                if isinstance(lastedit[0],int): #undo last add
                                    b[lastedit[0]]=' '
                                    msg='--- Undid addition of to column '+str(1+lastedit[0]-7*(lastedit[0]//7))+' ---'
                                else: #undo last clear
                                    for i in range(len(lastedit[0])): b[i]=lastedit[0][i]
                                    msg='--- Undid screen clear ---'
                            else: #column clear
                                _=0
                                for i in range(lastedit[0]-1,len(b)-7+lastedit[0],7):
                                    b[i]=lastedit[1][_]
                                    _+=1
                                msg='--- Undid clear of column '+str(lastedit[0])+' ---'
                        else: msg='--- no more edits to undo ---'
                    elif t.startswith('find'):
                        _=debug; ptItrLst=[]
                        if debug==0: debug=1
                        if len(t)==5:
                            if t[4].isdigit(): #'find4', 'find3', 'find2'
                                if t[4]=='4':
                                    for c in range(1,8):
                                        ptItr(c,x)
                                        ptItr(c,y)
                                if t[4]=='3':
                                    for c in range(1,8):
                                        ptItr(c,x,2)
                                        ptItr(c,y,2)
                                if t[4]=='2':
                                    for c in range(1,8):
                                        ptItr(c,x,1)
                                        ptItr(c,y,1)
                                msg='--- Found all potential '+t[4]+'-in-a-rows ---'
                        elif t=='findnext':
                            clst=[1,2,3,4,5,6,7]
                            for c in clst:
                                getPos(c); row-=1; pos-=7
                                if pos>=0: #move 1 up is open
                                    if ptItr(c,x,3,True): print(y+" shouldn't  move "+str(c))
                                    if ptItr(c,y,3,True): print(x+" shouldn't move "+str(c))  
                        else: #'find'
                            for c in range(1,8):
                                ptItr(c,x,2)
                                ptItr(c,y,2)
                                ptItr(c,x)
                                ptItr(c,y)
                            msg='--- Found all 4- and 3-in-a-rows ---'
                        debug=_
                        for i in range(len(ptItrLst)): #put ptItrLst into screen
                            res=[] #removes duplicates in ptItrLst
                            [res.append(x) for x in ptItrLst if x not in res]; res.sort()
                            ptItrLst=res
                            if i>15:
                                msg='--- Too many n-in-rows found! ('+len(ptItrLst)+')'+' ---'
                                break
                            if i<=7: after[i+1]=ptItrLst[i]
                            else: before[i-7]=ptItrLst[i]
                    else:
                        try: #should bypass errors from exec
                            exec(tt)
                            if speed<0.1 or speed>0.5: speed=0.2
                            if isinstance(ailvl,int): #correct ailevel
                                ailvl=[ailvl,ailvl] if gamemode==3 else [ailvl]
                            for i in range(len(ailvl)):
                                if ailvl[i]>4: ailvl[i]=4
                        except: msg="--- No-go. Type 'help' for help ---"
                    if t!='': g=0
                if t!='': msg=''
                title='Connect 4™'  #reset to print input screen
                name=name1+"'s turn:" if piece==x else name2+"'s turn:"
                movelst.append(b.copy()) #save state of edit board after editing
            else:
                g+=1
                if gamemode!=3: msg="--- Pick a column 1-7. Type 'help' for more ---"
            if t!='': g=0
            if g>=2 and gamemode==3: break #two times where no commands were picked
            printBoard()
            if '1' in a: #reset a after help
                a[0:7]=' '*7
                a[8:14]='_'*7
            msg=msg0=''; before=['']*10; after=['']*10 #reset screen
        if e: break #exit the game
        #------Computer Moves-----#
        if gamemode==1 and piece==y or gamemode==3:
            msg=name1 if gamemode==3 and piece==x else name2
            msg+=' placing optimal piece...'
            ai=1 if gamemode==3 and piece==y else 0
            opp=x if piece==y else y
            if not justreplay and gamemode==3: printBoard()
            ptItrLst=[]; clst=[] #column list, open column list
            [clst.append(c) for c in range(1,8) if b[c-1]==' ']
            olst=clst.copy()
            if debug>0: print('Available moves: '+', '.join(slst(clst)))
            if ailvl[ai]>=3: #don't do moves that will make win for player
                for c in olst:
                    getPos(c); row-=1; pos-=7
                    if pos>=0:
                        if ptItr(c,opp,3,True): #if move above will make opponent win
                            clst.remove(c)
                            if debug==2: print('- removed move '+str(c)+'; win for '+opp)
            if clst!=[] and clst!=olst:
                olst=clst.copy() #new default
                if debug>0: print('Available moves now: '+', '.join(slst(clst)))
            if ailvl[ai]==4: #don't do moves that will block win for computer
                for c in clst.copy():
                    getPos(c); row-=1; pos-=7
                    if pos>=0:
                        if ptItr(c,piece,3,True): #if move above will make self win
                            clst.remove(c)
                            if debug==2: print('- removed move '+str(c)+'; blocks win for '+piece)
            if debug>0 and clst!=olst: print('Available moves now: '+', '.join(slst(clst)))
            if len(clst)==0: #back to original moves
                clst=olst
                if debug>0: print('Defaulting moves back to: '+', '.join(slst(clst)))
            #picks random move
            move=clst[random.randint(0,len(clst)-1)]
            if debug>0: print('random move = '+str(move))
            #computer strategy
            if ailvl[ai]>=2:
                if debug==2: print(' – trying to make 3-in-row – ')
                for c in clst: #  makes 3 in a row
                    if ptItr(c,piece,2): move=c; break
            if ailvl[ai]>=3:
                if debug==2: print(' – trying to block 3-in-row – ')
                for c in clst: #  blocks 3 in a row
                    if ptItr(c,opp,2): move=c; break
            if ailvl[ai]==4: #check for 'open' 3-in-rows that will win game
                if debug==2: print(" – trying to block 'open' 3-in-row – ")
                for c in clst: #  block 'open' 3-in-row
                    if ptItr(c,opp,2):
                        temppos=pos; b[pos]=opp; op=0
                        for o in clst: #can make two 4-in-rows after
                            if ptItr(o,opp): op+=1
                        b[temppos]=' '
                        if op>=2: move=c; break
                if debug==2: print(" – trying to make 'open' 3-in-row – ")
                for c in clst: #  make 'open' 3-in-row
                    if ptItr(c,piece,2):
                        temppos=pos; b[pos]=piece; op=0
                        for o in clst: #can make two 4-in-rows after
                            if ptItr(o,piece): op+=1
                        b[temppos]=' '
                        if op>=2: move=c; break
            if ailvl[ai]>=3 and b[38]==' ' and 4 in clst: #move middle if not already
                if debug==2: print(" – moved middle bc why not –")
                move=4
            if ailvl[ai]>=1: #don't lose the game
                if debug==2: print(" – trying not to lose – ")
                for c in range(1,8): #blocks opponents 4 in a row
                    if ptItr(c,opp): move=c; break
            if ailvl[ai]>=2: #win the game
                if debug==2: print(" – trying to win – ")
                for c in range(1,8): #makes 4 in a row
                    if ptItr(c,piece): move=c; break
            if debug>0 or gamemode==3:
                res=[] #removes duplicates in ptItrLst
                [res.append(x) for x in ptItrLst if x not in res]
                res.sort(); ptItrLst=res
                for i in range(len(ptItrLst)): #put ptItrLst into screen
                    if i>15:
                        msg='--- Too many n-in-rows found! ('+len(ptItrLst)+') ---'
                        break
                    if i<=7: after[i+1]=ptItrLst[i]
                    else: before[i-7]=ptItrLst[i]
        #add move to board
        saveMove(move,piece)
        addMove(move,piece)

        if debug>0: print('-'.join(slst(movelst[len(movelst)-1])))
        if debug==2: t=input(':')
        
        #says where last move went
        msg='--- '+name1 if piece==x else '--- '+name2
        msg+=' placed '+piece+' at '+str(move)+' ---'
        
        #detect win
        if ptItr(move,piece,3,True): win=True if piece==x else False
        if win!='': break #you can use edit to win or lose if u want
        if ' ' not in b[0:7]: break #board full=tie
        
        piece=y if piece==x else x #switch between players

    #---------Post-Game Messages-------#
    if not e: #only if player didn't exit
        if win=='':
            str0="The computers tied... maybe bc they run on the same code!" if gamemode==3 else "Wow... a tie?! Well-played, well-played."
            numties+=1
        else:
            if win:
                numwins+=1
                str0="You ("+x+") beat the computer on difficulty "+str(ailvl[0])+"!" if gamemode==1 else name1+" ("+x+") won!"
            else:
                numlosses+=1
                str0="You lost to the computer ("+y+") on difficulty "+str(ailvl[0]) if gamemode==1 else name2+" ("+y+") won!"
        printBoard(False)
        print('-'*width+'\n'+centerLine(str0))
        if delay: time.sleep(2)
    e=specifications=keepgamemode=automatic=False; debug=replaydebug
    while 1:
        t=input('Replay?\n:')
        if t=='n' or 'no' in t or t=='exit': break
        if t.isdigit():
            replay(pre=int(t))
            break
        if t!='':
            replay()
            break
    str0=['1-player game','2-player game','game between computers'][gamemode-1]
    while 1: #play again?
        t=input('Continue playing Connect 4™?\n:').lower().strip()
        if 'copy' in t: #print current board
            print("b=['"+"','".join(b)+"']")
            time.sleep(5)
            continue
        if t=='stop' or t=='exit' or t=='end' or t=='n' or 'no' in t: e=True
        elif delay:
            print("Another game!")
            time.sleep(1)
        break
    if not e: #same specifications?
        t=input('Same specifications, '+str0+'?\n:').lower().strip()
        if t=='stop' or t=='exit' or t=='end': e==True
        elif t=='n' or t=='no' or 'dif' in t: specifications=True
        else:
            print('Playing another game with the same specifications...')
            if delay: time.sleep(1)
    if e: break;
#-----Exited Connect 4----#
if not skip:
    if gamemode==1: print(centerLine('You won '+str(numwins)+', lost '+str(numlosses)+', and tied '+str(numties)));
    else:
        print(centerLine(name1+' won '+str(numwins)+' time'+s(numwins)))
        print('\n'+centerLine(name2+' won '+str(numlosses)+' time'+s(numlosses)))
        print('\n'+centerLine('and '+("y'all" if gamemode!=3 else 'they')+' tied '+str(numties)+' time'+s(numties)))
    if delay: time.sleep(3)
    print('\n'+centerLine("Thanks for playing Connect 4™! Come again soon!"))
    if delay: time.sleep(2)
    print(centerLine("Don't forget to close IDLE so it doesn't crash")+'\n')
    if delay: time.sleep(2)
#---------Memes----------#
t=input('>>> ').lower().strip() #30 lines long
if 'squid' in t or 'hot' in t:
    txt='     ⠀⠀⠀⢀⣀⣤⣴⣶⣶⣾⣿⣷⣶⣶⣦⣄⡀⠀⠀⠀          ⠀⢠⣴⣿⣿⣿⣿⣿⣭⣭⣭⣭⣭⣿⣿⣿⣿⣧⣀⠀          ⢰⣿⣿⣿⣿⣿⣯⣿⡶⠶⠶⠶⠶⣶⣭⣽⣿⣿⣷⣆          ⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿          ⠈⢿⣿⣿⡿⠋⠉⠁⠈⠉⠛⠉⠀⠀⠀⠈⠻⣿⡿⠃          ⠀⠀⠀⠉⠁⠀⢴⣐⢦⠀⠀⠀⣴⡖⣦⠀⠀⠈⠀⠀          ⠀⠀⠀⠀⠀⠀⠈⠛⠋⠀⠀⠀⠈⠛⠁⠀⠀⠀⠀⠀          ⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⣀⠀⠀⠀⢀⡀⠀⠀⠀⠀          ⠀⠀⢀⡔⣻⣭⡇⠀⣼⣿⣿⣿⡇⠦⣬⣟⢓⡄⠀⠀          ⠀⠀⠀⠉⠁⠀⠀⠀⣿⣿⣿⣿⡇⠀⠀⠉⠉⠀⠀⠀          ⠀⠀⠀⠀⠀⠀⠀⠀⠻⠿⠿⠟⠁⠀⠀⠀⠀⠀⠀⠀               ⣠⣼⣿⣷⣶⣾⡷⢸⣿⣿⣿⣿⣿⣶⡄           ⣀⣤⣴⣾⣶⣮⣭⣭⣭⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀         ⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣸⣿⣿⣧         ⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⢻⣿⣿⡄        ⢸⣿⣮⣿⣿⣿⣿⣿⣿⣿⡟⢹⣿⣿⣿⡟⢛⢻⣷⢻⣿⣧         ⣿⡏⣿⡟⡛⢻⣿⣿⣿⣿⠸⣿⣿⣿⣷⣬⣼⣿⢸⣿⣿         ⣿⣧⢿⣧⣥⣾⣿⣿⣿⡟⣴⣝⠿⣿⣿⣿⠿⣫⢾⣿⣿⡆        ⢸⣿⣮⡻⠿⣿⠿⣟⣫⣾⣿⣿⣿⣷⣶⣾⣿⡏⣾⣿⣿⡇        ⢸⣿⣿⣿⡇⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⡇        ⢸⣿⣿⣿⡇ ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿         ⣼⣿⣿⣿⢃⣾⣿⣿⣿⣿⣿⢹⣿⣿⣿⣿⣿⣇⢿⣿⡇         ⣿⣿⡟⣵⣿⣿⣿⣿⣿⣿⣿⣼⣿⣿⣿⣿⣿⣿⣎⢿          ⣿⡟⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦          ⡏⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⣿⣿⣿⣿⣿⣷⡄        ⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢘⣿⣿⣿⣿⣿⣿⣿⡆      ⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡅⣿⣿⣿⣿⣿⣿⣿⣿⡀    ⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡅⣿⣿⣿⣿⣿⣿⣿⣿⡇   ⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⡇   ⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠣⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇   ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠑⣿⣮⣝⣛⠿⢿⣿⣿⣿⣿⠁  ⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟   ⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇    ⢹⣿⣿⣿⣿⣿⣿⣿⡟⠁   ⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏     ⢸⣿⣿⣿⣿⣿⣿⣿⠁    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟      ⠸⣿⣿⣿⣿⣿⣿⠋    ⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿       ⢸⣿⣿⣿⣿⣿⣿     ⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇       ⢸⣿⣿⣿⣿⣿⢟    '
    text=[txt[i:i+30] for i in range(0,len(txt),30)]
elif 'mario' in t.lower() or 'judah' in t.lower():
    text=['⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⡿⣿⢿⣻⡿⣿⣻⡿⣿⢿⡿⣿⢿⡿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣯⣷⣿⣾⣿⣿⣻⣿⣿⣻⣟⣯⣿⣿⣽⣿⣻⣿⣿⣿⣿⣿⣿⣾⣿⣾⣿⣯⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣷⣿⣿⡿⣿⡿⣿⣽⣿⣿⣽⣟⣿⣿⣷⣿⣷⣿⣿⢿⣷⣿⣿⣿⢿⣿⣿⣿⣿⣽⣷⣿⡿⣿⣾⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣽⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⡿⣷⣿⣿⣽⣿⣿⣿⣿⣿⣾⣿⡿⣿⣾⣿⣿⡿⣟⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⡿⣿⣾⣿⣿⣻⣽⢿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣽⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣻⣽⣿⣿⣿⡿⣿⣯⣷⣿⣟⣿⣯⣿⣿⡿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣿⣯⣿⣿⣯⣿⣯⣿⣿⡿⣿⣞⡯⣟⡗⣗⣟⢞⣟⡮⣗⢯⣺⣻⢽⣗⡯⣷⣻⣽⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣿⢿⣿⣻⣿⣿⣿⡿⣟⡯⣟⢮⢯⡺⣪⢧⡳⢝⢜⢮⡪⡳⡕⡷⣝⣞⢮⢗⣟⣞⣟⣾⣺⣽⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⢿⡽⣽⡳⣽⢺⡪⣎⢗⢜⢕⢕⢕⢕⢱⢙⢜⢮⢮⢯⣳⣳⣳⣳⣳⣟⣾⣻⡾⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⡿⣾⢯⣟⡮⣟⢮⣳⡹⡸⡸⡨⡢⡱⡨⠢⡡⢣⢫⢝⡵⣳⡣⣗⣗⣗⡷⣻⣞⣯⡿⣯⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⡿⣽⣻⣞⡽⣺⢝⢮⢎⢧⢳⢱⠱⡐⡜⢌⢌⢪⢪⢣⡻⣺⡪⣗⣗⣗⡯⡷⣯⢷⣿⣻⣽⣟⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣿⣿⣿⣟⣷⣻⡽⣞⡾⣝⢷⢽⢝⢮⢳⢱⢱⢹⢸⢸⢸⢸⢸⢸⢸⢚⢮⡺⣕⣗⢗⡯⡿⡽⣯⢷⣿⣽⢿⣿⢿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣿⣿⣿⡽⣗⣯⢯⣗⡯⡯⡳⣝⡕⣇⢣⢑⢑⠌⢜⢐⡑⢌⢌⢢⢡⢣⡣⡫⡮⢮⣳⡫⡯⡯⣯⢿⣺⣟⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣿⣿⣷⢿⣽⡾⣽⣺⣮⡯⣯⣺⣪⢎⣎⢆⢇⢕⢅⢳⢸⢰⢸⢸⢜⢮⣺⢵⣫⣗⣷⣯⣿⣽⣯⣿⣷⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⢟⡿⣟⣿⣻⡯⣿⣻⢾⡽⣕⢧⡳⣕⣕⢧⡫⡮⡯⣳⢯⡿⣯⢿⢷⣟⣿⣻⣟⣿⣻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣿⣿⣿⢷⣿⣺⢯⢯⣳⡳⣳⡫⣗⣯⣯⡯⣯⢗⣝⢎⢎⢞⢮⣫⢯⢯⣯⣿⡽⣟⡯⣗⡯⣞⣾⣳⣟⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣿⣿⣿⡿⣷⣻⣽⣷⢷⣻⣾⣿⣷⣷⣷⡿⣽⢽⡪⣏⢦⡓⣗⢗⡯⣟⣾⢷⣿⣿⣟⣯⣿⣻⣾⣷⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣿⡿⣾⢿⣿⣿⣿⣿⣿⢿⣿⢿⢯⠯⣟⡿⡽⣕⢯⢮⢇⢏⡮⣻⣺⢽⣞⣿⢿⢽⢼⣻⣿⣿⣿⣿⣿⣿⣿⣿⢿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣿⣻⣽⣻⣞⣯⣟⡯⡿⣽⡺⡵⣕⢯⡳⣝⣝⢮⡫⡮⣳⢱⢝⣞⣞⣗⢷⢽⢽⣝⣗⣗⣟⡾⣯⢿⣻⢿⣻⣾⣻⣯⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣿⡽⣞⣷⣳⣳⣳⣫⣻⡪⡮⡳⡕⣗⢝⢮⣪⡳⡝⣞⢜⢵⢝⢮⣞⢮⡯⣯⡳⣕⢧⣳⡳⣽⣺⢽⡽⣽⣳⢿⣽⡾⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣯⡿⣽⣞⣗⡗⣗⣕⢧⢳⢕⢵⢹⡸⣕⣗⢗⡽⣝⢮⢳⢱⢝⢵⣫⢯⣻⡺⣮⢳⢳⡱⣝⢮⡺⣽⣺⣳⣻⡽⣷⢿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣯⢿⣳⣗⣗⡯⣳⢳⡹⡜⡎⡎⡲⡱⣧⣳⢵⡹⡮⣳⡱⡨⣪⢷⣝⣗⡵⣽⣺⡽⡱⣹⡪⣳⢝⣞⣞⣞⣗⡿⣯⡿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣟⣯⢷⣗⡷⣫⢗⣗⢕⡇⡇⡇⡇⡯⣟⢿⢿⣿⣯⣷⣽⣺⣵⣟⣾⣷⣿⢿⣻⣿⢕⢕⡝⡮⣳⡳⣵⣳⢽⣯⢷⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣯⢿⣽⣺⢽⣺⡳⣕⢧⡳⡱⡑⢌⢪⢟⡯⣞⢼⡹⡹⢿⡿⡿⣿⣻⡫⡯⣷⡻⣏⢧⡣⡫⡮⣳⢝⣞⢾⡽⣾⣻⣽⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣿⣻⣺⣺⢽⣺⡺⣪⡳⣝⢎⢮⢪⣪⡳⡽⣕⣟⡮⣯⣷⢽⣺⡾⣮⣿⣽⣺⢝⡮⡳⣝⢽⢝⡾⣝⢾⢽⡽⣯⡿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣿⡽⡾⣝⣗⣗⢽⣪⢯⡺⣝⢮⡳⣕⡽⣞⣯⢟⣝⢗⣝⢽⢕⡯⣫⢯⣟⣷⣿⣺⢽⡺⡽⣽⣺⢽⡽⣽⢽⡷⣿⣻⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣿⣟⣯⢿⣺⡺⣝⡮⣳⢽⣺⢵⣻⣞⡿⣽⣺⢽⢮⣳⢵⣫⣗⣯⡳⣯⣞⣾⢽⣿⣯⣯⣯⢷⣯⡯⣯⢿⡽⣟⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣿⡿⣞⣯⢷⢯⣳⢽⣝⣯⣾⣟⣯⣷⡿⡿⡾⡻⣟⢷⢿⣳⢿⢞⡿⡷⡿⣾⢿⣷⣿⣷⣿⣟⣷⢿⡽⣯⣟⣿⣽⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣿⣿⡿⣽⣻⣽⣺⢵⣳⣟⡾⡯⣯⡳⡯⡯⣮⣫⡪⡪⡪⡎⡮⡪⣎⢗⡽⣕⣟⣞⣮⢷⡿⣽⢯⣯⣟⣷⢿⣽⣿⣾⣿⣿⣿⣿⣯⣿⣿⣾⣿⣷⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣿⣿⣿⢯⣷⣻⣞⣽⣺⢾⣻⡽⣳⢯⡿⣽⣳⣗⣟⣮⣟⣞⣮⣗⣯⣯⡿⣯⣿⣽⡾⣯⡿⣽⣟⣾⣽⡾⣿⣻⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣿⣿⢿⢿⣽⢾⣗⡿⣾⣟⣯⣿⢽⡯⣿⢯⡿⣿⢿⢿⢿⢿⢷⡿⣿⢿⡿⣿⢯⡷⣟⣯⡿⣯⣿⢷⣟⣿⣿⣻⣿⣽⣿⣿⣻⣿⣽⣿⣿⣻⣿⣟⣿⣾⣿',
          '⣿⣿⡿⢟⠫⡋⡂⢪⣻⣿⣻⣽⡿⣿⡿⣿⣽⡯⣿⢽⢽⣝⣞⢽⢕⢽⢸⡪⣮⡳⣽⡺⡽⡽⡽⣯⢿⣿⢿⣻⣿⡿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⢿⢿⢿⣿⣿⢿⣿⣻',
          '⡫⠱⡘⢔⢑⠨⢐⠡⢺⣿⣿⣷⣿⣿⣿⣿⣷⢿⣯⡯⣟⡮⣞⣵⡫⣗⣗⣽⣺⣺⣺⣺⢽⡽⣯⡿⣟⣿⣿⣿⣻⣿⣿⢿⣾⣿⡿⣟⣿⣿⣽⣾⢏⠪⡘⡜⡜⡛⠿⡿',
          '⢨⠨⡂⢅⠢⢈⢂⠅⢽⣟⣿⣿⣯⣿⣿⣻⣿⡿⣷⣿⣯⣿⣻⣾⡽⣗⣿⢾⣾⣳⣷⣯⣿⣻⣿⢿⣿⡿⣟⣿⣿⣻⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⢄⠃⢆⠊⢎⢎⢇⢇',
          '⢊⠔⠨⡂⠌⠔⡐⢈⢮⣿⣻⣿⣿⣿⣟⣿⣿⣿⣿⣿⣾⣿⣽⣾⣿⣟⣿⣿⣽⣷⣿⣷⣿⡿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣻⡕⡈⠢⠡⠡⡃⡇⡇',
          '⢐⠌⡪⢐⠡⡁⡂⢂⠕⣞⣯⣷⢿⣿⣿⣿⣷⣿⣿⣽⣿⣿⣻⣿⣿⣻⣿⣽⣿⣯⣷⣿⣿⣿⣿⣿⣾⣿⣯⣷⣿⣿⣿⣽⣿⣿⣿⡿⣿⣻⣽⣿⠢⠨⡈⡪⠨⠢⡪⡨',
          '⢐⠅⡊⢄⠅⡂⠔⡈⡯⢿⣹⣻⣯⣿⣽⣿⣿⣿⣿⣿⣟⣿⣿⣿⢿⣿⣿⡿⣿⣿⣿⡿⣿⣽⣾⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⢿⣿⣿⢿⡿⡁⠅⡂⡢⠡⡑⢌⠪',
          '⡰⢑⠌⡂⡊⡐⡐⠰⢭⢿⢳⣹⣷⣿⣺⢷⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣷⣿⣿⣷⣿⣿⣿⣿⣿⡾⣿⣿⣾⣿⢇⠂⠅⡂⡪⠨⡨⠢⡑',
          '⢐⢅⠪⡐⠔⡐⠨⡈⣎⢇⣟⡕⣿⣿⣾⣻⣗⡿⣟⣿⣿⣻⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣻⣿⣿⡿⡽⣷⣿⢿⣿⣾⡏⠢⡈⡂⡢⢊⠔⢌⢊⠢']
elif 'ob' in t:
    text=['⣳⠐⡴⡒⡣⠪⣰⢰⠬⢲⢒⠪⡴⣰⡡⠆⢫⣼⢾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⡷⣿⣿⣿⣯⣽⣿⣿⣷⣬⡘⢔⠲⡐⡔⡃⣃⢓⢒⠸⢆⢕⢜⠤⡡⡓⡜'
          '⡰⡱⠨⠱⠩⣐⡌⠆⠭⡐⠢⠹⢚⠲⣬⡾⡿⡿⣿⣿⣿⢿⣯⢿⡻⡿⣿⣟⡿⡿⣿⣿⢿⡝⣟⣿⢿⡺⣯⣿⡳⣿⣿⣿⣶⡥⢪⡲⡱⢇⠥⡎⣩⠐⠕⠅⣍⠕⢳⠱',
          '⡄⡆⠝⡘⢌⠂⠌⠮⡐⢌⠡⠣⢃⣼⣻⣝⣟⣭⢺⣴⢻⡯⣝⣧⢫⢷⠯⡏⡎⣯⣧⡟⣗⢿⡭⣿⣿⢿⣵⠿⣿⣿⣻⣿⣿⣿⡆⡜⢎⠑⠡⢂⢦⠊⣎⣑⡘⡺⡑⢅',
          '⡇⠨⢐⠡⢒⢙⠨⠠⢍⢉⢎⠇⣽⣯⡚⡬⢧⢃⣿⣾⣸⣕⣾⢊⣿⣾⣭⣧⢫⡿⣿⠝⡇⡽⣻⣷⢿⣮⣯⣾⣽⣿⣿⢿⣿⣻⣿⠈⠎⠊⠌⢜⢠⢋⠢⠐⠄⠇⡓⢕',
          '⣇⠪⠨⢨⢂⢔⢪⠘⣁⢁⢂⢱⣻⣝⣾⢯⣿⢸⣯⣧⣯⣾⢇⢯⣫⡇⡂⣻⢞⡇⢻⢷⣻⢿⣱⣟⡿⣿⣿⣿⣟⣯⣿⣿⢞⣿⣿⠠⡝⡍⢇⢣⠱⢔⡩⡪⢪⠢⡸⡔',
          '⣿⡐⢌⠪⡀⢜⢰⠨⢐⢀⣑⠘⣿⡽⢻⠙⠫⠿⠽⠹⠏⢃⠣⡳⠘⢑⣨⢻⢛⡀⠧⢹⣚⣱⣙⣛⣶⣪⣛⣻⡛⣿⡿⣟⣿⢿⡿⣀⣷⠔⢬⢐⢘⢔⢸⠐⡍⣤⠒⢌',
          '⣿⡇⢨⠨⢂⠡⢁⢚⠰⣐⡎⠥⣹⡇⢸⠈⣜⣥⢶⠾⢼⣻⣾⣛⣟⡰⠑⠠⢐⢅⣜⣟⠋⡟⢿⣿⣭⡽⣿⣻⡿⢿⣺⢟⢼⢿⢸⡇⣿⡎⡳⢌⢂⢢⣑⢌⠔⡱⡨⡢',
          '⠛⢷⠑⢀⠂⠔⠌⠖⢱⡅⡇⠅⡃⢼⢂⡜⡄⠴⢙⡪⠨⢾⣿⣒⢷⠳⠅⠓⠔⣆⣿⢾⠯⣹⠾⠶⠶⢭⡾⡷⣻⠏⡿⣾⡇⣿⣇⡳⣻⢇⢳⡣⠐⡰⠐⠅⠄⡇⡌⡂',
          '⣶⣾⡀⠥⢃⡨⡀⢊⠠⠹⡜⡘⡠⡭⣆⢒⣐⠆⠧⡀⠌⠂⠧⢑⠠⠐⠤⡁⠅⢝⢿⣜⡯⢖⡍⢗⢼⢡⠚⠄⡯⣪⢽⡜⠇⣾⠿⣫⢣⠸⠈⢺⠸⢑⠌⡊⡑⠌⠔⠅',
          '⣿⢿⣧⢘⢔⢐⠘⠄⢜⢨⠳⢝⠦⠳⢸⢡⠠⠐⡈⡄⢘⠉⢐⡠⠲⠊⣄⢁⡂⣨⣹⠽⣻⣷⣦⠑⢣⠳⣫⣇⣏⣽⢾⣿⣹⣍⠝⡥⣑⠬⢊⢂⢇⢂⠊⠤⠑⡍⢋⠊',
          '⡯⠦⠿⠌⢔⢑⠘⡨⢄⣂⡎⢌⠎⡆⡺⢸⡁⡆⠰⠆⠪⡰⠜⡀⢒⢨⡐⢴⡒⠛⣟⣿⠦⡩⣙⣑⣄⡊⣦⡯⣎⣳⣟⣜⢔⢄⠊⡐⡠⠁⠣⠂⡅⣂⠅⡚⠨⢢⢂⠜',
          '⣶⡦⡤⣒⢸⡐⢌⢀⠎⠔⣃⣊⡋⡐⢔⢏⢮⡐⡐⠈⡞⡬⠕⠰⣰⡙⣀⡓⢑⡴⣾⢶⣏⣗⣗⣿⢳⢱⠉⣟⢧⣻⠊⡐⡄⡥⠣⡐⣊⠈⢆⠈⡅⠆⡢⠡⡡⡁⣂⢊',
          '⣬⣟⣙⡿⣄⡭⡨⢊⠆⡑⡀⡦⢢⢪⢃⢏⣢⡓⡄⢣⢳⠋⠩⣉⢝⠋⣙⣋⠏⡹⣴⡽⡫⣝⢋⣧⣯⣣⣾⣿⠿⢐⠡⢢⠠⡀⡐⢀⠀⢆⠂⡂⡃⡌⢐⢑⠘⠌⡂⡆',
          '⡵⡭⠘⢶⡆⠢⡆⡆⡆⠔⢄⠳⢅⠧⡡⣪⢐⢚⣱⡑⢭⡂⠃⡒⢤⠨⠮⠭⢭⡕⢝⠜⡎⢟⣫⣿⣿⣽⣯⣎⡿⢰⣳⣎⡐⡌⡤⡡⠨⡁⢂⠡⠢⢈⢢⠊⢌⡂⡣⠰',
          '⣅⠙⢻⡄⢹⡃⢵⢃⠇⠱⡱⢕⢌⠧⣢⣚⣰⣧⡆⢳⠐⢍⢢⢠⡰⢐⣛⡈⣱⡄⡱⢺⣸⣷⡿⣟⢯⡪⡚⣕⠮⢡⣿⣿⣿⣦⣕⠡⠱⠨⢂⠅⡊⠕⡰⢁⢢⠌⡌⢢',
          '⣉⢣⢈⠷⣢⡈⠎⣢⣋⣶⣬⣶⣿⣿⣿⣿⣿⣿⢁⠄⠳⡐⢔⡄⡨⣩⡚⣚⠾⡳⢻⣛⣟⢷⡐⣭⣖⣗⣍⢒⣳⣿⣿⣿⣿⣿⣿⣿⣿⣶⣥⣗⣁⡮⠱⠍⠒⠕⠌⠜']
elif 'mi' in t or 'me' in t:
    text=['⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
          '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠄⢀⠈⠄⡀⡀⡀⠀⢀⠀⢀⠀⠀',
          '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢠⡠⡀⡂⢄⢀⠀⠀⠀⠀⠀⠀⢀⠄⠅⣡⢬⣤⣄⡂⠄⡑⢔⠠⠡⠠⢀',
          '⠀⠀⡀⠀⠀⢀⣀⡀⠀⢀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠐⠘⡆⢊⢐⠨⡂⢕⢔⠀⠀⠀⠀⠠⢁⣰⣿⡽⡯⡳⠫⡫⠦⡐⠨⡪⡨⢊⠢',
          '⠀⢀⡏⠀⠀⣼⢿⡇⠀⣼⣷⣺⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠄⠒⠁⢀⢑⢬⠢⡑⢌⢆⢇⢏⠄⠀⠂⠅⣞⣿⡗⢝⠨⢐⠡⢊⠌⢆⠨⢨⢺⢌⠪',
          '⠀⢸⡇⠀⣰⡿⠋⣿⠀⣿⠙⢇⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠐⠀⢀⢀⠂⠐⡀⢂⠂⢕⠨⡢⡣⣏⢷⣝⠀⠨⢐⣿⢿⢌⠢⢁⢂⢊⠐⠌⠪⠠⢡⢳⢽⡸',
          '⠀⠘⠁⠀⠈⠀⠀⠹⠀⠋⠀⠈⠃⠀⠀⠀⠀⠀⠀⠈⠀⠀⠈⠀⠀⠀⢀⡰⣜⣖⡈⠄⡂⠢⡡⢣⢱⢱⡝⣞⣽⣺⠀⡑⡘⣾⢕⠀⠈⣢⣂⡢⠡⠡⠣⡱⡕⡮⣻⣎',
          '⠀⠀⣄⡀⢀⡄⠀⢠⣤⣄⢠⣤⣤⠤⠄⠀⠀⠀⠀⡀⠀⠀⢰⣲⣪⢮⢞⡮⣗⣗⣗⣗⣬⣪⡐⡕⡕⡵⢽⢕⡧⣗⠀⢐⢄⢿⣕⠌⠀⡯⣿⢿⣽⠋⢥⡻⣱⢿⣿⣺',
          '⠀⢸⡟⣧⢸⠇⣴⠏⠀⢼⠀⠀⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢞⢮⢯⣳⢽⣞⣾⣺⣞⡷⣽⣳⢕⢵⢝⡵⣫⢞⡇⠀⡌⢆⢆⡻⢢⢂⠈⠿⠽⣊⠼⢕⣕⣯⣿⣳⣿',
          '⠀⢸⠇⠸⣿⠀⠻⣤⣾⠟⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠈⠉⠉⠉⠊⠊⠚⠪⢻⠽⡙⡎⣗⢽⡪⣗⢿⠀⢰⠨⢂⠕⡌⡣⠢⡕⢎⢎⢪⢼⣞⣯⣷⢟⢮⡺',
          '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠂⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠣⡑⢕⢱⢹⢮⡳⡏⠀⡐⠅⡅⢌⠂⢝⢳⣺⣳⡽⣯⣿⢯⢟⢮⢳⢕⡕',
          '⠀⠀⡶⢰⣶⠀⢰⡆⣠⣶⠲⠄⣰⢶⡆⠀⣶⡆⠀⣶⢰⡶⠖⠢⣺⠀⠀⠀⠀⠀⠀⠀⠀⢌⠐⢅⢣⢫⣳⣫⠃⠀⠎⠌⢼⠂⢊⠒⠕⢜⠼⠽⣝⢮⡫⣯⣺⢕⢇⢏',
          '⠀⢰⡇⣾⠏⣇⣿⠋⠛⠓⣤⢠⣿⣼⣷⢰⡿⢹⣸⡟⢼⠷⠒⠂⢿⠀⠀⠀⠀⠀⠠⠀⢈⢐⠨⠪⡸⣱⣳⡽⠀⡨⡊⠌⠜⢖⠐⠄⠔⠤⡁⡑⢘⠜⡜⡼⢝⢕⢝⢜',
          '⠀⠸⠇⠛⠀⠸⠟⠐⠶⠾⠋⠻⠁⠀⢿⠘⠃⠀⠿⠃⠷⠿⠛⠃⠶⠀⠀⠀⠀⠀⠀⠀⡀⡂⠜⡸⡸⣪⢷⠇⢰⡯⡦⣅⢕⡐⠡⡑⡐⠔⡠⡘⠜⢓⠡⠡⡡⡑⡅⢇',
          '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢀⠂⠄⡑⡜⣝⢾⢽⡶⡽⣿⢽⡺⣳⢽⢵⣲⢼⢬⣰⣐⡡⡑⡨⢨⠢⢪⢸⡨',
          '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢐⠐⠨⡈⡢⡹⣪⢿⢽⠻⡯⣗⣗⣟⣞⡽⣝⣞⡽⣽⣺⡵⡿⣽⣽⡷⣿⣻⣯⣿',
          '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠄⡈⡂⢆⢕⢝⡾⣽⣻⢔⡿⣵⣳⡳⣵⣯⣳⡳⣯⢗⣗⢿⢽⣯⣟⢯⢫⢳⢹⡸',
          '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠠⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⡀⠀⠄⠂⡁⠂⠌⡂⡊⢜⢘⠕⡫⣓⢛⠞⠮⡟⣯⣾⡷⣯⢯⣻⣺⢽⣻⢾⢝⢜⢎⢧⡣⣇',
          '⠀⠀⣀⠀⠀⠀⣤⡄⠀⠀⣀⠀⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠀⠀⠀⡐⠠⠁⠅⠄⢂⠁⡂⠡⠨⠠⠡⢑⢑⢈⢂⠢⡙⢌⠫⠪⡫⢫⢫⠻⡜⡼⡱⡳⣝⢮',
          '⠀⢠⡇⠀⠀⣸⣏⣿⣀⢸⢿⣾⢿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠢⡔⡁⠌⠐⡈⢀⠂⠄⠡⠈⠄⠅⢂⢐⢀⢂⠅⢂⠢⠡⡑⠌⡂⢅⠣⡑⢌⢊⠪⡨⡊',
          '⠀⢸⡇⠀⢠⡟⠁⢸⡇⣾⠈⠉⣾⠀⠀⠀⠀⠀⠀⠀⠂⠁⠀⠀⠠⠀⠁⠀⠀⡪⡐⠡⣁⡂⣂⢂⠅⢌⠨⠠⢁⠂⡐⢀⢂⢪⢐⡸⣔⠘⡔⣌⠕⡕⢭⡆⠥⡑⠔⢌',
          '⠀⠈⠁⠀⠀⠁⠀⠘⠂⠉⠀⠀⠁⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣝⢽⣺⣺⣺⣳⣗⡧⣎⡪⣐⣐⢐⠄⡢⢐⠡⡑⡈⡓⡯⢞⠕⡯⣗⠯⡪⢨⢊⢢',
          '⠀⠀⣦⣀⣴⡄⣶⠶⠖⢀⣦⡄⢰⡄⠶⢲⡖⠒⢀⣶⣦⠀⢰⡄⠀⠀⣰⡄⠀⠲⡕⢝⡾⣺⣺⣺⢮⡯⣯⢟⣶⣲⢥⡵⣬⣪⢮⢮⡮⣶⢵⣵⣵⣕⣎⡮⡪⣪⢪⢢',
          '⠀⢸⡿⣟⢻⢡⠿⠶⠒⢸⠏⢷⣸⠃⠀⣿⠃⠀⣼⣧⣿⡆⣸⠁⢀⠀⣿⠀⣀⠀⢻⡟⠩⠳⣳⣝⣗⡯⣯⢟⣾⣺⢯⢯⣗⡯⣟⡽⡾⣽⣻⣺⣞⡷⣯⢿⡽⣞⣮⡵',
          '⠀⢸⠇⠀⣺⠸⠾⠟⠛⠸⠀⠘⠏⠀⠀⣿⠀⠸⠏⠀⢹⡇⠽⠟⠛⠉⠿⠟⠛⠉⢿⠃⠀⠀⠀⠈⠊⠫⠞⡽⣺⣺⢽⣻⣺⢽⡽⣽⣫⢷⣳⣗⣯⢯⣯⡯⡿⣽⢾⡽',
          '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⣀⠀⠀⡀⢀⣀⣈⣭⣾⣾⣽⣽⣳⣯⡿⣾⣷⢿⣻⣷⣿⣻⡽⡯⣟',
          '⠀⢀⡇⠀⣾⠀⣿⢸⠇⠀⠀⢀⡿⣿⡀⢺⡟⣹⡆⢸⠃⣠⠞⠛⡷⣾⠂⢸⡇⣴⡾⢿⢾⣿⢾⣿⢽⢯⠯⡟⠾⠽⠽⠳⠛⠛⠙⠋⠋⠉⠙⢉⣽⣿⣿⣾⣿⠍⠉⠉',
          '⠀⢸⡟⢻⡿⢸⡇⣾⣠⣤⣀⣾⠗⢿⡇⣼⠻⣏⠀⣿⠸⣟⢀⣼⠟⣿⣠⣾⡇⠈⣙⣿⠍⡻⠈⡳⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⢀⣤⣤⣾⣻⣟⣿⣳⣿⠏⠀⠀⠀',
          '⠀⠈⠁⠘⠃⠘⠃⠚⠉⠉⠘⠋⠀⠘⠇⠙⠀⠙⠷⠛⠀⠉⠛⠁⠀⠈⠋⠹⠃⠹⠛⠁⠈⠛⠈⠛⠀⠀⠀⠀⠀⠀⠀⠀⠤⠖⠾⠯⠷⠷⠷⠻⠞⠷⠻⡾⠁⠀⠀⠀']
elif 'gru' in t or 'no' in t:
    text=['⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢟⣭⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣭⡛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣩⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣷⣮⡛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣡⣾⣿⣿⣿⣿⣿⣿⣿⣻⣟⣿⢿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣝⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⡿⠍⣺⣿⣿⣷⣷⣿⢿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣗⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⡿⣿⣽⣼⡎⡅⡀⣾⣿⣿⣿⠋⢻⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⡟⢯⣿⣷⣿⣟⣾⣿⣿⣿⣿⣆⠘⢿⣿⣿⣿⣿⣿⡿⣿⣿⣿⢿⣿',
          '⣿⣿⣿⣿⣿⣿⣿⣷⡟⣸⠅⣰⣿⣿⣿⣿⡀⠸⣿⣿⣿⢯⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣦⠸⣿⣿⣿⣟⣿⣿⣿⣿⣿⣷⣹⡎⢿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⡿⣿⡛⣰⣿⣽⣿⣿⣿⣿⣿⣿⣾⣼⣽⣷⣿⣿⣿⣿⣿⣯⣿⣾⣿⣿⣿⣿⢿⣿⣿⣿⣾⣽⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣎⢻⣿⣿⢿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣻⠏⡴⣳⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⡿⣟⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣎⢛⢿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⡛⢼⠀⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣟⣿⣿⣽⣿⣿⣿⡿⣿⣿⢿⣿⣿⣿⣿⣿⡽⣦⠫⢿⣿⣿⣯⣿⣿',
          '⣿⣿⡿⢃⣴⡗⢀⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣻⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣽⣿⣗⢿⣷⡔⡝⢿⣿⣿⣿',
          '⣿⢫⣲⣿⣿⡇⠠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⢿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣹⣿⣿⣗⣮⠻⣿⣿',
          '⣿⣺⣽⣿⣿⣷⢨⣿⣿⣿⣻⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣯⣿⣿⣿⣿⣾⣿⣿⣷⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣙⢿',
          '⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣻⣿⣿⣿⣿⣿⣿⢽⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣾⣿⣿⣽⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣯',
          '⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣳⢽⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣻⣿⣻⣿⣿⣿⣻⣿⣻⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿',
          '⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣻⣿⡿⣿⣿⢿⣿⣿⣯⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣷⣿⣿⣿⣻⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣿⣿⣟⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⡿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⡇⠙⣯⢸⡟⠟⢿⣿⣿⣻⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣻⣯⣿⣿⣻⣿⣟⣿⣿',
          '⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣟⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⡏⣸⡄⢸⡄⠟⣨⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣷⣿⣿⣟⣿⣿⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
          '⣿⣿⣿⣿⣿⣟⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⢿⣿⣟⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣽⣿⣿⣿⣿⣍⢻⣿⣿⣿⣿⣿⣿']
elif t!='':
    txt='⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⢿⣿⣿⠿⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠉⠀⣀⡤⢤⣤⣈⠁⣠⡔⠶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠋⠁⠀⠀⠀⣼⣿⠁⡀⢹⣿⣷⢹⡇⠄⠎⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠹⣇⣀⣡⣾⣿⡿⠉⠛⠒⠒⠋⠉⢸⣿⣿⣿⣿⣿⡿⠋⠁⠀⠀⢀⣤⣤⡀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠛⠉⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⢹⣧⡈⠿⣷⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⢄⣾⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠈⠻⢿⣶⣌⣙⡛⠛⠿⠶⠶⠶⠶⠶⠖⣒⣒⣚⣋⡩⢱⣾⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠛⠛⠻⠿⠿⠟⠛⠛⠛⠉⢉⣥⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠒⠶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠛⢻⣿⡟⠛⣿⡟⠛⠛⠛⠛⢻⣿⡿⠛⠛⠛⢻⡟⠛⠛⠛⠛⢻⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⢻⡇⠀⣿⣿⣿⠀⠀⣿⣿⡏⠀⣼⣿⣿⣿⡇⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⣧⠀⠀⠀⣿⣿⣿⠀⠀⣿⣿⡇⠀⣿⣿⣿⣿⡇⠀⣤⣤⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⣿⣧⠀⠀⣿⡟⠛⠀⠀⠛⢻⣷⣄⠈⠙⠛⢹⡇⠀⠉⠉⠉⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠛⠛⢻⣿⠿⠛⠛⠛⢿⣿⣿⡿⠛⠛⠛⢻⡟⠛⣿⡿⠛⣻⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⣼⣿⣿⣿⡇⠀⣾⣿⣧⠀⢻⡏⠀⣼⣿⣿⣿⡇⠀⡟⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⣿⣿⣿⣿⡄⠀⣿⣿⣿⠀⢸⡇⠀⣿⣿⣿⣿⡇⠀⣀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠈⠙⠛⢻⣧⡄⠙⠛⠉⣠⣿⣷⣄⠈⠙⠛⢹⡇⠀⣿⣧⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿'
    text=[txt[i:i+33] for i in range(0,len(txt),33)]
if t!='':
    for i in range(len(text)): text[i]=centerLine(text[i])
print('\n'.join(text))
