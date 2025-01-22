import discord
import os
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord import Member
import asyncio
import random
import urllib.request
import json
import subprocess

with open("config.json") as wl:
    config = json.load(wl)

bot = commands.Bot(command_prefix=config['prefix'], intents=discord.Intents.all())

bot.config = config

whitelist = config['whitelist']

bot.remove_command('help')

emcolor = config['embedcolor']

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name=config['status'], url="https://www.twitch.tv/hkbot"))
    print("\n----------------")
    print("|  BOT START   |")
    print("----------------")


@bot.command()
async def wl(ctx, member: discord.Member):
    auteur = ctx.message.author.id
    ssd = config['owner']
    if auteur in ssd:
        with open('config.json', 'r') as f:
            prefixes = json.load(f)
            prefixes['whitelist'].append(int(f"{member.id}")) 
            with open('config.json', 'w') as f:
                json.dump(prefixes, f, indent=4)
            await ctx.send(f"{member.name} est whitelist")
            os.system("python3 gestion.py")
            quit()
    else:
        await ctx.send("Vous n'êtes pas whitelist !")


@bot.command()
async def unwl(ctx, member: discord.Member):
    auteur = ctx.message.author.id 
    ssd = config['owner']
    if auteur in ssd:      
        with open('config.json', 'r') as f:
            file = json.load(f)
            file['whitelist'].remove(int(f"{member.id}"))  
            with open('config.json', 'w') as f:
                json.dump(file, f, indent=4)
            await ctx.send(f"{member.name} n'est plus whitelist")
            os.system("python3 gestion.py")
            quit()

@bot.command()
async def help(ctx):
    guild = ctx.guild
    embedVar = discord.Embed(title="HELP", description="Les commandes help", color=emcolor)
    embedVar.add_field(name="```"+bot.command_prefix +"utilitaire```", value="Envoie les commande utilitaire", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"moderation```", value="Envoie les commande de modération", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"captcha```", value="Envoie les commande du captcha", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"secur```", value="Envoie les commande de sécurité", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"divers```", value="Envoie les commande divers", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"configuration```", value="Envoie les commande de configuration", inline=False)
    embedVar.set_thumbnail(url=guild.icon)
    await ctx.send(embed=embedVar)

@bot.command()
async def moderation(ctx):
    guild = ctx.guild
    embedVar = discord.Embed(title="MODÉRATION", description="Les commandes de modération", color=emcolor)
    embedVar.add_field(name="```"+bot.command_prefix +"addrole [membre] <role>```", value="Ajoute le role ping au membre ping", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"bl [membre] <raison>```", value="Banni le memre du serveur", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"clear [nombre]```", value="Supprime le nombre de messages donnés", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"create [nom]```", value="Créer un channel dans le serveur", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"delete```", value="Supprime le channel dans lequel est fait cette commande", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"kick [membre] <raison>```", value="Kick le membre ping", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"lock```", value="Les membre ne pourront plus parler dans le channel", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"massiverole```", value="Ajoute le role ping a tous un role", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"mute [membre] <raison>```", value="Rend muet le membre ping", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"unbl [membre id]```", value="Débanni le membre", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"unmute [membre]```", value="Enlève le muet du membre ping", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"remrole [membre] <role>```", value="Retire le rôle a la personne ping", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"unlock```", value="Les membre pourront de nouveau parler dans le channel", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"unwl [membre]```", value="Retire le membre ping de la whitelist", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"wl [membre]```", value="Whitelist le membre ping", inline=False)
    embedVar.set_thumbnail(url=guild.icon)
    await ctx.send(embed=embedVar)

@bot.command()
async def utilitaire(ctx):
    guild = ctx.guild
    embedVar = discord.Embed(title="UTILITAIRE", description="Les commandes utilitaire", color=emcolor)
    embedVar.add_field(name="```"+bot.command_prefix +"botname [nom]```", value="Renomme le bot", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"say [message]```", value="Envoie votre message dans un embed", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"create [nom]```", value="Créer un channel dans le serveur", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"delete```", value="Supprime le channel dans lequel est fait cette commande", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"invites [membre id]```", value="Envoie le nombre d'invitations faites !", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"kick [membre] <raison>```", value="Kick le membre ping", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"lookup [membre]```", value="Envoie les informations du compte de la personne", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"mybots```", value="Envoie la liste des bots que l'on possède", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"pic```", value="Envoie la pp du membre", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"rename [membre] <nom>```", value="Renomme le membre ping", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"renew```", value="Recréer le channel ou vous faites la commande ", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"rg```", value="Envoie les T.O.S de discord", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"serverinfo```", value="Envoie les informations du serveur", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"setprefix [prefix]```", value="Change le préfixe du bot", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"setuplogs```", value="Setup les logs", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"snipe```", value="Envoie le dernier message supprimé", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"sondage [sondage]```", value="Envoie votre sondage dans un embed avec 2 réaction 1 et 2", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"status [status]```", value="Change le statut du bot", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"verif```", value="Vérifie le membre qui fais la commande", inline=False)
    embedVar.set_thumbnail(url=guild.icon)
    await ctx.send(embed=embedVar)

@bot.command()
async def secur(ctx):
    guild = ctx.guild
    embedVar = discord.Embed(title="SECUR", description="Les commandes de sécurité", color=emcolor)
    embedVar.add_field(name="```"+bot.command_prefix +"panic```", value="Verrouille tous, retire toutes les perms, bloque tous les channels (à utiliser qu’en cas d’urgence car après il faut attendre la crown pour tous débloquer)", inline=False)
    await ctx.send(embed=embedVar)

@bot.command()
async def captcha(ctx):
    guild = ctx.guild
    embedVar = discord.Embed(title="CAPTCHA", description="Les commandes du captcha", color=emcolor)
    embedVar.add_field(name="```"+bot.command_prefix +"captchaoff```", value="Désactive le captcha sur le serveur", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"captchaon```", value="Active le captcha sur le serveur", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"captchasetup```", value="Setup le captcha pour le serveur", inline=False)
    embedVar.set_thumbnail(url=guild.icon)
    await ctx.send(embed=embedVar)

@bot.command()
async def divers(ctx):
    guild = ctx.guild
    embedVar = discord.Embed(title="DIVERS", description="Les commandes divers", color=emcolor)
    embedVar.add_field(name="```"+bot.command_prefix +"ping```", value="Envoie si le bot est 'on' ou 'off' ", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"restart```", value="Redémarre le bot", inline=False)
    embedVar.add_field(name="```"+bot.command_prefix +"version```", value="Envoie la version du bot", inline=False)
    embedVar.set_thumbnail(url=guild.icon)
    await ctx.send(embed=embedVar)

@bot.command()
async def configuration(ctx):
    guild = ctx.guild
    embedVar = discord.Embed(title="CONFIG", description="Les commandes de config", color=emcolor)
    embedVar.add_field(name="```"+bot.command_prefix +"setjoinchannel [channel id]```", value="Définie le channel de message de join", inline=False)
    embedVar.set_thumbnail(url=guild.icon)
    await ctx.send(embed=embedVar)


@bot.command()
async def restart(ctx):
    auteur = ctx.message.author.id
    if auteur in whitelist:
        await ctx.send("Bot redémarrer !")
        os.system("python3 gestion.py")
        quit()
    else:
        await ctx.send("Vous n'êtes pas whitelist !")

@bot.command()
async def botname(ctx, content):
    await bot.user.edit(username=content)
    guild = ctx.guild
    embedVar = discord.Embed(title="RENAME", description="Nouveau nom: "+content, color=emcolor)
    await ctx.send(embed=embedVar)

#captcha
@bot.command()
async def captchasetup(ctx):
    auteur = ctx.message.author.id
    if auteur in whitelist:
        guild = ctx.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False, read_message_history=True, send_messages=False),
            }
        await guild.create_text_channel("📨・join", overwrites=overwrites)
        for channel in guild.channels:
            await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=False)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=True, read_messages=True, read_message_history=True, send_messages=True),
            }
        await guild.create_text_channel("✅・vérification", overwrites=overwrites)
        channel = discord.utils.get(ctx.guild.channels, name="✅・vérification")
        channel_id = channel.id
        for role in guild.roles:
            if role.name == "@everyone":
                permissions = discord.Permissions()
                permissions.update(view_channel = False)
                await role.edit(reason = None, permissions=permissions)
        perms = discord.Permissions(view_channel=True, read_message_history=True, connect=True, speak=True, send_messages=True, stream=True, use_voice_activation=True, create_instant_invite=True)
        await guild.create_role(name=config['rolecaptcha'], color=0, permissions=perms)
        embed = discord.Embed(title="CAPTCHA", description="@everyone faite +verif pour valider le captcha !", color=emcolor)
        await channel.send(embed=embed)
        for channel in guild.channels:
            role = discord.utils.get(ctx.guild.roles, name=config['rolecaptcha'])
            await ctx.channel.set_permissions(role, view_channel=True)
        await ctx.send("Captcha mis en place !")
    else:
        await ctx.send("Vous n'êtes pas whitelist !")

@bot.command()
async def verif(ctx):
    await ctx.message.delete()
    aut = ctx.message.author
    aute = ctx.message.author.id
    root = discord.utils.get(ctx.guild.roles, name=config['rolecaptcha'])
    await aut.add_roles(root)
    channel = bot.get_channel(config['joinchannel'])
    await channel.send("Bienvenue <@"+str(aute)+"> sur "+config['servername']+" !")

@bot.command()
async def setjoinchannel(ctx, arg1):
    auteur = ctx.message.author.id
    if auteur in whitelist:
        with open('config.json', 'r+') as f:
            data = json.load(f)
            data['joinchannel'] = int(arg1)
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
            f.close()
            await ctx.send('Nouveau join channel <#'+str(arg1)+">")
            os.system("python3 gestion.py")
            quit()
    else:
        await ctx.send("Vous n'êtes pas whitelist !")

@bot.command()
async def captchaon(ctx):
    auteur = ctx.message.author.id
    if auteur in whitelist:
        guild = ctx.guild
        for role in guild.roles:
            if role.name == "@everyone":
                permissions = discord.Permissions()
                permissions.update(view_channel = False)
                await role.edit(reason = None, permissions=permissions)
        for channel in guild.channels:
            try:
                await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=False, read_messages=False, read_message_history=False, send_messages=False)
            except:
                pass
        await ctx.send("Captcha activé !")
    else:
        await ctx.send("Vous n'êtes pas whitelist !")


@bot.command()
async def captchaoff(ctx):
    auteur = ctx.message.author.id
    if auteur in whitelist:
        guild = ctx.guild
        for role in guild.roles:
            if role.name == "@everyone":
                permissions = discord.Permissions()
                permissions.update(view_channel=True, read_messages=True, read_message_history=True, send_messages=True)
                await role.edit(reason = None, permissions=permissions)
        for channel in guild.channels:
            try:
                await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=False)
            except:
                pass
        await ctx.send("Captcha désactivé !")
    else:
        await ctx.send("Vous n'êtes pas whitelist !")


@bot.command()
async def setprefix(ctx, nprefix):
    prefix = nprefix
    auteur = ctx.message.author.id
    if auteur in whitelist:
        with open('config.json', 'r+') as f:
            data = json.load(f)
            data['prefix'] = prefix
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
            f.close()
            await ctx.send('Nouveau préfix: '+prefix)
            try:
                name = "["+nprefix+"] "+config['namebot']
                await bot.user.edit(username=name)
            except:
                pass
            os.system("python3 gestion.py")
            quit()
    else:
        await ctx.send("Vous n'êtes pas whitelist !")

@bot.command()
async def say(ctx, *, content: str):
    auteur = ctx.message.author.id
    if auteur in whitelist:
        await ctx.message.delete()
        await ctx.send(content)
    else:
        await ctx.send("Vous n'êtes pas whitelist !")

@bot.command()
async def panic(ctx):
    auteur = ctx.message.author.id
    if auteur in whitelist:
        guild = ctx.guild
        for role in guild.roles:
            permissions = discord.Permissions()
            permissions.update(view_channel=False, read_message_history=False, connect=False, speak=False, send_messages=False, stream=False, use_voice_activation=False, create_instant_invite=False, administrator=False)
            await role.edit(reason = None, permissions=permissions)
            embed = discord.Embed(title="PANIC", description="Le panic mode a été activé !", color=emcolor)
            await ctx.send(embed=embed)
    else:
        await ctx.send("Vous n'êtes pas whitelist !")


#ping
@bot.command()
async def ping(ctx):
    embedVar = discord.Embed(title="|---------------|\n| BOT START |\n|---------------|", color=emcolor)
    await ctx.send(embed=embedVar)



#lock / unlock
@bot.command()
async def lock(ctx):
    auteur = ctx.message.author.id
    if auteur in whitelist:
        await ctx.channel.set_permissions(ctx.guild.default_role,send_messages=False)
        await ctx.send("Les membre ne peuvent plus parler dans ce channel !")
    else:
        await ctx.send("Vous n'êtes pas whitelist !")


@bot.command()
async def unlock(ctx):
    auteur = ctx.message.author.id
    if auteur in whitelist:
        await ctx.channel.set_permissions(ctx.guild.default_role,send_messages=True)
        await ctx.send("Les membre peuvent maintenant parler dans ce channel !")
    else:
        await ctx.send("Vous n'êtes pas whitelist !")


#clear
@bot.command()
async def clear(ctx, amount=100):
    auteur = ctx.message.author.id
    if auteur in whitelist:
        await ctx.send("Message suprimé !")
        await ctx.channel.purge(limit=amount)
    else:
        await ctx.send("Vous n'êtes pas whitelist !")


#mute
@bot.command()
async def mute(ctx, member: discord.Member, *, reason=None):
    auteur = ctx.message.author.id
    if auteur in whitelist:
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")
        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")
            
        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
        embed = discord.Embed(title="MUTE", description=f"{member.mention} EST MUTE ", color=emcolor)
        embed.add_field(name="RAISON:", value=reason, inline=False)
        await ctx.send(embed=embed)
        await member.add_roles(mutedRole, reason=reason)
        await member.send(f" VOUS ÉTE MUTE DU SERVEUR: {guild.name} RAISON: {reason}")
        print("Commande = mute")
    else:
        await ctx.send("Vous n'êtes pas whitelist !")


@bot.command()
async def unmute(ctx, member: discord.Member):
    auteur = ctx.message.author.id
    if auteur in whitelist:
        mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(mutedRole)
        embed = discord.Embed(title="UNMUTE", description=f" UNMUTE {member.mention}", color=emcolor)
        await ctx.send(embed=embed)
        guild = ctx.guild
        await member.send(f" VOUS ÉTE UNMUTE DU SERVEUR: {guild.name}")
        print("Commande = unmute")
    else:
        await ctx.send("Vous n'êtes pas whitelist !")


#kick
@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    auteur = ctx.message.author.id
    if auteur in whitelist:
        await ctx.guild.kick(member)
        embed = discord.Embed(title="KICK", description=f" Le membre {member.mention} a été kick pour {reason}", color=emcolor)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Vous n'êtes pas whitelist !")


#ban
@bot.command()
async def bl(ctx, member : discord.Member, *, reason = None):
    auteur = ctx.message.author.id
    if auteur in whitelist:
        await ctx.guild.ban(member)
        embed = discord.Embed(title="BLACKLIST", description="<@"+str(member.id) + "> a été blackliste", color=emcolor)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Vous n'êtes pas whitelist !")



#unban
@bot.command()
async def unbl(ctx, id: int):
    auteur = ctx.message.author.id
    if auteur in whitelist:
        user = await bot.fetch_user(id)
        await ctx.guild.unban(user)
        embed = discord.Embed(title="UNBLACKLIST", description="<@"+str(user.id) + "> a été unblackliste", color=emcolor)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Vous n'êtes pas whitelist !")


#create / delete
@bot.command()
async def create(ctx, channel_name):
    auteur = ctx.message.author.id
    if auteur in whitelist:
        serv = ctx.guild
        await serv.create_text_channel(channel_name)
        await ctx.send("Channel créer !")
    else:
        await ctx.send("Vous n'êtes pas whitelist !")

@bot.command()
async def delete(ctx):
    auteur = ctx.message.author.id
    if auteur in whitelist:
        channel = ctx.channel
        await channel.delete()
    else:
        await ctx.send("Vous n'êtes pas whitelist !")


#renwe
@bot.command()
async def renew(ctx):
    auteur = ctx.message.author.id
    if auteur in whitelist:
        guild = ctx.guild
        channel = ctx.channel
        category = ctx.channel.category
        await ctx.channel.delete()
        role = discord.utils.get(ctx.guild.roles, name="💬")
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            role: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)
    }   
        await guild.create_text_channel(channel.name, overwrites=overwrites, category=category, reason=None)
    else:
        await ctx.send("Vous n'êtes pas whitelist !")


#nick
@bot.command()
async def rename(ctx, member: discord.Member, nick):
    auteur = ctx.message.author.id
    if auteur in whitelist:    
        await member.edit(nick=nick)
        await ctx.send(f'Nom de {member.mention} changer !')
    else:
        await ctx.send("Vous n'êtes pas whitelist !")

#lookup
@bot.command()
async def lookup(ctx, member: discord.Member):
    auteur = ctx.message.author.id
    if auteur in whitelist:
        embed = discord.Embed(title="LOOKUP", description=f"{member.mention}\n Bot : {member.bot}\n Pseudo : {member}\n ID:{member.id}\n Date de création du compte : {member.created_at}\n Rejoin le : {member.joined_at}\n Role le plus haut : {member.top_role}\n", color=emcolor)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Vous n'êtes pas whitelist !")


@bot.command()
async def addrole(ctx, user: discord.Member, role: discord.Role):
    auteur = ctx.message.author.id
    if auteur in whitelist:
        await user.add_roles(role)
        await ctx.send("Le role "+str(role)+" a bien été ajouter a "+str(user)+" !")
    else:
        await ctx.send("Vous n'êtes pas whitelist !")


@bot.command()
async def remrole(ctx, user: discord.Member, role: discord.Role):
    auteur = ctx.message.author.id
    if auteur in whitelist:
        await user.remove_roles(role)
        await ctx.send("Le role "+str(role)+" a bien été retiré a "+str(user)+" !")
    else:
        await ctx.send("Vous n'êtes pas whitelist !")


dyna = None

@bot.event
async def on_message_delete(message):
    global dyna
    dyna = discord.Embed(title="SNIPE", description=f"Auteur: {message.author.name}\nMessage supprimé: {message.content}", color=emcolor)
    guild = message.guild
    channel = discord.utils.get(guild.channels, name="📁・logs-message")
    embed = discord.Embed(title="LOGS-MESSAGE", description=f"Message supprimé: {message.content}\nPar {message.author.name}\nDate: {message.created_at}", color=emcolor)
    await channel.send(embed=embed)

@bot.command()
async def snipe(ctx):
    await ctx.send(embed=dyna)

@bot.command()
async def rg(ctx):
    auteur = ctx.message.author.id
    if auteur in whitelist:
        await ctx.message.delete()
        await ctx.send("Merci de respecter les T.OS de discord\n\nhttps://discord.com/terms\nhttps://discord.com/guidelines\n\n@everyone")
    else:
        await ctx.send("Vous n'êtes pas whitelist !")
        

@bot.command()
async def version(ctx):
    auteur = ctx.message.author.id
    if auteur in whitelist:
        embed = discord.Embed(title="VERSION", description="Version actuelle: 1.0", color=emcolor)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Vous n'êtes pas whitelist !")

@bot.command()
async def massiverole(ctx, role: discord.Role):
    auteur = ctx.message.author.id
    if auteur in whitelist:
        guild = ctx.guild
        for members in guild.members:
            await members.add_roles(role)
            await asyncio.sleep(1)
        embed = discord.Embed(title="MASSIVEROLE", description="Roles ajouté a tous le monde !", color=emcolor)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Vous n'êtes pas whitelist !")

@bot.command()
async def sondage(ctx, *, content: str):
    auteur = ctx.message.author.id
    if auteur in whitelist:
        await ctx.message.delete()
        embed = discord.Embed(title="SONDAGE", description=content, color=emcolor)
        mess = await ctx.send(embed=embed)
        await mess.add_reaction('1️⃣')
        await mess.add_reaction('2️⃣')
    else:
        await ctx.send("Vous n'êtes pas whitelist !")

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title="SERVER-INFO", description=f"**Nom du serveur**\n{guild.name}\n**ID**\n{guild.id}\n\n**Serveur owner**\n {guild.owner}\n**ID**\n{guild.owner_id}\n\n**Nombre de membres**\n{guild.member_count}\n\n**Nombre de boost**\n{guild.premium_subscription_count}\n\n**Nombre de channel text**\n{len(guild.text_channels)}\n\n**Nombre de channel vocale**\n{len(guild.voice_channels)}\n\n**Icone**\n{guild.icon}\n**Baniére**\n{guild.banner}", color=emcolor)
    await ctx.send(embed=embed)

 
#invites
@bot.command()
async def invites(ctx, *, content: str=None):
    auteur = content
    if auteur == None:
        auteur = ctx.message.author.id
    invtotal = 0
    inv = await ctx.guild.invites()
    for invite in inv:
        if str(invite.inviter.id) == str(auteur):
            print(invite.inviter.id)
            invtotal = invtotal + invite.uses
    await ctx.send("<@"+str(auteur)+f"> a {invtotal} invitations !")
  
 
@bot.command()
async def status(ctx, *, content: str=None):
    auteur = ctx.message.author.id
    if auteur in whitelist:
        with open('config.json', 'r+') as f:
            data = json.load(f)
            data['status'] = content
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
            f.close()
            await ctx.send('Nouveau status: '+content)
            os.system("python3 gestion.py")
            quit()
    else:
        await ctx.send("Vous n'êtes pas whitelist !")

@bot.command()
async def mybots(ctx):
    auteur = ctx.message.author.id
    if auteur == 1033476307083853925:
        embed = discord.Embed(title="Vos bots", description="[**Protect**](https://discord.com/api/oauth2/authorize?client_id=1046909749008019526&permissions=8&scope=bot): infini temps restants", color=emcolor)
        await ctx.send(embed=embed)
    if auteur == 1032282861774045304:
        embed = discord.Embed(title="Vos bots", description="[**boTournois**](https://discord.com/api/oauth2/authorize?client_id=1046887856003633192&permissions=8&scope=bot): infini temps restants", color=emcolor)
        await ctx.send(embed=embed)
    if auteur == 985968071351099413:
        embed = discord.Embed(title="Vos bots", description="[**Gestion**](https://discord.com/api/oauth2/authorize?client_id=1046513186238648400&permissions=8&scope=bot): infini temps restants", color=emcolor)
        await ctx.send(embed=embed)
    elif auteur == 992026485407895603:
        embed = discord.Embed(title="Vos bots", description="[**3boT🤖**](https://discord.com/api/oauth2/authorize?client_id=1046370716351737950&permissions=8&scope=bot): infini temps restants", color=emcolor)
        await ctx.send(embed=embed)
    elif auteur == 1032343353569837117:
        embed = discord.Embed(title="Vos bots", description="[**HKBOT**](https://discord.com/api/oauth2/authorize?client_id=1046117885334011924&permissions=8&scope=bot): infini temps restants", color=emcolor)
        await ctx.send(embed=embed) 
    else:
        embed = discord.Embed(title="Vos bots", description="Vous n'avez pas de bot", color=emcolor)
        await ctx.send(embed=embed)

@bot.command()
async def setuplogs(ctx):
    auteur = ctx.message.author.id
    if auteur in whitelist:
        await ctx.send("Logs mit en place !")
        guild = ctx.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            }
        category = await guild.create_category("・logs・", overwrites=overwrites, reason=None)
        await guild.create_text_channel(f"📁・logs-message", overwrites=overwrites, category=category, reason=None)
    else:
        await ctx.send("Vous n'êtes pas whitelist !")

#lookup
@bot.command()
async def pic(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.message.author
        embed = discord.Embed(title="PIC", description=f"{member.mention}", color=emcolor)
        embed.set_image(url=member.avatar)
        await ctx.send(embed=embed)            
    else:
        embed = discord.Embed(title="PIC", description=f"{member.mention}", color=emcolor)
        embed.set_image(url=member.avatar)
        await ctx.send(embed=embed)

bot.run(config['token'])
