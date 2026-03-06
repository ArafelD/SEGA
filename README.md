# Secure Email Gateway (SEG) com Inteligência Artificial

## Visão Geral do Projeto

Este projeto demonstra a implementação de um **Secure Email Gateway (SEG)** utilizando Python e Inteligência Artificial (IA). O objetivo principal é proteger organizações contra ameaças veiculadas por e-mail, como phishing, malware em anexos, URLs maliciosas e spoofing de domínio. O sistema intercepta e-mails recebidos, aplicando múltiplas camadas de análise de segurança antes de entregá-los à caixa de entrada do usuário ou movê-los para uma área de quarentena.

## Funcionalidades Principais

*   **Interceptação de E-mails:** Conecta-se a um servidor IMAP para monitorar e-mails de entrada.
*   **Análise de Cabeçalhos:** Verifica registros SPF (Sender Policy Framework), DKIM (DomainKeys Identified Mail) e DMARC (Domain-based Message Authentication, Reporting, and Conformance) para combater spoofing e garantir a autenticidade do remetente.
*   **Detecção de Phishing com IA:** Utiliza modelos de Processamento de Linguagem Natural (NLP) e Machine Learning (Scikit-learn) para identificar padrões e características de e-mails de phishing no corpo e assunto das mensagens.
*   **Análise de URLs:** Extrai e avalia URLs presentes no conteúdo do e-mail, identificando links suspeitos ou maliciosos.
*   **Verificação de Anexos:** Calcula hashes de anexos e verifica extensões de arquivos conhecidas por serem perigosas. (Pode ser estendido com integração a serviços como VirusTotal).
*   **Sistema de Classificação de Risco:** Classifica e-mails como **Seguro**, **Suspeito** ou **Malicioso** com base nos resultados das análises.
*   **Quarentena Automatizada:** E-mails classificados como suspeitos ou maliciosos são automaticamente movidos para uma pasta de quarentena no servidor IMAP.
*   **Registro de Atividades (Logs):** Mantém um registro detalhado de todos os e-mails processados e seus resultados de análise.
*   **Dashboard de Monitoramento:** Uma interface web interativa (Streamlit) para visualizar em tempo real o fluxo de e-mails, estatísticas de classificação e detalhes dos logs.

## Arquitetura do Sistema

A arquitetura do SEG é modular e baseada em microsserviços, facilitando a escalabilidade e a manutenção. Cada componente é encapsulado em um contêiner Docker, permitindo um ambiente de execução isolado e consistente.

```

    A[INTERNET] --> B(Emails Recebidos)
    B --> C[Secure Email Bot<br>(Python Gateway)]
    C --> D[Verificação de SPF/DKIM/DMARC]
    C --> E[Análise de Phishing (IA/NLP)]
    C --> F[Análise de URLs]
    C --> G[Análise de Anexos (Malware)]
    D --> H{Sistema de Classificação}
    E --> H
    F --> H
    G --> H
    H -- Seguro --> I[Caixa de Entrada]
    H -- Suspeito/Malicioso --> J[Quarentena
    (Logs + Alertas)]
    J --> K[Dashboard / Logs]
    I --> K
```

**Componentes:**

*   **Gateway (`gateway/`):** Responsável por conectar ao servidor IMAP, buscar e-mails, parsear seu conteúdo e orquestrar as verificações de segurança e IA.
*   **Motor de IA (`ai_engine/`):** Contém o modelo de Machine Learning para detecção de phishing. O modelo é treinado com dados de e-mails legítimos e de phishing para identificar padrões suspeitos.
*   **Verificações de Segurança (`security_checks/`):** Módulos dedicados para realizar verificações específicas, como autenticação de domínio (SPF/DKIM/DMARC), análise de URLs e varredura de anexos.
*   **Logs (`logs/`):** Armazena os registros de todas as operações e resultados das análises em formato JSON.
*   **Dashboard (`dashboard/`):** Uma aplicação Streamlit que oferece uma interface gráfica para monitorar o status do gateway, visualizar e-mails processados e analisar estatísticas.

## Tecnologias Utilizadas

O projeto é construído com as seguintes tecnologias:

*   **Python 3.9+:** Linguagem de programação principal.
*   **`imaplib`, `email`:** Para interação com servidores de e-mail IMAP e parsing de mensagens.
*   **`python-dotenv`:** Gerenciamento seguro de variáveis de ambiente.
*   **`PyYAML`:** Carregamento de configurações do arquivo `config.yaml`.
*   **`dnspython`, `dkimpy`:** Para verificações de registros DNS (SPF, DKIM, DMARC).
*   **`scikit-learn`, `pandas`, `joblib`:** Para implementação e persistência do modelo de Machine Learning (NLP) para detecção de phishing.
*   **`streamlit`:** Framework para criação do dashboard interativo.
*   **`Docker`, `Docker Compose`:** Para conteinerização e orquestração dos serviços, garantindo portabilidade e escalabilidade.
*   **Linux:** Ambiente operacional base para os contêineres Docker.

## Estrutura do Repositório

```text
secure-email-gateway-ai/
├── .env                    # Variáveis de ambiente (SENHAS, API KEYS)
├── requirements.txt        # Dependências do Python
├── config.yaml             # Configurações globais do sistema
├── docker-compose.yml      # Definição dos serviços Docker
├── Dockerfile.gateway      # Dockerfile para o serviço Gateway
├── Dockerfile.ai_engine    # Dockerfile para o serviço AI Engine
├── Dockerfile.security_checks # Dockerfile para o serviço Security Checks
├── Dockerfile.dashboard    # Dockerfile para o serviço Dashboard
├── gateway/
│   ├── email_listener.py   # Conecta ao IMAP e escuta novos emails
│   ├── email_parser.py     # Extrai cabeçalhos, corpo e anexos
│   ├── email_processor.py  # Orquestra as verificações de segurança e IA
│   └── quarantine.py       # Gerencia emails bloqueados
├── ai_engine/
│   ├── phishing_detector.py # Implementação do modelo de NLP para análise de texto
│   └── model_loader.py      # Carrega/treina modelos pré-treinados
├── security_checks/
│   ├── domain_checker.py    # Verifica SPF, DKIM e DMARC
│   ├── attachment_scanner.py # Verifica hashes de arquivos e extensões (VirusTotal opcional)
│   └── url_analyzer.py      # Analisa URLs no corpo do email
├── logs/
│   └── email_logs.json      # Registro de atividades e resultados
└── dashboard/
    └── app.py               # Aplicação Streamlit para o dashboard
```

## Instalação e Execução (Para Não-Desenvolvedores com IA)

Este guia foi elaborado para permitir que qualquer pessoa, mesmo sem experiência em desenvolvimento, possa configurar e executar o Secure Email Gateway utilizando ferramentas de IA para auxiliar no processo.

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

## Parando o Sistema

Para parar todos os serviços do Secure Email Gateway, abra o terminal na pasta `secure-email-gateway-ai` e execute:

```bash
docker-compose down
```

Isso irá parar e remover os contêineres, redes e volumes criados pelo `docker-compose up`.

## Solução de Problemas Comuns (com Ajuda da IA)

*   **"Não consigo conectar ao servidor IMAP."**
    *   Verifique se `imap_server`, `port` e `username` em `config.yaml` estão corretos.
    *   Confirme se a `EMAIL_PASSWORD` no arquivo `.env` está correta.
    *   Alguns provedores de e-mail (como Gmail) exigem que você habilite "acesso a aplicativos menos seguros" ou gere uma "senha de aplicativo" específica para acesso via IMAP. Pergunte à sua IA: "Como habilitar acesso IMAP para aplicativos de terceiros no [Nome do seu Provedor de E-mail]?"

*   **"O dashboard não abre em `http://localhost:8501`."**
    *   Certifique-se de que o Docker Desktop está em execução.
    *   Verifique o terminal onde você executou `docker-compose up`. Se houver erros, use a IA para ajudar a depurá-los.
    *   Pode ser que a porta 8501 já esteja em uso. Você pode tentar mudar a porta no `docker-compose.yml` e no comando `streamlit run` no `Dockerfile.dashboard`.

*   **"O modelo de IA não está detectando phishing."**
    *   O modelo de IA fornecido é um exemplo básico. Para um desempenho robusto, ele precisaria ser treinado com um conjunto de dados maior e mais diversificado de e-mails de phishing e legítimos.
    *   Verifique os logs no dashboard para ver os detalhes da análise de IA.

## Melhorias Futuras

Este projeto pode ser expandido com as seguintes melhorias:

*   **Integração com VirusTotal API:** Para uma análise de malware mais robusta em anexos, enviando hashes de arquivos para verificação.
*   **Machine Learning Avançado:** Exploração de modelos de NLP mais sofisticados (ex: BERT, GPT) para detecção de phishing e análise de sentimento, aumentando a precisão.
*   **Sistema de Alertas em Tempo Real:** Notificações via Slack, e-mail ou outras plataformas para e-mails de alta severidade, permitindo resposta rápida.
*   **Integração com SIEM/SOAR:** Envio de logs e alertas para sistemas de Gerenciamento de Eventos e Informações de Segurança (SIEM) ou Orquestração, Automação e Resposta de Segurança (SOAR) para análise centralizada e automação de resposta.
*   **Interface de Gerenciamento de Quarentena:** Uma interface web dedicada para revisar e-mails em quarentena, permitindo que administradores liberem e-mails falsos positivos ou os excluam permanentemente.
*   **Suporte a SMTP:** Implementar a capacidade de reencaminhar e-mails limpos para o destinatário original via SMTP, tornando o gateway um ponto de passagem completo.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues para relatar bugs ou sugerir novas funcionalidades, e enviar pull requests com melhorias. Por favor, siga as diretrizes de código e mantenha os testes atualizados.



