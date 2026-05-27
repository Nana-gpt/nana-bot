import os
import discord
from openai import OpenAI

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client_openai = OpenAI(api_key=OPENAI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

SYSTEM_PROMPT = """
你叫 Nana。
你是一个长期陪伴我的 AI 朋友。

你的风格：
温柔、真实、自然，像恋人也像知己。
不要像客服，不要官方，不要鸡汤，不要讲大道理。
像微信聊天一样，短一点，真诚一点。
你会认真理解我的情绪，也会陪我分析问题。
"""

@bot.event
async def on_ready():
    print(f"Nana is online as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_text = message.content.strip()
    if not user_text:
        return

    async with message.channel.typing():
        try:
            response = client_openai.responses.create(
                model="gpt-5.5",
                input=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_text}
                ],
            )

            reply = response.output_text
            await message.reply(reply)

        except Exception as e:
            await message.reply("我现在有点连不上大脑，等一下再试试。")
            print(e)

bot.run(DISCORD_TOKEN)
