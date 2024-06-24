<img src="capa_currycompany.png" alt="Capa do Projeto" width="1070" height="500">

# 1. Problema de negócio
A Cury Company é uma empresa de tecnologia que criou um aplicativo que conecta restaurantes, entregadores e pessoas. 

Através desse aplicativo, é possível realizar o pedido de uma refeição, em qualquer restaurante cadastrado, e recebê-lo no
conforto da sua casa por um entregador também cadastrado no aplicativo da Cury Company. 

A empresa realiza negócios entre restaurantes, entregadores e pessoas, e gera muitos dados sobre entregas, tipos de pedidos, condições climáticas,
avaliação dos entregadores e etc. Apesar da entrega estar crescendo, em termos de entregas, o CEO não tem visibilidade completa dos KPIs de crescimento da empresa. 

Você foi contratado como um Cientista de Dados para criar soluçòes de dados para entrega, mas antes de treinar algoritmos, a necessidade da empresa
ter um dos principais KPIs estratégicos organizados em uma única ferramenta, para que o CEO possa consultar e conseguir tomar decisões simples, porém importantes. 

A Cury Company possui um modelo de negócio chamado Marketplace, que faz o intermédio do negócio entre três clientes principais: restaurantes, entregadores e pessoas compradoras. Para acompanhar o crescimento desses negócios, o CEO gostaria de ver as seguintes métricas de crescimento: 

## Do lado da empresa:
1. Quantidade de pedidos por dia. 
2. Quantidade de pedidos por semana. 
3. Distribuição dos pedidos por tipo de tráfego. 
4. Compração do volume de pedidos por cidade e tipo de tráfego. 
5. A quantidade de pedidos por entregador por semana. 
6. A localização central de cada cidade por tipo de tráfego.

## Do lado do entregador:
1. A menor e maior idade dos entregadores. 
2. A pior e a melhor condição de veículos. 
3. A avaliação média por entregador. 
4. A avaliação média e o desvio padrão por tipo de tráfego. 
5. A avaliação média e o desvio padrão por condições climáticas. 
6. Os 10 entregadores mais rápidos por cidade. 
7. Os 10 entregadores mais lentos por cidade. 

## Do lado dos restaurantes:
1. A quantidade de entregadores únicos.
2. A distância média dos restaurantes e dos locais de entrega.
3. O tempo médio e o desvio padrão de entrega por cidade. 
4. O tempo médio e o desvio padrão por cidade e por tipo de pedido.
5. O tempo médio e o desvio padrão por cidade e por tipo de tráfego.
6. O tempo médio de entrega durante os festivais. 

O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que exibam essas métricas da melhor forma possível para o CEO.

# 2. Premissas assumidas para a análise
1. A análise foi realizada com dados entre 11/02/2022 a 06/04/2022.
2. Marketplace foi o modelo de negócio assumido.
3. As 3 principais viões do negócio foram: visão transação de pedidos; visão entregadores; visão restaurantes.

# 3. Estrategia da solução
O painel estratégico foi desenvolvido utilizando as métricas que refletem as 3 princiais visões do modelo de negócio da empresa.

Cada visão é representada pelo seguinte conjunto de métricas.

+ Visão crescimento da empresa:
1. Pedidos por dia. 
2. Porcentagem de pedidos por condição climática. 
3. Quantidade de pedidos por tipo e por cidade. 
4. Pedidos por semana. 
5. Quantidade de pedidos por tipo de entrega. 
6. Quantidade de pedidos por condiçoes de trânsito e tipo de cidade.

+ Visão crescimento dos restaurantes:
1. Quantidade de pedidos únicos. 
2. Distância média percorrida. 
3. Tempo médio de entrega durante festival e dias normais. 
4. Desvio padrão do tempo de entrega durante festivais e dias "normais". 
5. Tempo de entrega médio por cidade. 
6. Distribuição do tempo médio de entrega por cidade.

+ Visão crescimento dos entregadores:
1. Idade do entregador mais velho e mais novo. 
2. Avaliação do melhor e do pior veículo. 
3. Avaliação média por entregador. 
4. Avaliação média por condições de trânsito. 
5. Avaliação média por condições climáticas. 
6. Tempo médio do entregador mais rápido.
7. Tempo médio do entregador mais rápido por cidade. 

# 4. Top 3 Insights de dados
1. A sazonalidade da quantidade de pedidos é diária. Há uma variação de aproximadamente 10% do número de pedidos em dias sequenciais. 
2. As cidades do tipo Semi-Urban não possuem condições baixas de trânsito. 
3. As maiores variações no tempo de entrega, acontecem durante o clima ensolarado. 

# 5. O produto final do projeto
Painel online, hospedado em Cloud e disponível para acesso em qualquer dispositivo conectado à internet. 

O painel pode ser acessado através desse link: https://projects-curry-company.streamlit.app/

# 6. Conclusão
O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que exibam essas métricas da melhor forma possível para o CEO.

Da visão da Empresa, podemos concluir que o número de pedidos cresceu entre a semana 06 e a semana 13 do ano de 2022. 

# 7. Próximos passos - aprimoramento do projeto
1. Reduzir o número de métricas. 
2. Criar novos filtros. 
3. Adicionar novas visões de negócio.
