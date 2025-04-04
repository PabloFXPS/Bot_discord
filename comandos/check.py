import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime

class Check(commands.Cog, discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        self.criador = None 
        self.participantes = []
        super().__init__()

    async def atualizar_lista(self, interaction: discord.Interaction, titulo: str):
        embed = discord.Embed(
            title=f"Evento: {titulo}",
            description=f"Criado por: {self.criador.mention}\n"
                        f"📅 Data: {datetime.now().strftime('%d/%m/%Y')}\n"
                        f"🕒 Hora: {datetime.now().strftime('%H:%M')}",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="✅ Participantes", 
            value="\n".join(self.participantes) if self.participantes else "Ninguém participou ainda.", 
            inline=False
        )

        await interaction.message.edit(embed=embed, view=self)

    @discord.ui.button(label="✅ Participou", style=discord.ButtonStyle.green)
    async def participou(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user

        if user.mention not in self.participantes:
            self.participantes.append(user.mention)
            button.label = "❌ Sair" 
            button.style = discord.ButtonStyle.red
        else:
            self.participantes.remove(user.mention)
            button.label = "✅ Participou"  
            button.style = discord.ButtonStyle.green

        await self.atualizar_lista(interaction, interaction.message.embeds[0].title.replace("Evento: ", ""))
        await interaction.response.defer()  # Evita erro de "interação não respondida"

    @app_commands.command(name="checkin", description="Crie sua lista de participação")
    @app_commands.describe(titulo="Título do evento")
    async def criar_evento(self, interaction: discord.Interaction, titulo: str):
        self.criador = interaction.user
        self.participantes = [] 

        embed = discord.Embed(
            title=f"Evento: {titulo}",
            description=f"Criado por: {self.criador.mention}\n"
                        f"📅 Data: {datetime.now().strftime('%d/%m/%Y')}\n"
                        f"🕒 Hora: {datetime.now().strftime('%H:%M')}",
            color=discord.Color.blue()
        )

        embed.add_field(name="✅ Participantes", value="Ninguém participou ainda.", inline=False)

        view = Check(self.bot) 
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Check(bot))
