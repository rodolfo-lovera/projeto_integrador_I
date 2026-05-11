# Projeto Integrador I - Plano de ação

- Objetivo da disciplina: Desenvolver um software com framework web que utilize noções de banco de dados, praticando controle de versão;
- Ementa: Resolução de problemas; Levantamento de requisitos; Desenvolvimento web com framework; HTML; CSS; Banco de Dados; Controle de Versão. 

## Fase 1: Revisão e Ajustes (O Refinamento)

Olhando para os seus protótipos e para o seu modelo de banco de dados, encontrei um pequeno desalinhamento que podemos corrigir agora para evitar dor de cabeça no futuro:

* **Ajuste no Banco de Dados (A Tabela de Fornecedores):** No seu protótipo da "Tela de Compras Mastigada", existe um filtro importante que mostra os produtos agrupados por fornecedor (ex: "Massa Viva", "Sacolão do Alfase"). No entanto, o seu arquivo `schema.sql` não possui uma tabela `fornecedores` nem uma chave estrangeira na tabela `produtos` ligando o item a quem o fornece.
* *Por que fazer isso:* Se o gestor da sorveteria compra de 3 ou 4 locais diferentes, agrupar a lista de compras por fornecedor é o que realmente vai economizar o tempo dele.


* **Ajuste nos Protótipos (Cadastro):** Para que o filtro de compras funcione, precisaremos adicionar um campo "Fornecedor" no formulário da "Tela de Cadastro de Produtos".

## Fase 2: Configuração do Ambiente e "Hello World"

*O objetivo aqui é preparar o terreno e garantir que as ferramentas conversam entre si.*

* **Ação:** Entrar no GitHub Codespaces (que você definiu no documento), criar o ambiente virtual do Python, instalar o Flask e criar uma rota simples que devolva um texto na tela (ex: "IceWebCream funcionando!").
* **Por que fazer isso:** Evita que a gente tente resolver erros complexos de código quando, na verdade, o problema poderia ser apenas uma biblioteca mal instalada. É a fundação da casa.

## Fase 3: Conexão com o Banco e Dados Fictícios (Seed)

*O objetivo aqui é dar vida ao banco de dados.*

* **Ação:** Fazer o Python ler e executar o seu arquivo `schema.sql`. Depois, vamos criar um pequeno script em Python para inserir ("injetar") categorias, fornecedores e produtos falsos, além de simular algumas entradas e saídas.
* **Por que fazer isso:** Lembra das `triggers` fantásticas que você criou no banco? Precisamos ver elas funcionando na prática. É muito difícil construir telas HTML (frontend) sem ter dados visíveis para testar se as tabelas e os gráficos estão renderizando corretamente.

## Fase 4: Construção do Sistema em "Fatias" (O Desenvolvimento)

*O objetivo aqui é programar uma funcionalidade inteira (do banco até a tela) antes de passar para a próxima.*

1. **Fatia 1 - Cadastro e Listagem:** Vamos criar a tela de "Cadastro de Produtos" e fazer o botão "Salvar" gravar no banco. Depois, faremos uma lista simples para exibir o que foi cadastrado.
2. **Fatia 2 - O Coração (Movimentações):** Vamos criar a tela de "Contagem de Terça-feira". Aqui você vai ver a mágica do backend pegando a quantidade digitada e enviando para o banco, disparando as suas `triggers`.
3. **Fatia 3 - Inteligência (Visão do Dono e Compras):** Como o banco já estará calculando o estoque atual, vamos construir as telas que apenas "lêem" esses dados. Faremos a lógica de comparar o `estoque atual` com o `estoque minimo` para gerar os cards de "Itens em alerta".

## Fase 5: Testes e Validação

* **Ação:** Colocar o sistema (mesmo que rústico) na mão do gestor da sorveteria TISHI para que ele tente fazer uma contagem real de estoque.
* **Por que fazer isso:** O Design Science Research (DSR) exige que a gente teste o artefato no mundo real. Ele vai nos dizer se o botão está muito escondido ou se a lógica de compras faz sentido na prática dele.

