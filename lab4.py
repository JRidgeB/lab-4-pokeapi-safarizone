#Zachary Coleman
#10/8/2024
#lab4
#purpose: to simulate the safari zone



#includes-----------------------------------------------------------------------------
from sqlalchemy import Column, Integer, String, Double, BOOLEAN
import random
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from data_model import Base, Pokemon, PokemonSpecies
import requests
SQLALCHEMY_DATABASE_URL = "sqlite:///./data.db"
#-------------------------------------------------------------------------------------
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(bind=engine)
#--------------------------------------
#types
#this will later help inform bioms and help sort pokemon
# i removed stellar and unknown types as while listed in api, no pokemon should be in them
pokeapi_url_type = "https://pokeapi.co/api/v2/type/"
response_type = requests.get(pokeapi_url_type)
typeData = response_type.json()
pokemon_types = [type_info['name'] for type_info in typeData['results'] if type_info['name'] not in ['unknown', 'stellar']]
#--------------------------------------
#non-legendary pokemon
#this removes pokemon that should not be in safari zones
pokeapi_url_pokemon = "https://pokeapi.co/api/v2/pokemon?limit=100"
pokemon = session.query(PokemonSpecies).filter_by(is_legendary=False, is_mythical=False).all()
#---------------------------------------
#bioms
#each combo of types is a biome
num = 0
typeArr=[]
for type in pokemon_types:
    typeArr.append(type)
    num +=1

import numpy as np
arr = np.zeros((num+1,num+1))
biomes = arr.astype(str)
#each biome consists of two types, thus i made two arrays, one with an adjective for each type and the other with a place for each type
adj = ["normal","sparing","wind swept","poisonous","dirty","rocky","infested","spooky","metal","hot","flooded","lively","electric","wierd","polar","epic","dark","sparkly"]
place = ["flatland","dojo","hills","bog","plains","mountain","forest","graveyard","factory","volcana","ocean","prairie","turbine","alternate dimension","icecaps","ancient ruins","cave","castle"]



for i in range(0,18):
    for j in range(0,18):
        if i == j:
            biomes[i,j] = 'x'
        else:
            type1 = adj[i]
            type2 = place[j]
            biomes[i,j] = f"{type1} {type2}"
#-----------------------------------------
#catch rate
pokeapi_url_item = "https://pokeapi.co/api/v2/item"
##the pokiapi does not have the catch rating for each type of ball
ball = "safari ball"
ballRating = 1.5 #source:https://www.serebii.net/itemdex/safariball.shtml#:~:text=Safari%20Ball.%20The%20Safari%20Ball%20is%20a%20Pok%C3%A9Ball
#this is temp measure until i get a better solution
#------------------------------------------
#catch probability
#this is using both serebii and bulbapedia
#this is using specifically the hoenn gen 3 safari game with some modifications
def initCatchProb(pokeRating, ballRating):
    ballRating = 1.5 #used until i find a way to get more then one ball
    catchFactor = pokeRating/12.75 #main formula used in safari game
    if catchFactor < 1:
        catchFactor = 1
    catchFactor = catchFactor * ballRating
    return catchFactor 

#------------------------------------------------
def run(runaway):
    #this mimics the run away process in gen 3 safari
    chance = random.randint(0,100)
    if chance < runaway:
        return True
    else:
        return False
    
def shake(shakeTable,rate,pokename):
    #this mimics kinda that three shakes when you catch a pokemon
    catch1 = random.randint(0,255)
    catch2 = random.randint(0,255)
    catch3 = random.randint(0,255)
    threshhold = shakeTable[math.ceil(rate)]
    if catch1 < threshhold:
        print(f"*click! you caught the {pokename}")
        return True
    print("shake...")
    if catch2 < threshhold:
        print(f"*click! you caught the {pokename}")
        return True
    print("shake...")
    if catch3 < threshhold:
        print(f"*click! you caught the {pokename}")
        return True
    print("shake...\nOh no! it broke out")
    return False


#catch game
def catchGame(catchFactor,pokename,speed):
    #the catch game will use the catch method of the safari from gen 3, how ever to make it easier,
    #I will use the shake probability from gen 2, which is...
    '''First, a check is performed to determine whether the Pokémon is caught at all. 
    A random number between 0 and 255 is generated, and if this number is less than or equal to a, 
    the Pokémon is caught.
    Shake checks are only performed if the Pokémon is not caught.
    A single shake check consists of generating a random number between 0 and 255 and comparing it to b. 
    his is done at most three times, but if the number generated in a given shake check is greater 
    than or equal to b, no further shake checks will be performed. 
    The number of times the ball shakes is the same as the number of shake checks that were performed. 
    The table is essentially a very low-precision lookup table with numbers corresponding 
    to the shake rate in later generations, so ultimately, aside from rounding errors 
    (very bad ones in this case), the shake and capture rate remain similar between Generation II and 
    the formula later used in Generation III.'''
    #source:https://bulbapedia.bulbagarden.net/wiki/Catch_rate#Shake_probability_3
    shaketable = []
    total = 0
    for i in range(0,254):
        if i in range(0,1):
            shaketable.append(63)
        elif i == 2:
            shaketable.append(75)
        elif i == 3:
            shaketable.append(75)
        elif i == 5:
            shaketable.append(75)
        elif i == 255:
            shaketable.append(255)
        elif i in range(6,7):
            shaketable.append(103)
        elif i in range(8,10):
            shaketable.append(113)
        elif i in range(11,15):
            shaketable.append(126)
        elif i in range(16,20):
            shaketable.append(134)
        elif i in range(21,30):
            shaketable.append(149)
        elif i in range(31,40):
            shaketable.append(160)
        elif i in range(41,50):
            shaketable.append(169)
        elif i in range(51,60):
            shaketable.append(177)
        elif i in range(61,80):
            shaketable.append(191)
        elif i in range(81,100):
            shaketable.append(201)
        elif i in range(101,120):
            shaketable.append(211)
        elif i in range(121,140):
            shaketable.append(220)
        elif i in range(141,160):
            shaketable.append(227)
        elif i in range(161,180):
            shaketable.append(234)
        elif i in range(181,200):
            shaketable.append(240)
        elif i in range(201,220):
            shaketable.append(246)
        elif i in range(221,240):
            shaketable.append(251)
        elif i in range(241,254):
            shaketable.append(253)
    print(f"You have encoutnered a {pokename}\n\n")
    runaway = speed/10
    if runaway > .5:
        runaway = runaway * runaway
    if catchFactor > 255:
        catchFactor = 255
    
    init = shaketable[math.ceil(catchFactor)]
    while True:
        print("What would you like to do?\n1:Throw bait (decrease run chance, but also catch rate)\n2:Throw rock(increase catch rate but also run chance)\n3:Throw pokeball\n4:exit")
        choice = -1
        choice = input("Response? ")

        if choice == '1':#bait
            runaway = runaway/2
            init = init/2
            escape = run(runaway)
            if escape == True:
                print(f"{pokename} ran away")
                return None
        
        elif choice == '2':#rock
            runaway = runaway*2
            init = init*2
            escape = run(runaway)
            if escape == True:
                print(f"{pokename} ran away")
                return None
        elif choice == '3': #catch
            catch = shake(shaketable,init,pokename)
            if catch == True:
                print(f"you caught {pokename}!")
                return pokename
            escape = run(runaway)
            if escape == True:
                print(f"{pokename} ran away")
                return None
        elif choice == '4':
            return None
        else:
            print("invalid")
print("Welcome to the Safari zone!! I hope you have a wonderful time! \nIt is 20 pokedollars to come in")
enter = 0
#------------------------------------------------
#create safari biomes
def createSafari(size):
    Safari = [] #biome names
    type1Arr = [] #type 1
    type2Arr = [] #type 2
    if size <= 1:
        size = 1
    for i in range(0,size):

        type1 = random.randint(0,17)
        type2 = random.randint(0,17)
        while type1 == type2:
            type1 = random.randint(0,17)
            type2 = random.randint(0,17)
        biome = biomes[type1,type2]
        Safari.append(biome)
        type1Arr.append(type1)
        type2Arr.append(type2)
    return Safari,type1Arr,type2Arr

def randomPokemonOfType(type):
    stype_url = f"https://pokeapi.co/api/v2/type/{type}"
    stype_response = requests.get(stype_url)
    stype_data = stype_response.json()
    list = stype_data['pokemon']
    return random.choice(list)['pokemon']


def enterSafari(Safari,TypeOneArr,TypeTwoArr):
    display = 0
    print("Chose a biome below!!")
    for string in Safari:
        print(f"{display}:{str(string)}")
        display = display + 1
    choiceTemp = input("response? ")
    choice = int(choiceTemp) 
    try:

        saf = Safari[choice]
        t1 = TypeOneArr[choice]
        t2 = TypeTwoArr[choice]
        print(typeArr[t1])
        randpoke = []
        randpoke.append(randomPokemonOfType(typeArr[t1]))
        randpoke.append(randomPokemonOfType(typeArr[t2]))
        pokemon_details_url = randpoke[random.randint(0,1)]['url']
        pokemon_details_response = requests.get(pokemon_details_url)
        pokemon_details = pokemon_details_response.json()
        name = pokemon_details['name']
        speed = next(stat['base_stat'] for stat in pokemon_details['stats'] if stat['stat']['name'] == 'speed')
        species_url = pokemon_details['species']['url']
        species_response = requests.get(species_url)
        species_data = species_response.json()
        catch_rate = species_data['capture_rate']
        return catchGame(catch_rate,name,speed)


    except:
        print("\nBad choice. Going back to main menu")
        return None

Safari,TypeOneArr,TypeTwoArr = createSafari(4)
#----------------------------------------------
pokemonCaught = []
while True:
    choice = input("\n\n--------------\nWhat would you like to do? \n1: Enter the safari \n2:Reset the safari\n3:exit\nResponse? ")
    if choice == '3':
        break
    elif choice == '1':
        poke = enterSafari(Safari,TypeOneArr,TypeTwoArr)
        if poke != None:
            pokemonCaught.append(poke)
        




    








        


    










