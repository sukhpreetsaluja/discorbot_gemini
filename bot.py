import discord
from discord.ext import commands
import credentials as c
import google.generativeai as genai


bot = discord.Bot()

genai.configure(api_key=c.GEMINI_API)
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 16384,
  "response_mime_type": "text/plain",
}
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
]

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash-latest",
  safety_settings=safety_settings,
  generation_config=generation_config,
)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(
        name='This Server', url='https://www.twitch.tv/sukhpreetsaluja'))
    print("Bot is Ready")


@bot.slash_command(name = "ai", description = "Get Response from AI")
async def ai(ctx, prompt: discord.Option(str)):
    await ctx.defer()
    try:
        response = model.generate_content(prompt)
        if len(response.text) > 1800:
            with open("ai_response.txt", "w") as n:
                n.write(response.text)
            file = discord.File("ai_response.txt")
            await ctx.followup.send("Response is Greater than 2000 Characters, So I uploaded it as a text file instead!\nNote: Response is Limited to 13000 Characters!", file=file)
        else:
            await ctx.followup.send(f"{response.text}")
    except Exception as e:
        await ctx.followup.send(f"Due to Error Reponse was not Generated\nError Occured: `{e}`")

bot.run(c.FINAL_TOKEN)