# 🏗️ Documentação de Arquitetura: Padrão BCE

Este projeto foi estruturado seguindo o padrão de projeto **BCE (Boundary, Control, Entity)**, também conhecido como **Boundary-Control-Entity**. Esta arquitetura foca na separação de responsabilidades, facilitando a manutenção e a escalabilidade do sistema.

## 1. Camada de Entidade (Entity)
As entidades representam os objetos de domínio do sistema e contêm os dados e regras de negócio básicas. São objetos que possuem uma identidade e persistem no tempo.

* **`Filme`**: Contém metadados como título, duração, classificação e a lista de gêneros/atores.
* **`Ator` / `Atuacao`**: Representam o elenco e a relação N:N (Muitos para Muitos).
* **`Sessao`**: Agrega os 100 objetos `Assento` e gere a disponibilidade de horário.
* **`Assento`**: A menor unidade da sala, responsável por controlar o seu próprio estado (disponível ou ocupado).
* **`Ingresso`**: O registo final da transação, unindo cliente, assento e forma de pagamento.

## 2. Camada de Controlo (Control)
O controlador atua como o "cérebro" do sistema. Ele faz a ponte entre a interface e os dados, processando a lógica complexa sem interagir diretamente com o utilizador.

* **`ControladorVenda`**: 
    * Gere o fluxo de persistência (leitura e escrita no ficheiro JSON).
    * Valida a integridade dos dados (ex: verificar se um assento já foi ocupado antes de salvar).
    * Coordena a criação de novos ingressos em lote.

## 3. Camada de Fronteira (Boundary)
A fronteira é o ponto de contacto entre o sistema e o mundo exterior (neste caso, o utilizador através do terminal).

* **`TelaCompra`**: 
    * Exibe o catálogo e as mensagens de erro.
    * Recolhe os inputs do utilizador (sessão, quantidade, escolha de assentos).
    * Formata e emite o **Cupom Fiscal**, apresentando os dados processados pelo controlador de forma legível.

## 🔄 Fluxo de Mensagens (Diagrama de Sequência)

1.  **Usuário** solicita a compra à **Fronteira** (`TelaCompra`).
2.  A **Fronteira** consulta o **Controlo** (`ControladorVenda`) para saber as sessões disponíveis.
3.  O **Controlo** acede às **Entidades** (`Sessao` e `Assento`) para validar a disponibilidade.
4.  Após a escolha, o **Controlo** atualiza o estado das **Entidades** e persiste os dados.
5.  A **Fronteira** recebe a confirmação e gera o ticket para o **Usuário**.

---
*Documentação gerada para o projeto de Engenharia de Software - 3º Período.*