import discord
import time
from discord.ext import commands
from discord.utils import get
import random
import asyncio


intents = discord.Intents.default()
intents.members =  True
client = commands.Bot(command_prefix='!',intents=intents)

champions = ["Aatrox","Ahri","Akali","Akshan","Amumu","Anivia","Annie","Aphelios","Ashe","Aurelion_Sol","Azir","Bard","Blitzcrank","Brand","Braum","Caitlyn","Camille","Cassiopeia","ChoGath","Corki","Darius","Diana","Dr._Mundo","Draven","Ekko","Elise","Evelynn","Ezreal","Fiddlesticks","Fiora","Fizz","Galio","Gangplank","Garen","Gnar","Gragas","Graves","Gwen","Hecarim","Heimerdinger","Illaoi","Irelia","Ivern","Janna","Jarvan_IV","Jax","Jayce","Jhin","Jinx","Kaisa","Kalista","Karma","Karthus","Kassadin","Katarina","Kayle","Kennen","KhaZix","Kindred","Kled","KogMaw","Leblanc","Lee_Sin","Leona","Lillia","Lissandra","Lucian","Lulu","Lux","Malphite","Malzahar","Maokai","Miss_Fortune","Mordekaiser","Morgana","Nami","Nasus","Nautilus","Neeko","Nidalee","Nocturne","Nunu","Olaf","Orianna","Ornn","Pantheon","Poppy","Pyke","Qiyana","Quinn","Rakan","Rammus","RekSai","Rell","Renekton","Rengar","Riven","Rumble","Ryze","Samira","Sejuani","Senna","Seraphine","Sett","Shaco","Shen","Shyvana","Singed","Sion","Sivir","Skarner","Sona","Soraka","Swain","Sylas","Syndra","Tahm_Kench","Taliyah","Talon","Taric","Teemo","Thresh","Tristana","Trundle","Tryndamere","Twisted_Fate","Twitch","Udyr","Urgot","Varus","Vayne","Veigar","VelKoz","Vi","Viktor","Vladimir","Volibear","Warwick","Wukong","Xayah","Xerath","Xin_Zhao","Yasuo","Yone","Yorick","Yummi","Zac","Zed","Ziggs","Zilean","Zoe","Zyra","Alistar", "Kayn", "Master_Yi", "Viego"]
# file = open("total.txt","r+")
# total=int(file.readline())

#league lists
games = ["league of legends","valorant","tft","overcooked","rogue company"]


#valorant lists
roles = ["Controllers","Duelists","Initiators","Sentinels"]
controllers = ["Brimstone","Viper","Omen","Astra"]
duelists = ["Phoenix","Jett","Reyna","Raze","Yoru"]
initiators = ["Sova","Breach","Skye","KAY/O"]
sentinels = ["Killjoy","Cypher","Sage","Chamber"]



#EVENTS
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


#on_message
@client.event
async def on_message(message):
    if message.author == client.user:
         return    
    if message.content.startswith('!team4val'):
        valmessage = await message.channel.send('React with ⚔ for Duelist, ⚖ for Controller, 🏹 for Initiator, 🔧 for Sentinel')
        await valmessage.add_reaction('⚔')          
        await valmessage.add_reaction('⚖')  
        await valmessage.add_reaction('🏹')  
        await valmessage.add_reaction('🔧')  
    await client.process_commands(message)

#select an agent     
@client.event
async def on_reaction_add(reaction,user):
    channel = reaction.message.channel
    if client.user != user:
        if reaction.emoji == '⚔':
            duel=random.choice(duelists)
            await channel.send('{} selected duelist, u get {}'.format(user.mention,duel))
        if reaction.emoji == '⚖':
            control=random.choice(controllers)
            await channel.send('{} selected controller, u get {}'.format(user.mention,control))
        if reaction.emoji == '🏹':
            initiate=random.choice(initiators)
            await channel.send('{} selected initiator, u get {}'.format(user.mention,initiate))
        if reaction.emoji == '🔧':
            sen=random.choice(sentinels)
            await channel.send('{} selected sentinel, u get {}'.format(user.mention,sen))                        


@client.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("{} retry in {}".format(ctx.author.mention,time.strftime("%H:%M:%S",time.gmtime(error.retry_after))))
#COMMANDS

#goated
@client.command()
async def goated(ctx):
    role_name ='goated'
    member = discord.utils.get(ctx.guild.roles,name=role_name)
    async for user in ctx.guild.fetch_members(limit=None):
        if member in user.roles:
            member = discord.utils.get(ctx.guild.roles,name=role_name)
            await user.remove_roles(member)
            break
 
    user2 = ctx.author
    await ctx.send(f'{user2.mention} is now the goat :goat:')
    role = discord.utils.get(user2.guild.roles,name=role_name)
    await user2.add_roles(role)
    

#pagman command
@client.command()
async def pagman(ctx):
    await ctx.send("<:PagMan:821193446768640011>")

#chose a voter
@client.command()
async def pick(ctx):
    playing = []

    message = await ctx.send("React with 🤹")
    await message.add_reaction('🤹')
    await asyncio.sleep(10)
    
    message = await ctx.fetch_message(message.id)

    for reaction in message.reactions:
        if reaction.emoji == '🤹':
            async for user in reaction.users():
                if user!=client.user:
                    playing.append(user.mention)
    await ctx.send(f'{random.choice(playing)} pick the game')                

#commands
@client.command()
async def command(ctx):
    await ctx.send("```!team4val -> poll to randomly choose valorant agents based on roles \n!goated -> remove the goated role from the last user and gives it to you \n!pick -> randomly selects a user to pick a game \n```")

#addone

# @client.command()
# async def addone(ctx):
#     global total
#     total+=1
#     print(total)
#     file.seek(0)
#     file.write(str(total))
#     file.truncate
#     await ctx.send(str(total)+' times')


#lol champ game

# @client.command()
# @commands.cooldown(1,10800,commands.BucketType.user)
# async def lol(ctx):
#     champ = random.choice(champions)
#     pic = champ+"_Render.png"
#     await ctx.send(f"{ctx.author.mention} got {champ}")
#     await ctx.send(file=discord.File(pic))





#ODcxMjUzMzEzMjQzNDQ3MzM2.YQYn4A.AwawAiZldfMVq7JBuNmc2d_qIz0


client.run('ODcxMjUzMzEzMjQzNDQ3MzM2.YQYn4A.AwawAiZldfMVq7JBuNmc2d')        

