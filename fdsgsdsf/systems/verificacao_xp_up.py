def verificar_xp_up(jogador):
    subiu_level = False

    while True:
        xp_necessario = jogador["level"] * 10

        if jogador["xp"] < xp_necessario:
            break

        jogador["xp"] -= xp_necessario
        jogador["level"] += 1

        jogador["vida_max"] += 2
        jogador["atk_fisico"] += 1
        jogador["def_fisica"] += 1

        jogador["vida"] = jogador["vida_max"]

        subiu_level = True

    return subiu_level