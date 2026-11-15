# Planejamento TI

App web para planejar as atividades da TI e gerar relatórios (dia, semana, mês, trimestre, ano). É um site estático em um único `index.html`, sem build e sem dependências. Pode ser instalado no celular como aplicativo (PWA).

## Arquivos

| Arquivo | Para que serve |
| --- | --- |
| `index.html` | O app inteiro: telas, regras de classificação, relatórios e gráficos. |
| `manifest.webmanifest` | Nome, cores e ícones do app instalado no celular. |
| `sw.js` | Service worker: guarda o app para abrir rápido e funcionar sem internet no modo local. |
| `icons/` | Logo do app em todos os tamanhos. `gerar_icones.py` recria os ícones. |
| `vercel.json` | Cabeçalhos de segurança e de cache para a Vercel. |
| `.gitignore` | Impede que backups e relatórios com dados reais entrem no repositório. |

## Publicar

### 1. GitHub

1. Crie um repositório novo no GitHub (de preferência **privado**: o app traz o nome da empresa e as categorias de trabalho).
2. Envie esta pasta. Pelo site: **Add file → Upload files** e arraste o conteúdo da pasta. Pelo terminal, dentro da pasta:

```bash
git init
git add .
git commit -m "Primeira versão do Planejamento TI"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/planejamento-ti.git
git push -u origin main
```

### 2. Vercel

1. Em vercel.com, **Add New → Project** e importe o repositório.
2. **Framework Preset:** Other. Deixe Build Command e Output Directory vazios.
3. **Deploy.** Cada `git push` na `main` publica uma versão nova.

## Instalar no celular

- **Android (Chrome):** abra o site e toque em **Instalar app** (ou menu ⋮ → Instalar app).
- **iPhone (Safari):** abra o site, toque em **Compartilhar → Adicionar à Tela de Início**.

## Dados

O app não guarda dados no servidor da Vercel. Eles ficam em um destes lugares:

- **Modo local:** no navegador de cada aparelho. Cada endereço (arquivo no PC, site na Vercel, celular) tem seus próprios dados. Para levar os dados de um para outro, use **Ajustes → Baixar backup** e **Restaurar backup**.
- **Planilha do Google:** em **Ajustes → Conexão com a planilha**, cole a URL do app da web (termina em `/exec`) e o token. Assim todos os aparelhos veem os mesmos dados.

O token da planilha fica salvo só no navegador de quem conectou. **Nunca coloque o token, backups (`.json`) ou relatórios exportados no repositório.**

## Atualizar o app publicado

Depois de mudar o `index.html`, aumente `VERSAO` no topo do `sw.js` (por exemplo `pti-v1` → `pti-v2`) e publique. Assim os celulares com o app instalado trocam a versão guardada.

## Recriar os ícones

```bash
python icons/gerar_icones.py
```

Requer Python 3 e Pillow (`pip install pillow`).
