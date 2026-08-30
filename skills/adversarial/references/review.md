# Modo REVIEW — atacar um artefato pronto

Entrada: código, diff, spec, plano, feature pronta para merge.
Saída: DEFEITOS (corrijo) · DECISÕES (você responde) · FALSOS POSITIVOS (registrados).

## 1. Derivar as personas

**Leia o artefato inteiro antes de escolher qualquer coisa.**

Método: para cada parte substancial, pergunte **quem sofreria se isto estivesse
errado**. Essa pessoa é a persona.

| O artefato contém | A persona é |
|---|---|
| Modelo de dados | Quem vai migrar isto com dados reais dentro |
| Autenticação | Quem vai ser invadido por causa dela |
| Plano de deploy | Quem está de plantão às 3h da manhã |
| Contabilidade (quota, saldo, estoque) | O auditor que precisa fechar a conta |
| Testes | Quem confia neles para dormir tranquilo |
| Tarefas para agentes | O agente sem contexto que pega a tarefa 17 isolada |
| Um pedido do usuário | O usuário lendo o resultado, procurando o que pediu |
| Dependência de biblioteca | Quem roda `install` seis meses depois |
| Fluxo de arquivos/mídia | Quem sobe 400 fotos num 4G ruim |
| Decisões numeradas | Quem lê o documento daqui a um ano sem contexto |

**Quantidade: 4 a 15**, pela superfície real do artefato — não pelo tamanho em
linhas. Duas personas que fariam as mesmas perguntas viram uma: persona
redundante dilui sinal e gasta contexto.

### Persona obrigatória — Aderência ao real

Sempre presente, sob algum nome. O artefato afirma coisas sobre o mundo:
caminhos, linhas, assinaturas, versões, comportamento de plataforma, conteúdo de
outros repositórios. O trabalho dela é conferir **cada afirmação** contra o que
existe agora.

- Cada `file:line` citado existe e diz o que o artefato afirma?
- Cada símbolo referenciado existe com esse nome?
- Cada citação a outro documento aponta para o item certo?
- A branch está atrás da base? Algo mergeado redesenhou o que este trabalho edita?

Divergência aqui é CRITICAL/HIGH por padrão: artefato apoiado em algo que não
existe falha no primeiro passo.

## 2. Brief de cada agente

```
Você é um revisor adversarial. Seu mandato é ENCONTRAR FALHAS, não validar.

ARTEFATO: [caminhos]
DIRETÓRIO: [caminho absoluto, e em qual branch]
PERSONA: [quem você é, em uma frase — "você é quem vai operar isto às 3h"]

FOCO — hipóteses concretas que essa persona levantaria:
- [4 a 8 hipóteses ESPECÍFICAS deste artefato, não genéricas]
- [inclua as que você suspeita serem falsas — refutar também é resultado]

REGRAS
1. Toda afirmação carrega file:line, lido por você nesta sessão. Sem citação,
   não reporte.
2. Se um fato pode ser descoberto — no filesystem, na documentação oficial, ou
   RODANDO alguma coisa — DESCUBRA. Nunca reporte "não está claro se X" quando
   X é verificável.
3. Classifique cada achado:
   DEFEITO — o artefato contradiz o real, ou quebra sob entrada concreta.
             Descreva a ENTRADA que quebra, não o desconforto.
   DECISÃO — o artefato escolheu um caminho sem registrar a escolha, e a
             alternativa é defensável. Não é bug. Descreva as duas opções.
4. Diga também o que está CORRETO e você conferiu. O consolidador usa isso para
   derrubar falso positivo de outro agente — é metade do valor do seu relatório.
5. Responda explicitamente cada hipótese do FOCO, inclusive as que você refutou.

SAÍDA
[CRITICAL|HIGH|MEDIUM|LOW] [DEFEITO|DECISÃO] — file:line — problema —
consequência concreta — correção sugerida.
Um por parágrafo. Máximo 12 achados, os mais fortes.
```

Duas coisas mudam a qualidade do brief mais que qualquer outra:

- **Hipóteses específicas do artefato.** "Procure problemas de segurança" produz
  lugar-comum. "O `resolve()` filtra `deletedAt`? Um arquivo apagado continua
  servindo por link público?" produz achado.
- **Hipóteses que você suspeita serem falsas.** Refutada com evidência, ela te
  poupa de investigá-la depois — e o "conferi, está correto" vale tanto quanto
  um achado.

## 3. Triagem, antes de gastar verificador

| Achado | Destino |
|---|---|
| 3+ agentes independentes acharam sozinhos | Já corroborado. Não verifica. |
| Fonte única | Verificador A |
| Depende de fato externo (versão, plataforma, semântica de banco) | Verificador B, sempre |
| Outro agente disse "conferi, está correto" | Verificador decide |

## 4. Dois verificadores, em paralelo

**Verificador A — lógica interna**
```
Estes achados vieram de revisores adversariais. Seu mandato é REFUTAR.

Para cada um: abra o arquivo citado, leia o trecho E o contexto ao redor, siga o
caminho do dado. Determine se o cenário é reproduzível a partir do que está
escrito.

Assuma REFUTADO quando estiver em dúvida. Um achado sobrevive só se você
conseguir enunciar a ENTRADA CONCRETA que produz o comportamento errado.

Devolva CONFIRMADO (com o trecho lido e a entrada que quebra) ou REFUTADO (com o
que o documento realmente diz). Se for parcial, diga qual metade sobrevive.
```

**Verificador B — fatos externos**
```
Estes achados dependem de FATO EXTERNO. Seu mandato é REFUTAR.

Não se contente com documentação: quando der para VERIFICAR EMPIRICAMENTE,
verifique. Instale o pacote e rode. Suba o banco e meça. Faça a query e olhe o
EXPLAIN. Cite versão e data.

Assuma REFUTADO quando estiver em dúvida.

Devolva CONFIRMADO (com a evidência que você mesmo produziu ou leu, e a fonte)
ou REFUTADO (com o que a realidade diz).
```

O verificador B é o que mais paga: assinatura removida entre versões, default de
locale, índice que não vira o seletor que o código espera — nada disso aparece
lendo o artefato.

**Consolidação, depois da verificação:**

- 2+ agentes reportam o mesmo → confirmar, subir severidade
- 1 reporta, outro diz "conferi, está correto" → o verificador decide
- Refutado → registrar como **falso positivo investigado**, com o que o real faz.
  Nunca apagar.

## 5. Entregar, em três listas

**DEFEITOS** — tabela, e eu corrijo:

```
| # | Severidade | file:line | Problema | Correção |
```

Agrupe por **consequência**, não por dimensão de origem: *bloqueia execução*,
*segurança*, *perda de dados*, *corretude*. O usuário decide pelo que dói, não
por qual agente achou.

Ordem: CRITICAL bloqueia · HIGH antes de executar · MEDIUM se barato, senão
follow-up documentado · LOW vira comentário ou issue.

**DECISÕES** — uma por vez. Cada uma com as opções e a **sua recomendação
primeiro**, com o motivo. Não corrija em silêncio e não despeje todas de uma vez:
pergunta única, espera resposta, próxima.

**Resolva a dependência antes de perguntar.** A decisão que muda o significado
das outras vem primeiro — com 46 defeitos na mesa, a primeira pergunta é
*"corrigir ou reescrever?"*, porque a resposta dissolve metade das outras.

Decisão cuja alternativa não se sustenta **não é decisão**: escolha, diga que
escolheu e por quê, e siga.

**FALSOS POSITIVOS** — lista curta do que foi investigado e não se sustentou, com
o que o real faz.

## 6. Fechar

1. Nenhum CRITICAL/DEFEITO aberto
2. Toda DECISÃO respondida e refletida no artefato — **e nas decisões numeradas
   do projeto**, se houver. Decisão superada precisa ser marcada como superada no
   lugar onde ela mora, senão o próximo leitor implementa a versão velha.
3. Grave `REVIEW-<data>.md` com as três listas **e o que foi conferido e passou**.
   A última seção não é elogio: é o que impede a próxima rodada de reinvestigar o
   que já resistiu.
4. `fix(<escopo>): apply adversarial review findings`
5. MEDIUM/LOW não aplicados viram issue ou comentário no código.

## Sinais de que a rodada foi boa

- Achados que **contradizem o autor**, inclusive correções que ele mesmo aplicou
- Pelo menos um achado que **só apareceu rodando** alguma coisa
- Falsos positivos suficientes para a lista existir
- Convergência: o mesmo defeito raiz achado por personas que olhavam para lados
  diferentes
