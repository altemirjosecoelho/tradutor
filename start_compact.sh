#!/bin/bash

# Script para executar a versão compacta da ferramenta de ditado

echo "🎨 Ferramenta de Ditado Compacta"
echo "================================="
echo "🖥️  Versão Desktop com GUI Dark Moderna + Barra Horizontal"
echo ""

# Verificar se as dependências estão instaladas
if ! python3 -c "import tkinter, pyautogui, pynput, googletrans, speech_recognition, PIL, pyttsx3, pyperclip" 2>/dev/null; then
    echo "❌ Dependências não instaladas!"
    echo "📦 Execute: pip3 install --user tkinter pyautogui pynput googletrans==4.0.0rc1 SpeechRecognition Pillow pyttsx3 pyperclip"
    exit 1
fi

# Verificar microfone
echo "🔍 Verificando microfone..."
if ! python3 -c "import speech_recognition; r = speech_recognition.Recognizer(); print('Microfone OK')" 2>/dev/null; then
    echo "⚠️  Aviso: Problemas com microfone detectados"
    echo "💡 Verifique se o microfone está conectado e funcionando"
    echo "   Você pode continuar, mas pode haver problemas de áudio"
fi

# Verificar síntese de voz
echo "🔊 Verificando síntese de voz..."
if ! python3 -c "import pyttsx3; engine = pyttsx3.init(); print('Síntese de voz OK')" 2>/dev/null; then
    echo "⚠️  Aviso: Problemas com síntese de voz detectados"
    echo "💡 A funcionalidade de narração pode não funcionar"
fi

# Verificar internet
echo "🌐 Verificando conexão com internet..."
if ping -c 1 google.com &> /dev/null; then
    echo "✅ Conexão com internet OK"
else
    echo "❌ Sem conexão com internet!"
    echo "💡 Google Speech Recognition requer internet"
    exit 1
fi

echo ""
echo "✅ Tudo configurado! Iniciando aplicação compacta..."
echo ""
echo "🎯 CARACTERÍSTICAS DA VERSÃO COMPACTA:"
echo "   🎨 Design Dark moderno e elegante"
echo "   📱 Interface compacta e otimizada"
echo "   ⌨️ Atalhos de teclado visíveis (Ctrl+Shift+1)"
echo "   🌫️ Dois tons de cinza no background"
echo "   📊 Barra horizontal com status em tempo real"
echo "   🎤 Ditado + Tradução + Narração integrados"
echo ""
echo "🚀 Iniciando em 3 segundos..."
sleep 3

# Executar aplicação compacta
python3 scripts/dictation_gui_compact.py