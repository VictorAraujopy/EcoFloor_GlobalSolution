# 🌱 EcoFloor - Gestão Energética Inteligente de Salas de Aula

## 📖 Sobre o Projeto

O **EcoFloor** é uma solução IoT desenvolvida para combater o desperdício de energia em ambientes educacionais e corporativos. O sistema atua como um orquestrador inteligente que não apenas monitoriza, mas toma decisões ativas baseadas em dados.

## 🧠 Lógica de Termostato Inteligente

O sistema cruza dados de presença com a temperatura ambiente para decidir o estado do Ar Condicionado:

*   **Temperatura > 23°C + Presença:** ✅ AC Liga (Conforto).
*   **Temperatura < 23°C:** ❄️ AC Desliga (Economia, mesmo com gente).
*   **Sem Presença:** 🌑 Tudo Desliga (Economia Máxima).

## 🏗️ Arquitetura do Sistema

O projeto segue uma arquitetura modular robusta:

*   **Backend (Python/Flask):** API RESTful que centraliza a lógica de negócio e deteta desperdícios (`ML.py`). Utiliza um Connection Pool para comunicação eficiente com o banco.
*   **Banco de Dados (Oracle):** Armazenamento histórico seguro. Utiliza comandos `MERGE` para garantir integridade dos dados das salas.
*   **Hardware (ESP32/Wokwi):** Sensores (PIR, DHT22) e Atuadores (Relés/LEDs) que operam em tempo real baseados nos comandos da API.
*   **Data Analytics (R):** Scripts automatizados que geram relatórios visuais de eficiência energética e auditoria de desperdício.

## 📂 Estrutura do Projeto

```
ECOFLOOR_GLOBALSOLUTION/
├── Backend/
│   ├── api.py                 # Servidor API Flask (Controlador Principal)
│   ├── db_config.py           # Configuração de Banco (Oracle + Connection Pool)
│   ├── gerar_csv.py           # Automação para exportar dados do banco para CSV
│   ├── ML.py                  # Módulo de Inteligência (Classificação de Desperdício)
│   ├── requirements.txt       # Lista de dependências Python
│   └── .env                   # Credenciais do Banco (CRIAR MANUALMENTE)
│
├── data/
│   ├── analise/
│   │   └── analise_com.R      # Script R principal para gerar gráficos
│   ├── graficos/              # Pasta onde os PNGs são salvos automaticamente
│   ├── dados_gs_ecofloor.csv      # Dataset: Cenário Eficiente (Simulado)
│   └── dados_gs_sem_ecofloor.csv  # Dataset: Cenário de Desperdício
│
├── wokwi/
│   ├── diagram.json           # Diagrama de conexões do simulador
│   ├── sketch.ino             # Código C++ do ESP32
│   └── libraries.txt          # Bibliotecas Arduino (ArduinoJson, DHT)
│
└── README.md
```

## ⚙️ Guia de Instalação e Execução

### 1️⃣ Configuração do Banco de Dados (Segurança)

O arquivo de senhas não é enviado para o GitHub. Você deve criá-lo:

1.  Vá na pasta `Backend`.
2.  Crie um arquivo novo chamado `.env`.
3.  Adicione as suas credenciais Oracle:

```
DB_USER="SEU_RM"
DB_PASS="SUA_SENHA"
DB_DSN="oracle.fiap.com.br:1521/ORCL"
```

### 2️⃣ Rodar o Backend (API)

No VS Code, abra o terminal e instale as dependências:

```bash
pip install -r Backend/requirements.txt
```

Abra o arquivo `Backend/api.py` e clique no botão **Play ▶️**.

**CRÍTICO (Encaminhamento de Porta):**

1.  Vá na aba **PORTS** (ao lado do Terminal).
2.  Encontre a porta `5000`.
3.  Clique com botão direito em "Visibility" -> mude para **Public**.
4.  Copie o link gerado ("Forwarded Address").

### 3️⃣ Configurar o Hardware (Wokwi)

1.  Abra o arquivo `wokwi/sketch.ino`.
2.  Cole o link público da API na variável `url_base`:

```cpp
String url_base = "https://seu-link-aqui.app_github_dev";
```

3.  Inicie a simulação no Wokwi.

### 4️⃣ Análise de Dados (R)

1.  Abra o script `data/analise/analise_com.R` no RStudio.
2.  Execute o script.
3.  Quando solicitado, selecione os arquivos CSV localizados na pasta `data/`.
4.  Verifique a pasta `data/graficos` para ver os relatórios gerados.

## 📊 Resultados Esperados

O sistema gera gráficos comparativos demonstrando a economia:

*   **✅ Cenário Com Sistema:** O gráfico mostra o consumo de energia caindo para zero durante os intervalos (sala vazia).
*   **❌ Cenário Sem Sistema:** O gráfico mostra uma linha contínua de alto consumo, evidenciando o desperdício.

## 👨‍💻 Autores

Desenvolvido para a Global Solution - Engenharia de Software & IoT.

| Função | Nome |
| :--- | :--- |
| Backend & Integração | Victor Araujo Ferreira da Silva |
| Banco de Dados | Jonathan Gomes Ribeiro Franco |
| Hardware & Sensores | Pedro Zanon Castro Santana |
| Data Analytics | Filipe Marques Previato |
| Documentação | Jacqueline Nanami Matushima |

EcoFloor © 2025 - Tecnologia a favor da sustentabilidade. 🌍💡
