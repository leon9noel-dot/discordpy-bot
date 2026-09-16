import os
import asyncio
import discord
from discord.ext import commands
from openai import OpenAI

TOKEN = os.environ["DISCORD_TOKEN"]
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


@bot.event
async def on_ready():
    print(f"Conectado como {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"Comandos sincronizados: {len(synced)}")
    except Exception as e:
        print(f"Error sincronizando comandos: {e}")


@bot.tree.command(name="ping", description="Comprueba si Noel IA está funcionando")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 ¡Pong! Noel IA está online.")


@bot.tree.command(
    name="preguntar",
    description="Habla con Noel IA"
)
async def preguntar(
    interaction: discord.Interaction,
    mensaje: str
):
    await interaction.response.defer()

    if openai_client is None:
        await interaction.followup.send(
            "⚠️ Noel IA está conectado, pero todavía falta configurar la IA."
        )
        return

    try:
        response = await asyncio.to_thread(
            openai_client.responses.create,
            model="gpt-5.6-luna",
            instructions=(
                "Eres Noel IA, un asistente inteligente dentro de Discord. "
                "Responde en español, de forma natural, útil y cercana. "
                "Puedes usar humor cuando encaje, pero no seas excesivo."
            ),
            input=mensaje
        )

        respuesta = response.output_text

        if len(respuesta) > 1900:
            respuesta = respuesta[:1900] + "..."

        await interaction.followup.send(respuesta)

    except Exception as e:
        print(f"Error de OpenAI: {e}")
        await interaction.followup.send(
            "❌ Ha ocurrido un error al hablar con la IA."
        )


bot.run(TOKEN)
