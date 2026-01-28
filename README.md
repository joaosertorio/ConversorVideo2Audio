# ConversorVideo2Audio

> **Status:** 🚧 Work In Progress (WIP) - Versão 2.0 Stable
> **Data de Publicação:** 28 de Janeiro de 2026

## 📖 Sobre o Projeto
O **ConversorVideo2Audio** é uma ferramenta de automação desenvolvida em Python para converter grandes volumes de arquivos de vídeo em áudio (MP3) de alta fidelidade.

Diferente de conversores comuns, este software foi desenhado com um algoritmo recursivo que **preserva a estrutura original de diretórios**. Se você tem uma biblioteca organizada em pastas e subpastas, o software replicará essa organização na pasta de destino, garantindo que nenhum arquivo se perca ou se misture.

### ✨ Principais Funcionalidades
- **Espelhamento de Diretórios:** Lê subpastas recursivamente e recria a mesma árvore no destino.
- **Alta Fidelidade Sonora:** Conversão padronizada em MP3 192kbps / 44.1kHz.
- **Nomenclatura Inteligente:** Renomeia arquivos automaticamente evitando conflitos (Timestamp + ID).
- **Interface Gráfica (GUI):** Interface amigável desenvolvida com Tkinter, sem necessidade de linha de comando.
- **Logs em Tempo Real:** Feedback visual de sucesso ou falha para cada arquivo processado.

## 🛠️ Tecnologias Utilizadas
- **Linguagem:** Python 3.12
- **Motor de Mídia:** MoviePy (com FFmpeg)
- **Interface:** Tkinter
- **Compilação:** PyInstaller

## 🚀 Como Usar (Para Desenvolvedores)
Para rodar este projeto localmente:

1. Clone o repositório:
   ```bash
   git clone [https://github.com/joaosertorio/ConversorVideo2Audio.git](https://github.com/joaosertorio/ConversorVideo2Audio.git)