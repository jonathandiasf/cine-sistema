import json
import os
from datetime import datetime

class Genero:
    def __init__(self, nome):
        self.nome = nome

class Ator:
    def __init__(self, nome):
        self.nome = nome

class Atuacao:
    def __init__(self, ator, personagem):
        self.ator = ator
        self.personagem = personagem

class Filme:
    def __init__(self, titulo, duracao, classificacao, generos, elenco):
        self.titulo = titulo
        self.duracao = duracao
        self.classificacao = classificacao
        self.generos = generos 
        self.elenco = elenco

class Assento:
    def __init__(self, numero, fileira):
        self.numero = numero
        self.fileira = fileira
        self.disponivel = True
    
    def ocupar(self):
        self.disponivel = False

    def __str__(self):
        return f"{self.fileira}{self.numero}"

class Sessao:
    def __init__(self, id_s, horario, filme, sala, total_assentos=100):
        self.id_s = id_s
        self.horario = horario
        self.filme = filme
        self.sala = sala
        self.encerrada = False
        # Grade de 100 assentos: A-J (1-10)
        fileiras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        self.assentos = [Assento(n, f) for f in fileiras for n in range(1, 11)]

    def estaEncerrada(self):
        agora = datetime.now().strftime("%H:%M")
        return agora >= self.horario or self.encerrada

    def total_disponivel(self):
        return sum(1 for a in self.assentos if a.disponivel)

class Ingresso:
    def __init__(self, cliente, sessao, assento, tipo, forma_pagamento):
        self.cliente = cliente
        self.sessao = sessao
        self.assento = assento
        self.tipo = tipo
        self.forma_pagamento = forma_pagamento
        self.valor = 30.0 if tipo == "inteira" else 15.0

# 2. CONTROLADOR (Control)

class ControladorVenda:
    def __init__(self, sessoes):
        self.sessoes = sessoes
        self.arquivo_banco = "banco_vendas_final.json"
        self.carregar_dados()

    def salvar_dados(self):
        estado = {s.id_s: [str(a) for a in s.assentos if not a.disponivel] for s in self.sessoes}
        with open(self.arquivo_banco, "w", encoding="utf-8") as f:
            json.dump(estado, f, indent=4)

    def carregar_dados(self):
        if os.path.exists(self.arquivo_banco):
            with open(self.arquivo_banco, "r", encoding="utf-8") as f:
                dados = json.load(f)
                for s in self.sessoes:
                    ocupados = dados.get(s.id_s, [])
                    for assento_obj in s.assentos:
                        if str(assento_obj) in ocupados:
                            assento_obj.ocupar()

# 3. FRONTEIRA (Boundary)

class TelaCompra:
    def __init__(self, controlador):
        self.ctrl = controlador

    def imprimir_cupom_fiscal(self, ing):
        """Emissão do Cupom Fiscal Completo"""
        data_emissao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print("\n" + "═"*45)
        print("           CINE-SISTEMA ENTERTAINMENT          ")
        print("         CNPJ: 12.345.678/0001-99              ")
        print("═"*45)
        print(f" EMISSÃO: {data_emissao}")
        print(f" CLIENTE: {ing.cliente.upper()}")
        print("-" * 45)
        print(f" FILME:      {ing.sessao.filme.titulo.upper()}")
        print(f" SALA:       {ing.sessao.sala}")
        print(f" HORÁRIO:    {ing.sessao.horario}")
        print(f" ASSENTO:    {ing.assento}")
        print(f" CATEGORIA:  {ing.tipo.upper()}")
        print(f" FORMA PGTO: {ing.forma_pagamento.upper()}")
        print("-" * 45)
        print(f" VALOR ITEM:                 R$ {ing.valor:>7.2f}")
        print("═"*45)
        print("    Este cupom serve como seu comprovante    ")
        print("          TENHA UM ÓTIMO FILME!              ")
        print("═"*45 + "\n")

    def menu_venda(self):
        print("\n" + "█"*55)
        print("🎬  TOTEM DE AUTOATENDIMENTO - BEM-VINDO  🎬".center(55))
        print("█"*55)
        
        for i, s in enumerate(self.ctrl.sessoes, 1):
            print(f"{i}. {s.filme.titulo.upper()} | {s.horario} | Vagas: {s.total_disponivel()}/100")
        
        try:
            op = int(input("\nSelecione a sessão: ")) - 1
            sessao = self.ctrl.sessoes[op]
            
            if sessao.estaEncerrada():
                print("❌ Erro: Sessão encerrada."); return

            qtd = int(input("Quantidade de ingressos: "))
            if qtd <= 0 or qtd > sessao.total_disponivel():
                print("❌ Quantidade insuficiente."); return

            nome_cli = input("Nome do Cliente: ")
            
            # Escolha da Forma de Pagamento (Fictício)
            print("\n--- FORMAS DE PAGAMENTO ---")
            print("1. Cartão de Crédito/Débito\n2. PIX\n3. Dinheiro")
            p_op = input("Escolha a forma de pagamento: ")
            pagamentos = {"1": "Cartão", "2": "PIX", "3": "Dinheiro"}
            forma_escolhida = pagamentos.get(p_op, "Outros")

            ingressos_lote = []

            for i in range(qtd):
                while True:
                    print(f"\n[Ingresso {i+1}/{qtd}]")
                    # Dica: No seu VS Code, você pode digitar de A1 a J10
                    escolha = input("Assento (A1 a J10): ").upper()
                    assento_obj = next((a for a in sessao.assentos if str(a) == escolha and a.disponivel), None)
                    
                    if assento_obj:
                        tipo = input("Tipo (inteira/meia): ").lower()
                        assento_obj.ocupar()
                        ingressos_lote.append(Ingresso(nome_cli, sessao, assento_obj, tipo, forma_escolhida))
                        break
                    print("⚠️ Assento ocupado ou inválido!")

            # Persistência após o lote
            self.ctrl.salvar_dados()
            
            print(f"\n💰 Processando pagamento via {forma_escolhida}...")
            
            for ing in ingressos_lote:
                self.imprimir_cupom_fiscal(ing)

        except (ValueError, IndexError):
            print("❌ Erro na operação.")

# 4. SETUP COMPLETO (Filmes, Atores e Sessões)

acao, drama, scifi = Genero("Ação"), Genero("Drama"), Genero("Sci-Fi")
cillian, rdj, scarlett = Ator("Cillian Murphy"), Ator("Robert Downey Jr."), Ator("Scarlett Johansson")
florence, tom = Ator("Florence Pugh"), Ator("Tom Holland")

f1 = Filme("Oppenheimer", 180, "16+", [drama], [
    Atuacao(cillian, "J. Robert Oppenheimer"), Atuacao(rdj, "Lewis Strauss"), Atuacao(florence, "Jean Tatlock")
])
f2 = Filme("Vingadores: Ultimato", 181, "12+", [acao, scifi], [
    Atuacao(rdj, "Tony Stark"), Atuacao(scarlett, "Natasha Romanoff"), Atuacao(tom, "Peter Parker")
])
f3 = Filme("Duna: Parte 2", 166, "14+", [scifi, acao], [
    Atuacao(florence, "Princesa Irulan")
])

minhas_sessoes = [
    Sessao("S01", "14:00", f1, "SALA IMAX 01"),
    Sessao("S02", "18:00", f2, "SALA VIP 02"),
    Sessao("S03", "21:30", f3, "SALA 03 STANDARD")
]

if __name__ == "__main__":
    app = TelaCompra(ControladorVenda(minhas_sessoes))
    app.menu_venda()