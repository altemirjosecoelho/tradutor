#!/usr/bin/env python3
"""
Configurações da Ferramenta de Ditado e Tradução Compacta
"""

# Configurações de interface
WINDOW_TITLE = "🎤 Ferramenta de Ditado e Tradução Inteligente"
WINDOW_SIZE = "900x600"
MIN_SIZE = (800, 500)

# Cores do tema dark
COLORS = {
    'primary': '#1a1a1a',      # Fundo principal
    'secondary': '#2d2d2d',    # Fundo secundário
    'text': '#404040',         # Fundo das áreas de texto
    'white': '#ffffff',        # Texto principal
    'gray': '#95a5a6',        # Texto secundário
    'green': '#27ae60',       # Botões de ação positiva
    'red': '#e74c3c',         # Botões de ação negativa
    'blue': '#3498db',        # Botões de informação
    'orange': '#f39c12',      # Botões de ação especial
    'purple': '#9b59b6'       # Botões de funcionalidade
}

# Configurações de áudio
AUDIO_CONFIG = {
    'energy_threshold': 3000,
    'dynamic_energy_threshold': True,
    'pause_threshold': 0.8,
    'phrase_time_limit': 15,
    'timeout': 5
}

# Configurações de síntese de voz
SPEECH_CONFIG = {
    'rate': 150,
    'volume': 0.9
}

# Idiomas suportados
SUPPORTED_LANGUAGES = [
    'pt-BR',  # Português Brasileiro
    'en-US',  # Inglês Americano
    'es-ES',  # Espanhol
    'fr-FR',  # Francês
    'de-DE',  # Alemão
    'it-IT',  # Italiano
    'ru-RU',  # Russo
    'ja-JP',  # Japonês
    'ko-KR',  # Coreano
    'zh-CN'   # Chinês Simplificado
]

# Direções de tradução disponíveis
TRANSLATION_DIRECTIONS = [
    'pt-en',  # Português → Inglês
    'en-pt',  # Inglês → Português
    'pt-es',  # Português → Espanhol
    'es-pt',  # Espanhol → Português
    'pt-fr',  # Português → Francês
    'fr-pt',  # Francês → Português
    'pt-de',  # Português → Alemão
    'de-pt',  # Alemão → Português
    'pt-it',  # Português → Italiano
    'it-pt'   # Italiano → Português
]

# Atalhos de teclado
HOTKEYS = {
    'toggle_listening': 'ctrl+shift+1',
    'toggle_translation': 'ctrl+shift+2',
    'switch_language': 'ctrl+shift+3',
    'quit_app': 'ctrl+shift+4'
}

# Configurações de interface
UI_CONFIG = {
    'tab_padding': 20,
    'button_padding': (30, 15),
    'text_area_height': 8,
    'status_bar_height': 30,
    'font_family': 'Helvetica',
    'font_size_large': 20,
    'font_size_medium': 14,
    'font_size_small': 12,
    'font_size_tiny': 9
}

# Configurações de performance
PERFORMANCE_CONFIG = {
    'max_threads': 4,
    'audio_buffer_size': 1024,
    'recognition_timeout': 10,
    'translation_timeout': 5
}