#Ben Kroul
#Dec 18-31 2020
#Programming Club Meeting #5 Project
#esketit
#for some reason made this code 86 characters long but hangman prints in 83 characters

import sys, random, time

#------------------------------------Definitions-------------------------------------#
#-----word lists-----#
letters='A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split()
famousnames=['Rihanna','Justin Bieber','Barack Obama',
             'Kim Kardashian','Donald Trump','Beyonce','Steve Harvey','Ariana Grande',
             "Charli D'amelio",'Brad Pitt','Mia Khalifa','Kylie Jenner',
             'Albert Einstein','Stephen Hawking','Neil Degrasse Tyson',
             'britney spears','Dr. Phil']
rappers=['Jay-Z','Eminem','Cardi B','Meghan Thee Stallion','Nicki Minaj',
         'K.A.A.N.','Kanye','Tupac','Biggie Smalls','A$AP Rocky','NLE Choppa',
         '21 Savage','A Boogie wit da Hoodie','Lil baby','Lil yachty','lil uzi vert',
         'future','Juice wrld','6ix9ine','xxxtentacion','pop smoke','nipsey hussle',
         'coolio','dababy','migos','young thug','kid cudi','tyler the creator',
         'nba youngboy','lil tecca','lil dicky','chance the rapper','roddy ricch',
         'metro boomin','polo g','gunna','nas','dj khalid','drake','rod wave',
         'shek wes','tyga','fetty wap','ybn cordae','kendrick lamar','j. cole',
         'snoop dogg','dr. dre','50 cent','travis scott','busta rhymes','2 chainz',
         'lil wayne','joyner lucas','bobby shmurda','wiz khalifa']
seaanimals=['bottlenose dolphin','sea lion','seal','clownfish',
            'tuna','orca','blue whale','humpback whale','spearfish','goldfish',
            'sperm whale','giant squid','jellyfish','octopus','anemone','coral',
            'angler fish','sea cucumber','crab','lobster','electric eel',
            'great white shark','whale shark','baracuda']
landanimals=['bear','polar bear','grizzly bear','brown bear','moose',
             'orangutan','emperor tamarin','howler monkey','mouse','giraffe','lion',
             'caracal','king cobra','amur leopard','black leopard','arctic fox',
             'red fox','arctic wolf','grey wolf','ocelot','cheetah','snow monkey',
             'anteater','tiger','komodo dragon','wild boar','cottontail rabbit',
             'deer','mountain lion','snow leopard','cougar','mountain goat','marmot',
             'groundhog','beaver','porcupine','elephant','ostrich','kangaroo',
             'raccoon','zebra','camel','llama']
farmanimals=['horse','pig','dog','cat','cow','sheep','rabbit','chicken','rooster',
             'goat','donkey','buffalo','mule']
dogbreeds=['german shepherd','bulldog','poodle','beagle',
           'labrador retriever','golden retriever','chihuahua','siberian husky',
           'dachshund','great dane','grehound','rottweiler','shih tzu',
           'anatolian shepherd','great pyrenees','Bernese Mountain Dog','pug',
           'shiba inu','bull terrier','boston terrier']
colors=['red','blue','yellow','purple','green','orange','pink','black',
        'white','maroon','gray','silver','gold','cyan','turquoise','magenta','violet',
        'scarlet','indigo','brown','chartreuse','venta black']
beans=['garbanzo','pinto','kidney','lentil','lima','chickpea','black','broad','pinto',
       'split pea','soybean','red','pea','baked','black-eyed pea']
trees=['oak','maple','spruce','acacia','bonsai','european ash','weeping willow','fig',
       'sycamore','pistachio','palm','giant sequoia','cacao','birch','cork','rubber',
       'orange','lemon','lime','pine','fir','pecan','brazil nut','walnut','apple',
       'mango','cherry',]
#-----functions-----#
def centerLine(line): #center a line on screen of width 83
    if len(line)>83:
        line=''
        for l in range(0,83): line+=line[l]
    centeredline=' '*((83-len(line))//2)+line
    return(centeredline)
r=0
def printHangman(x,inGame=False,msg=False):
    lines=['     ___________________        ',
           '    |  /               |        ',
           '    | /                |        ',
           '    |/                          ',
           '    |                           ',
           '    |                           ',
           '    |                           ',
           '    |                           ',
           '    |                           ',
           '    |                           ',
           '    |                           ',
           '    |                           ', 
           '    |                           ',
           '    |                           ',
           '    |                           ',
           '    |                           ',
           '    |                           ',
           '    |                           ',
           ' ___|___                                  ']
    if x==-1: #window size/visual tool aid
        lines=['___________________________________________________________________________________',
               '|                                                                                 |',
               '|              Resize the window to the boundaries of this box                    |',
               '|                                                                                 |',
               '|                 Feel free to increase text size for a better Hangman            |',
               '|                                                                                 |',
               '|                                                                                 |',
               '|                                                                                 |',
               '|                                                                                 |',
               '|                                                                                 |',
               '|                                                                                 |',
               '|                                                                                 |', 
               '|                                                                                 |',
               '|                                                                                 |',
               '|                                                                                 |',
               '|                                                                                 |',
               '|                                                                                 |',
               '|                                                                                 |',
               '|_________________________________________________________________________________|']
    if 10>x>0: #ADD THE MAN
        lines[3]='    |/                ###       '
        lines[4]='    |                 ###       '
    if 10>x>1:
        lines[5]='    |                  #        '
        lines[6]='    |                 ###       '
        lines[7]='    |                 ###       '
        lines[8]='    |                 ###       '
        lines[9]='    |                 ###       '
    if 10>x>2:
        lines[6]='    |                ####       '
        lines[7]='    |               # ###       '
        lines[8]='    |              #  ###       '
    if 10>x>3:
        lines[6]='    |                #####      '
        lines[7]='    |               # ### #     '
        lines[8]='    |              #  ###  #    '
    if x==5:
        lines[10]='    |                #          '
        lines[11]='    |                #          '
        lines[12]='    |                #          '
        lines[13]='    |                #          '
        lines[14]='    |               ##          '
    if 10>x>5:
        lines[10]='    |                #   #      '
        lines[11]='    |                #   #      '
        lines[12]='    |                #   #      '
        lines[13]='    |                #   #      '
        lines[14]='    |               ##   ##     '
    if x==7 or x==9: #pp?
        lines[10]='    |                # '+siz[0]+' #      '
        lines[11]='    |                # '+siz[1]+' #      '
    if 10>x>7:
        lines[12]='    |           Y O U   L O S T '
    #hanging
    if x==10:
        lines[3]='    |/                /##       '
        lines[4]='    |                 ##/       '
        lines[5]='    |                 #         '
        lines[6]='    |               #####       '
        lines[7]='    |               #####       '
        lines[8]='    |               #####       '
        lines[9]='    |               #####       '
        lines[10]='    |               ## ##       '
        lines[11]='    |               # #         '
        lines[12]='    |               # #         '
        lines[13]='    |               # #         '
        lines[14]='    |               ## ##       '
        lines[17]='    |   you killed him.         '
    if x==11:
        lines[3]='    |/                /##       '
        lines[4]='    |                 ##/       '
        lines[5]='    |                 #         '
        lines[6]='    |               #####       '
        lines[7]='    |               #####       '
        lines[8]='    |               #####       '
        lines[9]='    |               #####       '
        lines[10]='    |               ## ##       '
        lines[11]='    |                # #        '
        lines[12]='    |                # #        '
        lines[13]='    |                # #        '
        lines[14]='    |               ## ##       '
        lines[17]='    |   you killed him.         '
    if x==12:
        lines[3]='    |/                ###       '
        lines[4]='    |                 ###       '
        lines[5]='    |                  #        '
        lines[6]='    |                #####      '
        lines[7]='    |                #####      '
        lines[8]='    |                #####      '
        lines[9]='    |                #####      '
        lines[10]='    |                ##'+siz[0]+'##      '
        lines[11]='    |                 #'+siz[1]+'#       '
        lines[12]='    |                 # #       '
        lines[13]='    |                 # #       '
        lines[14]='    |                ## ##      '
        lines[17]='    |   you killed him.         '
    if 15>x>12:
        lines[3]='    |/                ##\       '
        lines[4]='    |                 \##       '
        lines[5]='    |                   #       '
        lines[6]='    |                 #####     '
        lines[7]='    |                 #####     '
        lines[8]='    |                 #####     '
        lines[9]='    |                 #####     '
        lines[10]='    |                 ## ##     '
        lines[11]='    |                  # #      '
        lines[12]='    |                  # #      '
        lines[13]='    |                  # #      '
        lines[14]='    |                 ## ##     '
        lines[17]='    |   you killed him.         '
    if x==14:
        lines[11]='    |                   # #     '
        lines[12]='    |                   # #     '
        lines[13]='    |                   # #     '
    #dead (fumes effect)
    if 19>x>14:
        lines[3]='    |/                 $        '
        lines[9]='    |                  .        '
        lines[10]='    |                 ..        '
        lines[11]='    |                  .        '
        lines[12]='    |           Y O U   L O S T '
        lines[13]='    |                           '
        lines[14]='    |            .            . '
        lines[15]='    |            ..    .     .  '
        lines[16]='    |             .     .       '
        lines[17]='    |          /#| #_##_ /$ ##) '
        lines[18]=' ___|___       #############\##           '
    if x==16:
        lines[5]='    |                 .         '
        lines[6]='    |                  .        '
        lines[8]='    |                 .         '
        lines[9]='    |                           '
        lines[10]='    |                           '
        lines[11]='    |            .      .       '
        lines[12]='    |           Y O U   L O S T '
        lines[13]='    |            .      .     . '
        lines[14]='    |                           '
        lines[15]='    |                           '
        lines[16]='    |                           '
    if x==17:
        lines[5]='    |                           '
        lines[6]='    |                           '
        lines[7]='    |            .              '
        lines[8]='    |                          .'
        lines[9]='    |              .    ..     .'
        lines[10]='    |                   .     . '
        lines[11]='    |                           '
        lines[12]='    |           Y O U   L O S T '
        lines[13]='    |                           '
        lines[14]='    |                           '
        lines[15]='    |                           '
        lines[16]='    |                ..         '
    if x==18:
        lines[7]='    |                           '
        lines[8]='    |                           '
        lines[9]='    |                           '
        lines[10]='    |                           '
        lines[11]='    |                           '
        lines[13]='    |                ..         '
        lines[14]='    |                 .         '
        lines[15]='    |                         . '
        lines[16]='    |            ..    ..    .. '
    #win animation
    if r==0:
        if x==19:
            lines[11]='    |        Y O U   W O N ! !  '
            lines[12]='    |  P E R F E C T   G A M E !'
            lines[15]='    |              ^   ^        '
            lines[16]='    |                 >         '
            lines[17]='    |             \_____/       '
        if x==20:
            lines[11]='    |        Y O U   W O N ! !  '
            lines[12]='    |  P E R F E C T   G A M E !'
            lines[16]='    |              ^  >^        '
            lines[17]='    |             \_____/       '
    else:
        if x==19:
            lines[11]='    |        Y O U   W O N ! !  '
            lines[12]='    |        C O N G R A T S !  '
            lines[15]='    |              ^   ^        '
            lines[16]='    |                 >         '
            lines[17]='    |             \_____/       '
        if x==20:
            lines[11]='    |        Y O U   W O N ! !  '
            lines[12]='    |        C O N G R A T S !  '
            lines[16]='    |              ^  >^        '
            lines[17]='    |             \_____/       '
    #print game info to right side of picture lines
    if inGame:
        lines[1]+=' Category: '+category
        lines[2]+='~'*(len(category)+12)
        if len(lettersleft)>1: lines[4]+='           letters left: '+lettersleft
        else: lines[4]+='           letters left:                           '
        lines[5]+='                         '#+''.join(letterspicked)
        #prints expanded line of word only if line is there
        if wlist[0]!='': lines[8]+='   '+expandword(wlist[0])
        if wlist[1]!='': lines[10]+='   '+expandword(wlist[1])
        if wlist[2]!='': lines[12]+='   '+expandword(wlist[2])
        if wlist[3]!='': lines[14]+='   '+expandword(wlist[3])
        if wlist[4]!='': lines[16]+='   '+expandword(wlist[4])
    if msg: #add special message right above input
        msgfront=[] #conserves first half of last line
        for l in range(0,(83-len(message))//2): msgfront.append(lines[18][l])
        lines[18]=''.join(msgfront)+message
    print('\n'.join(lines))

def doHelpMenu(pg=0):
    sections=['how to play Hangman™','tips','about','credits','notes']
    while 1:
        lines=['___                                                                             ___',
               centerLine('Help Menu')+' '*(34-len(sections[pg]))+sections[pg]+' '+str(pg+1),
               centerLine('~~~~~~~~~~~'),
               '',
               '    General:',
               '        1. Click to the right of the colon on the bottom left.',
               '        2. Send an input by typing and pressing enter to the right of the colon',
               '        3. () specifies inputs that are being requested',
               '',
               '    in-Game inputs:',
               "        'exit' – exit help menu or game, twice: exit the script entirely",
               "        'help' – come back to this menu at any time",
               '',
               '',
               '',
               '',
               '',
               '',
               '(back)                                                                       (next)']
        if pg==1: #tips
            lines[4:16]=["\t  - Don't resize the screen when the script is in the middle of printing.",
                         '\t    IDLE will crash; resize before you type an input and press enter',
                         '',
                         '\t  - Increase the font size of IDLE and then resize the window to get an ',
                         '\t    optimal Hangman™ experience',
                         '',
                         '\t  - You can input the first letter of most words instead of the full one',
                         '\t    e.g. y instead of yes, b instead of back',
                         '',
                         '\t  - When playing hangman, you can specify two or more letters by separating',
                         "\t    them with a comma: 'a,b' - no",
                         '']
        if pg==2: #about
            lines[4:16]=['\t\tThis program works by printing things to the size of   ',
                         '\t    your browser window, which should be 83x19.5 characters. Of',
                         '\t    course, this only works with monospaced font, which this   ',
                         '\t    python shell (IDLE) uses. It is with this window that a    ',
                         '\t    visual space can be emulated and animations can be printed ',
                         '\t    as if a single screen is changing instead of lines printing',
                         '\t    from top to bottom. An interface is acheived through the   ',
                         '\t    input colon that you see at the bottom left, as the only   ',
                         '\t    way to communicate with a regular python program is by the ',
                         '\t    use of input(), from the player typing text and then       ',
                         '\t    pressing the enter key. To navigate through this help menu,',
                         "\t    input 'next', 'back', or a number. To exit, input 'exit'.  ",]
        if pg==3: #credits
            lines[4:16]=[centerLine('hangman.py'),
                         centerLine('Breck Programming Club Project #1'),
                         '',
                         centerLine('Created by: Ben Kroul'),
                         '\t\t',
                         centerLine('Date created: Dec. 18 2020'),
                         centerLine('Date finished: Jan. 5 2020'),
                         '',
                         centerLine('phrog:'),
                         centerLine('{•}  {•}'),
                         centerLine('\   ..   /'),
                         centerLine('\______/')]

        if pg==4: #notes
            lines[4:16]=['',
                         '',
                         '',
                         '',
                         centerLine('Feel free to suggest categories and words to the creator!'),
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '']
        print('\n'.join(lines))
        t=input(':').lower()
        if t=='next' or t=='n' or t=='d': pg+=1
        if t=='back' or t=='b' or t=='a': pg-=1
        if t=='exit': break
        if t.isdigit(): pg=int(t)-1
        if pg<0: pg=4
        if pg>4: pg=0

def expandword(word):
    expandedword=[]; end=''; right=False
    for l in word:
        if l.isalpha(): #ungessed letters = ___, guessed letters =  L 
            exp=' '+l+' ' if l in letterspicked else '___'
        elif l==' ': exp='   '
        elif l=='-' or l=='–' or l=='—': exp=' – '
        elif l!='=': exp=' '+l+' ' #add nonalpha except for hyphen character
        if l!='=': expandedword.append(exp)
    front=(N-len(word))//2
    if word[len(word)-1]=='=': #if last character is hyphen character
        front=(N+1-len(word))//2
        end='–'
    expandedline=' '.join(['   ']*front+expandedword)+end
    return(expandedline)

def hangingAnimation(n,inGame=False):
    for _ in range(n):
        printHangman(12,inGame)
        time.sleep(0.3)
        printHangman(11,inGame)
        time.sleep(0.3)
        printHangman(10,inGame)
        time.sleep(0.7)
        printHangman(11,inGame)
        time.sleep(0.3)
        printHangman(12,inGame)
        time.sleep(0.3)
        printHangman(13,inGame)
        time.sleep(0.3)
        printHangman(14,inGame)
        time.sleep(0.7)
        printHangman(13,inGame)
        time.sleep(0.3)

def deadAnimation(n,inGame=False):
    x=15
    for _ in range(n*4):
        printHangman(x,inGame)
        time.sleep(0.5)
        x+=1
        if x==19: x=15

def winAnimation(n,inGame=False):
    for _ in range(n):
        printHangman(19,inGame)
        time.sleep(0.7)
        printHangman(20,inGame)
        time.sleep(0.7)
        
def lettertonumber(L): #converts letter to number 1-26
    for i in range(0,len(letters)):
        if letters[i]==L.upper(): return i
#------------------------------------Introduction------------------------------------#
print('\n\n'+centerLine('~~        Welcome to Hangman™!        ~~')+'\n')
time.sleep(1.5)
print(centerLine('The game where you guess letters to form a word'))
time.sleep(1.5)
print(centerLine('while simultaneously drawing a man to death!'))
time.sleep(2)
print(centerLine('What fun!'))
time.sleep(1.5)
print('\n\n\t  1. Click to the right of the colon on the bottom left.')
print('\t  2. Send an input by typing and pressing enter to the right of the colon')
print("\t  3. Keep your cursor there, because that's the only way you can play the game!")
t=input('\n'*12+':')
print('\n\n'+centerLine("You're ready to play!")+'\n'*5)
time.sleep(3)
print('\n\n\n'+centerLine("Type help at any time to bring up the help menu"))
time.sleep(2)
while 1: #size da skreen
    message='Resize your window to fit the hangman and this sentence, then press enter      -->|'
    printHangman(-1,False,True)
    t=input(':')
    if t.lower()=='': break
    if t.lower()=='help': doHelpMenu()
#-------------------------------------Playing Hangman--------------------------------#
specifications=True
wordscycled=[]
alst=[' -->',' (2)',' (3)',' (4)',' (5)',' (6)',' (7)',' (8)',' (9)','(10)','(11)']
anum=0
e=False
while 1: #play multiple games of hangman in a row
    #-----specifications-----#
    if specifications:
        while 1: #number of tries selector (from 1-7)
            t=input('\n\nHow many tries for each game? Default is 6 btw (1-7)'+'\n'*18+':')
            if t.isdigit():
                if 0<int(t)<8:
                    numtries=int(t)
                    break
            if t.isdigit() or t=='':
                print(centerLine("We'll just keep it at six for now"))
                numtries=6
                time.sleep(2)
                break
            if t=='help': doHelpMenu()
            if t=='exit':
                e=True
                break
        if e: break
        siz='  '
        if numtries==7: #ask for size only for extra try )
            t=input('\n...size? (1-4)\n:')
            siz="# "
            if t=='1': siz="' "
            if t=='2': siz="! "
            if t=='3': siz="|'"
            if t=='4': siz="|!"
        while 1: #animation selector
            t=input('\nDo you want to show animations? (y)es/(n)o'+'\n'*18+':').lower()
            if t=='y' or t=='yes':
                animations=True
                break
            if t=='n' or t=='no':
                animations=False
                break
        alist=[['Rappers',rappers],['Random Famous People',famousnames],
               ['Colors',colors],['Types of Beans',beans],['Various Trees',trees],
               ['Farm Animals',farmanimals],['Land Animals',landanimals],
               ['Sea Animals',seaanimals],['Dog Breeds',dogbreeds],
               ['Animals',farmanimals+seaanimals+landanimals]]
        while 1: #category selection menu
            print('\n\nPick a category:                                               (1-12) '
                  'to select')
            print('                                                            enter again to'
                  ' finalize\n\n')
            print('    '+alst[0]+' Rappers         '+alst[1]+' Random Famous People\n')
            print('    '+alst[2]+' Colors          '+alst[3]+' Types of Beans  '+alst[4]+
                  ' Various Trees\n')
            print('    '+alst[5]+' Farm Animals    '+alst[6]+' Land Animals'+
                  '    '+alst[7]+' Sea Animals     '+alst[8]+' Dog Breeds\n')
            print('    '+alst[9]+' ALL Animals     '+alst[10]+' Random!!')
            a=input('\n'*7+':')
            if a.isdigit():
                if int(a)>11 or int(a)<1: pass
                alst[anum]='('+str(anum+1)+')'
                if anum<9: alst[anum]=' '+alst[anum]
                anum=int(a)-1
                alst[anum]=' -->'
            if a=='exit':
                e+=1
                break
            if a=='help': doHelpMenu()
            if a=='': break
        if e==1: break
    #-----assign variables-----#
    correctguesses=[]
    lettersinword=[]
    letterspicked=[]
    msg=False
    #assign category, list from category selection menu
    if anum==11:
        category='Random'
        list=alist[random.randint(0,10)][1] #pick a random list
    else:
        category=alist[anum][0]
        list=alist[anum][1]
    if all(item in wordscycled for item in list): #skips word picking if no more words in list
        word=lettersleft=''
    else:
        while 1: #word picker
            word=list[random.randint(0,len(list)-1)].strip() #pick & format word from list
            if word not in wordscycled: break
        wordscycled.append(word)
        #get list of letters in word, ordered, to compare to later
        word=word.upper()
        for l in word:
            if l.isalpha() and l not in lettersinword: lettersinword.append(l)
        lettersinword.sort()
        lettersleft=''.join(letters)
        letterspicked=[' ']*26
    #-----format word into 5 lines of length N-----#
    N=12 #number of characters in line
    short=False
    while 1: #run this once for long if too long run short if too long fail
        lword=word
        wlist=[]; hyph=0
        while 1: #separates word into lines by using spaces 
            subwrdlst=lword.split() #list of subwords split by space
            i=len(subwrdlst)-1 #start at last subword
            addingsubwrds=[subwrdlst[i]] #add last word in lword
            length=len(' '.join(addingsubwrds))
            if hyph==1: hyph+=1
            #if only takes up 1 line, just set line to lword
            if len(lword)<=N:
                if hyph>=2: lword+='='
                wlist.append(lword)
                break
            #add subwords to make line under N characters
            while i>0: #not on first word in lword
                i-=1 #go to second to last word
                if (length+len(subwrdlst[i])+1)<=N: #if next term will work
                    addingsubwrds.append(subwrdlst[i]) #add next term
                    length=len(' '.join(addingsubwrds))
                else: break
            #split up lines greater than N characters, add hyphen next round
            if length>N or (short and length<(N-1)): hyph+=1 #next line needs hyphen
            if length>N or short: length=N #print exactly 1 line length of lword
            #make line to subwrdlst w/ length, make lword the rest
            endwrd = restofwrd = ''
            for l in range(len(lword)-length,len(lword)): endwrd+=lword[l]
            for l in range(0,len(lword)-length): restofwrd+=lword[l]
            if hyph>=2:
                endwrd+='='
                hyph-=2
            wlist.append(endwrd.strip())
            lword=restofwrd.strip()
        #decide whether to break or restart
        if len(wlist)>5:
            if short: sys.exit('Word is greater than '+str(N*5))
            else: short=True
        else: break
    wlist+=['']*(5-len(wlist)) #fill in empty spaces for 5 long list
    wlist.reverse()
    #-----run game-----#
    win=False; postgame=True
    r=x=0
    if lettersinword==correctguesses: #instant win if none of letters are characters
        e=True
        postgame=False
    while r<numtries: #play game until runs out of tries (limbs)
        while 1: #asks for guess from player
            printHangman(x,True,msg)
            guess=input(':').upper().strip()
            if guess=='EXIT': e=True;#leave the game
            if guess=='DEBUG':
                print(word)
                print(wordscycled)
                time.sleep(5)
            if guess !='' and guess in lettersleft: break
            if e: #exit hangman
                postgame=False
                break
            message='type an available letter and press enter to guess; type help for more'
            msg=True
        if e: break; #exit
        if guess in word: #correct guess
            lnum=lettertonumber(guess)
            lettersleft=lettersleft.replace(guess,'✓') #replace guess with space in left
            letterspicked[lettertonumber(guess)]=guess #add guess to picked
            correctguesses+=guess; correctguesses.sort()
        else: #wrong guess: change limbs
            lettersleft=lettersleft.replace(guess,'✗')
            r+=1
            x+=1
            message=str(numtries-r)+' tries left'
            if (numtries-r)==1: message=str(numtries-r)+' try left'
            msg=True
            if numtries==2: x=2; #0-->2
            if numtries==3: x+=1; #0-->2-->4
            if numtries==4 and r>2: x+=1; #0-->1-->2-->4
        if lettersinword==correctguesses: #detect win
            win=True
            break

    #-----post-game animations and ask to replay game-----#
    if postgame:
        if win:
            if animations: winAnimation(4,True)
            x=19
        else: #lost
            x=7 if numtries==7 else 6
            printHangman(x,True)
            if animations:
                time.sleep(3)
                hangingAnimation(2,True)
                deadAnimation(4,True)
            x+=2
            message='-Your word was: '+word+' -' #say what the word was if lost
            printHangman(x,True,True)
            t=input(':') #pause until pressed enter
    while 1: #ask to keep playing game
        e=False
        message='-     Play again?     -'
        printHangman(x,True,True)
        t=input(':').lower().strip()
        if t=='y' or t=='yes' or t=='': break
        if t=='n' or t=='no' or t=='exit':
            e=True
            break
        if t=='debug':
            print(word)
            print(wordscycled)
            time.sleep(5)
        message='-     (y)es, (n)o     -'
        printHangman(x,True,True)
        time.sleep(1)
    if e: break
    while 1:
        message='-  Same category and specifications?  -'
        printHangman(x,True,True)
        t=input(':').lower()
        if t=='y' or t=='yes':
            specifications=False
            break
        if t=='n' or t=='no':
            specifications=True
            break
        message='-             (y)es, (n)o             -'
        printHangman(x,True,True)
        time.sleep(1)
print('\n'+centerLine("Exiting Hangman™..."))
time.sleep(2)
print("\nRemember to close IDLE so it doesn't crash from all of the lines it has printed!")
print("Hope to see you again soon!")
