import discord
import asyncio
import random
import os
from flask import Flask
from keep_alive import keep_alive
from settings import (
    is_prize_value_above_threshold,
    is_pool_value_above_threshold,
    is_pool_value_above_threshold_1,
    is_enters_value_at_most_4,
    is_pool_per_enters_above_threshold,
    extract_text_between_parentheses,
    is_pool_per_enters_worth_risk,
    is_prize_value_above_1
)

emoji_options = ['❤', '💙', '🚀', '🔥']

responses = [
    "thx",
    "ty",
    "thanks",
    "thank you",
    "lfg",
    "tysm",
    "thankss",
]

keep_alive()

# Flask setup
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

# Discord client setup
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

client = MyClient()

# Event: Message received
@client.event
async def on_message(message):
    if message.author.id == 1150448986264698980 and message.guild.id != 1102183639791452242 and message.guild.id != 1222623160734580736:
        print("Message from bot.")

        # Processing raffle ended messages
        for embed in message.embeds:
            if client.user.mentioned_in(message) and embed and embed.description and "Raffle ended" in embed.description:
                response = random.choice(responses)
                extracted_text = extract_text_between_parentheses(embed.description)

                if extracted_text:
                    print(f"Extracted text: {extracted_text}")

                await asyncio.sleep(random.randint(2, 4))
                async with message.channel.typing():
                    await asyncio.sleep(random.randint(2, 4))
                    await message.channel.send(response)

                try:
                    random_emoji = random.choice(emoji_options)
                    await asyncio.sleep(random.randint(5, 8))
                    await message.add_reaction(random_emoji)
                except Exception as e:
                    print(f"Failed to add reaction: {e}")

                # Example of sending to another channel
                channel_id = 1252625826109722664
                channel = client.get_channel(channel_id)

                if channel and extracted_text:
                    await asyncio.sleep(random.randint(2, 5))
                    await channel.send(f"<@740547277164249089> hmdlh rb7t {extracted_text}")

            elif client.user.mentioned_in(message) and "Airdrop collected" in embed.description:
                response = random.choice(responses)
                extracted_text = extract_text_between_parentheses(embed.description)

                if extracted_text:
                    print(f"Extracted text: {extracted_text}")

                channel_id = 1252731072081428500
                channel = client.get_channel(channel_id)

                if channel and extracted_text:
                    async with channel.typing():
                        await asyncio.sleep(random.randint(3, 7))
                        await channel.send(f"dit {extracted_text} f airdrop")

        # Example of handling different conditions for entering raffles or airdrops
        for embed in message.embeds:
            if  embed and embed.description and "Raffle created" in embed.description:
                if is_prize_value_above_1(embed.fields):
                    for component in message.components:
                        for child in component.children:
                            if child.label == "Enter":
            #                   await asyncio.sleep(random.randint(2, 4))
                                await child.click()
                elif is_prize_value_above_threshold(embed.fields):
                    for component in message.components:
                        for child in component.children:
                            if child.label == "Enter":
                                await asyncio.sleep(random.randint(3, 6))
                                await child.click()
            elif embed and embed.description and "Airdrop created" in embed.description:
                if is_pool_per_enters_worth_risk(embed.fields):
                    for component in message.components:
                        for child in component.children:
                            if child.label == "Enter":
                #               await asyncio.sleep(random.randint(3, 6))
                                await child.click()
                elif is_pool_value_above_threshold(embed.fields):
                    for component in message.components:
                        for child in component.children:
                            if child.label == "Enter":
                                await asyncio.sleep(random.randint(3, 6))
                                await child.click()
                elif is_pool_value_above_threshold_1(embed.fields) and is_enters_value_at_most_4(embed.fields):
                    for component in message.components:
                        for child in component.children:
                            if child.label == "Enter":
                                await child.click()
                                await asyncio.sleep(random.randint(5, 10))
                                async with message.channel.typing():
                                    await asyncio.sleep(random.randint(3, 6))
                                    await message.channel.send(response)
                elif is_pool_per_enters_above_threshold(embed.fields):
                    for component in message.components:
                        for child in component.children:
                            if child.label == "Enter":
                                await asyncio.sleep(random.randint(10, 30))
                                await child.click()
                else:
                    print("Conditions not met for any action, skipping")

# Run the client
if __name__ == "__main__":
    client.run(os.environ['TOKEN'])
