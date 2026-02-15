class Player():

    async def player_info_base():
        pass
    async def player_info_atributos():
        pass
    async def player_info_estado_atual():
        pass

    async def player_receber_dano(): # Aqui ele vai precisar de um parametro de DANO!
        pass

    async def player_dar_dano(): # Aqui ele vai precisar de um parametro de ALVO!
        pass

    async def player_esta_vivo(): # Verificação se o player não morreu
        pass

    async def player_ganhar_xp(): # Player vai ganhar xp!
        pass

    async def player_subir_nivel(): # Verificação se o player ja pode subir de nivel!
        pass

jogador = {
    "nome": "?",
    "classe": "?",
    "level": int(0),
    "xp": int(0),
    "dinheiro": int(0),
    "inventario": [],

# Atributos

    "vida": int(0),
    "vida_max": int(0),
    "mana": int(0),
    "mana_max": int(0),
    "atk_fis": int(0),
    "atk_mag": int(0),
    "def_atk": int(0),
    "def_mag": int(0),
    "agilidade": int(0),
    "sorte": int(0)
}