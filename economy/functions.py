import json
from os import remove
import random
import re
from config import *
import discord
from pymongo import MongoClient


client = MongoClient(CONNECTION_STRING)
db = client.get_database(DATABASE_NAME)
records = db.users


def check_account(user_id):
    is_exists = records.find_one({'user_id': user_id})
    if is_exists is not None:
        return True
    else:
        return False


def create_account(user_id):
    piper_coin = STARTING_BALANCE
    data = {'user_id':user_id,'piper_coin':piper_coin,'owned_gpu':[]}
    records.insert_one(data)

def beg_coin(user_id):
        probablity = random.randrange(1,101)
        if probablity > 8:
            amount = random.randrange(1,14)
            records.update_one({'user_id': user_id}, {'$inc': {'piper_coin':amount}})

            return amount
        if probablity < 8:
            amount = 0
            return amount

def balance(user_id):
    bal = records.find_one({'user_id': user_id})['piper_coin']
    em = discord.Embed(
        title=f"Balance",
        description=f"<@{user_id}> Piper Wallet",
        color=discord.Colour.from_rgb(255,215,0)
    )
    em.add_field(name=f"PiperCoins :coin:",value=f"{bal}",inline = False)
    return em

def leaderboard():
    user_dict = {}
    leaderboard_length = 5
    with open('data/users.json','r') as f:
        file = json.load(f)
        for i in range(len(file)):
            user_dict[file[i]['user_id']] = file[i]['piper_coin']
        sorted_list = sorted(user_dict.items(), key =lambda kv:(kv[1], kv[0]))
        if len(sorted_list) < 5:
            msg = "You need at least 5 actively playing players to get Leaderboards"
            return msg
        else:
            em = discord.Embed(
                title="Leaderboard",
                description="Top PiperCoin Holders",
                color=discord.Color.blurple()
            )
            for i in range(leaderboard_length):
                em.add_field(name='\u200b',value=f"<@{sorted_list[len(sorted_list)-i-1][0]}> - {sorted_list[len(sorted_list)-i-1][1]} :coin:",inline=False)
            return em

def invest(user_id,amount):
    percentage_increase = random.randrange(-4,7)
    if percentage_increase > 0:
        #file[index]['piper_coin'] = file[index]['piper_coin'] + round((amount*percentage_increase)/100)
        records.update_one({'user_id': user_id}, {'$inc': {'piper_coin':round((amount*percentage_increase)/100)}})
        msg = f"The stocks went :arrow_double_up: by {percentage_increase}%.You Won {round((amount*percentage_increase)/100)} :coin:"
        embed = discord.Embed(
        title="Result",
        description=f"{msg}",
        color=discord.Colour.brand_green()
        )
        return embed
    elif percentage_increase < 0:
        records.update_one({'user_id': user_id}, {'$inc': {'piper_coin':round((amount*percentage_increase)/100)}})
        msg = f"The stocks went :arrow_double_down: by {percentage_increase}%.You Lost {(round(amount*percentage_increase)/100)} :coin:"

        embed = discord.Embed(
        title="Result",
        description=f"{msg}",
        color=discord.Colour.brand_red()
        )
        return embed
    else:
        msg = f"The Stocks didn't go :arrow_double_up: or :arrow_double_down:.You did not Won anything."
        embed = discord.Embed(
        title="Result",
        description=f"{msg}",
        color=discord.Colour.yellow()
        )
        return embed


def get_gpu_details(user_id,name):
    gpu_price = None
    index = None
    gpu_name = None
    with open('data/gpu.json','r') as f:
        file = json.load(f)
        for i in range(len(file)):
            if file[i]["name"] == name:
                index = i
                gpu_name = file[index]["full_name"]
                gpu_price = file[index]['price']
                details = [gpu_name,gpu_price]
                f.seek(0)
                return details


        msg = f"<@{user_id}> Invalid GPU Name"
        emb = discord.Embed(
            title="Error",
            description=f"{msg}",
            color=discord.Colour.red()
        )
        f.seek(0)
        return emb

def check_bal(user_id,price):
    user = records.find_one({'user_id': user_id})
    if user['piper_coin'] > price:
        return True
    else:
        msg = f"<@{user_id}>, you do not have enough :coin: to buy the GPU"
        em = discord.Embed(
            title="Insufficient Coins",
            description=f"{msg}",
            color=discord.Colour.red() 
        )
        return em


def buy(user_id,price: int,name: str):
    records.update_one({'user_id': user_id}, {'$inc': {'piper_coin': -(price)}})
    records.update_one({'user_id': user_id}, {'$push': {'owned_gpu': name}})
    return True

def gpu_embed():
    with open('data/gpu.json') as f:
        file = json.load(f)
        em = discord.Embed(
            title="GPU List",
            description="Supported GPUs for Mining",
            color=discord.Colour.blurple()
        )
        for i in range(len(file)):
            em.add_field(name=f"{file[i]['full_name']}",value=f"Price-`{file[i]['price']}` :coin:\nEfficiency-`{file[i]['efficiency']}`\nname-`{file[i]['name']}`\n",inline=True)

        return em

def owns_gpu(user_id,name):
    user = records.find_one({'user_id': user_id})
    if name in user['owned_gpu']:
        return True
    else:
        return False

def sell(user_id,details: list,name):
    records.update_one({'user_id': user_id}, {'$inc': {'piper_coin': round(details[1]*0.9)}})
    records.update_one({'user_id': user_id}, {'$pull': {'owned_gpu': name}})
    return True


def exists_in_owned_gpu(user_id,name):
    user = records.find_one({'user_id': user_id})
    if name in user['owned_gpu']:
        return True
    else:
        return False


def max_gpu(user_id):
    user = records.find_one({'user_id': user_id})
    total = len(user['owned_gpu'])
    return total


def owned(user_id):
    owned = []
    user = records.find_one({'user_id': user_id})
    for i in range(len(user['owned_gpu'])):
        owned.append(user['owned_gpu'][i])
    return owned


def total_efficiency(user_id):
    efficiency = 0
    owned_gpu = owned(user_id)
    with open('data/gpu.json') as f:
        file = json.load(f)
        for i in range(len(owned_gpu)):
            for j in range(len(file)):
                if file[j]['name'] == owned_gpu[i]:
                    efficiency += file[j]['efficiency']
        return efficiency

def mine(user_id,value_list: list):
    total_gained = random.randrange(value_list[0],value_list[1])
    records.update_one({'user_id': user_id}, {'$inc': {'piper_coin':total_gained}})
    return total_gained

def daily(user_id):
    records.update_one({'user_id': user_id}, {'$inc': {'piper_coin':DAILY_BONUS}})
    return True