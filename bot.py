import discord
import requests
import math
from keys import GITHUB_DISCORD_TOKEN, GITHUB_FORTNITE_API_KEY

client = discord.Client()

# Constant
DISCORD_TOKEN = GITHUB_DISCORD_TOKEN
FORTNITE_API_KEY = GITHUB_FORTNITE_API_KEY

LIST = ['Verified']
VERIFIED = 4

# Return the current season squad K/D of the fortnite player
def get_ratio(username):
    try:
        print(username)
        link = 'https://api.fortnitetracker.com/v1/profile/pc/' + username
        response = requests.get(link, headers={'TRN-Api-Key': FORTNITE_API_KEY})
        if response.status_code == 200:
            collection = response.json()
            if 'error' in collection:
                return "-1"
            else:
                ratio = collection['stats']['curr_p9']['kd']['value']
                return ratio
            print("Invalid username")
            return "-1"
        else:
            print("Error parsing data.")
            return "-2"
    except KeyError:
        print("Error finding data. KeyError was returned.")
        return "-3"

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    # The command !patch return a link with the lastest patch note
    if message.content.startswith('!patch'):
        await message.channel.send('Latest patch notes: https://www.epicgames.com/fortnite/en-US/patch-notes/')
    # The command !help explains the one function
    if message.content.startswith('!help'):
        embed = discord.Embed(colour=discord.Colour(0x8e2626), url="https://github.com/af1/kdFortniteDiscordBot",)
        embed.set_author(name="Verify Bot Help", icon_url="")
        embed.add_field(name="Set your Discord nickname to be exacly the same as your Epic Games player name. Then type: !verify", value="You can change your nickname by typing \"/nick *YourEpicIGN*\". The bot looks at your squad K/D for the current season, so if you have no games played yet, the bot won\'t be able to verify you.", inline=False)
        await message.channel.send(embed=embed)
    # The command !verify return attribute a rank according to the K/D of the user
    if message.content.startswith("!verify"):
        for list in LIST:
            roles = discord.utils.get(message.guild.roles, name=list)
        username = '{0.author.display_name}'.format(message)
        ratio = float(get_ratio(username))
        msgRatio = str(ratio)
        msgVerified = str(VERIFIED)
        print(ratio)
        if ratio == -1.0:
            embed = discord.Embed(colour=discord.Colour(0x8e2626), url="https://github.com/af1/kdFortniteDiscordBot",)
            embed.set_author(name="Verify " + message.author.display_name, icon_url=message.author.avatar_url)
            embed.add_field(name="Fortnite player **" + message.author.display_name + "** not found.", value="\nYour Discord nickname and IGN must be exactly the same. Change your Discord nickname to your IGN and try again.", inline=False)
            await message.channel.send(embed=embed)
        elif ratio == -2.0:
            embed = discord.Embed(colour=discord.Colour(0x8e2626), url="https://github.com/af1/kdFortniteDiscordBot",)
            embed.set_author(name="Verify " + message.author.display_name, icon_url=message.author.avatar_url)
            embed.add_field(name="Data not found.", value="Fortnite Tracker is down. Please try again shortly.", inline=False)
            await message.channel.send(embed=embed)
        elif ratio == -3.0:
            embed = discord.Embed(colour=discord.Colour(0x8e2626), url="https://github.com/af1/kdFortniteDiscordBot",)
            embed.set_author(name="Verify " + message.author.display_name, icon_url=message.author.avatar_url)
            embed.add_field(name="No stats found for squad mode in the current season.", value="Play some games and try again.", inline=False)
            await message.channel.send(embed=embed)
        elif ratio > 0 and ratio < VERIFIED:
            print("🚫")
            print("-")
            embed = discord.Embed(colour=discord.Colour(0x45278e), url="https://github.com/af1/kdFortniteDiscordBot",)
            embed.set_author(name="Verify " + message.author.display_name, icon_url=message.author.avatar_url)
            embed.add_field(name=message.author.display_name + " does not have over a " + msgVerified + " K/D.", value="Current season squads K/D: **" + msgRatio + "**", inline=False)
            await message.channel.send(embed=embed)
        elif ratio >= VERIFIED:
            print("✅")
            print("-")
            role = discord.utils.get(message.guild.roles, name=LIST[0])
            embed = discord.Embed(colour=discord.Colour(0x45278e), url="https://github.com/af1/kdFortniteDiscordBot",)
            embed.set_author(name="Verify " + message.author.display_name, icon_url=message.author.avatar_url)
            embed.add_field(name=message.author.display_name + " has over a " + msgVerified + " K/D. Verified!", value="Current season squads K/D: **" + msgRatio + "**", inline=False)
            user=message.author
            await message.channel.send(embed=embed)
            await user.add_roles(role) 
            
@client.event
async def on_ready():
    print("-")
    print("Logged in as: " + client.user.name)
    print("With Client User ID: " + str(client.user.id))
    print("Verified set to: " + str(VERIFIED))
    print("-")

client.run(DISCORD_TOKEN)


