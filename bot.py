import discord
from discord.ext import commands
import yt_dlp
from dotenv import load_dotenv
import os

intents = discord.Intents.all()
intents.voice_states = True
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

song_queue = []

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

@bot.command()
async def play(ctx, *, query):
    voice_state = ctx.author.voice
    if voice_state is None or voice_state.channel is None:
        await ctx.send('You must be in a voice channel to use this command.')
        return

    voice_channel = voice_state.channel
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice_client and voice_client.is_connected():
        if voice_client.channel == voice_channel:
            await ctx.send('I am already in your voice channel.')
        else:
            await ctx.send('I am already in a voice channel. Please use the `stop` command to make me leave.')
        return

    print(f'{ctx.author.name} initiated the play command')

    if 'youtube.com' in query or 'youtu.be' in query:
        await play_song(ctx, voice_channel, query)
    else:
        await search_and_play(ctx, voice_channel, query)

async def search_and_play(ctx, voice_channel, query):
    await ctx.send(f'Searching for: {query}')
    search_query = f'ytsearch:{query}'

    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(search_query, download=False)

        if 'entries' in info:
            entries = info['entries']
            if entries:
                first_entry = entries[0]
                url = first_entry['webpage_url']
                await play_song(ctx, voice_channel, url)
            else:
                await ctx.send('No search results found.')
        else:
            await ctx.send('No search results found.')

async def play_song(ctx, voice_channel, url):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_connected():
        await voice_client.move_to(voice_channel)
    else:
        voice_client = await voice_channel.connect()

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': 'C:/ffmpeg-2023-07-10-git-1c61c24f5f-full_build/bin/ffmpeg.exe',  # Specify the path to your FFmpeg executable
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        song_url = info["url"]
        song_title = info["title"]

    song = {
        'url': song_url,
        'title': song_title,
        'requester': ctx.author.name
    }

    song_queue.append(song)
    await ctx.send(f'Song **{song_title}** added to the queue.')

    if not voice_client.is_playing():
        await play_next_song(ctx, voice_client)

async def play_next_song(ctx, voice_client):
    if len(song_queue) > 0:
        song = song_queue[0]
        voice_client.play(discord.FFmpegPCMAudio(song['url']), after=lambda e: bot.loop.create_task(play_next_song(ctx, voice_client)))
        embed = discord.Embed(title='Now playing', description=f'[{song["title"]}]({song["url"]})', color=discord.Color.blurple())
        embed.set_footer(text=f'Requested by {song["requester"]}')
        await ctx.send(embed=embed)
        song_queue.pop(0)
    else:
        await voice_client.disconnect()

@bot.command()
async def stop(ctx):
    voice_client = ctx.voice_client
    if voice_client and voice_client.is_playing():
        voice_client.stop()
    song_queue.clear()
    await voice_client.disconnect()

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f'An error occurred: {str(error)}')

bot.run(os.getenv('BOT_TOKEN'))
