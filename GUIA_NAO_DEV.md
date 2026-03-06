## Guia de Instalação e Execução para Não-Desenvolvedores (com Assistência de IA)

Este guia foi elaborado para permitir que qualquer pessoa, mesmo sem experiência em desenvolvimento, possa configurar e executar o Secure Email Gateway utilizando ferramentas de Inteligência Artificial (IA) para auxiliar no processo.

### Pré-requisitos

Para seguir este guia, você precisará de:

1.  **Acesso a um Terminal/Linha de Comando:** No Windows, você pode usar o PowerShell ou o Git Bash. No macOS e Linux, o Terminal padrão.
2.  **Docker Desktop:** Faça o download e instale o Docker Desktop para o seu sistema operacional (Windows, macOS, Linux). Ele inclui o Docker Engine e o Docker Compose.
    *   [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)
3.  **Um Editor de Texto Simples:** Como o Bloco de Notas (Windows), TextEdit (macOS) ou VS Code (multiplataforma). O VS Code é recomendado por sua facilidade de uso e recursos.
    *   [Download VS Code](https://code.visualstudio.com/)
4.  **Uma Conta de E-mail para Testes:** É altamente recomendável usar uma conta de e-mail dedicada para testes, que não seja sua conta principal, para evitar qualquer risco de segurança.
5.  **Acesso a uma IA Generativa (Ex: Gemini, ChatGPT, Copilot):** Para auxiliar na compreensão de comandos, depuração e personalização.

### Passos para Configuração

#### Passo 1: Obter o Código do Projeto

1.  **Crie uma Pasta para o Projeto:**

    Abra seu terminal e crie uma nova pasta para o projeto. Por exemplo:

    ```bash
    mkdir secure-email-gateway-ai
    cd secure-email-gateway-ai
    ```

2.  **Baixe os Arquivos do Projeto:**

    Você precisará baixar todos os arquivos do projeto (os que você recebeu ou de um repositório GitHub, se disponível). Se você recebeu um arquivo ZIP, descompacte-o na pasta `secure-email-gateway-ai` que você acabou de criar.

    *   **Dica de IA:** Se você tiver dificuldades para baixar ou descompactar, pergunte à sua IA: "Como faço para baixar um arquivo ZIP e descompactá-lo na pasta 'secure-email-gateway-ai' no meu sistema operacional (Windows/macOS/Linux)?"

#### Passo 2: Configurar Variáveis de Ambiente

1.  **Abra o Arquivo `.env`:**

    Na pasta `secure-email-gateway-ai`, localize o arquivo chamado `.env`. Abra-o com seu editor de texto.

2.  **Insira a Senha do seu E-mail:**

    Você verá uma linha como esta:

    ```
    EMAIL_PASSWORD=your_email_password_here
    ```

    Substitua `your_email_password_here` pela **senha da sua conta de e-mail de testes**. É crucial que esta seja a senha correta para que o gateway possa acessar sua caixa de entrada.

    *   **Importante:** Nunca compartilhe este arquivo `.env` com outras pessoas ou o envie para repositórios públicos (como GitHub) com sua senha real.

#### Passo 3: Configurar o `config.yaml`

1.  **Abra o Arquivo `config.yaml`:**

    Na mesma pasta, abra o arquivo `config.yaml` com seu editor de texto.

2.  **Ajuste as Configurações do Servidor de E-mail:**

    Localize a seção `email_server` e preencha com as informações do seu provedor de e-mail:

    ```yaml
    email_server:
      imap_server: imap.seuservidor.com # Ex: imap.gmail.com para Gmail
      smtp_server: smtp.seuservidor.com # Ex: smtp.gmail.com para Gmail
      port: 993                       # Porta IMAP SSL, geralmente 993
      username: seu_email@exemplo.com # Seu endereço de e-mail completo
      password_env_var: EMAIL_PASSWORD
      quarantine_folder: Quarentena   # Nome da pasta onde emails suspeitos serão movidos
    ```

    *   **Dica de IA:** Se você não souber as configurações IMAP/SMTP do seu provedor de e-mail, pergunte à sua IA: "Quais são as configurações IMAP e SMTP para [Nome do seu Provedor de E-mail, ex: Gmail, Outlook, Yahoo]?"

3.  **Ajuste Outras Configurações (Opcional):**

    Você pode habilitar ou desabilitar verificações de segurança na seção `security_checks` e ajustar o caminho do modelo de IA ou do arquivo de log, se necessário. Para a primeira execução, as configurações padrão são recomendadas.

#### Passo 4: Iniciar o Sistema com Docker Compose

1.  **Certifique-se de que o Docker Desktop está em Execução:**

    Verifique se o ícone do Docker Desktop está visível na sua bandeja do sistema (Windows) ou barra de menus (macOS), indicando que ele está em execução.

2.  **Abra o Terminal na Pasta do Projeto:**

    Navegue até a pasta `secure-email-gateway-ai` no seu terminal (se você já não estiver lá).

3.  **Construa e Inicie os Serviços:**

    Execute o seguinte comando:

    ```bash
    docker-compose up --build -d
    ```

    *   Este comando fará o download das imagens base do Python, instalará as dependências, construirá os contêineres para cada parte do seu sistema (gateway, IA, verificações de segurança, dashboard) e os iniciará em segundo plano.
    *   A primeira execução pode demorar um pouco, pois ele precisa baixar e construir tudo.
    *   **Dica de IA:** Se você encontrar erros durante este passo, copie a mensagem de erro completa e pergunte à sua IA: "Estou recebendo este erro ao executar `docker-compose up`. O que significa e como posso corrigi-lo? [Cole a mensagem de erro aqui]"

#### Passo 5: Acessar o Dashboard

1.  **Abra seu Navegador:**

    Após o Docker Compose iniciar todos os serviços (pode levar alguns minutos), abra seu navegador web.

2.  **Acesse o Endereço do Dashboard:**

    Digite o seguinte endereço na barra de URL e pressione Enter:

    ```
    http://localhost:8501
    ```

    Você deverá ver o dashboard do Secure Email Gateway, que começará a exibir os logs dos e-mails processados.

## Como Testar o Sistema

1.  **Envie E-mails de Teste:**

    Use uma conta de e-mail **diferente** da que você configurou no `.env` para enviar e-mails para a conta de testes. Tente enviar:
    *   Um e-mail normal (seguro).
    *   Um e-mail com um link suspeito (ex: um encurtador de URL).
    *   Um e-mail com um anexo de extensão perigosa (ex: `test.exe` - **CUIDADO: não execute este arquivo!**).
    *   Um e-mail com texto que simule phishing (ex: "Sua conta foi bloqueada, clique aqui para verificar.").

2.  **Monitore o Dashboard:**

    Observe o dashboard em `http://localhost:8501`. Ele deve mostrar os e-mails sendo processados e suas classificações. E-mails suspeitos/maliciosos devem aparecer com a classificação correspondente e serem movidos para a pasta "Quarentena" no seu servidor IMAP.

3.  **Verifique a Quarentena:**

    Acesse sua conta de e-mail de testes via webmail ou cliente de e-mail e verifique se os e-mails classificados como suspeitos/maliciosos foram movidos para a pasta "Quarentena".
