if (!require("ggplot2")) install.packages("ggplot2")
if (!require("dplyr")) install.packages("dplyr")
if (!require("rstudioapi")) install.packages("rstudioapi") 
library(ggplot2)
library(dplyr)

# Cria pasta de saida
if (!dir.exists("graficos")) dir.create("graficos")

# ==============================================================================
# SELECAO DE ARQUIVOS (JANELA DO WINDOWS)
# ==============================================================================

print("---------------------------------------------------------------------")
print("PASSO 1: Selecione o arquivo do CENARIO COM SISTEMA (Eficiente)")
print("---------------------------------------------------------------------")
arquivo_1 <- choose.files(caption = "Selecione o arquivo COM SISTEMA (Eficiente)", multi = FALSE)
if (length(arquivo_1) == 0) stop("Nenhum arquivo selecionado.")

print("---------------------------------------------------------------------")
print("PASSO 2: Selecione o arquivo do CENARIO SEM SISTEMA (Desperdicio)")
print("---------------------------------------------------------------------")
arquivo_2 <- choose.files(caption = "Selecione o arquivo SEM SISTEMA (Desperdicio)", multi = FALSE)
if (length(arquivo_2) == 0) stop("Nenhum arquivo selecionado.")

# ==============================================================================
# FUNCAO DE DESIGN (CORRIGIDA PARA ALINHAR BOLAS E LINHA)
# ==============================================================================
gerar_grafico_energia_preciso <- function(dados, titulo, subtitulo, tipo) {
  
  df <- dados %>%
    mutate(timestamp = as.POSIXct(timestamp_str, format="%Y-%m-%d %H:%M:%S")) %>%
    mutate(
      # Potencia (kW)
      potencia_kw = (luz_ligada * 0.2) + (ac_ligado * 2.5),
      
      situacao = case_when(
        presenca == 0 & ac_ligado == 1 ~ "DESPERDICIO (Gasto em Sala Vazia)",
        ac_ligado == 1 ~ "Consumo Alto (AC Ligado)",
        luz_ligada == 1 ~ "Consumo Baixo (So Luz)",
        TRUE ~ "Consumo Zero (Desligado)"
      )
    )
  
  dia_base <- as.Date(df$timestamp[1])
  
  if (tipo == "BOM") {
    texto_box <- "ECONOMIA:\nGasto caiu para ZERO!"
    cor_box <- "#27ae60"
    fundo_box <- "#e8f8f5"
  } else {
    texto_box <- "PREJUIZO:\nGasto continua ALTO!"
    cor_box <- "#c0392b"
    fundo_box <- "#fdedec"
  }
  
  g <- ggplot(df, aes(x = timestamp, y = potencia_kw)) +
    # Faixa de Intervalo
    annotate("rect", xmin = as.POSIXct(paste(dia_base, "12:00:00")), xmax = as.POSIXct(paste(dia_base, "13:30:00")), 
             ymin = -Inf, ymax = Inf, fill = "#f4f6f7", alpha = 0.5) +
    annotate("text", x = as.POSIXct(paste(dia_base, "12:45:00")), y = 3.2, label = "INTERVALO", color = "#7f8c8d", fontface="bold", size=3) +
    
    # CORRECAO: geom_line (Conecta os pontos exatamente)
    geom_line(color = "#bdc3c7", size = 1.5, alpha = 0.8, linejoin = "round") + 
    
    # Pontos (Agora vao ficar EXATAMENTE em cima da linha)
    geom_point(aes(color = situacao), size = 4.5, alpha = 0.9) +
    
    annotate("label", x = as.POSIXct(paste(dia_base, "12:45:00")), y = 1.5, 
             label = texto_box, fill = fundo_box, color = cor_box, size = 3.5, fontface = "bold") +
    
    expand_limits(y = 3.5) + 
    
    scale_color_manual(values = c(
      "Consumo Alto (AC Ligado)"      = "#3498db",
      "Consumo Baixo (So Luz)"        = "#f1c40f",
      "Consumo Zero (Desligado)"      = "#95a5a6",
      "DESPERDICIO (Gasto em Sala Vazia)" = "#c0392b"
    )) +
    
    labs(title = titulo, subtitle = subtitulo, x = "Horario", y = "Potencia Consumida (kW)", color = "Legenda") +
    theme_minimal() +
    theme(legend.position = "bottom", plot.title = element_text(size = 14, face = "bold", color = "#2c3e50"))
  
  return(g)
}

# ==============================================================================
# GERACAO DOS 2 GRAFICOS
# ==============================================================================

# 1. Carregar Dados
print("Lendo arquivos...")
dados_1 <- read.csv(arquivo_1)
dados_2 <- read.csv(arquivo_2)

# --- GRAFICO 1: ENERGIA COM SISTEMA (PRECISO) ---
print("Gerando Grafico 1...")
g1 <- gerar_grafico_energia_preciso(dados_1, "Grafico 1: Gasto Energetico COM Sistema", "O consumo desce para zero no intervalo (Economia).", "BOM")
print(g1)
ggsave("graficos/1_energia_com_sistema_final.png", plot = g1, width = 10, height = 6)

# --- GRAFICO 2: ENERGIA SEM SISTEMA (PRECISO) ---
print("Gerando Grafico 2...")
g2 <- gerar_grafico_energia_preciso(dados_2, "Grafico 2: Gasto Energetico SEM Sistema", "O consumo mantem-se alto e estavel (Desperdicio).", "RUIM")
print(g2)
ggsave("graficos/2_energia_sem_sistema_final.png", plot = g2, width = 10, height = 6)

print("SUCESSO! Graficos corrigidos e salvos.")