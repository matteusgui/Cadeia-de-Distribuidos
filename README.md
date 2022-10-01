# Cadeia-de-Distribuidos

* Fernando Kioshi Kaida, 769667
* Matteus Guilherme de Souza, 769816

## Link para o arquivo da apresentação realizada

https://drive.google.com/file/d/1i3VHmAAdu-2zRySyjmvL-qCsWjtGUjfd/view?usp=sharing

Trabalho da Disciplina de Sistemas Distribuídos utilizando Docker e o broker do HiveMQ para simular uma cadeia de distribuição de produtos

A ferramenta Docker é uma ferramenta muito atual, utilizada amplamente na indústria, que realiza a facilitação da portabilidade de código. Isto acontece uma vez que tal ferramenta separa a aplicação que está sendo executada do Sistema Operacional utilizado na máquina, se assemelhando as máquinas virtuais, sendo porém muito mais leve que tais plataformas. Tal sistema é muito utilizado hoje em dia pelo fato de que tal ferramenta facilita a transparência geográfica do sistema, já que a ferramenta é capaz de realizar chamadas remotas, este lado não foi porém muito utilizado no sistema realizado.

Para que fosse realizada uma simulação com outra ferramenta de mercado, utilizou-se o sistema de MQTT da plataforma HiveMQ, tal plataforma disponibiliza um broker gratuito, muito semelhante a um broker pago. Neste caso, o sistema desenvolvido utiliza tal broker como método para conectar os diferentes containers existentes.

O sistema, como pedido, possui 3 tipos de instâncias, sendo elas: Fábricas, Centro de Distribuição e Lojas. Que serão especificadas nas seções abaixo:

## Lojas

As lojas possuem 200 produtos, sendo que o sistema possui então 3 tipos diferentes de produtos, sendo eles dos tipos A, B e C, nomes genéricos. Foi definido que o sistema deveria ter diferentes tamanhos de estoque para cada um dos produtos existentes. Os produtos do tipo A devem ter 100 unidades de estoque na loja, os produtos do tipo B devem ter um estoque de 60 unidades por produto da categoria e os produtos do tipo C devem ter 20 unidades de cada produto da categoria.

O sistema então salva tais valores de estoque em um arquivo, de modo que o arquivo possa ser posteriormente recuperado e então ser realizada uma visualização das quedas de estoque ao longo do tempo.

Para simular as compras, teve-se que para cada produto no estoque, gera-se um número aleatório entre 2 e 7, de modo que essa será a quantidade a ser consumida daquele determinado produto naquela determinada loja naquela iteração. Se o estoque estiver baixo e não houver tal quantidade, o débito do estoque simplesmente não é realizado. Para cada produto então é checado se o estoque está abaixo de 25%, pois este é o ponto onde deve ser pedida reposição para o centro de distribuição. Quando tal ponto é atingido temos que o sistema dispara uma mensagem para o Centro de Distribuição, onde é processado tal pedido, para saber se ele poderá ou não ser atendido. Após isto, a loja hiberna por um tempo aleatório entre 30 e 50 segundos, para simular uma passagem de tempo, além de evitar que o sistema não fique impossível de monitorar, já que as iterações seriam virtualmente instantâneas.

## Fábrica

A modelagem da fábrica baseia-se na ideia de que a fábrica sempre será capaz de suprir o pedido feito pelo Centro de Distribuição. A fábrica diferentemente da loja, funciona à base de eventos, no caso, o recebimento de mensagens do centro de distribuição.

A ideia é que o Centro de Distribuição faz uma requisição para a fábrica, em modo de broadcast. As fábricas então devem pegar os pedidos que são somente para ela e então ele prepara uma mensagem, que é a simulação de um pacote a ser enviado, com a quantidade requisitada e envia tal pacote para o Centro de Distribuição.

## Centro de Distribuição

O Centro de Distribuição é um estoque com um valor de itens maior do que uma loja, ele é responsável por garantir que as lojas sempre terão seu estoque reposto e não falte produtos para elas.

O sistema proposto no caso, realiza o armazenamento da quantidade suficiente para realizar o reabastecimento total de todas as lojas de uma única vez.

O Centro de Distribuição incorpora algumas coisas existentes em ambas as pontas em que está conectado. O Centro de Distribuição incorpora o estoque, característica das lojas, com o fato de ser baseado em eventos, característica das fábricas.

O Centro de Distribuição foi modelado de modo a ele não entregar para a loja pedidos de modo parcial. Tal fato foi um requisisto imposto pelo professor.

O funcionamento padrão do sistema se baseia no momento em que ele recebe uma mensagem em um dos tópicos em que está inscrito, seja, na modelagem, um pedido de uma loja ou um produto chegando de uma fábrica. O sistema então decodifica a mensagem que lhe foi passada e checa em que tópico a mensagem foi publicada. Se a mensagem for mandada por uma loja, sabe-se que é um pedido de reposição e então é, se houver estoque, gerada a reposição. Caso a mensagem venha de uma fábrica, o Centro de Distribuição checa se o espaço existente para aquele produto é o suficiente para armazená-lo, se for, ele armazena tudo que foi recebido, se não for, o sistema então completa seu próprio estoque e então descarta o resto do que foi recebido.

## Comunicação entre containers

O sistema, como especificado, realiza a conexão entre containers através do broker fornecido pela HiveMQ. O sistema conta com 4 canais de comunicação, sendo 2 entre as lojas e o Centro de Distribuição e 2 entre o Centro de Distribuição e as fábricas. Tal decisão de projeto foi feita para facilitar a distinção entre mensagens.

Os canais entre o Centro de Distribuição e as lojas podem ser divididos em 2, um em que o Centro de Distribuição escreve, sem ouvir e todas as lojas estão de ouvintes e outro onde todas as lojas estão escrevendo porém somente o Centro de Distribuição consegue ouvir. Tal escolha foi feita pois assim, tem-se um isolamento entre o canal de comunicação de requisição de produtos e o de reabastecimento. Isto também reduz a quantidade de mensagens a serem filtradas por uma loja, já que o sistema realiza a checagem somente se for um reabastecimento, não estando preocupado com pedidos de reabastecimento que estão sendo feitos por outras lojas.

Os canais entre o Centro de Distribuição e as fábricas segue uma lógica similar, onde tem-se um canal para pedidos de reposição do Centro de Distribuição no qual o Centro de Distribuição somente escreve e faz-se um broadcast para todas as fábricas, ficando a cargo das fábricas saber se o pedido feito é com elas ou não. O outro canal é um canal onde todas as fábricas escrevem mas o único assinante é o Centro de Distribuição, o que gera um sistema, colocando sobre a perspectiva de um Pub-Sub de um tópico com diversos publishers mas somente um subscriber.

# Comandos necessários para rodar o sistema

Primeiramente é necessário iniciar o sistema Docker no sistema, em um sistema Linux para iniciar o sistema Docker já instalado tem-se que realizar o seguinte comando:
    
    sudo service docker start

Tem-se então que realizar a construção das imagens que serão utilizadas no Docker compose, para isso usaremos os seguintes comandos dentro da pasta compose:

    docker build -f DFLoja -t docker_loja .
    docker build -f DFfabrica -t docker_fabrica .
    docker build -f DFdiscen -t docker_discen .

Após isto, pode-se então subir a aplicação através do arquivo docker-compose.yml. Tal arquivo é responsável porsubir diversos containers independentes de uma única vez. Para que isso ocorra deve-se dar o seguinte comando:

    docker compose up

Após tal comando o sistema iniciará  instâncias de fábricas e diversas instâncias de lojas, além da instância de um Centro de Distribuição, a quantidade iniciada depende da quantidade de instâncias feitas no arquivo docker-compose.yml.

Para realizar a parada do sistema é somente necessário utilizar o comando Ctrl+C e após isto, para desligar o serviço Docker pode-se utilizar o comando

    sudo service docker stop
