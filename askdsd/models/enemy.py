class Enemy():
    def __init__(self, data):

        self.level = data["level"]
        self.vida_max = data["vida"]
        self.vida_atual = self.vida_max
        self.atk_fis = data["atk_fis"]
        self.atk_mag = data["atk_mag"]
        self.def_fis = data["def_fis"]
        self.def_mag = data["def_mag"]
        self.agilidade = data["agilidade"]
        self.drop_xp = data["drop_xp"]
        self.drop_dinheiro = data["drop_dinheiro"]
        self.drop_item = data["drop_item"]

    def Enemy_receber_dano(self, dano_fis): # Aqui ele vai precisar de um parametro de DANO!

        dano_final = int(dano_fis - self.def_fis)

        self.vida_atual -= dano_final
        return dano_final


    def Enemy_dar_dano(): # Aqui ele vai precisar de um parametro de ALVO!
        pass

    def Enemy_esta_vivo(self): # Verificar se inimigo morreu!
        if self.vida_atual <= 0:
            print("Slime morreu!")
