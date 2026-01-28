import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from moviepy import VideoFileClip
from datetime import datetime
import threading
import subprocess

class ConversorPontoUltimate:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor Video para Audio v2.1")
        self.root.geometry("800x650")
        self.root.configure(bg="#f0f2f5")
        
        self.pasta_origem = ""
        self.pasta_destino = ""
        self.abortar = False

        self.criar_menu_superior()
        self.criar_interface()

    def criar_menu_superior(self):
        menubar = tk.Menu(self.root)
        
        # Menu Ajuda/Sobre
        ajuda_menu = tk.Menu(menubar, tearoff=0)
        ajuda_menu.add_command(label="Sobre o Desenvolvedor", command=self.mostrar_sobre)
        menubar.add_cascade(label="Sobre", menu=ajuda_menu)
        
        self.root.config(menu=menubar)

    def mostrar_sobre(self):
        sobre = tk.Toplevel(self.root)
        sobre.title("Sobre")
        sobre.geometry("400x400")
        sobre.configure(bg="white")
        sobre.resizable(False, False)

        tk.Label(sobre, text="Conversor de vídeo para áudio MP3", font=("Helvetica", 12, "bold"), bg="white").pack(pady=(20, 5))
        tk.Label(sobre, text="Versão 2.0 - Build Stable", font=("Helvetica", 9), fg="#666", bg="white").pack()
        
        texto_dev = (
            "Desenvolvido por:\n"
            "Joao Adolfo Sertório\n\n"
            "Este software foi projetado para automação\n"
            "de alta fidelidade na conversão de arquivos\n"
            "de vídeo para áudio MP3 (192kbps),\n"
            "preservando a estrutura original de pastas.\n\n"
            "* Agradecimentos especiais à espiritualidade\n"
            "Por inspirar este projeto de estudo e desenvolvimento.\n\n"
            "Por este motivo, este software é oferecido gratuitamente\n"
            "para todos os usuários finais, bem como seu código-fonte\n"
            
        )
        tk.Label(sobre, text=texto_dev, font=("Arial", 10), bg="white", justify="center").pack(pady=20)
        
        tk.Button(sobre, text="Fechar", command=sobre.destroy, width=15).pack(pady=10)

    def criar_interface(self):
        # --- Título e Cabeçalho ---
        header_frame = tk.Frame(self.root, bg="#0078D7", height=80)
        header_frame.pack(fill="x")
        tk.Label(header_frame, text="SISTEMA DE CONVERSÃO - VIDEO -> AUDIO", 
                 font=("Segoe UI", 16, "bold"), bg="#0078D7", fg="white").pack(pady=15)
        tk.Label(header_frame, text="Conversão em Lote e com Preservação de Subpastas de uma única vez!", 
                 font=("Segoe UI", 10), bg="#0078D7", fg="#E3F2FD").pack(pady=(0, 15))

        # --- Área de Seleção (Card Branco) ---
        main_frame = tk.Frame(self.root, bg="#f0f2f5")
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Passo 1
        tk.Label(main_frame, text="PASSO 1: Onde estão os vídeos?", font=("Segoe UI", 10, "bold"), bg="#f0f2f5").pack(anchor="w")
        self.btn_origem = tk.Button(main_frame, text="📁 Selecionar Pasta de VÍDEOS (Origem)", command=self.sel_origem, 
                                    font=("Segoe UI", 9), bg="white", relief="groove", padx=10)
        self.btn_origem.pack(fill="x", pady=(5, 0))
        self.lbl_origem = tk.Label(main_frame, text="Nenhuma pasta selecionada", font=("Consolas", 8), bg="#f0f2f5", fg="#666")
        self.lbl_origem.pack(anchor="w", pady=(0, 10))

        # Passo 2
        tk.Label(main_frame, text="PASSO 2: Onde salvar os MP3?", font=("Segoe UI", 10, "bold"), bg="#f0f2f5").pack(anchor="w")
        self.btn_destino = tk.Button(main_frame, text="💾 Selecionar Pasta de Destino (MP3)", command=self.sel_destino, 
                                     font=("Segoe UI", 9), bg="white", relief="groove", padx=10)
        self.btn_destino.pack(fill="x", pady=(5, 0))
        self.lbl_destino = tk.Label(main_frame, text="Qualidade de saída: MP3 192kbps (Alta Fidelidade)", font=("Consolas", 8), bg="#f0f2f5", fg="#666")
        self.lbl_destino.pack(anchor="w", pady=(0, 20))

        # Botão de Ação
        self.btn_iniciar = tk.Button(main_frame, text="▶ INICIAR CONVERSÃO", command=self.iniciar_thread, 
                                     bg="#28a745", fg="white", font=("Segoe UI", 11, "bold"), state="disabled", height=2, cursor="hand2")
        self.btn_iniciar.pack(fill="x", pady=10)

        # Barra de Progresso e Status
        self.progress = ttk.Progressbar(main_frame, orient="horizontal", mode="determinate")
        self.progress.pack(fill="x", pady=5)
        
        self.status_label = tk.Label(main_frame, text="Aguardando configuração...", bg="#f0f2f5", font=("Segoe UI", 9, "italic"))
        self.status_label.pack()

        # Log
        log_frame = tk.Frame(main_frame)
        log_frame.pack(fill="both", expand=True, pady=10)
        
        tk.Label(log_frame, text="Log de Processamento:", bg="#f0f2f5", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        
        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_log = tk.Text(log_frame, height=8, font=("Consolas", 8), state="disabled", yscrollcommand=scrollbar.set)
        self.text_log.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.config(command=self.text_log.yview)

    def sel_origem(self):
        p = filedialog.askdirectory(title="Selecione a pasta RAIZ dos vídeos")
        if p:
            self.pasta_origem = p
            self.lbl_origem.config(text=f"Origem: {p}", fg="#0078D7")
            self.checar_pronto()

    def sel_destino(self):
        p = filedialog.askdirectory(title="Selecione onde salvar a estrutura de MP3")
        if p:
            self.pasta_destino = p
            self.lbl_destino.config(text=f"Destino: {p} (Qualidade MP3: 192kbps)", fg="#0078D7")
            self.checar_pronto()

    def checar_pronto(self):
        if self.pasta_origem and self.pasta_destino:
            self.btn_iniciar.config(state="normal")

    def log(self, msg):
        self.text_log.config(state="normal")
        self.text_log.insert(tk.END, msg + "\n")
        self.text_log.see(tk.END)
        self.text_log.config(state="disabled")

    def iniciar_thread(self):
        self.abortar = False
        self.btn_iniciar.config(state="disabled", text="PROCESSANDO...")
        self.btn_origem.config(state="disabled")
        self.btn_destino.config(state="disabled")
        threading.Thread(target=self.processar_recursivo, daemon=True).start()

    def processar_recursivo(self):
        extensoes = ('.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv')
        arquivos_para_processar = []

        self.status_label.config(text="Mapeando pastas e arquivos...")
        
        # Passo 1: Mapear todos os arquivos (Recursivo)
        for root, dirs, files in os.walk(self.pasta_origem):
            for file in files:
                if file.lower().endswith(extensoes):
                    caminho_completo = os.path.join(root, file)
                    arquivos_para_processar.append(caminho_completo)

        if not arquivos_para_processar:
            messagebox.showwarning("Aviso", "Nenhum vídeo encontrado na estrutura selecionada.")
            self.resetar_ui()
            return

        self.progress["maximum"] = len(arquivos_para_processar)
        self.log(f"--- Início: {len(arquivos_para_processar)} arquivos detectados ---")

        # Passo 2: Processar
        for idx, arquivo_in in enumerate(arquivos_para_processar, 1):
            if self.abortar: break

            try:
                # Descobrir a estrutura de subpasta relativa
                rel_path = os.path.relpath(os.path.dirname(arquivo_in), self.pasta_origem)
                
                # Criar a mesma estrutura no destino
                pasta_destino_final = os.path.join(self.pasta_destino, rel_path)
                os.makedirs(pasta_destino_final, exist_ok=True)

                # Definir nome do arquivo com a regra da PASTA PAI IMEDIATA
                nome_pasta_imediata = os.path.basename(os.path.dirname(arquivo_in))
                
                # Se o arquivo estiver na raiz, usa o nome da pasta raiz
                if nome_pasta_imediata == "" or nome_pasta_imediata == ".":
                    nome_pasta_imediata = os.path.basename(self.pasta_origem)

                timestamp = datetime.now().strftime("%d%m%y-%H%M%S")
                nome_saida = f"Ponto {nome_pasta_imediata} {timestamp}_{idx}.mp3"
                caminho_out = os.path.join(pasta_destino_final, nome_saida)

                self.status_label.config(text=f"Convertendo [{idx}/{len(arquivos_para_processar)}]: {os.path.basename(arquivo_in)}")
                
                # Conversão
                video = VideoFileClip(arquivo_in)
                if video.audio is None:
                    raise ValueError("Vídeo sem áudio")
                
                video.audio.write_audiofile(
                    caminho_out, 
                    bitrate="192k", 
                    fps=44100, 
                    logger=None
                )
                video.close()
                self.log(f"✅ OK: .../{nome_pasta_imediata}/{nome_saida}")

            except Exception as e:
                self.log(f"❌ ERRO: {os.path.basename(arquivo_in)} | {str(e)}")

            self.progress["value"] = idx
            self.root.update_idletasks()

        self.status_label.config(text="Processamento Concluído!")
        messagebox.showinfo("Sucesso", "Conversão finalizada!\nEstrutura de pastas mantida.")
        
        # Abrir a pasta raiz de destino
        if os.name == 'nt': os.startfile(self.pasta_destino)
        
        self.resetar_ui()

    def resetar_ui(self):
        self.btn_iniciar.config(state="normal", text="▶ INICIAR CONVERSÃO")
        self.btn_origem.config(state="normal")
        self.btn_destino.config(state="normal")
        self.progress["value"] = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = ConversorPontoUltimate(root)
    root.mainloop()