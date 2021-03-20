#Ben Kroul
#December 11
#Programming Club Meeting 4

import sys, random, time

templateBoard={"1":"1","2":"2","3":"3",
               "4":"4","5":"5","6":"6",
               "7":"7","8":"8","9":"9"}
def printBoard(board):
    print('\t'+board["1"]+"|"+board["2"]+"|"+board["3"])
    print('\t-+-+-')
    print('\t'+board["4"]+"|"+board["5"]+"|"+board["6"])
    print('\t-+-+-')
    print('\t'+board["7"]+"|"+board["8"]+"|"+board["9"])

#win conditions:
itr=[['1','2','3'],['4','5','6'],['7','8','9'],
     ['1','4','7'],['2','5','8'],['3','6','9'],
     ['1','5','9'],['3','5','7']]

#starting messages
print('Welcome to Tic Tac Toe!!!\n')
print("Use the numbers 1-9 to define where to place your move.")
print("Type 'help' when playing to bring this menu up again; type 'exit' to exit.")
printBoard(templateBoard)

#specifications
t=input('Play against computer or another person? ')
if t=='p' or 'pers' in t or '2' in t: multiplayer=True;
else: multiplayer=False;
t=input('\nX or O? ').lower()
if t=='o':
      x='O'
      y='X'
else:
      x='X'
      y='O'
while multiplayer==False:
    t=input('Do you want to face a good or bad computer? ').lower()
    if t=='good' or t=='g':
        opp='good'
        break
    if t=='bad' or t=='b':
        opp='bad'
        break
while 1:
    t=input('Best of...? (how many games) ')
    if t.isdigit():
        if int(t)>0 and int(t)<100:
            numgames=int(t)
            break
        else: print('Please type a number between 0 and 100')

blst=[] #saves games when ended to list
glst=[] #saves win state of games
numwins=numlosses=numties=0
gamenum=1
orignumgames=numgames
while gamenum<=numgames: #plays multiple games
    Brd = {"1":" ","2":" ","3":" ",
           "4":" ","5":" ","6":" ",
           "7":" ","8":" ","9":" "}
    movesdone=[]
    win=lose=False
    if x=='X': turn=x; #starts turn with X
    else: turn=y;
    if numgames>1:
        if multiplayer:
            print('\nPlayer 1: '+str(numwins)+', Player 2: '+str(numlosses)+'   Game '+str(gamenum)+'/'+str(orignumgames)+'\n')
        else:
            print('\nPlayer '+str(numwins)+', Computer '+str(numlosses)+'   Game '+str(gamenum)+'/'+str(orignumgames)+'\n')
    else: print('\n')  
    for i in range(9): #play da game
            printBoard(Brd)
            print()
            
            if turn==x or multiplayer: #player turn
                while 1:
                    #ask player to input turn
                    if multiplayer: str0=' 2' if turn==y else ' 1';
                    else: str0='';
                    move=input("Player"+str0+"'s turn for "+turn+": ") 

                    if move=='help': #print help screen
                        print("\nUse the numbers 1-9 to define where to place your move.")
                        print("Type 'help' when playing to bring this menu up again; type 'exit' to exit.")
                        printBoard(templateBoard)
                        time.sleep(3)
                        print('\n')
                        printBoard(Brd)
                    if move=='exit': #exit game
                        t=input('\nYou sure you want to exit? (t) ')
                        if t.lower()=='t': sys.exit('Thanks for playing!');
                    if move.isdigit():
                        if move not in movesdone and 0<int(move)<10: break;
                        else: print("Pick an available space; type 'help' to bring up spaces again");
            else: #computer turn
                if opp=='good': #smart AI
                    while 1:
                        move=str(random.randint(1,9))
                        if move not in movesdone: break;
                    if i>=3 and '5' not in movesdone: move='5';
                    for j in range(8): #don't lose the game
                        if Brd[itr[j][0]]==x and Brd[itr[j][1]]==x and Brd[itr[j][2]]==' ':
                            move=itr[j][2]
                            break
                        if Brd[itr[j][0]]==x and Brd[itr[j][2]]==x and Brd[itr[j][1]]==' ':
                            move=itr[j][1]
                            break
                        if Brd[itr[j][2]]==x and Brd[itr[j][1]]==x and Brd[itr[j][0]]==' ':
                            move=itr[j][0]
                            break
                    for j in range(8): #try to win the game
                        if Brd[itr[j][0]]==y and Brd[itr[j][1]]==y and Brd[itr[j][2]]==' ':
                            move=itr[j][2]
                            break
                        if Brd[itr[j][0]]==y and Brd[itr[j][2]]==y and Brd[itr[j][1]]==' ':
                            move=itr[j][1]
                            break
                        if Brd[itr[j][2]]==y and Brd[itr[j][1]]==y and Brd[itr[j][0]]==' ':
                            move=itr[j][0]
                            break
                else: #dumb AI (random number)
                    while 1:
                        move=str(random.randint(1,9))
                        if move not in movesdone: break;
                print('Computer turn: '+move)

            #add move to board
            Brd[move]=turn
            movesdone.append(move)
            
            #detect win
            for j in range(8):
                if Brd[itr[j][0]]==x and Brd[itr[j][1]]==x and Brd[itr[j][2]]==x:
                    win=True
                    break
                if Brd[itr[j][0]]==y and Brd[itr[j][1]]==y and Brd[itr[j][2]]==y:
                    lose=True
                    break
            if win or lose: break;

            #switch moves
            turn=x if turn==y else y

    #game ended; print final board and result
    printBoard(Brd)
    if not win and not lose:
        print("\nIt's a tie!")
        glst.append('tied')
    if win:
        if multiplayer: print("\nPlayer 1 won!")
        else: print("\nYou beat the computer! Good job!");
        numwins += 1
        glst.append('won')
    if lose:
        if multiplayer: print("\nPlayer 2 won!");
        else: print("\nYou lost... better luck next time!");
        numlosses += 1
        glst.append('lost')
    time.sleep(2)

    #archive board in list of boards
    blst.append(Brd)

    #dont leave multiple games as a tie
    if gamenum==numgames and numwins==numlosses: numgames+=1;

    #next game
    if numgames==1: sys.exit();
    gamenum+=1

#print results (for more than 1 game)
if multiplayer:
    print('\n\n\nFinal score out of '+str(numgames)+' games: Player 1: '+str(numwins)+', Player 2: '+str(numlosses))
else:
    print('\n\n\nFinal score out of '+str(numgames)+' games: Player '+str(numwins)+', Computer '+str(numlosses))
time.sleep(2)
if numwins>numlosses: print('You won!!');
else: print('You lost :/')
time.sleep(2)

str0='Player 1' if multiplayer else 'you'
print("\nHere's how "+str0+" did:\n")
#format tied, loss, and
l=len(glst)
for i in range(l):
    if len(glst[i])==3: glst[i]=' '+glst[i];
    glst[i]='  '+glst[i]+': '
i=0

#prints out games in stacks of 3
while l>0:
    if l>=3:
        print('\n        '+blst[i]['1']+'|'+blst[i]['2']+'|'+blst[i]['3']+'        '+blst[i+1]['1']+'|'+blst[i+1]['2']+'|'+blst[i+1]['3']+'        '+blst[i+2]['1']+'|'+blst[i+2]['2']+'|'+blst[i+2]['3'])
        print('        -+-+-        -+-+-        -+-+-')
        print(glst[i]+blst[i]['4']+'|'+blst[i]['5']+'|'+blst[i]['6']+glst[i+1]+blst[i+1]['4']+'|'+blst[i+1]['5']+'|'+blst[i+1]['6']+glst[i+2]+blst[i+2]['4']+'|'+blst[i+2]['5']+'|'+blst[i+2]['6'])
        print('        -+-+-        -+-+-        -+-+-')
        print('        '+blst[i]['7']+'|'+blst[i]['8']+'|'+blst[i]['9']+'        '+blst[i+1]['7']+'|'+blst[i+1]['8']+'|'+blst[i+1]['9']+'        '+blst[i+2]['7']+'|'+blst[i+2]['8']+'|'+blst[i+2]['9'])
        i+=3
        l-=3
    if l==2:
        print('\n        '+blst[i]['1']+'|'+blst[i]['2']+'|'+blst[i]['3']+'        '+blst[i+1]['1']+'|'+blst[i+1]['2']+'|'+blst[i+1]['3'])
        print('        -+-+-        -+-+-')
        print(glst[i]+blst[i]['4']+'|'+blst[i]['5']+'|'+blst[i]['6']+glst[i+1]+blst[i+1]['4']+'|'+blst[i+1]['5']+'|'+blst[i+1]['6'])
        print('        -+-+-        -+-+-')
        print('        '+blst[i]['7']+'|'+blst[i]['8']+'|'+blst[i]['9']+'        '+blst[i+1]['7']+'|'+blst[i+1]['8']+'|'+blst[i+1]['9'])
        break;
    if l==1:
        print('\n        '+blst[i]['1']+'|'+blst[i]['2']+'|'+blst[i]['3'])
        print('        -+-+-')
        print(glst[i]+blst[i]['4']+'|'+blst[i]['5']+'|'+blst[i]['6'])
        print('        -+-+-')
        print('        '+blst[i]['7']+'|'+blst[i]['8']+'|'+blst[i]['9'])
        break;
print('\nThanks for playing!!')
