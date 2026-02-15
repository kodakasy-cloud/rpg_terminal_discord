# 🎮 Aprendendo a Fazer Bot Discord em Python

Um guia completo para iniciantes sobre como criar bots Discord usando Python com a biblioteca `discord.py`.

## 📋 Índice

- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Conceitos Básicos](#conceitos-básicos)
- [Bot Básico](#bot-básico)
- [Comandos](#comandos)
- [Eventos](#eventos)
- [Embeds](#embeds)
- [Banco de Dados](#banco-de-dados)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Recursos Úteis](#recursos-úteis)

## 🔧 Pré-requisitos

Antes de começar, você precisa de:

- **Python 3.8+** instalado ([download aqui](https://www.python.org/downloads/))
- Uma conta no Discord
- Uma conta de desenvolvedor no Discord Developer Portal
- Noções básicas de Python (variáveis, funções, classes)

## 📦 Instalação

### 1. Criar uma Conta de Desenvolvedor

1. Acesse [Discord Developer Portal](https://discord.com/developers/applications)
2. Clique em "New Application" e dê um nome ao seu bot
3. Vá para a aba "Bot" e clique em "Add Bot"
4. Em "TOKEN", clique em "Copy" para copiar seu token (guarde com segurança!)
5. Habilite as "Intents" necessárias (Message Content Intent, etc.)

### 2. Instalar discord.py

```bash
pip install discord.py
```

Ou para instalar com recursos extras:

```bash
pip install discord.py[voice]  # Para suporte a áudio
```

### 3. Adicionar o Bot ao Servidor

1. No Developer Portal, vá para "OAuth2" → "URL Generator"
2. Selecione o escopo `bot`
3. Selecione as permissões necessárias (Send Messages, Read Messages, etc.)
4. Copie a URL gerada e abra no navegador
5. Selecione o servidor e autorize

## 💡 Conceitos Básicos

### O que é um Bot Discord?

Um bot Discord é um programa que se conecta ao Discord e interage com usuários através de:
- **Comandos**: Ativados por prefixo (ex: `!hello`)
- **Eventos**: Acionados por ações (ex: usuário entra no servidor)
- **Reações**: Respostas a mensagens

## 🚀 Bot Básico

### Seu Primeiro Bot

Crie um arquivo `main.py`:

```python
import discord
from discord.ext import commands

# Criar o bot com prefix '!'
bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

@bot.event
async def on_ready():
    """Chamado quando o bot se conecta ao Discord"""
    print(f'{bot.user} conectado ao Discord!')

@bot.command(name='oi')
async def hello(ctx):
    """Comando simples que responde 'Olá!'"""
    await ctx.send(f'Olá {ctx.author.name}!')

# Executar o bot
bot.run('SEU_TOKEN_AQUI')
```

**Importante**: Nunca compartilhe seu token! Use variáveis de ambiente:

```python
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)
```

Crie um arquivo `.env`:

```
DISCORD_TOKEN=seu_token_aqui
```

## 🎯 Comandos

### Tipos de Comandos

#### 1. Comando Simples

```python
@bot.command(name='ping')
async def ping(ctx):
    await ctx.send(f'🏓 Pong! {round(bot.latency * 1000)}ms')
```

#### 2. Comando com Argumentos

```python
@bot.command(name='saudacao')
async def greet(ctx, nome: str):
    await ctx.send(f'Olá {nome}! Bem-vindo ao servidor!')

# Uso: !saudacao João
```

#### 3. Comando com Argumentos Opcionais

```python
@bot.command(name='info')
async def info(ctx, usuario: discord.Member = None):
    if usuario is None:
        usuario = ctx.author
    await ctx.send(f'Usuário: {usuario.name}, ID: {usuario.id}')
```

#### 4. Comando com Múltiplos Argumentos

```python
@bot.command(name='calc')
async def calculate(ctx, operacao: str, a: int, b: int):
    if operacao == '+':
        resultado = a + b
    elif operacao == '-':
        resultado = a - b
    else:
        resultado = 'Operação inválida'
    
    await ctx.send(f'Resultado: {resultado}')

# Uso: !calc + 5 3
```

### Verificações (Checks)

```python
from discord.ext.commands import has_permissions, MissingPermissions

@bot.command(name='kick')
@has_permissions(kick_members=True)
async def kick(ctx, usuario: discord.Member):
    await usuario.kick()
    await ctx.send(f'{usuario.name} foi kickado!')

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send('Você não tem permissão para kickar membros!')
```

## 📡 Eventos

### Eventos Comuns

```python
@bot.event
async def on_ready():
    """Bot conectado"""
    print(f'Bot {bot.user} está online!')

@bot.event
async def on_message(message):
    """Nova mensagem recebida"""
    if message.author == bot.user:
        return
    
    if message.content == 'oi bot':
        await message.channel.send('Oi!')
    
    # Importante: Processar comandos depois
    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    """Novo membro entrou no servidor"""
    canal = discord.utils.get(member.guild.channels, name='bem-vindo')
    if canal:
        await canal.send(f'Bem-vindo ao servidor, {member.mention}!')

@bot.event
async def on_member_remove(member):
    """Membro saiu do servidor"""
    print(f'{member.name} saiu do servidor')

@bot.event
async def on_message_edit(before, after):
    """Mensagem editada"""
    print(f'{before.author} editou uma mensagem')

@bot.event
async def on_reaction_add(reaction, user):
    """Reação adicionada"""
    if user == bot.user:
        return
    print(f'{user} reagiu com {reaction.emoji}')
```

## 🎨 Embeds

Embeds são mensagens formatadas visualmente:

```python
import discord

@bot.command(name='perfil')
async def profile(ctx, usuario: discord.Member = None):
    if usuario is None:
        usuario = ctx.author
    
    embed = discord.Embed(
        title=f'Perfil de {usuario.name}',
        description=f'ID: {usuario.id}',
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name='Status',
        value=str(usuario.status),
        inline=True
    )
    
    embed.add_field(
        name='Criado em',
        value=usuario.created_at.strftime('%d/%m/%Y'),
        inline=True
    )
    
    embed.set_thumbnail(url=usuario.avatar.url)
    embed.set_footer(text=f'Solicitado por {ctx.author.name}')
    
    await ctx.send(embed=embed)
```

### Cores Disponíveis

```python
discord.Color.red()
discord.Color.green()
discord.Color.blue()
discord.Color.yellow()
discord.Color.gold()
discord.Color.purple()
discord.Color.random()
```

## 💾 Banco de Dados

### Usar SQLite (Simples)

```python
import sqlite3

def criar_banco():
    conn = sqlite3.connect('dados.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios
                 (id INTEGER PRIMARY KEY, discord_id INTEGER, nivel INTEGER, xp INTEGER)''')
    conn.commit()
    conn.close()

@bot.command(name='xp')
async def add_xp(ctx, xp: int):
    conn = sqlite3.connect('dados.db')
    c = conn.cursor()
    c.execute('INSERT INTO usuarios VALUES (NULL, ?, ?, ?)', 
              (ctx.author.id, 1, xp))
    conn.commit()
    conn.close()
    await ctx.send(f'Você ganhou {xp} XP!')
```

## 📁 Estrutura do Projeto

Uma boa estrutura para um bot maior:

```
meu_bot/
│
├── main.py              # Arquivo principal
├── .env                 # Variáveis de ambiente
├── requirements.txt     # Dependências
│
├── comandos/
│   ├── __init__.py
│   ├── mod.py          # Comandos de moderação
│   ├── fun.py          # Comandos divertidos
│   └── info.py         # Comandos de informação
│
├── eventos/
│   ├── __init__.py
│   ├── mensagens.py    # Eventos de mensagens
│   └── membros.py      # Eventos de membros
│
├── utils/
│   ├── __init__.py
│   ├── database.py     # Funções de banco de dados
│   └── decorators.py   # Decoradores customizados
│
└── views/              # Componentes interativos (botões, etc)
    ├── __init__.py
    └── botoes.py
```

### Carregando Cogs (Extensões)

`main.py`:
```python
import discord
from discord.ext import commands
import os

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    await load_commands()
    print(f'{bot.user} está online!')

async def load_commands():
    for arquivo in os.listdir('./comandos'):
        if arquivo.endswith('.py') and arquivo != '__init__.py':
            await bot.load_extension(f'comandos.{arquivo[:-3]}')
            print(f'Carregado: {arquivo}')

bot.run('TOKEN')
```

`comandos/mod.py`:
```python
from discord.ext import commands
import discord

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='kick')
    async def kick(self, ctx, usuario: discord.Member):
        await usuario.kick()
        await ctx.send(f'{usuario} foi kickado!')

async def setup(bot):
    await bot.add_cog(Mod(bot))
```

## 📚 Recursos Úteis

### Documentação Oficial
- [discord.py Documentation](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/applications)

### Tutoriais e Comunidades
- [Discord Developer Community](https://discord.gg/discord-developers)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/discord.py)

### Ferramentas Úteis
- **discord.py-stubs**: Autocompletar melhorado
  ```bash
  pip install discord.py-stubs
  ```

- **python-dotenv**: Gerenciar variáveis de ambiente
  ```bash
  pip install python-dotenv
  ```

- **asyncpg**: Banco de dados assíncrono
  ```bash
  pip install asyncpg
  ```

## 🎓 Exemplo Completo: Bot RPG

Veja os exemplos neste repositório na pasta `fdsgsdsf/` para um bot RPG completo com:
- Sistema de combate
- Ranks e experiência
- Exploração
- Embeddings customizados

## ⚠️ Boas Práticas

1. **Sempre use async/await**: Discord.py é assíncrono
2. **Guarde seu token com segurança**: Use `.env` e `.gitignore`
3. **Trate erros**: Use try/except em comandos
4. **Organize com Cogs**: Deixe o código limpo
5. **Use type hints**: Melhore a legibilidade
6. **Documente seu código**: Adicione docstrings

## 🐛 Troubleshooting

### Bot não conecta
- Verifique o token
- Verifique as intents no Developer Portal

### Comando não funciona
- Verifique o prefix
- Verifique se `await bot.process_commands(message)` está no `on_message`

### Erro de permissões
- Verifique se o bot tem as permissões necessárias no servidor
- Verifique a ordem das roles

---

**Boa sorte em sua jornada como desenvolvedor de bots Discord!** 🚀
