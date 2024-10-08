#Zachary Coleman
#10/8/2024
#lab4
#purpose: to simulate the safari zone



#includes-----------------------------------------------------------------------------
from sqlalchemy import Column, Integer, String, Double, BOOLEAN
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
data = response_type.json()
pokemon_types = [type_info['name'] for type_info in data['results'] if type_info['name'] not in ['unknown', 'stellar']]
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


    










