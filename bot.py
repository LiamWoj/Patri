import os
import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands

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

TRIGGERS = {
    "patri": "EY MAMA MIA",
    "lucht": "MANIPULATIE VAN DE WEER!",
    "wk": "TIJD VOOR HET WK OHHHH WAT SPANNEND!",
    "dujardin": "HEY DUJARDIN!",
}

# --- Event: Reageer op berichten ---
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()
    for word, response in TRIGGERS.items():
        if word in content:
            await message.channel.send(response)
            break

    await bot.process_commands(message)

# --- Voice join voor specifieke gebruiker ---
TARGET_USER_ID = 1097126388236030083  # jouw target user ID
MP3_FILE = "voorbeeld.mp3"  # ✅ bestand moet in je projectmap staan!

@bot.event
async def on_voice_state_update(member, before, after):
    if member.id != TARGET_USER_ID:
        return

    if before.channel is None and after.channel is not None:
        channel = after.channel

        voice_client = discord.utils.get(bot.voice_clients, guild=member.guild)
        if voice_client is None:
            voice_client = await channel.connect()

        print(f"Speelt MP3 af: {MP3_FILE}")

        # ✅ GEEN executable pad meer (werkt op Railway)
        audio_source = discord.FFmpegPCMAudio(MP3_FILE, executable="ffmpeg")

        if not voice_client.is_playing():
            voice_client.play(audio_source)

        while voice_client.is_playing():
            await asyncio.sleep(1)

        await voice_client.disconnect()

# --- Commands ---
@bot.command()
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("Je moet eerst in een voice channel zitten!")
        return

    channel = ctx.author.voice.channel
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice_client is None:
        await channel.connect()
        await ctx.send(f"Joined {channel.name}!")
    else:
        await ctx.send("Ik ben al verbonden in een voice channel!")

@bot.command()
async def leave(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
        await ctx.send("Bye! 👋")
    else:
        await ctx.send("Ik zit nergens in een voice channel.")

# --- Run bot ---
bot.run(TOKEN)

