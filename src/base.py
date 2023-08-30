from pathlib import Path
import requests
import numpy as np
import pandas as pd
import os


folder_dir = os.path.join(Path(__file__).parents[0], 'data')
class Base:
    """
    Class handles all connection to the API object and returns a dataframe
    from it's initialization. 
    """

    def __init__(self):
        #used for iterating through larger dictionaries as a base string
        self.base_url = "https://www.dnd5eapi.co"
        self.mystr= 'https://www.dnd5eapi.co/api/monsters/'
        self.response= requests.get(self.mystr).json()['results']

        #append all data found at url into list
        monsters=[]
        #iterate through the urls from the previous response
        for i in self.response:
            newstr=self.base_url+(i['url'])
            mdata= requests.get(newstr).json()
            monsters.append(mdata)

        #build base monster_master DF
        self.df_mon = pd.DataFrame.from_dict(monsters)
        #build dfs needed for the 3 remaining tables (these will be called in later functions)
        
        #mitigation table
        self.df_mon_mit = self.df_mon[['index','damage_vulnerabilities','damage_resistances','damage_immunities','condition_immunities']]
        #characteristics table
        self.df_mon_facet= self.df_mon[['index','proficiencies','senses','languages','forms']]
        #action table
        self.df_mon_action= self.df_mon[['index','actions','special_abilities','legendary_actions']]

        self.get_monster_master() 
        print('monsters master complete')
        self.get_monster_resists()
        print('monster resists complete')
        self.get_monster_characteristics()
        print('monster characteristics complete')

    def get_monster_master(self):
        '''Scraping data from the API and creating a Dataframe from it'''
        '''We create the mystr,response,and monsters locally'''
        #extract the natural ac from the table
        self.df_mon['natural_ac']= [ac[0]['value'] for ac in self.df_mon.armor_class] 
        #extract the speeds from the nested data columns
        walk =[]
        swim=[]
        fly=[]
        burr=[]
        #api was designed to not have null if it does not exist so try except 
        #is the only way to grab every record or fill it with null to maintain
        #SQL data normalization
        for s in self.df_mon.speed:
            try:
                walk.append(s['walk'].split(" ")[0])
            except:
                walk.append(np.nan)
            try:
                swim.append(s['swim'].split(" ")[0])
            except:
                swim.append(np.nan)
            try:
                fly.append(s['fly'].split(" ")[0])
            except:
                fly.append(np.nan)
            try:
                burr.append(s['burrow'].split(" ")[0])
            except:
                burr.append(np.nan)

        self.df_mon['speed_walk']=walk
        self.df_mon['speed_swim']=swim
        self.df_mon['speed_fly']=fly
        self.df_mon['speed_burrow']=burr

        self.mon_csv=self.df_mon[['index','name','size','type','alignment','natural_ac','speed_walk','speed_swim','speed_fly','speed_burrow','strength','dexterity','constitution','intelligence','wisdom','charisma','challenge_rating','xp','image','desc']]
        self.mon_csv.rename(columns={'index': 'monster_id'}, inplace=True)
        self.mon_csv.rename(columns={'desc': 'descrip'}, inplace=True)
        self.mon_csv.to_csv(f'{folder_dir}/monsters.csv',index=False)

    def get_monster_resists(self):
        #now lets loop through and create a massive list for this.
        #empty lists to 
        resistances=[]
        #df headers
        h=['monster_id','type','value']
        #iterate through the resist columns and strip the values
        #some values are dictionaries, some values are lists
        #I originally wrote this to be very fast with multiple functions to avoid
        #double for loops but since i was only running this like, ONCE.
        #I opted for my original more readable solution as I having trouble 
        #remembering what the point all of the functions were for to begin with.
        for imm in self.df_mon_mit.values:
            for j in range(1,len(self.df_mon_mit.keys())):
                if len(imm[j])>0:
                    if type(imm[j][0])==dict:
                        for i in imm[j]:
                            resistances.append([imm[0],self.df_mon_mit.columns[j],i['name']])
                    else:
                        for i in imm[j]:
                            resistances.append([imm[0],self.df_mon_mit.columns[j],i])
                    


        self.df_resist = pd.DataFrame(resistances,columns=h)
        self.df_resist.head()
        self.df_resist.to_csv(f'{folder_dir}/monster_resists.csv',index=False)

    def get_monster_characteristics(self):
        features=[]
        h=['monster_id','characteristic','attribute_name','value']
        #due to the varying degrees of how the data is stored there is only messy way to clean it up

        #-----------------------proficiencies---------------------------
        for imm in self.df_mon_facet[['index','proficiencies']].values:
            #all dictionaries are in a list
            if type(imm[1])== list:
                #iterate through listed dictionary
                for i in imm[1]:
                    features.append([imm[0],'proficiency',i['proficiency']['name'],i['value']])

        #-----------------------languagess-----------------------------
        for imm in self.df_mon_facet[['index','languages']].values:
            if type(imm[1])== str:
                #these for some reason are comma split as a string and not a list
                for i in imm[1].split(','):
                    #very weird one off case of telepgathy having a value but not listed as a value
                    #so we extract it from the string
                    val=''.join(j for j in i if j.isnumeric()==True)
                    #sanitize the variable
                    if len(val)==0:
                        val=np.nan
                    else:
                        val=int(val)
                    features.append([imm[0],'language',i,val])

        #--------------------------grab forms -------------------
        for imm in self.df_mon_facet[['index','forms']].values:

            if type(imm[1])!= float:
                for i in imm[1]:
                    features.append([imm[0],'forms',i['name'],np.nan])
                
        #-----------------------grab sense data-------------------
        for imm in self.df_mon_facet[['index','senses']].values:
            if len(imm)>0:
                for k,v in imm[1].items():
                    if type(v)==str:
                        val = v.split(" ")
                        val= val[0]
                    else:
                        val=v    
                    features.append([imm[0],'senses',k,val])


        self.df_characteristics= pd.DataFrame(features,columns=h)

        self.df_characteristics.head()
        self.df_characteristics.to_csv(f'{folder_dir}\monster_characteristics.csv',index=False)

    def get_monster_actions(self):
        actions=[]
        for cols in range(1,4):
            for imm in self.df_mon_action.values:
                    #all dictionaries are in a list if not NAN
                    if type(imm[cols])==list:
                        #iterate through listed dictionary
                        for i in imm[cols]:
                            if (i['name']!='Multiattack' and i['name']!='Breath Weapons') :
                                # try block to iterate through the dictionary and parse the data
                                name = i['name']
                                #--------------------------------------------------------------------
                                try:
                                    AB = i['attack_bonus']
                                except:
                                    AB = np.nan
                                #--------------------------------------------------------------------
                                try:
                                    damagetype = " & ".join(j['damage_type']['name'] for j in i['damage'])
                                except:
                                    damagetype = np.nan
                                #---------------------------------------------------------------------------
                                try:
                                    damagetype = " & ".join(j['damage_type']['name'] for j in i['damage'])
                                except:
                                    damagetype = np.nan
                                #---------------------------------------------------------------------------
                                try:
                                    damagedice = " + ".join(j['damage_dice'] for j in i['damage'])
                                except:
                                    damagedice = np.nan
                                #-------------------------------------------------------------------
                                try:
                                    dc_type = i['dc']['dc_type']['name']
                                except:
                                    dc_type = np.nan
                                #-----------------------------------------------------------------------           
                                try:
                                    dc_value = i['dc']['dc_value']
                                except:
                                    dc_value = np.nan
                                #--------------------------------------------------------------------
                                try:
                                    desc= i['desc']
                                except:
                                    desc= np.nan
                    
                                actions.append([imm[0],self.df_mon_action.columns[cols],i['name'],damagetype,AB,damagedice,dc_type,dc_value,np.nan,'',desc])
        #append the very nested dragon logic
        for cols in range(1,4):
            for imm in self.df_mon_action.values:
                    #all dictionaries are in a list if not NAN
                    if type(imm[cols])==list:
                        #iterate through listed dictionary
                        for i in imm[cols]:
                            if (i['name']!='Multiattack' and i['name']=='Breath Weapons') :
                                for k in i['options']['from']['options']:
                                    # try block to iterate through the dictionary and parse the data
                                    name = k['name']
                                    #--------------------------------------------------------------------
                                    AB = np.nan
                                    #--------------------------------------------------------------------
                                    try:
                                        damagetype = " & ".join(j['damage_type']['name'] for j in k['damage'])
                                    except:
                                        damagetype = np.nan
                                    #---------------------------------------------------------------------------
                                    try:
                                        damagetype = " & ".join(j['damage_type']['name'] for j in k['damage'])
                                    except:
                                        damagetype = np.nan
                                    #---------------------------------------------------------------------------
                                    try:
                                        damagedice = " + ".join(j['damage_dice'] for j in k['damage'])
                                    except:
                                        damagedice = np.nan
                                    #-------------------------------------------------------------------
                                    try:
                                        dc_type = k['dc']['dc_type']['name']
                                    except:
                                        dc_type = np.nan
                                    #-----------------------------------------------------------------------           
                                    try:
                                        dc_value = k['dc']['dc_value']
                                    except:
                                        dc_value = np.nan
                                    #--------------------------------------------------------------------
                                    desc= np.nan
                                    #----------------------------------------------------------------
                                    actions.append([imm[0],self.df_mon_action.columns[cols],name,damagetype,AB,damagedice,dc_type,dc_value,np.nan,'',desc])
                
        h=['monster_id','action_type','action_name','damage_type','attack_bonus','damage_dice','dc_type','dc_value','multi_attack','multi_attack_descrip','descrip']
        self.df_actions = pd.DataFrame(actions,columns=h)
        #bring in our multi attack logic to iterate over all present abilities

        multi=[]

        for cols in range(1,4):
            for imm in self.df_mon_action.values:
                    #all dictionaries are in a list if not NAN
                    if type(imm[cols])==list:
                        #iterate through listed dictionary
                        for i in imm[cols]:
                            if (i['name']=='Multiattack' and i['name']!='Breath Weapons') :
                                # try block to iterate through the dictionary and parse the data
                                for k in i['actions']:
                                    multi.append([imm[0],k['action_name'],k['count'],i['desc']])

        #update our data frame with these multi attack values 
        for i in multi:
            self.df_actions.loc[(self.df_actions['monster_id'] == i[0]) & (self.df_actions['action_name'] == i[1]), 'multi_attack'] = i[2]
            self.df_actions.loc[(self.df_actions['monster_id'] == i[0]) & (self.df_actions['action_name'] == i[1]), 'multi_attack_descrip'] = i[3]

        #create our data csv    
        self.df_actions.to_csv(f'{folder_dir}/monster_actions.csv',index=False)
                
        self.df_actions.head()


if __name__ == '__main__':
    c= Base()
    print('monster data complete.')