# Sistema Acadêmico — Python (Exercício 3)

Refatoração do projeto Java 17 para Python, com interface gráfica em **CustomTkinter**.

## Pré-requisitos

- Python 3.10+
- pip

## Instalação

```bash
pip install -r requirements.txt
```

## Executar

```bash
cd academic_system
python main.py
```

## Credenciais padrão

| Usuário    | Senha      | Perfil    |
|------------|------------|-----------|
| admin      | admin123   | ADMIN     |
| professor  | prof123    | PROFESSOR |

## Estrutura do Projeto

```
academic_system/
├── main.py                  # Entry point
├── logging_config.py        # Configuração de logging
├── requirements.txt
├── data/                    # Arquivos gerados (TXT, XML, JSON)
├── logs/                    # Logs da aplicação
├── exceptions/              # Exceções customizadas
├── security/                # Role, User
├── model/                   # AcademicClass, Assessment
├── repository/              # Repositórios + PersistenceType
├── service/                 # Services (auth, class, assessment, persistence, report)
├── controller/              # AcademicSystemController
└── view/                    # GUI completa com CustomTkinter
```

## Histórias de Usuário implementadas

| # | Código      | Descrição                                                    |
|---|-------------|--------------------------------------------------------------|
| 1 | US-2361     | Cadastrar avaliações em turmas                               |
| 2 | TUS-2362    | Persistir dados em arquivo TXT                               |
| 3 | US-2363     | Registrar turmas                                             |
| 6 | US-2366     | Autenticar usuários e autorizar ações por papel               |
| 7 | US-2367     | Tratar erros do domínio com exceções customizadas            |
| 9 | US-2369     | Tratar erros de autenticação/autorização com exceções        |
| 12| US-2372     | Configurar tipo de persistência como administrador           |
| 13| US-2373     | Salvar dados em XML                                          |
| 14| US-2374     | Salvar dados em JSON                                         |
| 15| US-2375     | Gerar relatório resumo de avaliações por turma               |
| 16| US-2376     | Gerar relatório de peso de avaliações                        |
| 17| US-2377     | Gerar relatório de configuração de persistência              |
| 18| US-2378     | Renderização dinâmica de menu baseada em papel               |
| 19| US-2379     | Logout                                                       |
| 30| TUS-2390    | Logging de autenticação, persistência e relatórios           |
| 36| TUS-2396    | ClassService                                                 |
| 37| TUS-2397    | AssessmentService                                            |
| 38| TUS-2398    | PersistenceService                                           |
| 39| TUS-2399    | ReportService                                                |
| 47| TUS-2407    | Tela de login (CustomTkinter)                                |
| 48| TUS-2408    | Tela principal baseada em papel                              |
| 49| TUS-2409    | Tela de cadastro de turmas                                   |
| 50| TUS-2410    | Tela de cadastro de avaliações                               |
| 51| TUS-2411    | Tela de relatórios                                           |
| 52| TUS-2412    | Tela de configuração de persistência                         |
| 53| TUS-2413    | Tela de visualização de turmas e avaliações                  |
