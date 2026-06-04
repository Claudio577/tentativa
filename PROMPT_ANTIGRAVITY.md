# Prompt para o Antigravity

Atualize/crie um projeto Streamlit chamado `dashboard_chamados_helpdesk` com upload progressivo de arquivos Excel.

## Fluxo obrigatório

O dashboard deve funcionar assim:

1. O usuário primeiro faz upload do arquivo do mês atual, exemplo Maio.
2. Assim que o mês atual for carregado, o dashboard já deve mostrar:
   - 5 KPIs principais no topo;
   - comparativo geral do mês atual;
   - setores com maior demanda;
   - principais dores operacionais;
   - top impactadores do mês atual.
3. O arquivo do mês anterior, exemplo Abril, deve ser opcional.
4. Quando o usuário fizer upload do mês anterior, o dashboard deve liberar a comparação entre mês anterior e mês atual.
5. A comparação deve aparecer em gráfico de barras, não em cards soltos.

## Uploads na sidebar

Colocar primeiro:

- Nome do mês atual, padrão `Maio`;
- Upload `1) Arquivo do mês atual`.

Depois:

- Nome do mês anterior, padrão `Abril`;
- Upload `2) Arquivo do mês anterior`.

## KPIs principais

No topo, sempre que o mês atual for carregado, mostrar 5 cards:

- Total de chamados;
- % Dentro do SLA;
- % 1º retorno até 1h;
- Backlog por status;
- Tratados acima de 72h.

## Comparação em barras

Somente quando os dois arquivos forem carregados, comparar:

- Total de chamados;
- Dentro SLA;
- Fora SLA;
- Tratados até 72h;
- Tratados acima de 72h;
- Em aberto / sem encerramento;
- Backlog por status;
- Empresas;
- FCR tratado;
- First Call Resolution até 1h;
- Resolvidos acima de 1h;
- % SLA;
- % FCR 1h;
- % 1º retorno até 1h.

Gerar dois gráficos:

1. Volumes e produtividade;
2. Indicadores percentuais.

Também exibir uma tabela com:

- Indicador;
- Mês anterior;
- Mês atual;
- Diferença;
- Variação %.

## Regras de cálculo

- Total de chamados: quantidade de linhas válidas.
- Dentro SLA: `Encerramento <= Vencimento`.
- Fora SLA: `Encerramento > Vencimento`.
- % SLA: `Dentro SLA / (Dentro SLA + Fora SLA)`.
- Tratados até 72h: `Encerramento - Abertura <= 72 horas`.
- Tratados acima de 72h: `Encerramento - Abertura > 72 horas`.
- Em aberto / sem encerramento: encerramento vazio.
- Backlog por status: status que não contém `Encerrada`.
- FCR tratado: chamados com encerramento preenchido.
- First Call Resolution até 1h: `Encerramento - Abertura <= 1 hora`.
- % FCR 1h: `First Call Resolution até 1h / FCR tratado`.
- % 1º retorno até 1h: chamados com `1 Retorno - Abertura <= 1 hora` dividido pelo total de chamados.

## Estrutura de arquivos

```text
dashboard_chamados_helpdesk/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   └── config.toml
└── data/
    └── .gitkeep
```

Não subir planilhas reais para GitHub público.
