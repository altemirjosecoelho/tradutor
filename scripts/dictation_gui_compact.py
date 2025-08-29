#!/usr/bin/env python3
"""
Ferramenta de Ditado Compacta com Interface Dark Moderna
Google Speech Recognition + Tradução + Narração
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import pyautogui
from googletrans import Translator
import speech_recognition as sr
from PIL import Image, ImageTk, ImageDraw
import os
import pyttsx3
import pyperclip
import numpy as np
import pyaudio
import wave
import io
import base64

class CompactDictationGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_variables()
        self.setup_speech_engine()
        self.setup_gui()
        self.setup_speech_recognition()
        
        # Thread para reconhecimento de voz
        self.recognition_thread = None
        self.is_listening = False
        
        # Variáveis para VU Meter e áudio
        self.audio_data = []
        self.audio_thread = None
        self.is_recording_audio = False
        self.audio_frames = []
        self.audio_format = pyaudio.paInt16
        self.audio_channels = 1
        self.audio_rate = 44100
        self.audio_chunk = 1024
        
        # Variáveis para ícone e bandeja do sistema
        self.tray_icon = None
        self.is_minimized = False
        self.original_icon = None
        self.recording_icon = None
        
    def setup_window(self):
        """Configura a janela principal"""
        self.root.title("🎤 Ditado Inteligente")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)
        
        # Centralizar na tela
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"900x600+{x}+{y}")
        
        # Configurar estilo dark moderno
        self.root.configure(bg='#1a1a1a')
        
        # Configurar tema escuro
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#1a1a1a', borderwidth=0)
        style.configure('TNotebook.Tab', background='#2d2d2d', foreground='#ffffff', padding=[10, 5])
        style.map('TNotebook.Tab', background=[('selected', '#404040'), ('active', '#353535')])
        
    def setup_variables(self):
        """Configura variáveis de controle"""
        self.translation_mode = tk.BooleanVar(value=True)
        self.language = tk.StringVar(value='pt-BR')
        self.auto_narrate = tk.BooleanVar(value=False)
        self.narrate_speed = tk.DoubleVar(value=1.0)
        
        # Tradutor
        self.translator = Translator()
        
        # Reconhecedor de voz
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 3000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
    
    def setup_speech_engine(self):
        """Configura o motor de síntese de voz"""
        try:
            self.speech_engine = pyttsx3.init()
            
            # Configurar voz
            voices = self.speech_engine.getProperty('voices')
            if voices:
                # Tentar encontrar voz em português
                for voice in voices:
                    if 'portuguese' in voice.name.lower() or 'pt' in voice.id.lower():
                        self.speech_engine.setProperty('voice', voice.id)
                        break
                else:
                    # Usar primeira voz disponível
                    self.speech_engine.setProperty('voice', voices[0].id)
            
            # Configurar velocidade
            self.speech_engine.setProperty('rate', 150)
            
            # Configurar volume
            self.speech_engine.setProperty('volume', 0.9)
            
        except Exception as e:
            print(f"⚠️ Erro ao configurar síntese de voz: {e}")
            self.speech_engine = None
    
    def setup_gui(self):
        """Configura a interface gráfica"""
        # Notebook para abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Aba de Ditado
        self.dictation_frame = tk.Frame(self.notebook, bg='#1a1a1a')
        self.notebook.add(self.dictation_frame, text='🎤 Ditado')
        self.setup_dictation_tab()
        
        # Aba de Tradução
        self.translation_frame = tk.Frame(self.notebook, bg='#1a1a1a')
        self.notebook.add(self.translation_frame, text='🌍 Tradução')
        self.setup_translation_tab()
        
        # Aba de Configurações
        self.settings_frame = tk.Frame(self.notebook, bg='#1a1a1a')
        self.notebook.add(self.settings_frame, text='⚙️ Config')
        self.setup_settings_tab()
        
        # Barra de status compacta
        self.status_bar = tk.Frame(self.root, bg='#2d2d2d', height=30)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_bar.pack_propagate(False)
        
        # Status do microfone
        self.mic_status = tk.Label(
            self.status_bar,
            text="⏸️ Pausado",
            font=('Helvetica', 10),
            fg='#e74c3c',
            bg='#2d2d2d'
        )
        self.mic_status.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Status da tradução
        self.trans_status = tk.Label(
            self.status_bar,
            text="🌍 Tradução: ON",
            font=('Helvetica', 10),
            fg='#27ae60',
            bg='#2d2d2d'
        )
        self.trans_status.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Idioma atual
        self.lang_status = tk.Label(
            self.status_bar,
            text="🗣️ PT-BR",
            font=('Helvetica', 10),
            fg='#3498db',
            bg='#2d2d2d'
        )
        self.lang_status.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Separador
        separator = tk.Frame(self.status_bar, bg='#404040', width=1, height=20)
        separator.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Atalhos de teclado
        shortcuts_label = tk.Label(
            self.status_bar,
            text="⌨️ Ctrl+Shift+1: Ditado | Ctrl+Shift+2: Tradução | Ctrl+Shift+3: Idioma | Ctrl+Shift+4: Sair",
            font=('Helvetica', 9),
            fg='#95a5a6',
            bg='#2d2d2d'
        )
        shortcuts_label.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Configurar eventos
        self.root.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)
        
        # Atalhos de teclado
        self.root.bind('<Control-Key-1>', lambda e: self.toggle_listening())
        self.root.bind('<Control-Key-2>', lambda e: self.toggle_translation())
        self.root.bind('<Control-Key-3>', lambda e: self.switch_language())
        self.root.bind('<Control-Key-4>', lambda e: self.quit_app())
        
        # Criar ícones
        self.create_app_icons()
        
        # Configurar bandeja do sistema
        self.setup_system_tray()
    
    def setup_dictation_tab(self):
        """Configura a aba de ditado por voz"""
        # Frame principal
        main_frame = tk.Frame(self.dictation_frame, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="🎤 Ditado por Voz",
            font=('Helvetica', 20, 'bold'),
            fg='#ffffff',
            bg='#1a1a1a'
        )
        title_label.pack(pady=(0, 20))
        
        # VU Meter e controles de áudio
        audio_frame = tk.Frame(main_frame, bg='#2d2d2d', relief=tk.FLAT, bd=0)
        audio_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Título do VU Meter
        vu_title = tk.Label(
            audio_frame,
            text="🎤 Monitor de Áudio",
            font=('Helvetica', 14, 'bold'),
            fg='#ffffff',
            bg='#2d2d2d'
        )
        vu_title.pack(pady=(15, 10))
        
        # Frame do VU Meter
        vu_container = tk.Frame(audio_frame, bg='#2d2d2d')
        vu_container.pack(pady=(0, 15))
        
        # VU Meter
        self.vu_canvas = tk.Canvas(
            vu_container,
            width=300,
            height=40,
            bg='#1a1a1a',
            highlightthickness=0,
            relief=tk.FLAT
        )
        self.vu_canvas.pack(side=tk.LEFT, padx=(0, 20))
        
        # Barra de áudio (VU Meter)
        self.audio_bar = self.vu_canvas.create_rectangle(
            10, 30, 10, 10,
            fill='#27ae60',
            outline='#27ae60',
            width=0
        )
        
        # Indicador de nível
        self.level_label = tk.Label(
            vu_container,
            text="0 dB",
            font=('Helvetica', 12, 'bold'),
            fg='#ffffff',
            bg='#2d2d2d'
        )
        self.level_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Botão Play para escutar áudio capturado
        self.play_button = tk.Button(
            vu_container,
            text="🔊 Play",
            font=('Helvetica', 12),
            bg='#3498db',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=self.play_captured_audio,
            activebackground='#2980b9',
            activeforeground='white',
            state=tk.NORMAL
        )
        self.play_button.pack(side=tk.LEFT, padx=(0, 20))
        
        # Status do áudio
        self.audio_status = tk.Label(
            vu_container,
            text="⏸️ Sem áudio",
            font=('Helvetica', 10),
            fg='#95a5a6',
            bg='#2d2d2d'
        )
        self.audio_status.pack(side=tk.LEFT)
        
        # Frame de controles principais
        controls_frame = tk.Frame(main_frame, bg='#2d2d2d', relief=tk.FLAT, bd=0)
        controls_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Botão principal de ativação com atalho
        button_frame = tk.Frame(controls_frame, bg='#2d2d2d')
        button_frame.pack(pady=20)
        
        self.toggle_button = tk.Button(
            button_frame,
            text="🎤 Iniciar Ditado",
            font=('Helvetica', 16, 'bold'),
            bg='#27ae60',
            fg='white',
            relief=tk.FLAT,
            padx=30,
            pady=15,
            command=self.toggle_listening,
            activebackground='#2ecc71',
            activeforeground='white'
        )
        self.toggle_button.pack()
        
        # Atalho de teclado abaixo do botão
        shortcut_label = tk.Label(
            button_frame,
            text="⌨️ Ctrl+Shift+1",
            font=('Helvetica', 12),
            fg='#95a5a6',
            bg='#2d2d2d'
        )
        shortcut_label.pack(pady=(5, 0))
        
        # Botão para minimizar para bandeja
        minimize_button = tk.Button(
            button_frame,
            text="📱 Minimizar para Bandeja",
            font=('Helvetica', 10),
            bg='#9b59b6',
            fg='white',
            relief=tk.FLAT,
            padx=15,
            pady=5,
            command=self.minimize_to_tray,
            activebackground='#8e44ad',
            activeforeground='white'
        )
        minimize_button.pack(pady=(10, 0))
        
        # Frame de configurações rápidas
        quick_config = tk.Frame(controls_frame, bg='#2d2d2d')
        quick_config.pack(pady=(0, 20))
        
        # Tradução automática
        tk.Checkbutton(
            quick_config,
            text="🌍 Tradução automática (PT → EN)",
            variable=self.translation_mode,
            font=('Helvetica', 12),
            fg='#ffffff',
            bg='#2d2d2d',
            selectcolor='#1a1a1a',
            activebackground='#2d2d2d',
            activeforeground='#ffffff',
            command=self.update_translation_status
        ).pack(side=tk.LEFT, padx=20)
        
        # Idioma
        tk.Label(
            quick_config,
            text="🗣️ Idioma:",
            font=('Helvetica', 12),
            fg='#ffffff',
            bg='#2d2d2d'
        ).pack(side=tk.LEFT, padx=(20, 5))
        
        language_combo = ttk.Combobox(
            quick_config,
            textvariable=self.language,
            values=['pt-BR', 'en-US', 'es-ES', 'fr-FR', 'de-DE'],
            state='readonly',
            font=('Helvetica', 12),
            width=10
        )
        language_combo.pack(side=tk.LEFT, padx=(0, 20))
        language_combo.bind('<<ComboboxSelected>>', self.update_language_status)
        
        # Frame de saída com dois tons de cinza
        output_frame = tk.Frame(main_frame, bg='#2d2d2d', relief=tk.FLAT, bd=0)
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título da saída
        output_title = tk.Label(
            output_frame,
            text="📝 Saída do Reconhecimento",
            font=('Helvetica', 14, 'bold'),
            fg='#ffffff',
            bg='#2d2d2d'
        )
        output_title.pack(pady=(15, 10))
        
        # Área de texto para saída com dois tons de cinza
        text_frame = tk.Frame(output_frame, bg='#404040', relief=tk.FLAT, bd=0)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        self.dictation_output = scrolledtext.ScrolledText(
            text_frame,
            height=8,
            font=('Consolas', 11),
            bg='#404040',  # Cinza mais claro para o fundo do texto
            fg='#ffffff',
            insertbackground='#ffffff',
            relief=tk.FLAT,
            padx=15,
            pady=15,
            selectbackground='#3498db',
            selectforeground='#ffffff'
        )
        self.dictation_output.pack(fill=tk.BOTH, expand=True)
        
        # Botões de ação
        buttons_frame = tk.Frame(main_frame, bg='#1a1a1a')
        buttons_frame.pack(fill=tk.X, pady=(15, 0))
        
        tk.Button(
            buttons_frame,
            text="🗑️ Limpar",
            font=('Helvetica', 11),
            bg='#e74c3c',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=lambda: self.clear_output(self.dictation_output),
            activebackground='#c0392b',
            activeforeground='white'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            buttons_frame,
            text="📋 Copiar Último",
            font=('Helvetica', 11),
            bg='#3498db',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=lambda: self.copy_last_text(self.dictation_output),
            activebackground='#2980b9',
            activeforeground='white'
        ).pack(side=tk.LEFT, padx=(0, 10))
    
    def setup_translation_tab(self):
        """Configura a aba de tradução de texto"""
        # Frame principal
        main_frame = tk.Frame(self.translation_frame, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="🌍 Tradução de Texto",
            font=('Helvetica', 20, 'bold'),
            fg='#ffffff',
            bg='#1a1a1a'
        )
        title_label.pack(pady=(0, 20))
        
        # Frame de entrada
        input_frame = tk.Frame(main_frame, bg='#2d2d2d', relief=tk.FLAT, bd=0)
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Título da entrada
        input_title = tk.Label(
            input_frame,
            text="📝 Texto de Entrada",
            font=('Helvetica', 14, 'bold'),
            fg='#ffffff',
            bg='#2d2d2d'
        )
        input_title.pack(pady=(15, 10))
        
        # Área de texto de entrada
        input_text_frame = tk.Frame(input_frame, bg='#404040', relief=tk.FLAT, bd=0)
        input_text_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        self.input_text = scrolledtext.ScrolledText(
            input_text_frame,
            height=5,
            font=('Consolas', 11),
            bg='#404040',
            fg='#ffffff',
            insertbackground='#ffffff',
            relief=tk.FLAT,
            padx=15,
            pady=15,
            selectbackground='#3498db',
            selectforeground='#ffffff'
        )
        self.input_text.pack(fill=tk.BOTH, expand=True)
        
        # Frame de controles de tradução
        translation_controls = tk.Frame(main_frame, bg='#2d2d2d', relief=tk.FLAT, bd=0)
        translation_controls.pack(fill=tk.X, pady=(0, 20))
        
        controls_title = tk.Label(
            translation_controls,
            text="⚙️ Configurações de Tradução",
            font=('Helvetica', 14, 'bold'),
            fg='#ffffff',
            bg='#2d2d2d'
        )
        controls_title.pack(pady=(15, 15))
        
        controls_grid = tk.Frame(translation_controls, bg='#2d2d2d')
        controls_grid.pack(pady=(0, 15))
        
        # Direção da tradução
        tk.Label(
            controls_grid,
            text="🔄 Direção:",
            font=('Helvetica', 12),
            fg='#ffffff',
            bg='#2d2d2d'
        ).grid(row=0, column=0, sticky=tk.W, padx=20, pady=5)
        
        self.translation_direction = tk.StringVar(value='pt-en')
        direction_combo = ttk.Combobox(
            controls_grid,
            textvariable=self.translation_direction,
            values=['pt-en', 'en-pt', 'pt-es', 'es-pt', 'pt-fr', 'fr-pt'],
            state='readonly',
            font=('Helvetica', 12),
            width=15
        )
        direction_combo.grid(row=0, column=1, sticky=tk.W, padx=20, pady=5)
        
        # Narração automática
        tk.Checkbutton(
            controls_grid,
            text="🔊 Narração automática",
            variable=self.auto_narrate,
            font=('Helvetica', 12),
            fg='#ffffff',
            bg='#2d2d2d',
            selectcolor='#1a1a1a',
            activebackground='#2d2d2d',
            activeforeground='#ffffff'
        ).grid(row=0, column=2, sticky=tk.W, padx=20, pady=5)
        
        # Botões de ação
        action_buttons = tk.Frame(controls_grid, bg='#2d2d2d')
        action_buttons.grid(row=1, column=0, columnspan=3, pady=10)
        
        tk.Button(
            action_buttons,
            text="📋 Colar do Clipboard",
            font=('Helvetica', 11),
            bg='#9b59b6',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=self.paste_from_clipboard,
            activebackground='#8e44ad',
            activeforeground='white'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            action_buttons,
            text="🌍 Traduzir",
            font=('Helvetica', 11),
            bg='#27ae60',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=self.translate_text,
            activebackground='#2ecc71',
            activeforeground='white'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            action_buttons,
            text="🔊 Narrar",
            font=('Helvetica', 11),
            bg='#f39c12',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=self.narrate_text,
            activebackground='#e67e22',
            activeforeground='white'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            action_buttons,
            text="🗑️ Limpar",
            font=('Helvetica', 11),
            bg='#e74c3c',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=lambda: self.clear_output(self.input_text),
            activebackground='#c0392b',
            activeforeground='white'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Frame de saída
        output_frame = tk.Frame(main_frame, bg='#2d2d2d', relief=tk.FLAT, bd=0)
        output_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Título da saída
        output_title = tk.Label(
            output_frame,
            text="📝 Texto Traduzido",
            font=('Helvetica', 14, 'bold'),
            fg='#ffffff',
            bg='#2d2d2d'
        )
        output_title.pack(pady=(15, 10))
        
        # Área de texto de saída
        output_text_frame = tk.Frame(output_frame, bg='#404040', relief=tk.FLAT, bd=0)
        output_text_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        self.translation_output = scrolledtext.ScrolledText(
            output_text_frame,
            height=5,
            font=('Consolas', 11),
            bg='#404040',
            fg='#ffffff',
            insertbackground='#ffffff',
            relief=tk.FLAT,
            padx=15,
            pady=15,
            selectbackground='#3498db',
            selectforeground='#ffffff'
        )
        self.translation_output.pack(fill=tk.BOTH, expand=True)
        
        # Botões de saída
        output_buttons = tk.Frame(main_frame, bg='#1a1a1a')
        output_buttons.pack(fill=tk.X, pady=(15, 0))
        
        tk.Button(
            output_buttons,
            text="📋 Copiar Tradução",
            font=('Helvetica', 11),
            bg='#3498db',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=self.copy_translation,
            activebackground='#2980b9',
            activeforeground='white'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            output_buttons,
            text="🔊 Narrar Tradução",
            font=('Helvetica', 11),
            bg='#f39c12',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=lambda: self.narrate_text(self.translation_output.get(1.0, tk.END).strip()),
            activebackground='#e67e22',
            activeforeground='white'
        ).pack(side=tk.LEFT, padx=(0, 10))
    
    def setup_settings_tab(self):
        """Configura a aba de configurações"""
        # Frame principal
        main_frame = tk.Frame(self.settings_frame, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="⚙️ Configurações",
            font=('Helvetica', 20, 'bold'),
            fg='#ffffff',
            bg='#1a1a1a'
        )
        title_label.pack(pady=(0, 20))
        
        # Frame de configurações
        settings_frame = tk.Frame(main_frame, bg='#2d2d2d', relief=tk.FLAT, bd=0)
        settings_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Configurações de áudio
        audio_frame = tk.LabelFrame(
            settings_frame,
            text="🎤 Configurações de Áudio",
            font=('Helvetica', 14, 'bold'),
            fg='#ffffff',
            bg='#2d2d2d',
            relief=tk.FLAT,
            bd=0
        )
        audio_frame.pack(fill=tk.X, padx=15, pady=15)
        
        # Sensibilidade do microfone
        tk.Label(
            audio_frame,
            text="🎤 Sensibilidade do microfone:",
            font=('Helvetica', 12),
            fg='#ffffff',
            bg='#2d2d2d'
        ).pack(pady=5)
        
        self.sensitivity_scale = tk.Scale(
            audio_frame,
            from_=1000,
            to=8000,
            orient=tk.HORIZONTAL,
            bg='#2d2d2d',
            fg='#ffffff',
            highlightbackground='#2d2d2d',
            troughcolor='#404040',
            activebackground='#3498db',
            command=self.update_sensitivity
        )
        self.sensitivity_scale.set(self.recognizer.energy_threshold)
        self.sensitivity_scale.pack(pady=(0, 10))
        
        # Configurações de narração
        narration_frame = tk.LabelFrame(
            settings_frame,
            text="🔊 Configurações de Narração",
            font=('Helvetica', 14, 'bold'),
            fg='#ffffff',
            bg='#2d2d2d',
            relief=tk.FLAT,
            bd=0
        )
        narration_frame.pack(fill=tk.X, padx=15, pady=15)
        
        # Velocidade da narração
        tk.Label(
            narration_frame,
            text="⚡ Velocidade da narração:",
            font=('Helvetica', 12),
            fg='#ffffff',
            bg='#2d2d2d'
        ).pack(pady=5)
        
        self.speed_scale = tk.Scale(
            narration_frame,
            from_=0.5,
            to=2.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            bg='#2d2d2d',
            fg='#ffffff',
            highlightbackground='#2d2d2d',
            troughcolor='#404040',
            activebackground='#3498db',
            command=self.update_speed
        )
        self.speed_scale.set(1.0)
        self.speed_scale.pack(pady=(0, 10))
        
        # Botões de ação
        action_frame = tk.Frame(settings_frame, bg='#2d2d2d')
        action_frame.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Button(
            action_frame,
            text="✅ Aplicar Configurações",
            font=('Helvetica', 11),
            bg='#27ae60',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=self.apply_settings,
            activebackground='#2ecc71',
            activeforeground='white'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            action_frame,
            text="🔄 Restaurar Padrões",
            font=('Helvetica', 11),
            bg='#3498db',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=self.reset_settings,
            activebackground='#2980b9',
            activeforeground='white'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            action_frame,
            text="🚪 Sair",
            font=('Helvetica', 11),
            bg='#e74c3c',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=self.quit_app,
            activebackground='#c0392b',
            activeforeground='white'
        ).pack(side=tk.RIGHT)
    
    def update_sensitivity(self, value):
        """Atualiza a sensibilidade do microfone"""
        self.recognizer.energy_threshold = int(value)
    
    def update_speed(self, value):
        """Atualiza a velocidade da narração"""
        try:
            if self.speech_engine:
                # Tratar valores com vírgula (formato brasileiro)
                if isinstance(value, str):
                    value = value.replace(',', '.')
                
                # Converter para float e aplicar multiplicador
                speed_value = float(value) * 150
                self.speech_engine.setProperty('rate', int(speed_value))
                print(f"✅ Velocidade atualizada: {value}x ({speed_value})")
        except Exception as e:
            print(f"❌ Erro ao atualizar velocidade: {e}")
            # Fallback para velocidade padrão
            try:
                self.speech_engine.setProperty('rate', 150)
            except:
                pass
    
    def update_translation_status(self):
        """Atualiza o status da tradução na barra"""
        status = "ON" if self.translation_mode.get() else "OFF"
        color = "#27ae60" if self.translation_mode.get() else "#e74c3c"
        self.trans_status.config(text=f"🌍 Tradução: {status}", fg=color)
    
    def update_language_status(self, event=None):
        """Atualiza o status do idioma na barra"""
        lang = self.language.get()
        self.lang_status.config(text=f"🗣️ {lang}")
    
    def apply_settings(self):
        """Aplica as configurações"""
        messagebox.showinfo("Configurações", "Configurações aplicadas com sucesso!")
    
    def reset_settings(self):
        """Restaura as configurações padrão"""
        self.sensitivity_scale.set(3000)
        self.speed_scale.set(1.0)
        self.recognizer.energy_threshold = 3000
        if self.speech_engine:
            self.speech_engine.setProperty('rate', 150)
        messagebox.showinfo("Configurações", "Configurações restauradas!")
    
    def paste_from_clipboard(self):
        """Cola texto do clipboard"""
        try:
            text = pyperclip.paste()
            self.input_text.delete(1.0, tk.END)
            self.input_text.insert(1.0, text)
            self.log_output(self.dictation_output, f"📋 Texto colado do clipboard: {len(text)} caracteres")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao colar do clipboard:\n{e}")
    
    def translate_text(self):
        """Traduz o texto de entrada"""
        try:
            text = self.input_text.get(1.0, tk.END).strip()
            if not text:
                messagebox.showwarning("Aviso", "Digite ou cole um texto para traduzir!")
                return
            
            # Obter direção da tradução
            direction = self.translation_direction.get()
            src, dest = direction.split('-')
            
            # Traduzir
            translated = self.translator.translate(text, src=src, dest=dest)
            
            # Mostrar resultado
            self.translation_output.delete(1.0, tk.END)
            self.translation_output.insert(1.0, translated.text)
            
            # Log
            self.log_output(self.dictation_output, f"🌍 Traduzido ({direction}): {len(text)} → {len(translated.text)} caracteres")
            
            # Narrar se ativado
            if self.auto_narrate.get() and self.speech_engine:
                self.narrate_text(translated.text)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na tradução:\n{e}")
    
    def narrate_text(self, text=None):
        """Narra o texto especificado"""
        if not self.speech_engine:
            messagebox.showwarning("Aviso", "Síntese de voz não disponível!")
            return
        
        try:
            if text is None:
                text = self.translation_output.get(1.0, tk.END).strip()
            
            if not text:
                messagebox.showwarning("Aviso", "Nenhum texto para narrar!")
                return
            
            # Narrar em thread separada
            threading.Thread(target=self._narrate_thread, args=(text,), daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na narração:\n{e}")
    
    def _narrate_thread(self, text):
        """Thread para narração"""
        try:
            self.speech_engine.say(text)
            self.speech_engine.runAndWait()
        except Exception as e:
            print(f"Erro na narração: {e}")
    
    def copy_translation(self):
        """Copia a tradução para o clipboard"""
        try:
            text = self.translation_output.get(1.0, tk.END).strip()
            if text:
                pyperclip.copy(text)
                messagebox.showinfo("Sucesso", "Tradução copiada para o clipboard!")
            else:
                messagebox.showwarning("Aviso", "Nenhuma tradução para copiar!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao copiar:\n{e}")
    
    def clear_output(self, text_widget):
        """Limpa a área de texto especificada"""
        text_widget.delete(1.0, tk.END)
    
    def copy_last_text(self, text_widget):
        """Copia o último texto reconhecido"""
        try:
            lines = text_widget.get(1.0, tk.END).split('\n')
            for line in reversed(lines):
                if "Reconhecido:" in line:
                    text = line.split("Reconhecido:")[1].strip()
                    pyperclip.copy(text)
                    messagebox.showinfo("Sucesso", f"Texto copiado: {text}")
                    break
            else:
                messagebox.showwarning("Aviso", "Nenhum texto para copiar!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao copiar:\n{e}")
    
    def log_output(self, text_widget, message):
        """Adiciona mensagem à área de saída"""
        timestamp = time.strftime("%H:%M:%S")
        full_message = f"[{timestamp}] {message}\n"
        
        # Executar na thread principal
        self.root.after(0, lambda: text_widget.insert(tk.END, full_message))
        self.root.after(0, lambda: text_widget.insert(tk.END, full_message))
        self.root.after(0, lambda: text_widget.see(tk.END))
    
    def setup_speech_recognition(self):
        """Configura o reconhecimento de voz"""
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            self.update_status("✅ Microfone configurado", "green")
        except Exception as e:
            self.update_status(f"❌ Erro no microfone: {e}", "red")
            messagebox.showerror("Erro", f"Não foi possível configurar o microfone:\n{e}")
    
    def create_app_icons(self):
        """Cria ícones para a aplicação"""
        try:
            # Criar ícone padrão (microfone azul)
            self.original_icon = self.create_microphone_icon('#3498db')
            
            # Criar ícone de gravação (microfone vermelho)
            self.recording_icon = self.create_microphone_icon('#e74c3c')
            
            # Definir ícone padrão
            self.root.iconphoto(True, self.original_icon)
            
            print("✅ Ícones criados com sucesso")
            
        except Exception as e:
            print(f"❌ Erro ao criar ícones: {e}")
    
    def create_microphone_icon(self, color):
        """Cria um ícone de microfone com a cor especificada"""
        try:
            # Criar imagem 32x32
            img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Desenhar microfone
            # Base do microfone
            draw.ellipse([8, 20, 24, 28], fill=color, outline='#2c3e50', width=1)
            
            # Corpo do microfone
            draw.rectangle([12, 8, 20, 20], fill=color, outline='#2c3e50', width=1)
            
            # Topo do microfone
            draw.ellipse([10, 6, 22, 10], fill=color, outline='#2c3e50', width=1)
            
            # Grelha do microfone
            for i in range(3):
                y = 10 + i * 2
                draw.line([(12, y), (20, y)], fill='#2c3e50', width=1)
            
            # Converter para PhotoImage
            return ImageTk.PhotoImage(img)
            
        except Exception as e:
            print(f"❌ Erro ao criar ícone: {e}")
            return None
    
    def setup_system_tray(self):
        """Configura a bandeja do sistema"""
        try:
            print("✅ Configurando bandeja do sistema para Linux")
            self.setup_pystray_tray()
                
        except Exception as e:
            print(f"❌ Erro ao configurar bandeja do sistema: {e}")
    
    def setup_pystray_tray(self):
        """Configura bandeja usando pystray"""
        try:
            import pystray
            
            # Menu da bandeja
            menu = pystray.Menu(
                pystray.MenuItem("🔊 Mostrar", self.show_from_tray),
                pystray.MenuItem("🎤 Iniciar Ditado", self.toggle_listening),
                pystray.MenuItem("🌍 Tradução", self.toggle_translation),
                pystray.MenuItem("⚙️ Configurações", self.show_settings),
                pystray.MenuItem("🚪 Sair", self.quit_app)
            )
            
            # Criar ícone da bandeja
            self.tray_icon = pystray.Icon(
                "tradutor",
                self.original_icon,
                "🎤 Ferramenta de Ditado",
                menu
            )
            
            print("✅ Bandeja do sistema configurada com pystray")
            
        except Exception as e:
            print(f"❌ Erro ao configurar pystray: {e}")
            print("⚠️ Fallback: usando método alternativo")
            self.setup_fallback_tray()
    
    def setup_fallback_tray(self):
        """Configura fallback para bandeja"""
        try:
            print("✅ Usando método alternativo de bandeja")
            self.tray_icon = None
            
        except Exception as e:
            print(f"❌ Erro no método alternativo: {e}")
    
    def minimize_to_tray(self):
        """Minimiza a aplicação para a bandeja do sistema"""
        try:
            print("🔄 Minimizando para bandeja...")
            
            # Esconder janela principal
            self.root.withdraw()
            self.is_minimized = True
            
            # Mostrar notificação
            self.show_tray_notification("🎤 Aplicação minimizada para bandeja")
            
            # Iniciar bandeja se disponível
            if hasattr(self, 'tray_icon') and self.tray_icon:
                try:
                    # Executar bandeja em thread separada
                    tray_thread = threading.Thread(target=self.run_tray_icon, daemon=True)
                    tray_thread.start()
                    print("✅ Bandeja iniciada com sucesso")
                except Exception as e:
                    print(f"⚠️ Erro ao iniciar bandeja: {e}")
            else:
                print("⚠️ Bandeja não disponível, usando fallback")
                # Fallback: mostrar janela de restauração
                self.create_restore_window()
            
        except Exception as e:
            print(f"❌ Erro ao minimizar para bandeja: {e}")
            # Fallback: apenas esconder
            self.root.withdraw()
    
    def run_tray_icon(self):
        """Executa o ícone da bandeja em thread separada"""
        try:
            if self.tray_icon:
                print("🔄 Iniciando ícone da bandeja...")
                self.tray_icon.run()
                print("✅ Ícone da bandeja iniciado")
        except Exception as e:
            print(f"❌ Erro ao executar bandeja: {e}")
    
    def create_restore_window(self):
        """Cria uma janela pequena para restaurar a aplicação (fallback)"""
        try:
            # Criar janela de restauração
            self.restore_window = tk.Toplevel()
            self.restore_window.title("🎤 Ditado Inteligente")
            self.restore_window.geometry("350x160")
            self.restore_window.configure(bg='#2d2d2d')
            self.restore_window.resizable(False, False)
            
            # Centralizar na tela
            self.restore_window.geometry("+%d+%d" % (
                (self.restore_window.winfo_screenwidth() // 2) - 175,
                (self.restore_window.winfo_screenheight() // 2) - 80
            ))
            
            # Sempre no topo
            self.restore_window.attributes('-topmost', True)
            
            # Frame principal com padding
            main_frame = tk.Frame(self.restore_window, bg='#2d2d2d')
            main_frame.pack(expand=True, fill='both', padx=20, pady=15)
            
            # Conteúdo da janela
            title_label = tk.Label(
                main_frame,
                text="🎤 Ditado Inteligente",
                font=('Helvetica', 18, 'bold'),
                fg='white',
                bg='#2d2d2d'
            )
            title_label.pack(pady=(0, 8))
            
            status_label = tk.Label(
                main_frame,
                text="Aplicação minimizada para bandeja",
                font=('Helvetica', 11),
                fg='#95a5a6',
                bg='#2d2d2d'
            )
            status_label.pack(pady=(0, 20))
            
            # Frame para botões
            button_frame = tk.Frame(main_frame, bg='#2d2d2d')
            button_frame.pack()
            
            # Botão para restaurar
            restore_button = tk.Button(
                button_frame,
                text="🔊 Restaurar Aplicação",
                font=('Helvetica', 13, 'bold'),
                bg='#3498db',
                fg='white',
                relief=tk.FLAT,
                padx=35,
                pady=18,
                command=self.show_from_tray,
                activebackground='#2980b9',
                activeforeground='white',
                cursor='hand2'
            )
            restore_button.pack()
            
            # Aplicar borda redonda ao botão
            self.apply_rounded_button(restore_button, '#3498db', '#2980b9')
            
            # Configurar fechamento - X fecha definitivamente
            self.restore_window.protocol("WM_DELETE_WINDOW", self.quit_app)
            
            print("✅ Janela de restauração criada (fallback)")
            
        except Exception as e:
            print(f"❌ Erro ao criar janela de restauração: {e}")
    
    def show_from_tray(self):
        """Mostra a aplicação da bandeja do sistema"""
        try:
            print("🔄 Restaurando aplicação...")
            
            # Mostrar janela principal
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
            self.is_minimized = False
            
            # Fechar janela de restauração se existir (fallback)
            if hasattr(self, 'restore_window') and self.restore_window:
                try:
                    self.restore_window.destroy()
                    self.restore_window = None
                except:
                    pass
            
            # Parar bandeja se estiver rodando
            if hasattr(self, 'tray_icon') and self.tray_icon:
                try:
                    if hasattr(self.tray_icon, 'visible') and self.tray_icon.visible:
                        print("🔄 Parando ícone da bandeja...")
                        self.tray_icon.stop()
                        print("✅ Ícone da bandeja parado")
                except Exception as e:
                    print(f"⚠️ Erro ao parar bandeja: {e}")
                
            print("✅ Aplicação restaurada com sucesso")
                
        except Exception as e:
            print(f"❌ Erro ao mostrar da bandeja: {e}")
    
    def show_tray_notification(self, message):
        """Mostra notificação da bandeja"""
        try:
            # Tentar usar notificação do sistema Linux
            os.system(f'notify-send "🎤 Ditado Inteligente" "{message}" --icon=dialog-information')
            print(f"✅ Notificação enviada: {message}")
                
        except Exception as e:
            print(f"⚠️ Erro na notificação: {e}")
    
    def show_settings(self):
        """Mostra a aba de configurações"""
        try:
            self.show_from_tray()
            self.notebook.select(2)  # Selecionar aba de configurações
            
        except Exception as e:
            print(f"❌ Erro ao mostrar configurações: {e}")
    
    def apply_rounded_button(self, button, normal_color, hover_color):
        """Aplica estilo de borda redonda ao botão"""
        try:
            # Configurar estilo personalizado
            button.configure(
                relief=tk.FLAT,
                borderwidth=0,
                highlightthickness=0
            )
            
            # Criar efeito de borda redonda
            def on_enter(e):
                button.configure(bg=hover_color)
                
            def on_leave(e):
                button.configure(bg=normal_color)
            
            # Vincular eventos de mouse
            button.bind('<Enter>', on_enter)
            button.bind('<Leave>', on_leave)
            
        except Exception as e:
            print(f"⚠️ Erro ao aplicar estilo redondo: {e}")
    
    def toggle_listening(self):
        """Ativa/desativa o reconhecimento de voz"""
        if not self.is_listening:
            self.start_listening()
        else:
            self.stop_listening()
    
    def start_listening(self):
        """Inicia o reconhecimento de voz"""
        self.is_listening = True
        self.toggle_button.config(text="⏸️ Parar Ditado", bg='#e74c3c', activebackground='#c0392b')
        self.update_status("🎤 Ouvindo... (fale agora)", "green")
        self.mic_status.config(text="🎤 Ouvindo...", fg='#27ae60')
        self.status_bar.config(bg='#2d2d2d')
        
        # Mudar ícone para gravação
        if self.recording_icon:
            self.root.iconphoto(True, self.recording_icon)
            if self.tray_icon:
                self.tray_icon.icon = self.recording_icon
        
        # Iniciar monitoramento de áudio para VU Meter
        self.start_audio_monitoring()
        
        # Iniciar thread de reconhecimento
        self.recognition_thread = threading.Thread(target=self.recognition_loop, daemon=True)
        self.recognition_thread.start()
    
    def stop_listening(self):
        """Para o reconhecimento de voz"""
        self.is_listening = False
        self.toggle_button.config(text="🎤 Iniciar Ditado", bg='#27ae60', activebackground='#2ecc71')
        self.update_status("⏸️ Pausado", "red")
        self.mic_status.config(text="⏸️ Pausado", fg='#e74c3c')
        self.status_bar.config(bg='#2d2d2d')
        
        # Restaurar ícone padrão
        if self.original_icon:
            self.root.iconphoto(True, self.original_icon)
            if self.tray_icon:
                self.tray_icon.icon = self.original_icon
        
        # Parar monitoramento de áudio
        self.stop_audio_monitoring()
    
    def recognition_loop(self):
        """Loop principal de reconhecimento"""
        try:
            with sr.Microphone() as source:
                while self.is_listening:
                    try:
                        audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=15)
                        
                        if self.is_listening:
                            threading.Thread(target=self.process_audio, args=(audio,), daemon=True).start()
                            
                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        continue
                    except Exception as e:
                        self.log_output(self.dictation_output, f"⚠️ Erro: {e}")
                        continue
                        
        except Exception as e:
            self.log_output(self.dictation_output, f"❌ Erro no microfone: {e}")
            self.stop_listening()
    
    def process_audio(self, audio):
        """Processa o áudio reconhecido"""
        try:
            text = self.recognizer.recognize_google(audio, language=self.language.get())
            
            if text:
                self.log_output(self.dictation_output, f"🎤 Reconhecido: {text}")
                
                if self.translation_mode.get() and self.language.get() == 'pt-BR':
                    try:
                        translated = self.translator.translate(text, src='pt', dest='en')
                        final_text = translated.text
                        self.log_output(self.dictation_output, f"🌍 Traduzido: {final_text}")
                    except Exception as e:
                        final_text = text
                        self.log_output(self.dictation_output, f"⚠️ Erro na tradução: {e}")
                else:
                    final_text = text
                
                self.log_output(self.dictation_output, f"✍️ Digitando: {final_text}")
                
                pyautogui.write(final_text + " ")
                
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            self.log_output(self.dictation_output, f"❌ Erro na requisição: {e}")
        except Exception as e:
            self.log_output(self.dictation_output, f"⚠️ Erro inesperado: {e}")
    
    def update_status(self, message, color):
        """Atualiza o status do microfone"""
        color_map = {
            "green": "#27ae60",
            "red": "#e74c3c",
            "yellow": "#f39c12",
            "blue": "#3498db"
        }
        
        # Atualizar status na barra
        self.mic_status.config(fg=color_map.get(color, "#ecf0f1"))
    
    def update_vu_meter(self, level):
        """Atualiza o VU Meter com o nível de áudio"""
        try:
            # Converter nível para dB (0-100)
            if level > 0:
                db_level = min(100, int(level * 100))
            else:
                db_level = 0
            
            # Atualizar barra visual
            bar_width = int((db_level / 100) * 280) + 10
            self.vu_canvas.coords(self.audio_bar, 10, 30, bar_width, 10)
            
            # Mudar cor baseado no nível
            if db_level < 30:
                color = '#27ae60'  # Verde (baixo)
            elif db_level < 70:
                color = '#f39c12'  # Laranja (médio)
            else:
                color = '#e74c3c'  # Vermelho (alto)
            
            self.vu_canvas.itemconfig(self.audio_bar, fill=color, outline=color)
            
            # Atualizar label de nível
            self.level_label.config(text=f"{db_level} dB")
            
            # Debug
            if level > 0.01:
                print(f"🎤 VU Meter: {db_level} dB (nível: {level:.4f})")
            
        except Exception as e:
            print(f"❌ Erro ao atualizar VU Meter: {e}")
            # Resetar VU Meter em caso de erro
            try:
                self.vu_canvas.coords(self.audio_bar, 10, 30, 10, 10)
                self.level_label.config(text="0 dB")
            except:
                pass
    
    def start_audio_monitoring(self):
        """Inicia o monitoramento de áudio para o VU Meter"""
        try:
            # Verificar se já existe uma instância de PyAudio
            if hasattr(self, 'audio') and self.audio:
                self.audio.terminate()
            
            self.audio = pyaudio.PyAudio()
            
            # Listar dispositivos de entrada disponíveis
            info = self.audio.get_host_api_info_by_index(0)
            numdevices = info.get('deviceCount')
            
            # Encontrar dispositivo de entrada padrão
            input_device = None
            for i in range(0, numdevices):
                if (self.audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                    input_device = i
                    break
            
            if input_device is None:
                raise Exception("Nenhum dispositivo de entrada encontrado")
            
            self.audio_stream = self.audio.open(
                format=self.audio_format,
                channels=self.audio_channels,
                rate=self.audio_rate,
                input=True,
                input_device_index=input_device,
                frames_per_buffer=self.audio_chunk
            )
            
            self.is_recording_audio = True
            self.audio_frames = []
            
            # Atualizar status
            self.audio_status.config(text="🎤 Iniciando...", fg='#f39c12')
            
            # Thread para monitoramento de áudio
            self.audio_thread = threading.Thread(target=self.audio_monitor_loop, daemon=True)
            self.audio_thread.start()
            
            print("✅ Monitoramento de áudio iniciado com sucesso")
            
        except Exception as e:
            print(f"❌ Erro ao iniciar monitoramento de áudio: {e}")
            self.audio_status.config(text="❌ Erro no áudio", fg='#e74c3c')
            # Tentar usar reconhecimento de voz como fallback
            self.fallback_audio_monitoring()
    
    def fallback_audio_monitoring(self):
        """Método de fallback usando reconhecimento de voz para simular VU Meter"""
        try:
            self.audio_status.config(text="🔄 Modo fallback", fg='#f39c12')
            print("🔄 Usando modo fallback para monitoramento de áudio")
            
            # Simular monitoramento de áudio
            self.is_recording_audio = True
            self.audio_frames = []
            
            # Thread para simulação
            self.audio_thread = threading.Thread(target=self.fallback_audio_loop, daemon=True)
            self.audio_thread.start()
            
        except Exception as e:
            print(f"❌ Erro no modo fallback: {e}")
            self.audio_status.config(text="❌ Sem áudio", fg='#e74c3c')
    
    def fallback_audio_loop(self):
        """Loop de fallback para simular VU Meter"""
        try:
            while self.is_recording_audio:
                # Simular nível de áudio baseado no reconhecimento
                # Usar um valor aleatório baixo para simular silêncio
                import random
                level = random.uniform(0, 0.1)  # Simular silêncio
                
                # Atualizar VU Meter na thread principal
                self.root.after(0, lambda l=level: self.update_vu_meter(l))
                
                # Atualizar status
                self.root.after(0, lambda: self.audio_status.config(text="🔇 Modo fallback", fg='#95a5a6'))
                
                time.sleep(0.1)  # 100ms entre atualizações
                
        except Exception as e:
            print(f"❌ Erro no loop de fallback: {e}")
    
    def stop_audio_monitoring(self):
        """Para o monitoramento de áudio"""
        try:
            self.is_recording_audio = False
            if hasattr(self, 'audio_stream'):
                self.audio_stream.stop_stream()
                self.audio_stream.close()
            if hasattr(self, 'audio'):
                self.audio.terminate()
            
            # Resetar VU Meter
            self.update_vu_meter(0)
            self.audio_status.config(text="⏸️ Sem áudio", fg='#95a5a6')
            
        except Exception as e:
            print(f"Erro ao parar monitoramento de áudio: {e}")
    
    def audio_monitor_loop(self):
        """Loop de monitoramento de áudio para VU Meter"""
        try:
            print("🎤 Iniciando loop de monitoramento de áudio...")
            
            while self.is_recording_audio:
                try:
                    if hasattr(self, 'audio_stream') and self.audio_stream and self.audio_stream.is_active():
                        # Capturar dados de áudio
                        data = self.audio_stream.read(self.audio_chunk, exception_on_overflow=False)
                        self.audio_frames.append(data)
                        
                        # Calcular nível de áudio
                        audio_data = np.frombuffer(data, dtype=np.int16)
                        if len(audio_data) > 0:
                            rms = np.sqrt(np.mean(audio_data**2))
                            level = rms / 32768.0  # Normalizar para 0-1
                            
                            # Atualizar VU Meter na thread principal
                            self.root.after(0, lambda l=level: self.update_vu_meter(l))
                            
                            # Atualizar status
                            if level > 0.01:
                                self.root.after(0, lambda: self.audio_status.config(text="🎤 Capturando...", fg='#27ae60'))
                            else:
                                self.root.after(0, lambda: self.audio_status.config(text="🔇 Silêncio", fg='#95a5a6'))
                        
                        # Limitar frames para não consumir muita memória
                        if len(self.audio_frames) > 100:
                            self.audio_frames = self.audio_frames[-50:]
                        
                        time.sleep(0.05)  # 50ms entre atualizações
                    else:
                        print("⚠️ Stream de áudio não está ativo, usando fallback...")
                        # Se o stream não estiver ativo, usar fallback
                        self.fallback_audio_monitoring()
                        break
                        
                except Exception as e:
                    print(f"⚠️ Erro no loop de áudio: {e}")
                    # Continuar tentando
                    time.sleep(0.1)
                    
        except Exception as e:
            print(f"❌ Erro fatal no loop de monitoramento de áudio: {e}")
            # Usar fallback
            self.root.after(0, self.fallback_audio_monitoring)
    
    def play_captured_audio(self):
        """Reproduz o áudio capturado"""
        try:
            if not self.audio_frames:
                # Se não há áudio capturado, usar síntese de voz como fallback
                self.play_fallback_audio()
                return
            
            # Habilitar botão play
            self.play_button.config(state=tk.DISABLED, text="🔊 Reproduzindo...")
            
            # Thread para reprodução
            threading.Thread(target=self._play_audio_thread, daemon=True).start()
            
        except Exception as e:
            print(f"❌ Erro ao reproduzir áudio: {e}")
            # Tentar fallback
            self.play_fallback_audio()
    
    def play_fallback_audio(self):
        """Reproduz áudio de fallback usando síntese de voz"""
        try:
            if not self.speech_engine:
                messagebox.showwarning("Aviso", "Síntese de voz não disponível!")
                return
            
            # Desabilitar botão
            self.play_button.config(state=tk.DISABLED, text="🔊 Fallback...")
            
            # Texto de exemplo para reproduzir
            fallback_text = "Áudio capturado não disponível. Usando síntese de voz como alternativa."
            
            # Thread para síntese de voz
            threading.Thread(target=self._fallback_speech_thread, args=(fallback_text,), daemon=True).start()
            
        except Exception as e:
            print(f"❌ Erro no fallback de áudio: {e}")
            messagebox.showerror("Erro", f"Erro ao reproduzir áudio:\n{e}")
            self.play_button.config(state=tk.NORMAL, text="🔊 Play")
    
    def _fallback_speech_thread(self, text):
        """Thread para síntese de voz de fallback"""
        try:
            self.speech_engine.say(text)
            self.speech_engine.runAndWait()
            
            # Restaurar botão
            self.root.after(0, lambda: self.play_button.config(state=tk.NORMAL, text="🔊 Play"))
            
        except Exception as e:
            print(f"❌ Erro na síntese de voz: {e}")
            self.root.after(0, lambda: self.play_button.config(state=tk.NORMAL, text="🔊 Play"))
    
    def _play_audio_thread(self):
        """Thread para reprodução de áudio"""
        try:
            # Criar arquivo temporário de áudio
            temp_audio = io.BytesIO()
            
            # Salvar frames como WAV
            with wave.open(temp_audio, 'wb') as wav_file:
                wav_file.setnchannels(self.audio_channels)
                wav_file.setsampwidth(self.audio.get_sample_size(self.audio_format))
                wav_file.setframerate(self.audio_rate)
                wav_file.writeframes(b''.join(self.audio_frames))
            
            temp_audio.seek(0)
            
            # Reproduzir áudio
            temp_audio.seek(0)
            with wave.open(temp_audio, 'rb') as wav_file:
                # Configurar stream de reprodução
                play_stream = self.audio.open(
                    format=self.audio.get_format_from_width(wav_file.getsampwidth()),
                    channels=wav_file.getnchannels(),
                    rate=wav_file.getframerate(),
                    output=True
                )
                
                # Reproduzir dados
                data = wav_file.readframes(self.audio_chunk)
                while data:
                    play_stream.write(data)
                    data = wav_file.readframes(self.audio_chunk)
                
                play_stream.stop_stream()
                play_stream.close()
            
            # Restaurar botão
            self.root.after(0, lambda: self.play_button.config(state=tk.NORMAL, text="🔊 Play"))
            
        except Exception as e:
            print(f"Erro na reprodução de áudio: {e}")
            self.root.after(0, lambda: self.play_button.config(state=tk.NORMAL, text="🔊 Play"))
    
    def toggle_translation(self):
        """Liga/desliga a tradução"""
        self.translation_mode.set(not self.translation_mode.get())
        self.update_translation_status()
        status = "ATIVADA" if self.translation_mode.get() else "DESATIVADA"
        self.log_output(self.dictation_output, f"🌍 Tradução automática: {status}")
    
    def switch_language(self):
        """Troca o idioma de entrada"""
        current = self.language.get()
        languages = ['pt-BR', 'en-US', 'es-ES', 'fr-FR', 'de-DE']
        current_index = languages.index(current)
        next_index = (current_index + 1) % len(languages)
        self.language.set(languages[next_index])
        
        self.update_language_status()
        self.log_output(self.dictation_output, f"🗣️ Idioma alterado para: {languages[next_index]}")
    
    def quit_app(self):
        """Sai da aplicação"""
        try:
            if self.is_listening:
                self.stop_listening()
            
            # Criar popup de confirmação personalizado e centralizado
            if self.show_quit_confirmation():
                print("✅ Usuário confirmou saída da aplicação")
                self.root.quit()
            else:
                print("✅ Usuário cancelou saída da aplicação")
                
        except Exception as e:
            print(f"❌ Erro ao sair da aplicação: {e}")
            # Fallback: sair diretamente
            self.root.quit()
    
    def show_quit_confirmation(self):
        """Mostra popup de confirmação personalizado e centralizado"""
        try:
            # Criar janela de confirmação
            confirm_window = tk.Toplevel()
            confirm_window.title("🚪 Confirmar Saída")
            confirm_window.geometry("500x280")
            confirm_window.configure(bg='#2d2d2d')
            confirm_window.resizable(False, False)
            
            # Centralizar na tela com offset para evitar sobreposição
            screen_width = confirm_window.winfo_screenwidth()
            screen_height = confirm_window.winfo_screenheight()
            
            # Posicionar ligeiramente acima do centro para evitar sobreposição
            x_pos = (screen_width // 2) - 250
            y_pos = (screen_height // 2) - 140  # Offset para cima
            
            confirm_window.geometry("+%d+%d" % (x_pos, y_pos))
            
            # Sempre no topo com Z-index máximo
            confirm_window.attributes('-topmost', True)
            confirm_window.lift()  # Trazer para frente
            confirm_window.focus_force()  # Focar na janela
            
            # Variável para resultado
            result = tk.BooleanVar(value=False)
            
            # Frame principal com padding maior
            main_frame = tk.Frame(confirm_window, bg='#2d2d2d')
            main_frame.pack(expand=True, fill='both', padx=40, pady=40)
            
            # Ícone e título
            title_label = tk.Label(
                main_frame,
                text="🚪 Sair da Aplicação",
                font=('Helvetica', 18, 'bold'),
                fg='white',
                bg='#2d2d2d'
            )
            title_label.pack(pady=(0, 25))
            
            # Mensagem
            message_label = tk.Label(
                main_frame,
                text="Deseja realmente sair da aplicação?\n\nTodas as funcionalidades serão encerradas.",
                font=('Helvetica', 12),
                fg='#ecf0f1',
                bg='#2d2d2d',
                justify=tk.CENTER
            )
            message_label.pack(pady=(0, 35))
            
            # Frame para botões com espaçamento
            button_frame = tk.Frame(main_frame, bg='#2d2d2d')
            button_frame.pack()
            
            # Botão Cancelar com padding maior
            cancel_button = tk.Button(
                button_frame,
                text="❌ Cancelar",
                font=('Helvetica', 13, 'bold'),
                bg='#95a5a6',
                fg='white',
                relief=tk.FLAT,
                padx=40,
                pady=18,
                command=lambda: [result.set(False), confirm_window.destroy()],
                activebackground='#7f8c8d',
                activeforeground='white',
                cursor='hand2'
            )
            cancel_button.pack(side=tk.LEFT, padx=(0, 20))
            
            # Botão Sair com padding maior
            quit_button = tk.Button(
                button_frame,
                text="🚪 Sair",
                font=('Helvetica', 13, 'bold'),
                bg='#e74c3c',
                fg='white',
                relief=tk.FLAT,
                padx=40,
                pady=18,
                command=lambda: [result.set(True), confirm_window.destroy()],
                activebackground='#c0392b',
                activeforeground='white',
                cursor='hand2'
            )
            quit_button.pack(side=tk.LEFT, padx=(20, 0))
            
            # Aplicar bordas redondas
            self.apply_rounded_button(cancel_button, '#95a5a6', '#7f8c8d')
            self.apply_rounded_button(quit_button, '#e74c3c', '#c0392b')
            
            # Configurar fechamento
            confirm_window.protocol("WM_DELETE_WINDOW", lambda: [result.set(False), confirm_window.destroy()])
            
            # Garantir que está sempre no topo
            def keep_on_top():
                confirm_window.lift()
                confirm_window.attributes('-topmost', True)
                confirm_window.after(100, keep_on_top)
            
            keep_on_top()
            
            # Aguardar resultado
            confirm_window.wait_window()
            
            return result.get()
            
        except Exception as e:
            print(f"❌ Erro ao mostrar confirmação: {e}")
            # Fallback: usar messagebox padrão
            return messagebox.askokcancel("Sair", "Deseja realmente sair da aplicação?")
    
    def run(self):
        """Executa a aplicação"""
        self.root.mainloop()

def main():
    """Função principal"""
    try:
        app = CompactDictationGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Erro Fatal", f"Erro ao iniciar a aplicação:\n{e}")
        import sys
        sys.exit(1)

if __name__ == "__main__":
    main()