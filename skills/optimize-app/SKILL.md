---
name: optimize-app
description: >
  Use quando o usuário quer que o app fique mais rápido, no front ou no back:
  tempo de startup, abertura de cada tela, carregamento de conteúdo, scroll e
  carregamento de conteúdo antigo, bundle pesado, renders demais, requests em
  cascata, queries lentas. Acha onde está a lacuna real de performance, aplica as
  correções e mede antes e depois de cada uma. Triggers: "optimize app", "deixa o
  app mais rápido", "melhora a performance", "otimiza o startup", "app tá
  lento", "query lenta", "bundle pesado", /optimize-app
---

# Optimize app

O app a acelerar é o do projeto atual; se o usuário passou argumento, ele
delimita o foco (uma tela, um fluxo, uma plataforma).

Your job is to make this app faster. Improve the startup time, how fast each screen opens, how fast its content loads, and the scrolling, so everything feels lighter and older content loads faster. Find where the real performance gap is, apply the fixes, and benchmark before and after each one to see if it actually works or not.

## O que conta como medição

A linha de base vem antes de qualquer mudança, e do material mais cru que o
projeto tiver: traces e transações lentas de produção (Sentry, APM) contam mais
que uma medição local, porque mostram onde o usuário real espera. Sem isso, os
fluxos principais scriptados no Playwright e cronometrados, mais o instrumento
que mede a lacuna atacada — Web Vitals e a aba Performance do DevTools, o
profiler da framework para renders, o analisador de bundle do build, log de
queries com `EXPLAIN ANALYZE` no banco.

Antes e depois são medidos nas mesmas condições: mesmo build de produção, mesmo
dispositivo e throttling, mesmos dados, várias rodadas. Uma rodada só mede ruído,
e um ganho menor que a variação entre rodadas não é ganho.

## Antes de entregar

Reverta toda correção que não mostrou ganho: ela fica no código como
complexidade sem retorno. Rode de novo os fluxos do Playwright (ou os testes do
projeto) para mostrar que nada quebrou.

Entregue uma tabela com uma linha por correção — o que mudou, a métrica, antes,
depois — incluindo as revertidas, com o número que as derrubou.
