import os
import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import app_commands

# --- Load token ---
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN is None:
    raise ValueError("Discord token niet gevonden! Zet DISCORD_TOKEN in Railway Variables.")

# --- Bot setup ---
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# --- Jouw server voor instant sync ---
MY_GUILD_ID = 1444812723916374160  # <- VERVANG DIT MET JOUW SERVER ID
MY_GUILD = discord.Object(id=MY_GUILD_ID)

# --- Triggers ---
TRIGGERS = {
    "patri": "EY ik ben ufoloog en profesioneel siciliaanse kok EN IK HAAT JEROEN MEUS",
    "lucht": "MANIPULATIE VAN DE WEER!",
    "wk": "TIJD VOOR HET WK OHHHH WAT SPANNEND!",
    "dujardin": "HEY DUJARDIN!",
    "brraaa": "EY!",
    "jeroen": "JEROEN MEUS VERNEUKT DE ITALIAANSE KEUKEN DIE VUILE SMEERLAP",
    "jorrit": "JO JO JO JORIT DOM JORIT DOM DOM",
    "nigga": "NEGERS????!!!!!!",
    "max": "Max verstappen is de goat",
}

# --- Ready event ---
@bot.event
async def on_ready():
    # Direct voor jouw server (instant)
    await tree.sync(guild=MY_GUILD)
    # Globaal voor andere servers (kan 5–60 min duren)
    await tree.sync()
    print(f"Bot is online als {bot.user} en slash commands gesynced!")

# --- Message trigger system ---
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()
    for word, response in TRIGGERS.items():
        if word in content:
            await message.channel.send(response)
            break

# --- Voice join sounds ---
JOIN_SOUNDS = {
    1097126388236030083: "voorbeeld.mp3",
    782316245117960232: "sound2.mp3",
    1008491071061373051: "sound3.mp3",
}

async def play_sound_and_disconnect(channel, sound):
    voice_client = discord.utils.get(bot.voice_clients, guild=channel.guild)
    if voice_client is None:
        voice_client = await channel.connect()

    audio = discord.FFmpegPCMAudio(sound, executable="ffmpeg")
    voice_client.play(audio)

    while voice_client.is_playing():
        await asyncio.sleep(1)

    await voice_client.disconnect()

@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return

    if member.id in JOIN_SOUNDS:
        if before.channel is None and after.channel is not None:
            sound = JOIN_SOUNDS[member.id]
            print(f"Speelt MP3 af: {sound}")
            await play_sound_and_disconnect(after.channel, sound)

# --- Slash commands ---
@tree.command(name="join", description="Laat de bot jouw voice channel joinen.")
async def join(interaction: discord.Interaction):
    if interaction.user.voice is None:
        await interaction.response.send_message("Je moet eerst in een voice channel zitten gij kalf!")
        return

    channel = interaction.user.voice.channel
    voice_client = discord.utils.get(bot.voice_clients, guild=interaction.guild)

    if voice_client is None:
        await channel.connect()
        await interaction.response.send_message(f"Joined {channel.name}!")
    else:
        await interaction.response.send_message("Ik ben al verbonden in een voice channel eh kalf!")

@tree.command(name="leave", description="Laat de bot de voice channel verlaten.")
async def leave(interaction: discord.Interaction):
    if interaction.guild.voice_client is not None:
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("CIAO CIAO ")
    else:
        await interaction.response.send_message("Ik zit nergens in een voice channel eh kalf.")

@tree.command(name="dujardin", description="Speel het HEY DUJARDIN geluid af.")
async def dujardin(interaction: discord.Interaction):
    if interaction.user.voice is None:
        await interaction.response.send_message("Ga eerst in een voice channel zitten!")
        return

    channel = interaction.user.voice.channel
    await play_sound_and_disconnect(channel, "voorbeeld.mp3")
    await interaction.response.send_message("🎧 *HEY DUJARDIN wordt afgespeeld...*")

@tree.command(name="marco", description="Speel het CIAO MARCO geluid af.")
async def marco(interaction: discord.Interaction):
    if interaction.user.voice is None:
        await interaction.response.send_message("Ga eerst in een voice channel zitten eh kalf!")
        return

    channel = interaction.user.voice.channel
    await play_sound_and_disconnect(channel, "marco.mp3")
    await interaction.response.send_message("🎧 *CIAO MARCO wordt afgespeeld...*")

# --- De rest van de slash commands blijven exact hetzelfde ---
@tree.command(name="triggerlist", description="Toon alle woorden die triggers hebben.")
async def triggerlist(interaction: discord.Interaction):
    lijst = "\n".join(f"**{t}** → {r}" for t, r in TRIGGERS.items())
    await interaction.response.send_message(f"📜 **Triggerlijst:**\n{lijst}")

@tree.command(name="scheld", description="Laat de bot iemand uitschelden.")
async def scheld(interaction: discord.Interaction, user: discord.Member):
    scheldwoorden = [
        "gij dom varken",
        "gij achterlijke pangolin",
        "gij kunt nog geen ei bakken zonder Jeroen Meus te bellen",
        "ge zijt trager dan een Airfryer van Action",
        "ik hoop dat ge stikt in een gehaktbal", 
        "ik maak pizza van u gij achterlijke negerin die ge zijt"
    ]
    import random
    await interaction.response.send_message(f"{user.mention} {random.choice(scheldwoorden)}")

@tree.command(name="ufo", description="UFO alert!!!!!")
async def ufo(interaction: discord.Interaction):
    await interaction.response.send_message("🛸 *IK ZIE LICHTEN AAN DE HEMEL — DIT IS GEEN VOGEL DIT IS GEEN VLIEGTUIG — DIT IS ABSOLUTE MANIPULATIE VAN DE WEER!!!*")

@tree.command(name="8ball", description="Stel een vraag aan patri die de toekomst kan zien.")
async def eightball(interaction: discord.Interaction, vraag: str):
    antwoorden = ["Ja.", "Nee.", "Misschien.", "Vraag het later nog eens.", "Bro… nee.", "Zeer waarschijnlijk."]
    import random
    await interaction.response.send_message(random.choice(antwoorden))

@tree.command(name="kook", description="De bot kookt een gerecht op Siciliaanse wijze.")
async def kook(interaction: discord.Interaction):
    lines = [
        "Ik ben spaghetti aan het maken, GEEN ROOM GEBRUIKEN EH!",
        "Mamma mia wat een misbaksel van een keuken hier.",
        "Wie heeft hier weer de pasta kapot gekookt? 8 minuten MAXIMUM!"
    ]
    import random
    await interaction.response.send_message(random.choice(lines))

@tree.command(name="rant", description="Laat de bot volledig flippen.")
async def rant(interaction: discord.Interaction):
    rant = (
        "IK ZEG HET U — DE WEERKAARTEN WORDEN GECONTROLEERD DOOR MIDDEL VAN DE EIFELTOREN VAN JAPAN JOH! "
        "DE ITALIAANSE KEUKEN WORDT AANGEVALLEN! "
        "EN JEROEN MEUS IS DAAR DE LEIDER VAN!!!"
    )
    await interaction.response.send_message(rant)

@tree.command(name="sus", description="Beschuldig iemand van SUS gedrag.")
async def sus(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.send_message(f"🚨 {user.mention} gedraagt zich *verdacht*. Ik hou u in het oog. Gij vieze sussy baka")

@tree.command(name="hack", description="Laat patri iemand hacken door middel van zijn spaghetti computer")
async def hack(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.send_message(f"💻 Hacking {user.name}...\n0% [..........]")
    await asyncio.sleep(1)
    await interaction.followup.send("35% [###.......]")
    await asyncio.sleep(1)
    await interaction.followup.send("79% [#######...]")
    await asyncio.sleep(1)
    await interaction.followup.send("100% [##########] ✔\n**Resultaat:** gebruiker is een achterlijke neger joh ga terug naar uw eigen land!")

@tree.command(name="quote", description="Krijg een inspirerende quote.")
async def quote(interaction: discord.Interaction):
    quotes = [
        "Doe eens niet.",
        "Het leven is te kort voor slechte pasta.",
        "Hou uw bek en geniet van de dag.",
        "Iedereen heeft een brein. Niet iedereen gebruikt het (he Dujardin)"
    ]
    import random
    await interaction.response.send_message(random.choice(quotes))

# --- Run bot ---
bot.run(TOKEN)


