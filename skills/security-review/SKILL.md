---
name: security-review
description: >
  Use quando uma aplicação vai para produção e precisa de uma varredura completa
  antes: release candidate, entrega para cliente, feature grande fechada, app
  que nunca foi auditado, ou suspeita de exposição de dados. Use também quando a
  pergunta na mesa é "dá pra lançar?".
  Triggers: "security review", "auditoria", "audita o app", "revisão de
  segurança", "dá pra lançar", "pode subir pra produção", /security-review
---

# Security Review

Auditoria completa da aplicação: segurança, concorrência, confiabilidade,
acessibilidade, consistência visual e comportamento responsivo. Um passe
exaustivo, com veredito de release no fim.

**Relação com a skill `adversarial`:** lá o catálogo é proibido e as personas
derivam do alvo — a meta é profundidade, o achado que ninguém procurava. Aqui o
catálogo é fixo de propósito — a meta é cobertura, nada esquecido. Use
`adversarial` antes de mergear; use esta antes de lançar.

## Antes de começar

- **Não modifique código durante a auditoria.** Primeiro o relatório completo;
  o plano de correção vem depois dele, e a correção depois do plano.
- **Trace fluxos ponta a ponta**, não arquivo por arquivo. Auditoria por arquivo
  encontra lint; auditoria por fluxo encontra o IDOR.
- Cubra: arquitetura, fluxo de dados, chamadas de API, autenticação e
  autorização, gerência de estado, operações assíncronas, tratamento de erro e as
  interfaces que o usuário vê.
- **Codebase grande:** despache um agente por dimensão, em paralelo, cada um com
  o mesmo formato de achado. Um agente só percorrendo as seis dimensões perde
  qualidade nas últimas.

## 1. Vulnerabilidades e exposição de dados

- Falhas de autenticação e autorização: checagem de permissão ausente **no
  servidor**, escalação de privilégio, IDOR, acesso entre tenants.
- Informação sensível vazando por código client-side, variáveis de ambiente,
  resposta de API, log, analytics, URL, localStorage, sessionStorage, cookie,
  mensagem de erro ou source map.
- Injeção: SQL, comando, template, prompt, HTML e script, onde couber.
- XSS, CSRF, SSRF, redirect inseguro, upload sem validação, path traversal,
  sessão fraca, token guardado de forma insegura, fronteira de segurança ausente.
- Regra de banco, endpoint, política de CORS, bucket de storage, handler de
  webhook ou integração de terceiro permissiva demais.
- Segredo, API key, credencial, endpoint interno, dado pessoal ou detalhe de
  implementação exposto sem querer.
- Validação e sanitização ausente na fronteira de confiança. **Nunca assuma que
  validação no cliente basta.**

## 2. Concorrência e integridade de estado

- Submissão duplicada por clique repetido, retry, refresh ou request concorrente.
- Operação não idempotente que cria registro, pagamento, mensagem, reserva ou
  job duplicado.
- Estado obsoleto, falha de optimistic update, lost update, escrita conflitante,
  resposta assíncrona fora de ordem.
- Effect, subscription, listener, timer e request sem cleanup correto.
- Estado de UI em que a ação continua disponível com a operação já em curso.
- Invalidação de cache e divergência entre estado do cliente, do servidor e do
  que está persistido.
- Cenários de múltiplas abas, múltiplos dispositivos e rede ruim, onde couber.

## 3. Confiabilidade e falha

- Promise rejeitada sem tratamento, erro engolido, falha silenciosa, loading
  infinito, retry em loop, rollback incompleto.
- Estados ausentes: loading, vazio, erro, offline, timeout, sucesso parcial.
- Caminho de falha que deixa dado ou UI em estado inconsistente.
- Suposição sobre resposta de API, nulabilidade, ordenação, timing ou
  disponibilidade de rede que derruba em produção.
- Vazamento de memória, rerender desnecessário, operação cara e gargalo óbvio
  que o usuário sente.

## 4. Acessibilidade

- HTML semântico: landmark, heading, label, lista, tabela, botão e link corretos.
- Navegação por teclado, ordem de tab lógica, foco visível, foco preso em modal,
  foco restaurado ao fechar.
- Nome acessível, label, descrição e atributo ARIA ausentes ou errados.
- Contraste, legibilidade, tamanho de alvo de toque, comportamento no zoom,
  suporte a reduced-motion, e significado comunicado só por cor.
- Comportamento de leitor de tela em modal, menu, dropdown, tab, toast, erro de
  validação, estado de carregamento e conteúdo atualizado dinamicamente.
- Formulário com instrução obscura, validação inacessível, `autocomplete`
  ausente, recuperação de erro ruim.
- Referência: **WCAG 2.2 AA**, onde aplicável.

## 5. Consistência visual e de interação

- Espaçamento, tipografia, cor, raio de borda, sombra, tamanho de ícone,
  alinhamento, dimensão de componente e comportamento responsivo inconsistentes.
- Componentes que parecem iguais e se comportam diferente, ou se comportam igual
  e estão implementados de formas diferentes.
- Uso incorreto ou inconsistente de design token e componente compartilhado.
- Estados ausentes ou inconsistentes: hover, focus, active, selected, disabled,
  loading, success, warning, destructive, error.
- Layout shift, clipping, overflow, truncamento, quebra de linha, problema de
  breakpoint, estado vazio inconsistente.
- Texto: terminologia divergente, capitalização, pontuação, formato de data,
  formato de número e label de ação inconsistentes.

## 6. Responsivo e casos de borda

- Telas estreitas, tablet, desktop, telas muito largas, interface com zoom,
  fonte grande do sistema.
- Nome longo, e-mail longo, texto traduzido ou expandido, valor vazio, dataset
  muito grande, zero resultados, conteúdo malformado.
- Suposições que só funcionam com conteúdo ideal ou num viewport específico.

## Formato de cada achado

| Campo | Conteúdo |
|---|---|
| **Severidade** | Critical · High · Medium · Low · Informational |
| **Categoria** | Segurança · Concorrência · Confiabilidade · Acessibilidade · Performance · Consistência visual |
| **Local** | Arquivo, componente, função, endpoint ou fluxo exato |
| **Problema** | O que está errado |
| **Impacto** | O que pode acontecer de verdade em produção |
| **Evidência** | O caminho de código, o comportamento ou a condição reproduzível |
| **Reprodução** | Passos para disparar ou conferir, onde couber |
| **Correção** | Remediação específica e acionável |
| **Confiança** | Confirmado · Alta confiança · Precisa verificar |

Priorize por **impacto real e explorabilidade**. Separe vulnerabilidade
confirmada de preocupação teórica, e não reporte suspeita sem evidência.

## Entrega

O relatório completo primeiro, agrupado por severidade e categoria. Depois dele:

1. **Plano de remediação priorizado**
2. **Quick wins** — o que dá pra corrigir com baixo risco de regressão
3. **O que exige mudança arquitetural** ou investigação mais funda
4. **Recomendação de release**, uma das três, com justificativa:
   **Pode lançar** · **Lançar com riscos conhecidos** · **Não lançar**

## Postura

Adversarial na parte de segurança. Sistemático na de acessibilidade. Preciso na
de UI.

Não pare no que o linter pegaria. Percorra fluxos reais e cenários de falha,
questione as suposições, e ache o que aparece com usuário de verdade, rede
instável, ações concorrentes e entrada maliciosa.
