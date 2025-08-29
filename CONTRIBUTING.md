# 🤝 Contribuindo para o Projeto

Obrigado por considerar contribuir para a **Ferramenta de Ditado e Tradução Inteligente**! 🎤✨

## 📋 **Como Contribuir**

### **1. Reportar Bugs**
- Use a aba **Issues** do GitHub
- Descreva o problema detalhadamente
- Inclua passos para reproduzir
- Adicione screenshots se relevante
- Especifique seu sistema operacional

### **2. Sugerir Funcionalidades**
- Abra uma **Issue** com label "enhancement"
- Explique a funcionalidade desejada
- Descreva o caso de uso
- Discuta com outros contribuidores

### **3. Contribuir com Código**
- Faça um **Fork** do projeto
- Crie uma **Branch** para sua feature
- Implemente as mudanças
- Adicione testes se possível
- Faça um **Pull Request**

## 🚀 **Processo de Desenvolvimento**

### **Configuração do Ambiente**
```bash
# 1. Fork e clone
git clone https://github.com/SEU_USUARIO/tradutor.git
cd tradutor

# 2. Instalar dependências
pip3 install -r requirements.txt

# 3. Criar branch
git checkout -b feature/nova-funcionalidade
```

### **Padrões de Código**
- **Python**: PEP 8 (usar black ou flake8)
- **Documentação**: Docstrings em português
- **Commits**: Mensagens claras em português
- **Testes**: Adicionar testes para novas funcionalidades

### **Estrutura do Projeto**
```
tradutor/
├── scripts/                    # Código principal
├── docs/                      # Documentação
├── tests/                     # Testes
├── examples/                  # Exemplos de uso
└── requirements.txt           # Dependências
```

## 🎯 **Áreas para Contribuição**

### **Funcionalidades**
- [ ] Suporte a mais idiomas
- [ ] Reconhecimento offline
- [ ] Integração com APIs de IA
- [ ] Interface mobile
- [ ] Plugins para editores

### **Melhorias Técnicas**
- [ ] Otimização de performance
- [ ] Testes automatizados
- [ ] CI/CD pipeline
- [ ] Docker container
- [ ] Instalador universal

### **Documentação**
- [ ] Tutoriais em vídeo
- [ ] Exemplos práticos
- [ ] Traduções para outros idiomas
- [ ] Guias de troubleshooting
- [ ] API documentation

### **Interface**
- [ ] Temas adicionais
- [ ] Personalização avançada
- [ ] Atalhos configuráveis
- [ ] Widgets personalizados
- [ ] Integração com sistema

## 📝 **Template de Pull Request**

### **Título**
```
feat: Adiciona suporte a reconhecimento offline
```

### **Descrição**
```markdown
## 🎯 Descrição
Adiciona funcionalidade de reconhecimento offline usando Vosk

## 🔧 Mudanças
- Implementa reconhecimento offline
- Adiciona seleção de modelo de idioma
- Integra com interface existente

## ✅ Testes
- [ ] Testado no Linux
- [ ] Testado no Windows
- [ ] Funciona com microfone USB
- [ ] Compatível com Python 3.8+

## 📸 Screenshots
[Adicione screenshots se relevante]

## 🔗 Issues Relacionadas
Closes #123
```

## 🧪 **Testes**

### **Executar Testes**
```bash
# Testes básicos
python3 -m pytest tests/

# Testes com cobertura
python3 -m pytest --cov=scripts tests/

# Linting
flake8 scripts/
black --check scripts/
```

### **Criar Testes**
```python
# tests/test_dictation.py
import pytest
from scripts.dictation_gui_compact import CompactDictationGUI

def test_gui_initialization():
    """Testa inicialização da interface"""
    app = CompactDictationGUI()
    assert app.root is not None
    assert app.is_listening == False
```

## 📚 **Documentação**

### **Adicionar Documentação**
- **README**: Atualizar com novas funcionalidades
- **Docstrings**: Comentar código em português
- **Exemplos**: Criar casos de uso práticos
- **Tutoriais**: Guias passo a passo

### **Formato de Documentação**
```python
def nova_funcao(parametro):
    """
    Descrição da função em português.
    
    Args:
        parametro: Descrição do parâmetro
        
    Returns:
        Descrição do retorno
        
    Example:
        >>> resultado = nova_funcao("teste")
        >>> print(resultado)
        'Resultado do teste'
    """
    pass
```

## 🚀 **Deploy e Release**

### **Versionamento**
- **SemVer**: MAJOR.MINOR.PATCH
- **Changelog**: Documentar mudanças
- **Release notes**: Notas de lançamento
- **Binários**: Distribuições para diferentes sistemas

### **Processo de Release**
1. **Desenvolver** funcionalidades
2. **Testar** em diferentes ambientes
3. **Documentar** mudanças
4. **Criar** tag de versão
5. **Publicar** release no GitHub

## 🤝 **Comunidade**

### **Canais de Comunicação**
- **GitHub Issues**: Bugs e funcionalidades
- **GitHub Discussions**: Discussões gerais
- **Pull Requests**: Contribuições de código
- **Wiki**: Documentação colaborativa

### **Código de Conduta**
- **Respeito**: Tratar todos com respeito
- **Inclusão**: Bem-vindo a todos os níveis
- **Colaboração**: Trabalhar em conjunto
- **Aprendizado**: Compartilhar conhecimento

## 📋 **Checklist para Contribuição**

### **Antes de Enviar**
- [ ] Código segue padrões do projeto
- [ ] Testes passam localmente
- [ ] Documentação atualizada
- [ ] Commit messages claras
- [ ] Branch atualizada com main

### **Pull Request**
- [ ] Descrição clara das mudanças
- [ ] Screenshots se relevante
- [ ] Testes incluídos
- [ ] Documentação atualizada
- [ ] Issues relacionadas mencionadas

## 🎉 **Reconhecimento**

### **Contribuidores**
- Nome adicionado ao README
- Créditos no changelog
- Agradecimento em releases
- Badge de contribuidor

### **Tipos de Contribuição**
- 🐛 **Bug fixes**
- ✨ **Nova funcionalidade**
- 📚 **Documentação**
- 🧪 **Testes**
- 🎨 **Interface**
- 🚀 **Performance**

---

## 🚀 **Comece a Contribuir Agora!**

1. **Fork** o projeto
2. **Clone** seu fork
3. **Crie** uma branch
4. **Implemente** suas mudanças
5. **Teste** tudo
6. **Envie** um Pull Request

**🎤 Juntos podemos criar a melhor ferramenta de ditado do mundo!** ✨🤝