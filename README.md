# Video2Mp3 Converter

> **Versão:** 3.5 Stable
> **Desenvolvedor:** João Sertório

## 📖 Sobre o Projeto
O **Video2Mp3** é uma ferramenta de software desenvolvida para facilitar estudos e organização de mídia. Ele converte vídeos em áudio de alta fidelidade, preservando meticulosamente a estrutura de pastas do usuário e oferece um player integrado para consumo imediato do conteúdo.

Este projeto foi **inspirado pela espiritualidade** como forma de aprimorar meus estudos e contribuir com a comunidade. Por este motivo, o software é **totalmente gratuito** e de código aberto.

---

## 🚀 Funcionalidades Principais

### 1. Conversão Inteligente e Neutra
* **Formatos Aceitos:** .MP4, .MKV, .AVI, .MOV, .FLV, .WMV.
* **Saída de Áudio:** MP3 192kbps (Constant Bitrate) / 44.1kHz Estéreo.
* **Espelhamento de Pastas:** O software lê subpastas recursivamente e recria a mesma árvore de diretórios no destino.
* **Nomeação Dinâmica:** Os arquivos convertidos assumem automaticamente o nome da pasta de origem + data/hora, garantindo organização sem prefixos fixos.

### 2. Player Integrado
* **Playlist Automática:** Carrega as músicas da pasta de destino assim que a conversão termina.
* **Controles:** Play, Pause, Próximo, Anterior e Barra de Progresso.
* **Gestão:** Botões dedicados para limpar a playlist ou selecionar novas pastas de música independentemente da conversão.

### 3. Interface Moderna
* Desenvolvido com **CustomTkinter** (Dark Mode nativo).
* Design limpo, intuitivo e focado na experiência do usuário (UX).

---

## 📚 Instruções de Uso

### Para Converter:
1.  Abra o aplicativo.
2.  Na aba **Conversor**, clique em "Buscar Pasta" no campo **Origem** (onde estão seus vídeos).
3.  Clique em "Buscar Pasta" no campo **Destino** (onde os MP3 serão salvos).
4.  Clique no botão verde **INICIAR CONVERSÃO**.
5.  Aguarde a barra de progresso. Ao final, o player carregará automaticamente.

### Para Ouvir:
1.  Vá para a aba **Player MP3**.
2.  Se você acabou de converter, a lista já estará lá.
3.  Para ouvir outra pasta, clique em **"Selecionar / Trocar Pasta de Músicas"**.
4.  Use os controles multimídia para navegar.

---

## 🛠️ Instalação (Para Desenvolvedores)

Se você deseja estudar o código-fonte ou contribuir:

```bash
# Clone o repositório
git clone [https://github.com/joaosertorio/Video2Mp3.git](https://github.com/joaosertorio/Video2Mp3.git)

# Entre na pasta
cd Video2Mp3

# Crie o ambiente virtual
python -m venv venv
# Ative o venv (Windows: .\venv\Scripts\Activate)

# Instale as dependências
pip install -r requirements.txt

# Execute
python main.py


📬 Contato e Feedback
Ficarei feliz em receber feedback ou conectar com outros desenvolvedores e estudantes.

LinkedIn: linkedin.com/in/joão-sertório
GitHub: github.com/joaosertorio
E-mail: sertorio.joao@gmail.com

Feito com propósito e tecnologia.