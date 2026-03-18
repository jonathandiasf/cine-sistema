# 🎬 Cine-Sistema Totem: Gestão de Vendas de Cinema

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Status](https://img.shields.io/badge/status-3%C2%BA%20Per%C3%ADodo%20Engenharia-green)

Este projeto é um simulador de autoatendimento para cinemas, focado na aplicação de conceitos avançados de **Engenharia de Software** e **Programação Orientada a Objetos (POO)**. O sistema permite a gestão de sessões, escolha de múltiplos assentos em tempo real, processamento de pagamentos fictícios e persistência de dados.

## 🚀 Funcionalidades

- **Catálogo Dinâmico:** Exibição de filmes com elenco detalhado (Relacionamento N:N) e gêneros.
- **Mapa de Assentos:** Gestão de 100 assentos por sessão (Fileiras A-J).
- **Venda em Lote:** Permite comprar múltiplos ingressos em uma única transação.
- **Persistência JSON:** As vendas são salvas em um arquivo local, garantindo que os assentos ocupados permaneçam salvos após fechar o programa.
- **Emissão de Cupom:** Geração de ticket detalhado com dados de pagamento e compliance.

## 🏗️ Arquitetura (Padrão BCE)

O sistema segue o padrão **Boundary-Control-Entity**, garantindo uma separação clara de responsabilidades:

1. **Boundary (Fronteira):** `TelaCompra` - Gerencia toda a interface de terminal.
2. **Control (Controle):** `ControladorVenda` - Processa as regras de negócio e persistência.
3. **Entity (Entidade):** `Filme`, `Sessao`, `Assento`, `Ingresso`, `Ator`, `Atuacao`.

## 🛠️ Como Rodar o Projeto

1. Certifique-se de ter o Python 3.10 ou superior instalado.
2. Clone o repositório:
   ```bash
   git clone [https://github.com/jonathandiasf/cine-sistema.git](https://github.com/jonathandiasf/cine-sistema.git)