import os
import threading
from datetime import datetime
import customtkinter as ctk
from tkinter import filedialog, messagebox
import pygame
from moviepy import VideoFileClip, AudioFileClip

# Configuração Global de Tema
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Inicializa o Mixer de Áudio
        pygame.mixer.init()

        # Configuração da Janela
        self.title("Conversor Audio System v3.0 | Pro Edition")
        self.geometry("950x700")
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Variáveis de Estado
        self.pasta_origem = ""
        self.pasta_destino = ""
        self.playlist_arquivos = []  # Lista de caminhos dos MP3
        self.index_atual = -1        # Qual música está tocando?
        self.tocando = False
        self.duracao_atual = 0       # Segundos da música atual

        self.criar_sidebar()
        self.criar_tela_conversor()
        self.criar_tela_player()
        self.criar_tela_sobre()

        self.selecionar_frame("conversor")
        
        # Loop de atualização da barra de progresso (a cada 1 segundo)
        self.atualizar_progresso()

    def criar_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Audio System\nUltimate", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_nav_conversor = ctk.CTkButton(self.sidebar_frame, text="Conversor", command=lambda: self.selecionar_frame("conversor"))
        self.btn_nav_conversor.grid(row=1, column=0, padx=20, pady=10)

        self.btn_nav_player = ctk.CTkButton(self.sidebar_frame, text="Player MP3", command=lambda: self.selecionar_frame("player"))
        self.btn_nav_player.grid(row=2, column=0, padx=20, pady=10)

        self.btn_nav_sobre = ctk.CTkButton(self.sidebar_frame, text="Sobre", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=lambda: self.selecionar_frame("sobre"))
        self.btn_nav_sobre.grid(row=3, column=0, padx=20, pady=10)

        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"], command=ctk.set_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 20))

    def criar_tela_conversor(self):
        self.frame_conversor = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        
        ctk.CTkLabel(self.frame_conversor, text="Estúdio de Conversão", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)

        card = ctk.CTkFrame(self.frame_conversor)
        card.pack(fill="x", padx=20, pady=10)

        # Inputs
        ctk.CTkLabel(card, text="1. Origem (Vídeos)", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(15,5))
        self.entry_origem = ctk.CTkEntry(card, placeholder_text="Selecione a pasta...")
        self.entry_origem.pack(fill="x", padx=15, pady=5)
        ctk.CTkButton(card, text="Buscar Pasta", command=self.sel_origem, width=100).pack(anchor="e", padx=15, pady=(0,10))

        ctk.CTkLabel(card, text="2. Destino (MP3)", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=5)
        self.entry_destino = ctk.CTkEntry(card, placeholder_text="Selecione a pasta...")
        self.entry_destino.pack(fill="x", padx=15, pady=5)
        ctk.CTkButton(card, text="Buscar Pasta", command=self.sel_destino, width=100, fg_color="#E0A800", hover_color="#C69500", text_color="black").pack(anchor="e", padx=15, pady=(0,15))

        self.btn_iniciar = ctk.CTkButton(self.frame_conversor, text="INICIAR PROCESSAMENTO", height=50, font=ctk.CTkFont(size=15, weight="bold"), fg_color="#28a745", hover_color="#218838", command=self.iniciar_thread)
        self.btn_iniciar.pack(fill="x", padx=20, pady=20)

        self.label_status = ctk.CTkLabel(self.frame_conversor, text="Pronto para iniciar", text_color="gray")
        self.label_status.pack()
        
        self.progressbar_conv = ctk.CTkProgressBar(self.frame_conversor)
        self.progressbar_conv.pack(fill="x", padx=20, pady=5)
        self.progressbar_conv.set(0)

        self.textbox_log = ctk.CTkTextbox(self.frame_conversor, height=100)
        self.textbox_log.pack(fill="both", expand=True, padx=20, pady=20)

    def criar_tela_player(self):
        self.frame_player = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        
        ctk.CTkLabel(self.frame_player, text="Player Integrado", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        
        # Botão Recarregar Playlist
        ctk.CTkButton(self.frame_player, text="🔄 Atualizar Playlist (Ler Destino)", command=self.carregar_playlist).pack(pady=5)

        # Lista de Músicas (Scrollable)
        self.scroll_playlist = ctk.CTkScrollableFrame(self.frame_player, label_text="Arquivos na Pasta de Destino")
        self.scroll_playlist.pack(fill="both", expand=True, padx=20, pady=10)

        # Informações da Música
        self.lbl_musica_atual = ctk.CTkLabel(self.frame_player, text="Nenhuma música selecionada", font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_musica_atual.pack(pady=(10,0))
        
        self.lbl_tempo = ctk.CTkLabel(self.frame_player, text="00:00 / 00:00", text_color="gray")
        self.lbl_tempo.pack(pady=(0,10))

        # Barra de Progresso do Audio
        self.progresso_audio = ctk.CTkProgressBar(self.frame_player, height=10)
        self.progresso_audio.pack(fill="x", padx=40, pady=5)
        self.progresso_audio.set(0)

        # Controles
        controles = ctk.CTkFrame(self.frame_player, fg_color="transparent")
        controles.pack(pady=20)
        
        ctk.CTkButton(controles, text="⏮", width=50, command=self.voltar_musica).pack(side="left", padx=10)
        self.btn_play_pause = ctk.CTkButton(controles, text="▶", width=80, height=40, font=ctk.CTkFont(size=20), command=self.toggle_play)
        self.btn_play_pause.pack(side="left", padx=10)
        ctk.CTkButton(controles, text="⏭", width=50, command=self.proxima_musica).pack(side="left", padx=10)
        ctk.CTkButton(controles, text="⏹", width=50, fg_color="#dc3545", hover_color="#c82333", command=self.parar_musica).pack(side="left", padx=10)

    def criar_tela_sobre(self):
        self.frame_sobre = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        ctk.CTkLabel(self.frame_sobre, text="Sobre o Projeto", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=40)
        texto = "Desenvolvido por João Adolfo.\nVersão 3.0 Pro\n\nSoftware gratuito para estudo e\ndesenvolvimento espiritual e técnico."
        ctk.CTkLabel(self.frame_sobre, text=texto, font=ctk.CTkFont(size=14)).pack()

    # --- Lógica de Navegação ---
    def selecionar_frame(self, nome):
        self.frame_conversor.grid_forget()
        self.frame_player.grid_forget()
        self.frame_sobre.grid_forget()
        
        self.btn_nav_conversor.configure(fg_color=("gray75", "gray25") if nome == "conversor" else "transparent")
        self.btn_nav_player.configure(fg_color=("gray75", "gray25") if nome == "player" else "transparent")
        self.btn_nav_sobre.configure(fg_color=("gray75", "gray25") if nome == "sobre" else "transparent")

        if nome == "conversor": self.frame_conversor.grid(row=0, column=1, sticky="nsew")
        if nome == "player": 
            self.frame_player.grid(row=0, column=1, sticky="nsew")
            # Se a playlist estiver vazia, tenta carregar
            if not self.playlist_arquivos and self.pasta_destino:
                self.carregar_playlist()
        if nome == "sobre": self.frame_sobre.grid(row=0, column=1, sticky="nsew")

    # --- Lógica do Conversor ---
    def sel_origem(self):
        p = filedialog.askdirectory()
        if p:
            self.pasta_origem = p
            self.entry_origem.delete(0, "end"); self.entry_origem.insert(0, p)

    def sel_destino(self):
        p = filedialog.askdirectory()
        if p:
            self.pasta_destino = p
            self.entry_destino.delete(0, "end"); self.entry_destino.insert(0, p)

    def log(self, msg):
        self.textbox_log.insert("end", msg + "\n")
        self.textbox_log.see("end")

    def iniciar_thread(self):
        if not self.pasta_origem or not self.pasta_destino:
            messagebox.showwarning("Atenção", "Selecione as pastas.")
            return
        self.btn_iniciar.configure(state="disabled", text="PROCESSANDO...")
        threading.Thread(target=self.processar_recursivo, daemon=True).start()

    def processar_recursivo(self):
        # ... (Mesma lógica de antes)
        extensoes = ('.mp4', '.mkv', '.avi')
        arquivos = []
        for root, dirs, files in os.walk(self.pasta_origem):
            for file in files:
                if file.lower().endswith(extensoes):
                    arquivos.append(os.path.join(root, file))
        
        total = len(arquivos)
        if total == 0:
            self.log("Nenhum vídeo encontrado."); self.resetar_ui(); return

        self.log(f"Iniciando: {total} arquivos.")
        for idx, arquivo_in in enumerate(arquivos, 1):
            try:
                rel_path = os.path.relpath(os.path.dirname(arquivo_in), self.pasta_origem)
                pasta_final = os.path.join(self.pasta_destino, rel_path)
                os.makedirs(pasta_final, exist_ok=True)

                nome_pasta = os.path.basename(os.path.dirname(arquivo_in))
                if nome_pasta in ["", "."]: nome_pasta = os.path.basename(self.pasta_origem)
                
                timestamp = datetime.now().strftime("%d%m%y-%H%M%S")
                nome_saida = f"Ponto {nome_pasta} {timestamp}_{idx}.mp3"
                caminho_out = os.path.join(pasta_final, nome_saida)

                self.progressbar_conv.set(idx / total)
                self.label_status.configure(text=f"Convertendo: {os.path.basename(arquivo_in)}")
                
                video = VideoFileClip(arquivo_in)
                video.audio.write_audiofile(caminho_out, bitrate="192k", logger=None)
                video.close()
                self.log(f"✅ {nome_saida}")
            except Exception as e:
                self.log(f"❌ Erro: {e}")

        self.label_status.configure(text="Concluído!")
        messagebox.showinfo("Sucesso", "Processamento Finalizado!")
        self.resetar_ui()
        # Atualiza o player automaticamente
        self.carregar_playlist()

    def resetar_ui(self):
        self.btn_iniciar.configure(state="normal", text="INICIAR PROCESSAMENTO")
        self.progressbar_conv.set(0)

    # --- Lógica do Player (FASE 2) ---
    def carregar_playlist(self):
        if not self.pasta_destino:
            return

        # Limpa visual antigo
        for widget in self.scroll_playlist.winfo_children():
            widget.destroy()

        self.playlist_arquivos = []
        arquivos_temp = []

        # Varre recursivamente buscando MP3
        for root, dirs, files in os.walk(self.pasta_destino):
            for file in files:
                if file.lower().endswith('.mp3'):
                    caminho_completo = os.path.join(root, file)
                    arquivos_temp.append(caminho_completo)

        if not arquivos_temp:
            ctk.CTkLabel(self.scroll_playlist, text="Nenhum MP3 encontrado na pasta de destino.").pack()
            return

        self.playlist_arquivos = sorted(arquivos_temp)
        
        # Cria botões para cada música
        for idx, caminho in enumerate(self.playlist_arquivos):
            nome_arquivo = os.path.basename(caminho)
            btn = ctk.CTkButton(
                self.scroll_playlist, 
                text=f"{idx+1}. {nome_arquivo}", 
                anchor="w",
                fg_color="transparent",
                border_width=1,
                border_color="gray30",
                command=lambda i=idx: self.tocar_musica(i)
            )
            btn.pack(fill="x", padx=5, pady=2)

    def tocar_musica(self, index):
        if 0 <= index < len(self.playlist_arquivos):
            self.index_atual = index
            caminho = self.playlist_arquivos[index]
            
            try:
                # Carrega e toca
                pygame.mixer.music.load(caminho)
                pygame.mixer.music.play()
                self.tocando = True
                self.btn_play_pause.configure(text="⏸", fg_color="#E0A800") # Amarelo para Pause
                
                # Visual: Atualiza nome e reseta botões da lista
                self.lbl_musica_atual.configure(text=os.path.basename(caminho))
                
                # Pega duração total (usando MoviePy apenas para leitura rápida)
                try:
                    clip = AudioFileClip(caminho)
                    self.duracao_atual = clip.duration
                    clip.close()
                except:
                    self.duracao_atual = 0 # Falha na leitura da duração
                
            except Exception as e:
                print(f"Erro ao tocar: {e}")

    def toggle_play(self):
        if not self.playlist_arquivos: return
        
        if self.tocando:
            pygame.mixer.music.pause()
            self.tocando = False
            self.btn_play_pause.configure(text="▶", fg_color="#28a745") # Verde para Play
        else:
            if self.index_atual == -1:
                self.tocar_musica(0)
            else:
                pygame.mixer.music.unpause()
                self.tocando = True
                self.btn_play_pause.configure(text="⏸", fg_color="#E0A800")

    def parar_musica(self):
        pygame.mixer.music.stop()
        self.tocando = False
        self.btn_play_pause.configure(text="▶", fg_color="#28a745")
        self.progresso_audio.set(0)
        self.lbl_tempo.configure(text="00:00 / 00:00")

    def proxima_musica(self):
        if self.playlist_arquivos:
            prox = (self.index_atual + 1) % len(self.playlist_arquivos)
            self.tocar_musica(prox)

    def voltar_musica(self):
        if self.playlist_arquivos:
            ant = (self.index_atual - 1) % len(self.playlist_arquivos)
            self.tocar_musica(ant)

    def formatar_tempo(self, segundos):
        m = int(segundos // 60)
        s = int(segundos % 60)
        return f"{m:02}:{s:02}"

    def atualizar_progresso(self):
        # Esta função roda a cada 500ms
        if self.tocando and pygame.mixer.music.get_busy():
            # get_pos retorna milissegundos desde o 'play'
            tempo_atual = pygame.mixer.music.get_pos() / 1000
            
            if self.duracao_atual > 0:
                progresso = tempo_atual / self.duracao_atual
                self.progresso_audio.set(progresso)
                
                # Atualiza texto (Ex: 01:20 / 03:45)
                txt_atual = self.formatar_tempo(tempo_atual)
                txt_total = self.formatar_tempo(self.duracao_atual)
                self.lbl_tempo.configure(text=f"{txt_atual} / {txt_total}")
                
                # Auto-Next: Se estiver a 1s do fim, pula
                if tempo_atual >= self.duracao_atual - 1:
                    self.proxima_musica()
        
        # Chama a si mesma novamente em 500ms
        self.after(500, self.atualizar_progresso)

if __name__ == "__main__":
    app = App()
    app.mainloop()