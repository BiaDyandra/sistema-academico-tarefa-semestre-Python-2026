<a id="top"></a>

# Sistema Acadêmico — Python

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-Modern--GUI-darkgreen)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-habilitado-blue)
![Status](https://img.shields.io/badge/status-concluído-green)

Este projeto consiste na **refatoração e migração** do Sistema Acadêmico desenvolvido originalmente em Java 17 para a linguagem **Python**, utilizando **Modelos de Grandes Linguagens (LLMs)** como assistentes de engenharia de software. O trabalho foi desenvolvido como parte das atividades práticas da disciplina de Orientação a Objetos, ministrada pelo professor Rodrigo Martins Pagliares no curso de Bacharelado em Ciência da Computação da Universidade Federal de Alfenas (UNIFAL-MG).

A aplicação exercita a transição de conceitos de programação orientada a objetos (POO), arquitetura de software em camadas, segurança (RBAC), logging distribuído, persistência polimórfica e práticas modernas de CI/CD para o ecossistema do Python.

---

## Equipe

| Nome | GitHub |
|------|--------|
| Bianca Dyandra | [@BiaDyandra](https://github.com/BiaDyandra) |
| Gabriela Mazon | [@Gabriela-Mazon](https://github.com/Gabriela-Mazon) |
| Leticia Alves | [@LuthorW](https://github.com/LuthorW) |
| Isabela Mageste | [@Isabela-Mageste](https://github.com/Isabela-Mageste) |

---

## Índice

- [Visão Geral](#visão-geral)
- [Objetivos da Refatoração com LLMs](#objetivos-da-refatoração-com-llms)
- [Principais Conceitos Praticados](#principais-conceitos-praticados)
- [Tecnologias](#tecnologias)
- [Arquitetura do Projeto](#arquitetura-do-projeto)
- [Modelo de Segurança](#modelo-de-segurança)
- [Estrutura do Repositório](#estrutura-do-repositório)
- [Como Baixar e Rodar](#como-baixar-e-rodar)
- [Como Testar a Interface Gráfica](#como-testar-a-interface-gráfica)
- [Evolução da Persistência](#evolução-da-persistência)
- [Roadmap de Histórias de Usuário](#roadmap-de-histórias-de-usuário)
- [Finalidade Educacional](#finalidade-educacional)

---

<a id="visão-geral"></a>

## Visão Geral

O sistema permite que professores e administradores gerenciem de forma eficiente turmas e avaliações por meio de uma interface gráfica rica e moderna construída com **CustomTkinter**.

A migração preservou todas as regras de negócio e histórias de usuário estabelecidas na especificação original em Java, adaptando a infraestrutura para as melhores práticas e convenções nativas do ecossistema Python (como o gerenciamento de pacotes com `pip`, tratamento de propriedades via decoradores e isolamento de escopo).

[↑ Voltar ao topo](#top)

---

<a id="objetivos-da-refatoração-com-llms"></a>

## Objetivos da Refatoração com LLMs

- **Migração de Paradigma:** Utilizar LLMs para traduzir estruturas estritas de tipos do Java para o dinamismo forte do Python, sem perder os pilares da Orientação a Objetos.
- **Eficiência de Código:** Adaptar heranças, polimorfismo e encapsulamento usando as convenções pythônicas (`__init__`, `self`, gerenciamento de exceções nativas).
- **Substituição Tecnológica Dinâmica:** Auxiliar na substituição da stack de interface gráfica (de JavaFX para CustomTkinter) e de frameworks de infraestrutura.

[↑ Voltar ao topo](#top)

---

<a id="principais-conceitos-praticados"></a>

## Principais Conceitos Praticados

- Abstração, Herança, Polimorfismo e Encapsulamento em Python.
- Gerenciamento de estado de objetos e identidade (`__eq__` e `__hash__`).
- Padrões de Projeto (Design Patterns): Singleton, Repository e Strategy para persistência variada.
- Controle de Acesso Baseado em Papéis (RBAC - Role-Based Access Control) e Sessões seguras.
- Arquitetura baseada em MVC (Model-View-Controller) com desacoplamento via Camada de Serviços.
- Validação de regras de negócio em tempo de execução com tratamento de exceções customizadas.
- Automação de pipelines de Integração Contínua (CI) com GitHub Actions aplicados ao ecossistema Python.

[↑ Voltar ao topo](#top)

---

<a id="tecnologias"></a>

## Tecnologias

| Tecnologia | Finalidade |
|------------|-----------|
| Python 3.10+ | Linguagem de programação principal |
| CustomTkinter | Biblioteca para a construção da interface gráfica (UI) moderna |
| Python Logging | Módulo nativo para auditoria e rastreamento de logs |
| JSON / XML / TXT | Formatos de arquivos para persistência polimórfica de dados |
| GitHub Actions | Automação e execução do pipeline de CI |

[↑ Voltar ao topo](#top)

---

<a id="arquitetura-do-projeto"></a>

## Arquitetura do Projeto

A aplicação adota uma divisão rígida em camadas inspirada no padrão arquitetural MVC:

- **`model`**: Contém as entidades centrais do domínio acadêmico.
- **`repository`**: Gerencia o acesso físico aos dados, aplicando estratégias para gravação e leitura síncrona.
- **`service`**: Isola as regras de negócio e validações acadêmicas, protegendo os modelos de manipulações diretas inválidas.
- **`controller`**: Orquestra e dita o fluxo de dados entre as interações do usuário e os serviços subjacentes.
- **`view`**: Implementa as telas do sistema isolando componentes visuais em CustomTkinter da lógica operacional.

[↑ Voltar ao topo](#top)

---

<a id="modelo-de-segurança"></a>

## Modelo de Segurança

O controle de acesso valida a permissão do usuário de forma estrita em tempo de renderização da interface e execução das chamadas de serviço.

### Papéis Suportados

| Papel | Permissões Principais |
|-------|----------------------|
| ADMIN | Cadastrar turmas, alterar estratégias de persistência, salvar base de dados, gerar relatórios globais |
| PROFESSOR | Cadastrar avaliações acadêmicas, consultar turmas existentes, gerar relatórios de pesos |

### Credenciais de Teste

| Usuário | Senha | Papel |
|---------|-------|-------|
| admin | admin123 | ADMIN |
| professor | prof123 | PROFESSOR |

[↑ Voltar ao topo](#top)

---

<a id="estrutura-do-repositório"></a>

## Estrutura do Repositório

```
academic_system_python/
├── .github/
│   └── workflows/
│       └── ci.yml               # Pipeline de CI (GitHub Actions)
├── academic_system/
│   ├── main.py                  # Ponto de entrada do sistema
│   ├── logging_config.py        # Módulo de parametrização de Logs
│   ├── requirements.txt         # Gerenciador de dependências externas
│   ├── data/                    # Arquivos gerados de persistência (TXT, XML, JSON)
│   ├── logs/                    # Arquivo físico de saída de logs de auditoria
│   ├── exceptions/              # Infraestrutura de Exceções Customizadas do domínio
│   ├── security/                # Entidades e validações de controle de acesso e usuários
│   ├── model/                   # Classes de dados e modelos puros de POO
│   ├── repository/              # Camada de dados e enumerações de persistência
│   ├── service/                 # Regras acadêmicas (auth, class, assessment, report)
│   ├── controller/              # Controladores centralizadores da lógica de negócio
│   └── view/                    # Interface Visual Moderna construída com CustomTkinter
├── LICENSE                      # Licença MIT obrigatória
└── README.md                    # Documentação do projeto
```

[↑ Voltar ao topo](#top)

---

<a id="como-baixar-e-rodar"></a>

## Como Baixar e Rodar

### Requisitos

- Python 3.10 ou superior
- Gerenciador de pacotes `pip` instalado

### 1. Clonar o Repositório

```bash
git clone https://github.com/BiaDyandra/sistema-academico-tarefa-semestre-Python-2026.git
cd sistema-academico-tarefa-semestre-Python-2026
```

### 2. Instalar as Dependências

```bash
pip install -r academic_system/requirements.txt
```

### 3. Executar a Aplicação

```bash
cd academic_system
python main.py
```

[↑ Voltar ao topo](#top)

---

<a id="como-testar-a-interface-gráfica"></a>

## Como Testar a Interface Gráfica

Execute o arquivo `main.py` e execute o plano de testes funcionais abaixo para certificar-se da integridade do ecossistema:

1. **Tentativa de Autenticação Inválida:** Tente logar inserindo dados aleatórios. O sistema interceptará o fluxo disparando um aviso visual de erro de credenciais.
2. **Acesso como Administrador (`admin` / `admin123`):** Certifique-se de que o painel exibe de forma dinâmica as opções de *Cadastro de Turmas*, *Configurações de Persistência*, *Salvar Dados*, *Relatórios*, além das funções padrões.
3. **Acesso como Professor (`professor` / `prof123`):** Realize o logout, autentique-se como professor e verifique que os botões de *Cadastrar Turma* e *Configurar Persistência* foram completamente omitidos da árvore de renderização.
4. **Fluxo Acadêmico Completo:** Como administrador, cadastre uma turma. Realize o login como professor e vincule uma avaliação com peso específico a essa turma gerada.
5. **Geração e Emissão de Relatórios:** Clique no módulo de relatórios para verificar a computação em tela de pesos das notas e o resumo consolidado.

[↑ Voltar ao topo](#top)

---

<a id="evolução-da-persistência"></a>

## Evolução da Persistência

O sistema implementa o padrão de projeto *Strategy* para alternar em tempo de execução a persistência sem violar o princípio Aberto/Fechado (SOLID).

| Nível | Formato de Armazenamento | Escopo de Implementação |
|-------|--------------------------|------------------------|
| V1 | Arquivo Texto Puro | Armazenamento delimitado estruturado em `.txt` |
| V2 | Documento Estruturado XML | Serialização via manipulação com árvores de elementos nativas |
| V3 | Objeto Notacional JSON | Mapeamento de dicionários e objetos tipados nativos em `.json` |

[↑ Voltar ao topo](#top)

---

<a id="roadmap-de-histórias-de-usuário"></a>

## Roadmap de Histórias de Usuário

Abaixo estão listadas as histórias de usuário migradas e validadas com sucesso no ecossistema Python:

| Código | Descrição da História de Usuário | Status |
|--------|----------------------------------|--------|
| **US-2361** | Cadastrar avaliações vinculadas a turmas válidas | ✅ |
| **TUS-2362** | Persistir dados da aplicação em arquivos de texto plano (TXT) | ✅ |
| **US-2363** | Registrar turmas acadêmicas no ecossistema local | ✅ |
| **US-2366** | Autenticar usuários no sistema e autorizar ações com base no papel operacional (RBAC) | ✅ |
| **US-2367** | Interceptar falhas e violações do domínio acadêmico lançando Exceções Customizadas | ✅ |
| **US-2369** | Tratar tentativas de quebras de segurança de autenticação/autorização de forma isolada | ✅ |
| **US-2372** | Fornecer ao Administrador a capacidade de alterar o tipo de persistência em runtime | ✅ |
| **US-2373** | Codificar e exportar os dados do sistema acadêmico no formato estruturado XML | ✅ |
| **US-2374** | Codificar e exportar os dados do sistema acadêmico no formato chave-valor JSON | ✅ |
| **US-2375** | Gerar relatórios analíticos de resumo das avaliações ordenadas por turma | ✅ |
| **US-2376** | Gerar relatórios de verificação e auditoria de soma total de pesos de avaliações | ✅ |
| **US-2377** | Gerar relatórios informativos de configuração e integridade da persistência ativa | ✅ |
| **US-2378** | Executar a renderização dinâmica e condicional dos menus de acordo com o papel do usuário | ✅ |
| **US-2379** | Permitir o encerramento seguro de sessão ativa (Logout) e retorno ao fluxo de Login | ✅ |
| **TUS-2390** | Rastrear eventos e falhas gerando logs detalhados de persistência, segurança e relatórios | ✅ |
| **TUS-2396** | Implementar isolamento das turmas por meio da classe `ClassService` | ✅ |
| **TUS-2397** | Implementar isolamento e regras de pesos por meio da classe `AssessmentService` | ✅ |
| **TUS-2398** | Implementar controle polimórfico de gravação por meio do `PersistenceService` | ✅ |
| **TUS-2399** | Implementar o motor de extração de relatórios por meio do `ReportService` | ✅ |
| **TUS-2407** | Construir e estilizar tela de Login responsiva utilizando a biblioteca CustomTkinter | ✅ |
| **TUS-2408** | Projetar Painel Principal adaptável baseado na identidade visual escura/clara da UI | ✅ |
| **TUS-2409** | Projetar formulário e telas de diálogos para inserção e validação de novas Turmas | ✅ |
| **TUS-2410** | Projetar formulário de vinculação de Avaliações com validação dinâmica de pesos | ✅ |
| **TUS-2411** | Criar visualizador unificado em tela para renderização de relatórios do sistema | ✅ |
| **TUS-2412** | Criar seletor interativo gráfico para alternância de motores de persistência ativa | ✅ |
| **TUS-2413** | Construir grades dinâmicas de dados para listagem em tempo real de turmas cadastradas | ✅ |

[↑ Voltar ao topo](#top)

---

<a id="finalidade-educacional"></a>

## Finalidade Educacional

Este software foi refatorado e adaptado estritamente com objetivos acadêmicos na UNIFAL-MG. O exercício prático serviu para comprovar a viabilidade e eficácia no uso de Modelos de Grandes Linguagens (LLMs) como co-pilotos eficientes na engenharia de software, garantindo qualidade, portabilidade e fidelidade arquitetural entre ecossistemas de linguagens distintas.

[↑ Voltar ao topo](#top)
