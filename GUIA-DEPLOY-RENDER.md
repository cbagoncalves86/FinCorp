# 🚀 GUIA PASSO A PASSO - DEPLOY NO RENDER.COM

## 📦 ARQUIVOS NECESSÁRIOS

Você precisa dos seguintes arquivos (TODOS já foram criados):

1. ✅ `backend-beta-api.py` - O código principal
2. ✅ `requirements.txt` - Dependências Python
3. ✅ `Procfile` - Comando de inicialização
4. ✅ `runtime.txt` - Versão do Python

**BAIXE TODOS OS 4 ARQUIVOS!**

---

## 🌐 PASSO A PASSO COMPLETO

### **PASSO 1: Criar Conta no Render**

1. Vá em: **https://render.com**
2. Clique em **"Get Started for Free"**
3. Escolha uma opção:
   - **Sign up with GitHub** (recomendado)
   - **Sign up with GitLab**
   - **Sign up with Google**
   - Ou crie com email

4. Confirme seu email se necessário

✅ **Conta criada!**

---

### **PASSO 2A: OPÇÃO GITHUB (Recomendada)**

Se você tem ou criou conta GitHub:

1. **Criar repositório no GitHub:**
   - Vá em: https://github.com
   - Clique no **"+"** no canto superior direito
   - Escolha **"New repository"**
   - Nome: `uhy-beta-calculator`
   - Deixe **Public**
   - Clique **"Create repository"**

2. **Fazer upload dos arquivos:**
   - Na página do repositório criado
   - Clique em **"uploading an existing file"**
   - Arraste os 4 arquivos para a área de upload:
     - `backend-beta-api.py`
     - `requirements.txt`
     - `Procfile`
     - `runtime.txt`
   - Clique **"Commit changes"**

3. **Conectar ao Render:**
   - Volte para https://render.com
   - No dashboard, clique **"New +"**
   - Escolha **"Web Service"**
   - Clique **"Build and deploy from a Git repository"**
   - Clique **"Connect GitHub"** (autorize se necessário)
   - Encontre o repositório `uhy-beta-calculator`
   - Clique **"Connect"**

4. **Configure (já vem quase tudo preenchido):**
   - **Name:** `uhy-beta-calculator` (ou escolha outro)
   - **Region:** Escolha o mais próximo (ex: Oregon (US West))
   - **Branch:** `main`
   - **Root Directory:** deixe vazio
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python backend-beta-api.py`
   - **Instance Type:** **Free**

5. Clique **"Create Web Service"**

6. **AGUARDE ~5-10 minutos** enquanto faz deploy
   - Você vai ver logs aparecendo
   - Quando aparecer "Live" com bolinha verde = PRONTO!

7. **Pegue a URL:**
   - No topo da página vai ter algo como:
   ```
   https://uhy-beta-calculator.onrender.com
   ```
   - **COPIE ESSA URL!**

---

### **PASSO 2B: OPÇÃO SEM GITHUB (Alternativa)**

Se NÃO quiser usar GitHub:

1. **No Render Dashboard:**
   - Clique **"New +"**
   - Escolha **"Web Service"**
   - Escolha **"Deploy from Git"**
   - Depois **"Public Git repository"**
   
2. **Problema:** Render precisa de um repositório Git

3. **SOLUÇÃO ALTERNATIVA - Railway.app:**
   - Railway permite upload direto de arquivos
   - Vá em: https://railway.app
   - Crie conta (GitHub ou Email)
   - Clique **"Start a New Project"**
   - Escolha **"Deploy from GitHub repo"** OU **"Empty Project"**
   - Se escolher Empty Project:
     - Clique no projeto criado
     - Clique **"+ New"** → **"Empty Service"**
     - Nas configurações, adicione os arquivos
   
Railway é mais simples mas tem limite de horas grátis (500h/mês = ~16h/dia)

---

### **PASSO 3: TESTAR SE FUNCIONOU**

1. Abra seu navegador
2. Cole a URL que o Render te deu + `/health`
   ```
   https://sua-url.onrender.com/health
   ```

3. Deve aparecer:
   ```json
   {
     "status": "ok",
     "message": "UHY Beta Calculator API funcionando"
   }
   ```

✅ **SE APARECEU ISSO = SUCESSO TOTAL!**

---

### **PASSO 4: ME AVISAR**

Me mande a URL completa, exemplo:
```
https://uhy-beta-calculator.onrender.com
```

Aí eu crio o **frontend HTML** que se conecta nessa URL e você pode usar! 🎉

---

## 🆘 PROBLEMAS COMUNS

### **"Build failed"**
- Verifique se TODOS os 4 arquivos foram enviados
- Verifique se `requirements.txt` não tem erros de digitação

### **"Application failed to start"**
- Aguarde uns 2-3 minutos, pode estar inicializando
- Veja os logs (botão "Logs" no Render)

### **"Service unavailable"**
- Normal no plano grátis, aguarde ~30 segundos
- Render "dorme" após 15 min sem uso

### **Demora muito para responder**
- Primeira requisição demora ~1 min (plano grátis)
- Depois fica rápido

---

## 💡 DICAS

1. **URL personalizada:** Você pode mudar o nome do serviço nas configurações
2. **Logs:** Sempre que der erro, veja os logs no dashboard
3. **Grátis:** 750 horas/mês grátis (suficiente para uso pessoal)
4. **Sem cartão:** Não precisa cartão de crédito

---

## 📞 PRECISA DE AJUDA?

Me avise em qual passo você está:

- [ ] Criei conta no Render
- [ ] Criei repositório no GitHub
- [ ] Fiz upload dos 4 arquivos
- [ ] Conectei GitHub ao Render
- [ ] Deploy em andamento
- [ ] Deploy completo - tenho a URL
- [ ] Testei /health - funciona!

**Qualquer dúvida, me pergunte! Estou aqui! 😊**
