# ChatBot com Interface Visual Moderna

Um chatbot com interface web moderna usando Flask, HTML5, CSS3 e JavaScript, conectado à API do ChatGPT.

## 🚀 Versões Disponíveis

### 1. Versão Terminal (chatbot.py)
- Interface simples no terminal
- Ideal para testes rápidos

### 2. Versão Web (app.py + templates/index.html)
- Interface visual moderna e responsiva
- Animações suaves
- Design elegante com gradientes
- Indicador de digitação
- Histórico de conversa
- Botão para limpar chat

## ✨ Funcionalidades da Interface Web

- 🎨 **Design Moderno**: Interface com gradientes e animações suaves
- 📱 **Responsivo**: Funciona perfeitamente em desktop e mobile
- 💬 **Chat em Tempo Real**: Mensagens instantâneas com a API do ChatGPT
- ⌨️ **Indicador de Digitação**: Mostra quando o bot está "pensando"
- 🗑️ **Limpar Chat**: Botão para reiniciar a conversa
- ⚡ **Atalhos**: Enviar mensagem com Enter
- 🔄 **Auto-scroll**: Rola automaticamente para novas mensagens
- ❌ **Tratamento de Erros**: Mensagens de erro amigáveis

## 🛠️ Como Executar

### Versão Terminal:
```bash
export OPENAI_API_KEY='sua-chave-aqui'
/home/admin/Desktop/Projetos/chatbot/.venv/bin/python chatbot.py
```

### Versão Web:
```bash
export OPENAI_API_KEY='sua-chave-aqui'
/home/admin/Desktop/Projetos/chatbot/.venv/bin/python app.py
```

Depois acesse: http://localhost:5000

## � Estrutura do Projeto

```
chatbot/
├── app.py                 # Backend Flask
├── chatbot.py            # Versão terminal
├── requirements.txt      # Dependências
├── templates/
│   └── index.html       # Interface web moderna
├── README.md            # Documentação
└── .env.example         # Exemplo de configuração
```

## 🎯 Tecnologias Utilizadas

### Backend:
- **Python 3.12**
- **Flask** - Framework web
- **OpenAI API** - Integração com ChatGPT
- **Flask-CORS** - Suporte a CORS

### Frontend:
- **HTML5** - Estrutura
- **CSS3** - Estilização moderna com flexbox e gradientes
- **JavaScript** - Interatividade e comunicação com API
- **Font Awesome** - Ícones

## � Personalização

### Modificar Aparência:
- Edite o CSS em `templates/index.html`
- Altere cores, gradientes e animações

### Alterar Comportamento do Bot:
- Modifique o prompt do sistema em `app.py`
- Ajuste parâmetros como `temperature` e `max_tokens`

### Adicionar Funcionalidades:
- Salvar conversas em banco de dados
- Upload de arquivos
- Múltiplas sessões de chat
- Temas escuro/claro

## 🌟 Interface

A interface inclui:
- Header com gradiente azul/roxo
- Área de mensagens com scroll personalizado
- Avatares para usuário e bot
- Animações de entrada das mensagens
- Indicador de digitação com pontos animados
- Campo de input com bordas arredondadas
- Botões com efeitos hover

## 🚀 Próximos Passos

1. **Banco de Dados**: Salvar histórico de conversas
2. **Autenticação**: Sistema de usuários
3. **Temas**: Modo escuro/claro
4. **Mobile App**: Versão nativa
5. **Deploy**: Hospedar na nuvem
