# Especificações do Projeto

<span style="color:red">Pré-requisitos: <a href="1-Documentação de Contexto.md"> Documentação de Contexto</a></span>

# Personas

*Persona 1 – Lucas Alves*

Idade: 18 anos
Profissão: Estudante Universitário
Localização: Belo Horizonte – MG
Formação: Ensino Superior em andamento
Objetivo: Iniciar em um projeto de pesquisa

Descrição:
Estudante do primeiro período de Engenharia de Computação, 18 anos. É proativo e possui grande interesse em participar da vida acadêmica, mas sente-se desorientado pela falta de um ponto de partida claro e de uma rede de contatos na universidade.

Dores:
A informação sobre projetos é pulverizada em diversos canais, tornando o acompanhamento difícil e ineficiente. Além disso, sente-se inseguro para abordar professores diretamente sem um processo formal.

Expectativas:
Encontrar uma plataforma única que centralize todas as oportunidades e ter acesso a projetos com baixa barreira de entrada, ideais para uma primeira experiência.


*Persona 2 – Juliana Costa*

Idade: 26 anos
Profissão: Estudante Universitária
Localização: São Paulo – SP
Formação: Ensino Superior em andamento
Objetivo: Primeira experiência acadêmica apra enriquecer seu currículo em uma iniciação científica.

Descrição:
Aluna do sétimo período de Relações Internacionais, 26 anos. Está focada em sua carreira e busca uma experiência de pesquisa de alto impacto para enriquecer seu currículo para uma futura pós-graduação.

Dores:
Perde muito tempo filtrando oportunidades irrelevantes para seus objetivos específicos e acha frequentemente vagas interessantes sem uma descrição, impedindo uma avaliação clara do escopo do trabalho.

Expectativas: Utilizar filtros de busca avançados para encontrar rapidamente vagas em sua área de nicho e acessar informações detalhadas sobre pré-requisitos, atividades e resultados esperados.

*Persona 3 – Profª. Drª. Helena Medeiros (Docente Pesquisadora Estabelecida)*

Idade: 48 anos
Profissão: Professora e Pesquisadora Universitária
Localização: Rio de Janeiro – RJ
Formação: Pós-doutorado completo
Objetivo: Recrutar estudantes empenhados a produzir materiais para pesquisas e que buscam seguir a carreira acadêmica.

Descrição:
Pesquisadora do Departamento de Biologia e professora adjunta, 48 anos. Coordena um laboratório com múltiplos projetos e considera o recrutamento de alunos um ônus administrativo que consome tempo de pesquisa.

Dores:
O processo de divulgação de vagas é burocrático e atinge um público limitado. 
Recebe um volume elevado de candidaturas de alunos que não possuem o perfil técnico necessário.

Expectativas:
Ter um canal único e eficiente para divulgar suas vagas para toda a universidade.
Receber candidaturas mais qualificadas através de pré-requisitos claros.

*Persona 4 – Prof. Dr. Ricardo Barros (Docente em Início de Carreira)*

Idade: 34 anos
Profissão: Professor e Pesquisador Universitário
Localização: Manaus – AM 
Formação: Pós-graduação concluída
Objetivo: Divulgar para estudantes seu projeto de extensão

Descrição:
Professor recém-contratado do Departamento de Letras, 34 anos. Está motivado para iniciar seu primeiro projeto de extensão, mas não possui uma rede de contatos com os estudantes e teme que seu projeto não tenha visibilidade.

Dores:
Insegurança sobre quais os canais mais eficazes e seguros para divulgar seu novo projeto.
Receio de não receber um número suficiente de candidatos qualificados.

Expectativas:
Uma plataforma que dê visibilidade igualitária a todos os projetos, novos ou antigos.
Alcançar um público amplo e interdisciplinar de estudantes que possam se interessar pelo seu tema.

*Persona 5 – Drª. Carolina Lima (Pesquisadora Focada em Segurança)*

Idade: 32 anos
Profissão: Pesquisadora
Localização: Pernambuco - PE
Formação: Pós-doutorado em andamento
Objetivo: Utilização de um ambiente profissional seguro e formal desde o primeiro contato

Descrição:
Drª. Carolina Lima, 32 anos, é uma pesquisadora de pós-doutorado no Instituto de Química. Recentemente, conseguiu financiamento para seu primeiro projeto de iniciação científica e busca recrutar uma aluna ou aluno. Como uma mulher jovem em uma posição de liderança acadêmica, ela se preocupa com a dinâmica de poder e preza pela criação de um ambiente profissional seguro e formal desde o primeiro contato.

Dores:
Exposição e Vulnerabilidade: Sente-se desconfortável em divulgar seu e-mail e contato pessoal em canais públicos ou listas de e-mail departamentais, temendo receber contatos inadequados, spam ou até mesmo assédio. Quer evitar comunicações fora de hora ou por canais não profissionais (como redes sociais pessoais), mantendo todas as interações dentro de um contexto estritamente acadêmico.

Expectativas:
Ambiente Controlado e Verificado, espera uma plataforma de acesso restrito à comunidade acadêmica (com login institucional), garantindo que todos os usuários são estudantes verificados. 
Deseja que a comunicação inicial ocorra dentro da plataforma, protegendo suas informações de contato direto até que ela se sinta segura para compartilhar.

# Histórias de Usuários

Com base na análise das personas, foram identificadas as seguintes histórias de usuários. Elas foram organizadas por contexto, de forma a facilitar a compreensão dos requisitos funcionais e não funcionais relacionados à aplicação.

## Cadastro e Divulgação de Docentes e Funcionários Universitários

| EU COMO... `PERSONA` | QUERO/PRECISO ... `FUNCIONALIDADE`                            | PARA ... `MOTIVO/VALOR`                                          |
| -------------------- | ------------------------------------------------------------- | ---------------------------------------------------------------- |
| Drª. Carolina Lima (Pesquisadora Focada em Segurança) | preciso de um sistema de mensagens interno na plataforma para o contato inicial com candidatos             | para proteger minhas informações pessoais (e-mail, telefone) e evitar comunicações inadequadas       |
| Drª. Carolina Lima (Pesquisadora Focada em Segurança) | preciso que a plataforma exija autenticação via login institucional |para garantir que estou interagindo apenas com estudantes verificados da comunidade acadêmica     |
| Profª. Drª. Helena Medeiros (Docente Pesquisadora) | preciso de um formulário simples e rápido para publicar novas vagas                     | para reduzir o tempo gasto com burocracia e focar na minha pesquisa  |
| Profª. Drª. Helena Medeiros (Docente Pesquisadora) | preciso definir pré-requisitos obrigatórios (como curso, período ou habilidades) no anúncio da vaga |  para que o sistema filtre automaticamente os candidatos que não atendem aos critérios mínimos |
| Prof. Dr. Ricardo Barros (Docente em Início de Carreira) |  preciso que minha vaga tenha a mesma visibilidade que os projetos de pesquisadores já estabelecidos  | para garantir uma competição justa por talentos e dar um bom início ao meu projeto de extensão  |
| Prof. Dr. Ricardo Barros (Docente em Início de Carreira) | preciso que a plataforma permita a divulgação para estudantes de diferentes cursos | para alcançar um público amplo e interdisciplinar que possa se interessar pelo tema |


## Busca e Cadastro de Alunos Universitários

| EU COMO... `PERSONA`               | QUERO/PRECISO ... `FUNCIONALIDADE`                                    | PARA ... `MOTIVO/VALOR`                                            |
| ---------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------ |
| Lucas Alves (Estudante 1º período) | preciso visualizar todas as oportunidades de pesquisa em um único lugar | para não perder nenhuma vaga e economizar tempo de busca em vários canais |
| Lucas Alves (Estudante 1º período) | preciso de um filtro ou uma tag para projetos que aceitam iniciantes   | para encontrar vagas compatíveis com meu nível de conhecimento e aumentar minhas chances de ser selecionado.  |
| Clara (Consumidora de baixa renda) | Receber apenas ofertas ainda válidas                                  | Garantir que os alimentos estejam próprios para consumo            |
| João (Consumidor consciente)       | Pesquisar e filtrar produtos por nome ou categoria                    | Localizar rapidamente itens que desejo comprar                     |
| João (Consumidor consciente)       | Acessar informações completas da empresa (nome, endereço, avaliações) | Garantir que compro de feirantes confiáveis e sustentáveis         |
| João (Consumidor consciente)       | Avaliar feirantes com notas e comentários                             | Ajudar a comunidade e incentivar boas práticas                     |
| Luana (Estudante universitária)    | Navegar no feed de ofertas pelo celular                               | Conciliar minha rotina corrida com hábitos de alimentação saudável |
| Luana (Estudante universitária)    | Ter carregamento rápido nas páginas (≤2s)                             | Não perder tempo durante o uso da aplicação                        |
| Luana (Estudante universitária)    | Ver data/hora de criação das ofertas                                  | Confiar que as informações estão atualizadas e corretas            |


# Requisitos

As tabelas que se seguem apresentam os requisitos funcionais e não funcionais que detalham o escopo do projeto.

### Requisitos Funcionais

|ID    | Descrição do Requisito  | Prioridade |
|------|-------------------------|----|
|RF-001| A aplicação deve permitir o **cadastro de pessoa** (nome, e-mail, senha, endereço completo: logradouro, número, bairro, cidade, UF, CEP). | ALTA |
|RF-002| A aplicação deve permitir a **autenticação** do usuário (login/logout) | ALTA |
|RF-003| A aplicação deve permitir o **cadastro de empresa/feira** com **CNPJ obrigatório** e **endereço completo** (logradouro, número, bairro, cidade, UF, CEP). | ALTA |
|RF-004| O backend deve **validar o CNPJ** (formato e dígito verificador) no cadastro/edição de empresa. | ALTA |
|RF-005| A aplicação deve permitir que um usuário autenticado se **associe ao perfil de feirante (empresa)** para **publicar ofertas**. | ALTA |
|RF-006| O backend deve **validar a cidade** do usuário e **retornar apenas feiras/ofertas da mesma cidade** do endereço da pessoa. | ALTA |
|RF-007| A aplicação deve disponibilizar uma **tela de ofertas** (feed) para pesquisa/visualização de **posts da mesma cidade** do usuário. | ALTA |
|RF-008| A criação de **post de oferta** deve permitir: **foto** do produto (obrigatória), nome, descrição, **data de validade**, **preço promocional** e **quantidade**. | ALTA |
|RF-009| Cada **card de oferta** deve exibir: **foto**, nome do produto, preço, **data de validade**, **nome da empresa** e **média de avaliação** da empresa. | ALTA |
|RF-010| Ao **clicar no card**, o usuário deve visualizar a **página da empresa/feira** (nome, CNPJ mascarado, endereço, contato/horário se houver), **ofertas ativas** e **avaliações**. | ALTA |
|RF-011| A aplicação deve permitir que usuários autenticados **avaliem a empresa** (nota **1 a 5 estrelas** e **comentário**). | ALTA |
|RF-012| O sistema deve **persistir avaliações** em tabela própria **idEmpresa, nota, descrição**. | ALTA |
|RF-013| O sistema deve **recalcular e atualizar** o campo **MediaNota** na tabela **Empresa** a cada **inserção/edição/exclusão** de avaliação. | ALTA |
|RF-014| A **listagem de ofertas** deve **exibir somente** posts com **validade = data atual + 1 dia** (“vencem amanhã”). | ALTA |
|RF-015| Ofertas com **validade ≤ data atual** não devem ser listadas; se a validade for o **dia atual**, o **anúncio deve ser excluído automaticamente** pelo sistema. | ALTA |
|RF-016| O feed de ofertas deve permitir **busca por termo** (ex.: “tomate”). | MÉDIA |
|RF-017| A aplicação deve **paginar** a listagem de ofertas. | MÉDIA |
|RF-018| O feirante deve poder **editar** e **excluir** suas próprias ofertas. | MÉDIA |
|RF-019| A aplicação deve **impedir avaliações anônimas** e **limitar** múltiplas avaliações por usuário/empresa. | MÉDIA |
|RF-020| O sistema deve **registrar data/hora de criação e atualização** para pessoa, empresa, oferta e avaliação. | MÉDIA |

# Requisitos não Funcionais

|ID     | Descrição do Requisito  | Prioridade |
|-------|-------------------------|----|
|RNF-001| A aplicação deve ser **responsiva** e funcionar nos principais navegadores modernos. | ALTA |
|RNF-002| **Desempenho**: páginas de listagem (ofertas) devem responder em até **2 s** em condições normais (até 100 usuários simultâneos). | ALTA |
|RNF-003| **Validação de dados**: CNPJ deve ter **formato e dígitos verificadores** válidos; CEP em padrão nacional. | ALTA |
|RNF-004| **Confiabilidade**: a exclusão automática de ofertas do dia deve ocorrer via **tarefa agendada** confiável. | ALTA |
|RNF-005| **Usabilidade**: ações principais (buscar oferta e abrir card) devem ocorrer em **até 3 cliques** a partir da home. | MÉDIA |
|RNF-006| **Compatibilidade de mídia**: aceitar upload de **imagem** em JPG/PNG/WebP com **limite de tamanho** (ex.: 2 MB). | MÉDIA |
|RNF-007| **Proteção contra abuso**: limitar **tamanho do comentário** (ex.: 200 caracteres) e aplicar **rate-limit** para avaliações/edições. | BAIXA |

Com base nas Histórias de Usuário, enumere os requisitos da sua solução. Classifique esses requisitos em dois grupos:

# Restrições

O projeto está restrito pelos itens apresentados na tabela a seguir.

|ID| Restrição                                             |
|--|-------------------------------------------------------|
|01| O projeto deverá ser entregue até o final do semestre |
|02| Não pode ser desenvolvido um módulo de backend        |

# Diagrama de Casos de Uso

O diagrama de casos de uso é o próximo passo após a elicitação de requisitos, que utiliza um modelo gráfico e uma tabela com as descrições sucintas dos casos de uso e dos atores. Ele contempla a fronteira do sistema e o detalhamento dos requisitos funcionais com a indicação dos atores, casos de uso e seus relacionamentos. 

As referências abaixo irão auxiliá-lo na geração do artefato “Diagrama de Casos de Uso”.

> **Links Úteis**:
> - [Criando Casos de Uso](https://www.ibm.com/docs/pt-br/elm/6.0?topic=requirements-creating-use-cases)
> - [Como Criar Diagrama de Caso de Uso: Tutorial Passo a Passo](https://gitmind.com/pt/fazer-diagrama-de-caso-uso.html/)
> - [Lucidchart](https://www.lucidchart.com/)
> - [Astah](https://astah.net/)
> - [Diagrams](https://app.diagrams.net/)
