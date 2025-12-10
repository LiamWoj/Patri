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
@bot.event\async def on_ready():
    await tree.sync()
    print(f"Bot is online als {bot.user} en slash commands gesynced!")

# --- Message trigger system ---
@bot.event\async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()
    for word, response in TRIGGERS.items():
        if word in content:
            await message.channel.send(response)
            break

# No bot.process_commands needed for slash commands

# --- Voice join sounds ---
JOIN_SOUNDS = {
    1097126388236030083: "voorbeeld.mp3",
    782316245117960232: "sound2.mp3",
    1008491071061373051: "sound3.mp3",
}

@bot.event\async def on_voice_state_update(member, before, after):
    if member.bot:
        return

    if member.id in JOIN_SOUNDS:
        if before.channel is None and after.channel is not None:
            channel = after.channel
            voice_client = discord.utils.get(bot.voice_clients, guild=member.guild)

            if voice_client is None:
                voice_client = await channel.connect()

            sound = JOIN_SOUNDS[member.id]
            print(f"Speelt MP3 af: {sound}")

            audio = discord.FFmpegPCMAudio(sound, executable="ffmpeg")
            voice_client.play(audio)

            while voice_client.is_playing():
                await asyncio.sleep(1)

            await voice_client.disconnect()

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
    voice_client = interaction.guild.voice_client

    if voice_client is None:
        voice_client = await channel.connect()

    audio = discord.FFmpegPCMAudio("voorbeeld.mp3", executable="ffmpeg")
    voice_client.play(audio)

    await interaction.response.send_message("🎧 *HEY DUJARDIN wordt afgespeeld...*")

@tree.command(name="marco", description="Speel het CIAO MARCO geluid af.")
async def marco(interaction: discord.Interaction):
    if interaction.user.voice is None:
        await interaction.response.send_message("Ga eerst in een voice channel zitten eh kalf!")
        return

    channel = interaction.user.voice.channel
    voice_client = interaction.guild.voice_client

    if voice_client is None:
        voice_client = await channel.connect()

    audio = discord.FFmpegPCMAudio("marco.mp3", executable="ffmpeg")
    voice_client.play(audio)

    await interaction.response.send_message("🎧 *CIAO MARCO wordt afgespeeld...*")

# --- Run bot ---
bot.run(TOKEN)





