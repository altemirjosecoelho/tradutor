# 🚀 Guia de Instalação - Ferramenta de Ditado e Tradução

## 📋 **Pré-requisitos**

### **Sistema Operacional**
- ✅ **Linux**: Ubuntu 20.04+, Debian 11+, Fedora 35+, Arch Linux
- ✅ **Windows**: Windows 10, Windows 11
- ✅ **macOS**: macOS 10.15+ (Catalina)

### **Python**
- ✅ **Versão**: Python 3.8 ou superior
- ✅ **Pip**: Gerenciador de pacotes Python
- ✅ **Tkinter**: Interface gráfica (incluído no Python)

### **Hardware**
- ✅ **Microfone**: Funcional e configurado
- ✅ **Memória RAM**: Mínimo 4 GB, recomendado 8 GB+
- ✅ **Processador**: Dual-core 2.0 GHz+
- ✅ **Internet**: Conexão estável para APIs Google

## 🔧 **Instalação por Sistema Operacional**

### **🐧 Linux (Ubuntu/Debian)**

#### **1. Atualizar o sistema**
```bash
sudo apt update && sudo apt upgrade -y
```

#### **2. Instalar Python e dependências do sistema**
```bash
sudo apt install -y python3 python3-pip python3-tk python3-dev portaudio19-dev
```

#### **3. Instalar dependências Python**
```bash
pip3 install --user pyautogui pynput googletrans==4.0.0rc1 SpeechRecognition Pillow pyttsx3 pyperclip
```

#### **4. Verificar instalação**
```bash
python3 -c "import tkinter, pyautogui, pynput, googletrans, speech_recognition, PIL, pyttsx3, pyperclip; print('✅ Todas as dependências instaladas!')"
```

---

### **🐧 Linux (Fedora/RHEL)**

#### **1. Atualizar o sistema**
```bash
sudo dnf update -y
```

#### **2. Instalar Python e dependências do sistema**
```bash
sudo dnf install -y python3 python3-pip python3-tkinter python3-devel portaudio-devel
```

#### **3. Instalar dependências Python**
```bash
pip3 install --user pyautogui pynput googletrans==4.0.0rc1 SpeechRecognition Pillow pyttsx3 pyperclip
```

---

### **🐧 Linux (Arch Linux)**

#### **1. Atualizar o sistema**
```bash
sudo pacman -Syu
```

#### **2. Instalar Python e dependências do sistema**
```bash
sudo pacman -S python python-pip tk portaudio
```

#### **3. Instalar dependências Python**
```bash
pip3 install --user pyautogui pynput googletrans==4.0.0rc1 SpeechRecognition Pillow pyttsx3 pyperclip
```

---

### **🪟 Windows**

#### **1. Instalar Python**
- Baixar Python 3.8+ de [python.org](https://python.org)
- **IMPORTANTE**: Marcar "Add Python to PATH" durante instalação
- Reiniciar o computador após instalação

#### **2. Abrir PowerShell como Administrador**
```powershell
# Verificar Python
python --version

# Atualizar pip
python -m pip install --upgrade pip
```

#### **3. Instalar dependências**
```powershell
pip install pyautogui pynput googletrans==4.0.0rc1 SpeechRecognition Pillow pyttsx3 pyperclip
```

---

### **🍎 macOS**

#### **1. Instalar Homebrew (se não tiver)**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### **2. Instalar Python**
```bash
brew install python3
```

#### **3. Instalar dependências do sistema**
```bash
brew install portaudio
```

#### **4. Instalar dependências Python**
```bash
pip3 install pyautogui pynput googletrans==4.0.0rc1 SpeechRecognition Pillow pyttsx3 pyperclip
```

---

## 📥 **Download e Configuração do Projeto**

### **1. Clonar o repositório**
```bash
git clone https://github.com/seu-usuario/tradutor.git
cd tradutor
```

### **2. Verificar estrutura**
```bash
ls -la
# Deve mostrar:
# - scripts/dictation_gui_compact.py
# - start_compact.sh
# - requirements.txt
# - README.md
# - README_INSTALL.md
```

### **3. Tornar script executável (Linux/macOS)**
```bash
chmod +x start_compact.sh
```

### **4. Verificar dependências**
```bash
python3 -c "
import tkinter, pyautogui, pynput, googletrans, speech_recognition, PIL, pyttsx3, pyperclip
print('✅ Todas as dependências estão instaladas!')
print('✅ Projeto configurado com sucesso!')
"
```

---

## 🧪 **Teste de Instalação**

### **1. Teste básico de Python**
```bash
python3 --version
pip3 --version
```

### **2. Teste de importações**
```bash
python3 -c "
print('🔍 Testando importações...')
import tkinter; print('✅ Tkinter OK')
import pyautogui; print('✅ PyAutoGUI OK')
import pynput; print('✅ Pynput OK')
import googletrans; print('✅ Googletrans OK')
import speech_recognition; print('✅ SpeechRecognition OK')
import PIL; print('✅ Pillow OK')
import pyttsx3; print('✅ Pyttsx3 OK')
import pyperclip; print('✅ Pyperclip OK')
print('🎉 Todas as importações funcionaram!')
"
```

### **3. Teste de microfone**
```bash
python3 -c "
import speech_recognition as sr
r = sr.Recognizer()
try:
    with sr.Microphone() as source:
        print('🎤 Microfone detectado!')
        print('🔊 Ajustando para ruído ambiente...')
        r.adjust_for_ambient_noise(source, duration=1)
        print('✅ Microfone configurado com sucesso!')
except Exception as e:
    print(f'❌ Erro no microfone: {e}')
"
```

### **4. Teste de síntese de voz**
```bash
python3 -c "
import pyttsx3
try:
    engine = pyttsx3.init()
    print('🔊 Motor de síntese de voz OK!')
    voices = engine.getProperty('voices')
    print(f'🎤 Vozes disponíveis: {len(voices)}')
    for voice in voices:
        print(f'   - {voice.name} ({voice.id})')
except Exception as e:
    print(f'❌ Erro na síntese de voz: {e}')
"
```

---

## 🚀 **Primeira Execução**

### **1. Executar a aplicação**
```bash
# Linux/macOS
./start_compact.sh

# Windows
python scripts/dictation_gui_compact.py
```

### **2. Verificar interface**
- ✅ Janela deve abrir com tema dark
- ✅ Três abas devem estar visíveis
- ✅ Barra de status inferior deve aparecer
- ✅ Botões devem estar funcionais

### **3. Teste de funcionalidades**
- 🎤 **Aba Ditado**: Clique em "Iniciar Ditado"
- 🌍 **Aba Tradução**: Cole texto e traduza
- ⚙️ **Aba Config**: Ajuste configurações

---

## 🔧 **Configuração de Microfone**

### **Linux (PulseAudio)**
```bash
# Abrir controle de áudio
pavucontrol

# Verificar dispositivos
pactl list short sources

# Definir microfone padrão
pactl set-default-source [ID_DO_MICROFONE]
```

### **Linux (ALSA)**
```bash
# Listar dispositivos
arecord -l

# Testar microfone
arecord -D hw:1,0 -f S16_LE -r 44100 -c 1 test.wav
```

### **Windows**
- Configurações → Sistema → Som → Entrada
- Selecionar microfone correto
- Testar microfone

### **macOS**
- Preferências do Sistema → Som → Entrada
- Selecionar microfone correto
- Ajustar nível de entrada

---

## 🐛 **Solução de Problemas**

### **Problema: "No module named 'tkinter'"**
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk

# macOS
brew install python-tk
```

### **Problema: "No module named 'pyaudio'"**
```bash
# Ubuntu/Debian
sudo apt install portaudio19-dev python3-pyaudio

# Fedora
sudo dnf install portaudio-devel python3-pyaudio

# Arch
sudo pacman -S portaudio python-pyaudio

# macOS
brew install portaudio
pip3 install pyaudio
```

### **Problema: Microfone não funciona**
```bash
# Verificar permissões
ls -la /dev/snd/

# Verificar usuário no grupo audio
groups $USER

# Adicionar usuário ao grupo audio
sudo usermod -a -G audio $USER

# Reiniciar sessão
```

### **Problema: Erro de permissão no script**
```bash
# Tornar executável
chmod +x start_compact.sh

# Verificar permissões
ls -la start_compact.sh
```

### **Problema: Interface não abre**
```bash
# Verificar display (Linux)
echo $DISPLAY

# Verificar variáveis de ambiente
env | grep DISPLAY

# Testar tkinter
python3 -c "import tkinter; root = tkinter.Tk(); root.destroy(); print('OK')"
```

---

## 📱 **Configuração de Atalhos de Teclado**

### **Linux (GNOME)**
1. Configurações → Teclado → Atalhos de Teclado
2. Adicionar atalhos personalizados:
   - `Ctrl+Shift+1`: `./start_compact.sh`
   - `Ctrl+Shift+2`: Ativar/desativar tradução
   - `Ctrl+Shift+3`: Trocar idioma

### **Linux (KDE)**
1. Configurações do Sistema → Atalhos de Teclado
2. Adicionar atalhos globais
3. Configurar comandos personalizados

### **Windows**
1. Criar atalhos no desktop
2. Propriedades → Atalho de Teclado
3. Definir combinações de teclas

### **macOS**
1. Preferências do Sistema → Teclado → Atalhos
2. Serviços → Atalhos personalizados
3. Configurar comandos

---

## 🔄 **Atualizações**

### **Atualizar dependências Python**
```bash
pip3 install --upgrade pyautogui pynput googletrans SpeechRecognition Pillow pyttsx3 pyperclip
```

### **Atualizar o projeto**
```bash
git pull origin main
chmod +x start_compact.sh
```

### **Verificar versões**
```bash
python3 -c "
import pyautogui, pynput, googletrans, speech_recognition, PIL, pyttsx3, pyperclip
print(f'PyAutoGUI: {pyautogui.__version__}')
print(f'Pynput: {pynput.__version__}')
print(f'Googletrans: {googletrans.__version__}')
print(f'SpeechRecognition: {speech_recognition.__version__}')
print(f'Pillow: {PIL.__version__}')
print(f'Pyttsx3: {pyttsx3.__version__}')
print(f'Pyperclip: {pyperclip.__version__}')
"
```

---

## 📚 **Recursos Adicionais**

### **Documentação**
- [Python SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [Google Translate API](https://pypi.org/project/googletrans/)
- [Tkinter Tutorial](https://docs.python.org/3/library/tkinter.html)
- [PyAutoGUI](https://pyautogui.readthedocs.io/)

### **Comunidade**
- [GitHub Issues](https://github.com/seu-usuario/tradutor/issues)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/python)
- [Python Discord](https://discord.gg/python)

### **Ferramentas Relacionadas**
- **Vosk**: Reconhecimento offline
- **DeepSpeech**: IA para reconhecimento
- **Azure Speech**: Serviço Microsoft
- **AWS Transcribe**: Serviço Amazon

---

## ✅ **Verificação Final**

Após a instalação, execute este comando para verificar tudo:

```bash
python3 -c "
print('🔍 VERIFICAÇÃO COMPLETA DE INSTALAÇÃO')
print('=' * 50)

# Verificar Python
import sys
print(f'✅ Python {sys.version}')

# Verificar dependências
deps = ['tkinter', 'pyautogui', 'pynput', 'googletrans', 'speech_recognition', 'PIL', 'pyttsx3', 'pyperclip']
for dep in deps:
    try:
        __import__(dep)
        print(f'✅ {dep}')
    except ImportError:
        print(f'❌ {dep}')

# Verificar microfone
try:
    import speech_recognition as sr
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('✅ Microfone funcionando')
except Exception as e:
    print(f'❌ Microfone: {e}')

# Verificar síntese de voz
try:
    import pyttsx3
    engine = pyttsx3.init()
    print('✅ Síntese de voz funcionando')
except Exception as e:
    print(f'❌ Síntese de voz: {e}')

print('=' * 50)
print('🎉 INSTALAÇÃO VERIFICADA!')
"
```

---

## 🎯 **Próximos Passos**

1. **✅ Instalar dependências** (conforme guia acima)
2. **✅ Configurar microfone** (verificar permissões)
3. **✅ Testar aplicação** (executar start_compact.sh)
4. **✅ Configurar atalhos** (opcional)
5. **✅ Personalizar configurações** (dentro da aplicação)

**🎤 Sua ferramenta de ditado está pronta para uso!** ✨