# 🕵️ Instagram OSINT – KGB_Arruda InstaOSINT

## Descrição

Esta é uma **ferramenta em Python** desenvolvida para a coleta de informações públicas e a geração de um **relatório OSINT (Open Source Intelligence)** estruturado em formato PDF, a partir de perfis do Instagram.

O script realiza consultas utilizando um `sessionid` válido de uma conta logada e produz um relatório detalhado contendo:

*   Dados básicos do perfil.
*   Lista de seguidores recentes.
*   Postagens recentes.
*   Metadados das postagens (legenda, data, localizações, likes e comentários).
*   Análise básica de engajamento, incluindo a identificação de top comentadores.

## ⚠️ Aviso Legal

> Esta ferramenta destina-se exclusivamente a **fins educacionais e pesquisa em OSINT**. O usuário é totalmente responsável pelo uso que fizer da ferramenta e pelo respeito à legislação vigente e aos termos de serviço do Instagram.

## ✨ Funcionalidades

| Funcionalidade | Detalhe |
| :--- | :--- |
| **Coleta de Perfil** | Obtenção de informações públicas essenciais do perfil alvo. |
| **Seguidores Recentes** | Captura de uma lista de seguidores mais recentes. |
| **Postagens Recentes** | Coleta de dados das últimas postagens do perfil. |
| **Extração de Metadados** | Extração de legenda, data, localização, contagem de likes e comentários. |
| **Top Comentadores** | Identificação dos usuários mais ativos nos comentários. |
| **Relatório em PDF** | Geração automática de um relatório estruturado chamado `relatorio.pdf`. |

## 🛠️ Requisitos

Para o funcionamento correto do script, são necessários os seguintes requisitos:

*   **Python 3.9** ou superior.
*   Conexão com a internet.
*   Um `sessionid` válido de uma conta logada no Instagram.

## 📥 Instalação e Funcionamento

### 🐧 Instalação no KALI (ou Linux)

Siga os passos abaixo para configurar e rodar o programa em ambientes Linux:

1.  **Clonar o repositório** (assumindo que o repositório esteja disponível):
    ```bash
    git clone [URL_DO_REPOSITORIO]
    ```
2.  **Entrar na pasta** do projeto:
    ```bash
    cd KGB_ARRUDA_INSTAOSINT
    ```
3.  **Gerar ambiente virtual** (recomendado):
    ```bash
    python3 -m venv venv
    ```
4.  **Habilitar ambiente** virtual:
    ```bash
    source venv/bin/activate
    ```
5.  **Instalar dependências**:
    ```bash
    pip install -r requirements.txt
    ```
6.  **Rodar o programa**:
    ```bash
    python3 KGB_ARRUDA_INSTAOSINT1.0.py
    ```

### 🪟 Instalação no WINDOWS

Siga os passos abaixo para configurar e rodar o programa no Windows:

1.  **Instalar Python**: Certifique-se de que a opção "Add Python to PATH" foi ativada durante a instalação.
2.  **Baixar o programa** e descompactar (`unzip`).
3.  **Navegar até a pasta** onde se encontram os arquivos `KGB_ARRUDA_INSTAOSINT1.0.py` e `requirements.txt`.
4.  **Instalar dependências** (em um terminal/CMD):
    ```bash
    pip install -r requirements.txt
    ```
5.  **Rodar o programa**:
    ```bash
    python KGB_ARRUDA_INSTAOSINT1.0.py
    ```

## 🔑 Obtendo o `sessionid` do Instagram

O `sessionid` é crucial para que o script possa realizar as consultas.

1.  **Logar** em uma conta válida do Instagram no seu navegador.
2.  **Instalar um add-on** de edição de cookies (ex: "Cookies Editor" para Chrome/Firefox).
3.  **Ativar o add-on** na página do Instagram logado e **obter o valor** do cookie chamado `sessionid`.

## 📄 Saída

Após a execução, o arquivo **`relatorio.pdf`** será gerado na mesma pasta onde o programa foi instalado.

## 📧 Contato e Créditos

*   **Autor**: KGB\_Arruda
*   **E-mail**: arrudacibersec@proton.me

## 🖼️ Screenshot

<img src="Images/Sem título.jpg" width="900" alt="Captura de tela da interface do programa InstaOSINT">

