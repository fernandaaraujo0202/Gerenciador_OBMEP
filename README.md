#Gerenciador de Tarefas 

![Status do Projeto](https://img.shields.io/badge/status-concluido-green)

Sistema web desenvolvido com **FastAPI** para gestão de tarefas, controle de eventos em calendário e anexos em PDF.

## Tecnologias

- **Backend:** FastAPI (Python)
- **Frontend:** HTML/Jinja2, CSS (Static Files)
- **Segurança:** SessionMiddleware com criptografia
- **Ambiente:** Python Dotenv para variáveis sensíveis
- **SUPABASE** para armazenar os dados registrados na tabela e no bloco de notas


#### O SUPABASE

Acesse: https://supabase.com/  

e crie uma conta no SUPABASE para armazenar seus dados em tabelas;

Em seguida, crie um projeto de nome "gerenciador-tarefas" e:

- uma tabela de nome **tarefas**  e as seguintes colunas: 

```
| ID | | Descrição | | Status | | Data | |Responsável | | Observações | | PDF | | Selecionar | | NomeArquivo |
```
-outra tabela de nome **eventos** com as seguintes colunas:

    | ID | | titulo | | descricao | | data |



## Pré-requisitos
- Python 3.9+
- Pip (gerenciador de pacotes)


## Instalação e Execução

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/fernandaaraujo0202/Gerenciador-de-tarefas.git]

   cd web_gerenciador-de-tarefas 
   ```
2. Configure o seu .env: em chave, gere uma aleatória rodando no terminal

    ```python -c "import secrets; print(secrets.token_urlsafe(32))" ```
3. Execute
    ```
    uvicorn main:app --reload

    ```


