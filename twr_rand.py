import csv
import random

#TODO:
# merge class csvs
# add class promotion restricts
# add default weapon
# handle weapon skills
# load config
# 

def list_diff(a,b):
    return [int(a[n])-int(b[n]) for n in range(len(a))]
def list_sum(a,b):
    return [int(a[n])+int(b[n]) for n in range(len(a))]
def list_bound(a, lw, up):
    return [max(lw,min(a[n],up)) for n in range(len(a))]
   

attr_names = ('Vitality','Strength','Skill','Agility','Endurance','Defense')
wpntype_names = ('oneHandedSword', 'twoHandedSword', 'oneHandedLance', 'twoHandedLance', 'oneHandedAxe', 'twoHandedAxe', 'bow')
skill_xp = {'SS':260, 'S':180, 'A':100, 'B':40, 'C':0, '-':-1}
lvl_index = 1,3,4,6,8,10,12,14,16,17,18,19,21,23,25,27,29,30,32,35
attr_cnt = 6
skill_cnt = 7

weapon_data = []
wpn_names = []
wpn_ranks = []
wpn_type = []
wpn_tier = []
wpn_type_nums = dict()
idx=0
with open('wpns.csv',mode='r',newline='') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)

    for row in csv_reader:
        weapon_data.append(row)
        wpn_type_nums[row[1]]=idx
        wpn_names.append(row[0])
        wpn_type.append(row[1])
        wpn_ranks.append(row[2])
        wpn_tier.append(int(row[3]))
        #wpn_wgt.append(row[4])
        idx+=1

equip_data = []
eqp_names = []
eqp_type = []
eqp_cat = []
eqp_tier = []
with open('equip.csv',mode='r',newline='') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)

    for row in csv_reader:
        secondary_wpn=-1
        equip_data.append(row)
        secondary_wpn=-1
        #eqp_type_nums[row[1]]=idx
        eqp_names.append(row[0])
        eqp_type.append(int(row[1]))
        eqp_cat.append(int(row[2]))
        eqp_tier.append(int(row[3]))

eqp_cnt = len(equip_data)
wpn_cnt = len(weapon_data)

#base_data = []
#base_names = []
#base_wpns = []
#base_stats = []
#base_growths = []
#base_class_nums = dict()
#idx = 0
#with open('base_stats.csv',mode='r',newline='') as file:
#    csv_reader = csv.reader(file)
#    next(csv_reader)
#
#    for row in csv_reader:
#        #class_data.append(row)
#        base_class_nums[row[0]]=idx
#        base_names.append(row[0])
#        base_stats.append(row[1:7])
#        base_growths.append(row[7:13])
#        base_wpns.append(row[13:20])
#        idx+=1
#        
#promo_data = []
#promo_names = []
#promo_stats = []
#promo_wpns = []
#promo_class_nums = dict()
#idx = 0
#with open('promo_stats.csv',mode='r',newline='') as file:
#    csv_reader = csv.reader(file)
#    next(csv_reader)
#
#    for row in csv_reader:
#        promo_data.append(row)
#        promo_class_nums[row[0]]=idx
#        promo_names.append(row[0])
#        promo_stats.append(row[2:8])
#        promo_wpns.append(row[8:15])
#        idx+=1

class_data = []
class_names = []
class_wpns = []
class_stats = []
class_nums = dict()
idx = 0
with open('class_stats.csv',mode='r',newline='') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)

    for row in csv_reader:
        class_data.append(row)
        class_nums[row[0]]=idx
        class_names.append(row[0])
        class_stats.append(row[2:8])
        class_wpns.append(row[8:15])
        idx+=1

class_growths = []
alwd_aclass= []
alwd_eclass= []
with open('base_class.csv',mode='r',newline='') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)

    for row in csv_reader:
        class_growths.append(row[1:7])
        alwd_aclass.append(row[7:10])
        alwd_eclass.append(row[10:13])
   
class RandGenerator:
    deck_idx=0

    growth_rng = 1
    base_rng = 2

    #exclude_final_chars = True
    exclude_final_chars = False
    restricted_class = True

    deck = []
    
    
    def __init__(self):
        #self.fullDeck = [1,1,1,1,2,2,3,3,5,6,6,7,7,8,9,9,10,10,10,11,11,12,12,13,14,14,14,15,17,20,20,20,20,20]
        if self.exclude_final_chars:
            self.deck = [6,6,7,7,8,9,9,10,10,10,11,11,12,12,13,14,14,14,15,17]
        else:
            self.deck = [6,6,7,7,8,9,9,10,10,10,11,11,12,12,13,14,14,14,15,17,20,20,20,20,20]
        random.shuffle(self.deck)
        
        
        
    def pullChapter(self, firstChapter):
        print(firstChapter)
        if firstChapter<=5:
            return firstChapter
        elif firstChapter==20 and self.exclude_final_chars:
            return 20
        else:
            self.deck_idx=self.deck_idx+1
            return self.deck[self.deck_idx-1]
            
        #return random.randint(4,20) 

    def pullClass(self,chapter):
        # generate classes
        rclass0 = random.randint(0,5)
        if self.restricted_class:
            rclass1 = int(alwd_aclass[rclass0][random.randint(0,2)])-2
            rclass2 = int(alwd_eclass[rclass0][random.randint(0,2)])-2
        else:
            rclass1 = random.randint(6,18) #previously 0-12
            rclass2 = random.randint(20,33) #previously 14-27

        # return the right tier
        if chapter < 9:        
            return (rclass0,)
        elif chapter < 15:
            return (rclass0,rclass1)
        else:
            return (rclass0,rclass1,rclass2)

    def randomizeStats(self,stats):
        return [s + random.randint(-self.base_rng,self.base_rng) for s in stats]

    def randomizeGrowths(self,growths):
        return [g + 5*random.randint(-self.growth_rng,self.growth_rng) for g in growths]

    def randomizeSkills(self,charclass):
        return 0

    def pick_weapon(self, type, rank, tier):
        avail_weapons = [w for w in range(wpn_cnt) if wpn_type[w]==wpntype_names[type]]
        avail_weapons = [w for w in avail_weapons if skill_xp[wpn_ranks[w]]<=skill_xp[rank]]
        avail_weapons = [w for w in avail_weapons if wpn_tier[w]<=tier]

        return random.sample(avail_weapons,1) [0]

    def pick_shield(self, type, tier):
        avail_shields = [e for e in range(eqp_cnt) if eqp_type[e]==0]
        avail_shields = [e for e in avail_shields if eqp_cat[e]==type]
        avail_shields = [e for e in avail_shields if eqp_tier[e]<=tier]

        return random.sample(avail_shields,1) [0]

    def pick_item(self, tier):
        avail_items = [e for e in range(eqp_cnt) if eqp_type[e]==1]
        avail_items = [e for e in avail_items if eqp_tier[e]<=tier]

        return random.sample(avail_items,1) [0]

    def randomizeEquipment(self, character):
        one_hand_wpns = (0,2,4)

        wpn_tier = 2
        itm_tier = 4

        if character.lvl <= 4:
            itm_tier = 0
        elif character.lvl <=11:
            itm_tier = 1
        elif character.lvl <=15:
            itm_tier = 2
        
        b_idx = character.charClass[0]
        base_weapons = [n for n in range(skill_cnt-1) if class_wpns[b_idx][n]!='-']
        all_weapons = [n for n in range(skill_cnt-1) if character.wskills[n]!='-']

        # choose random valid melee (of highest tier?), add weapon
        primary_wpn = random.sample(base_weapons,1)[0]
        secondary_wpn=-1
        character.wpn0 = self.pick_weapon(primary_wpn, character.wskills[primary_wpn], wpn_tier)

        if character.lvl >= 4:
            secondary_wpn = random.sample(all_weapons,1)[0]
            character.wpn1 = self.pick_weapon(secondary_wpn, character.wskills[secondary_wpn], wpn_tier)
            if character.wpn1 == character.wpn0:
                character.wpn1 = []
        
        # if bow skill add bow
        if character.wskills[6]!='-':
            character.wpn2 = self.pick_weapon(6, character.wskills[6], wpn_tier)

        # if has onehandedweapon, add shield
        if primary_wpn in one_hand_wpns or secondary_wpn in one_hand_wpns:
            c = character.charClass[0]
            
            # skirmisher/archer/spiritualist = round
            # defender = tower (or kite if level 1)
            # fighter/soldier = kite
            shield_type = 0
            if c==3: # if defender
                shield_type = 2
            elif c==1 or c==2: # if soldier or fighter
                shield_type = 1 
            character.shld = self.pick_shield(shield_type, itm_tier)

        # either rare, or second weapon type

           
        if character.lvl==1:
            character.itm0 = 12
        else:
            character.itm0 = self.pick_item(itm_tier)

        # fix slot if only two weapons
        if character.wpn1==[]:
            character.wpn1=character.wpn2
            character.wpn2=[]

        return

class Character:
    name=[]
    charClass=[]
    firstChapter=1
    
    wpn0=[]
    wpn1=[]
    wpn2=[]
    shld=[]
    itm0=[]
    itm1=[]

    base_stats=[]
    base_lvl=1
    growths=[]
    stats=[]
    adj_growths=[]
    adj_stats=[]
    wskills=['-','-','-','-','-','-','-']
    mov = 4

    def __init__(self,char_row):
        self.name=char_row[0]
        self.firstChapter=int(char_row[1])
        self.lvl=int(char_row[2])
        self.charClass=char_row[3:6]
        self.stats=char_row[6:12]
        self.adj_stats=char_row[6:12]
        self.growths=char_row[12:18]
        self.adj_growths=char_row[12:18]

        if self.lvl == 35:
            b_idx = class_nums[self.charClass[0]]
            self.growths = class_growths[b_idx]
            self.adj_growths = class_growths[b_idx]
        
        self.adj_stats=[int(float(self.adj_stats[n])-float(self.growths[n])*(float(self.lvl)-1)/100) for n in range(attr_cnt)]
        
        if self.charClass[2] != '-':
            p_idx = class_nums[self.charClass[2]]
            self.adj_stats = list_diff(self.adj_stats,class_stats[p_idx])
            self.charClass[2] = p_idx
        else:
            self.charClass=self.charClass[:2]
            
        if self.charClass[1] != '-':
            p_idx = class_nums[self.charClass[1]]
            self.adj_stats = list_diff(self.adj_stats,class_stats[p_idx])
            self.charClass[1] = p_idx
        else:
            self.charClass=self.charClass[:1]

        b_idx = class_nums[self.charClass[0]]
        self.charClass[0] = b_idx
        self.adj_stats = list_diff(self.adj_stats,class_stats[b_idx])

        print(self.adj_growths)
        print(class_growths[b_idx])
        self.adj_growths = list_diff(self.adj_growths,class_growths[b_idx])

    def updateWeaponSkills(self):
        b_idx = self.charClass[0]
        self.wskills = class_wpns[b_idx]

        if self.lvl > 4:
            self.wskills = ['B' if w!='-' else w for w in self.wskills]
        if self.lvl > 11:
            self.wskills = ['A' if w!='-' else w for w in self.wskills]
        if self.lvl > 24:
            self.wskills = ['S' if w!='-' else w for w in self.wskills]
        if self.lvl > 30:
            self.wskills = ['SS' if w!='-' else w for w in self.wskills]

        def skill_max(a, b):
            return a if skill_xp[a]>skill_xp[b] else b
            
        if len(self.charClass)>1:
            p_idx = self.charClass[1]
            self.wskills = [skill_max(self.wskills[n],class_wpns[p_idx][n]) for n in range(skill_cnt)]
        if len(self.charClass)>2:
            p_idx = self.charClass[2]
            self.wskills = [skill_max(self.wskills[n],class_wpns[p_idx][n]) for n in range(skill_cnt)]

        if self.lvl > 14:
            self.wskills = ['B' if w=='C' else w for w in self.wskills]
        if self.lvl > 24:
            self.wskills = ['A' if w=='C' or w=='B' else w for w in self.wskills]
       

    def updateStats(self):    
        self.lvl = lvl_index[self.firstChapter-1]

        b_idx = self.charClass[0]
        self.stats = list_sum(self.adj_stats,class_stats[b_idx])
        self.growths = list_sum(self.adj_growths,class_growths[b_idx])

        if len(self.charClass)>1:
            p_idx = self.charClass[1]
            self.stats = list_sum(self.stats,class_stats[p_idx])
        if len(self.charClass)>2:
            p_idx = self.charClass[2]
            self.stats = list_sum(self.stats,class_stats[p_idx])

        self.stats=[int(float(self.stats[n])+float(self.growths[n])*(float(self.lvl)-1)/100) for n in range(attr_cnt)]

        self.stats = list_bound(self.stats,0,70)
        self.growths = list_bound(self.growths,10,100)
    
    def write_string(self):
        out_str = ''
        out_str += self.write_snippet('ShouldUseDefaultEquipment',False) 
        out_str += self.write_snippet('Movement',self.mov)
        out_str += self.write_snippet('level',self.lvl)
        out_str += self.write_snippet('FirstBaseChapter',self.firstChapter)
        out_str += self.write_snippet('BaseClass',class_names[self.charClass[0]]) 
        if len(self.charClass) > 1:
            out_str += self.write_snippet('AdvancedClass',class_names[self.charClass[1]]) 
        else:
            out_str += self.write_snippet('AdvancedClass','') 
        if len(self.charClass) > 2:
            out_str += self.write_snippet('ExaltedClass',class_names[self.charClass[2]]) 
        else:
            out_str += self.write_snippet('ExaltedClass','') 
        for n,v in enumerate(self.stats):
            out_str += self.write_snippet(attr_names[n],v)
        for n,v in enumerate(self.growths):
            out_str += self.write_snippet(attr_names[n]+'Growth',v)

        if self.wpn0 != []:
            out_str += self.write_snippet('Weapon0',wpn_names[self.wpn0]) 
        if self.wpn1 != []:
            out_str += self.write_snippet('Weapon1',wpn_names[self.wpn1]) 
        if self.wpn2 != []:
            out_str += self.write_snippet('Weapon2',wpn_names[self.wpn2]) 
        if self.shld != []:
            out_str += self.write_snippet('Shield',eqp_names[self.shld]) 
        if self.itm0 != []:
            out_str += self.write_snippet('Item0',eqp_names[self.itm0]) 
        if self.itm1 != []:
            out_str += self.write_snippet('Item1',eqp_names[self.itm1]) 

        for n in range(skill_cnt):
            out_str += self.write_snippet(wpntype_names[n]+'Exp', skill_xp[self.wskills[n]])

        return out_str

    def write_snippet(self, subname, value):
        out_str = ''
        out_str += '\t"' + self.name + subname +  '" : {' + '\n'
        if isinstance(value, str):
            out_str += '\t\t"__type" : "string",' + '\n'
            out_str += '\t\t"value" : "' + value + '"\n'
        elif isinstance(value, bool):
            word = 'true' if value else 'false'
            out_str += '\t\t"__type" : "bool",' + '\n'
            out_str += '\t\t"value" : ' + word + '\n'
        elif isinstance(value, int):
            out_str += '\t\t"__type" : "int",' + '\n'
            out_str += '\t\t"value" : ' + str(value) + '\n'

        return out_str+'\t},\n'
        


char_data = []
characters = []
with open('chars.csv',mode='r',newline='') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)

    for row in csv_reader:
        char_data.append(row)
        characters.append(Character(row))

randgen = RandGenerator()
#rangen.chapterMode='N'
#rangen.classMode='U'

for c in characters:
	c.firstChapter=randgen.pullChapter(c.firstChapter)
	c.charClass=randgen.pullClass(c.firstChapter)
	c.adj_stats=randgen.randomizeStats(c.adj_stats)
	c.adj_growths=randgen.randomizeGrowths(c.adj_growths)
	c.updateStats() #uses class,stats,level
	c.updateWeaponSkills()
	c.weaponSkills=randgen.randomizeSkills(c.charClass) #pu into update stats?
	randgen.randomizeEquipment(c)

# debug: super arland
DEBUG=True
if DEBUG:
    characters[3].stats = [100,100,100,100,100,100]
    characters[3].mov = 40
    for c in characters:
        c.firstChapter=1


# generate final string
output = ''
output += '{\n\t"Chapter" : {\n\t\t"__type" : "int",\n\t\t"value" : 0\n	},'
output += '\n\t"SaveSlot" : {\n\t\t"__type" : "int",\n\t\t"value" : 3\n\t},'
output += '\n\t"Difficulty" : {\n\t\t"__type" : "int",\n\t\t"value" : 2\n\t},'
output += '\n\t"Growths" : {\n\t\t"__type" : "int",\n\t\t"value" : 0\n\t},'
output += '\n\t"Permadeath" : {\n\t\t"__type" : "int",\n\t\t"value" : 0\n\t},\n'

for c in characters:
    output += c.write_string()

    
output+='\t"OverwriteEarlyChapterDefaultEquipment" : {\n\t\t"__type" : "bool",\n\t\t"value" : true\n\t},\n'
output+='\t"ModdingEnabled" : {\n\t\t"__type" : "bool",\n\t\t"value" : true\n\t}\n'

output+='}'

with open('output.txt', 'w') as f:
    f.write(output)
