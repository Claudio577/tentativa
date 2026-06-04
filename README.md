# Dashboard de Chamados | Upload progressivo

Projeto em **Streamlit** para analisar chamados de Help Desk a partir de arquivos Excel `.xls` ou `.xlsx`.

## Fluxo correto do dashboard

1. Primeiro faça upload do **mês atual**, por exemplo `Consolidado mês maio.xls`.
   - O dashboard já mostra os 5 KPIs principais.
   - Mostra também o comparativo geral do mês atual, setores, dores operacionais e top impactadores.

2. Depois faça upload do **mês anterior**, por exemplo `Consolidado abril.xls`.
   - O dashboard libera a comparação entre mês anterior e mês atual.
   - Os dados da comparação aparecem em gráficos de barra.
   - Também aparece a tabela com diferença e variação percentual.

## Ordem da tela

1. 5 KPIs principais:
   - Total de chamados
   - % Dentro do SLA
   - % 1º retorno até 1h
   - Backlog por status
   - Tratados acima de 72h

2. Comparação em gráficos de barra, somente quando os dois meses forem carregados.

3. Comparativo geral do mês atual.

4. Setores com maior demanda.

5. Principais dores operacionais.

6. Top impactadores do mês atual.

## Como rodar localmente

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

No Linux/Mac:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Segurança dos dados

As planilhas reais não devem ser enviadas para um GitHub público, porque podem conter nomes de clientes, responsáveis e dados operacionais.

O `.gitignore` já bloqueia arquivos `.xls` e `.xlsx` dentro da pasta `data/`.
