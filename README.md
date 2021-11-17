### Produzido por Henrique Eissmann Buzzi ###

Código para aplicação de Chromakey

main possui versão mais otimizada, demora 0,02 até 0,06 segundos para calcular a distância em cada frame;
versao-original é a primeira versão escrita, é a menos otimizada e demorada, dando então origem as versões otimizadas;
versao-2-primeiraOtimização é a primeira otimização implementada, diminuindo em 50% o tempo, mas ainda acima de 1s;

######### Modo de usar:

Antes de executar, defina seu Limiar (define qual o threshold aceitável para proximidade), quanto menor o valor, pega apenas os pixels que ficaram mais próximas da cor de referência. Define um valor acima de 0.
Automaticamente o Limiar está em 30 (o melhor encontrado pelo projetista para a tela verde de exemplo)
A cor do chroma-key de referência é definido na execucação do código, é definido pelo usuário usando o Mouse, clicando sobre o chroma-key

######### Executando:
Ao abrir a imagem pela primeira vez, tem-se as seguintes opções:

-- Espaço: Vai para o próximo frame, isso é feito para que o usuário possa encontrar o frame onde tenha o Chromakey de referência.

-- Pressionar Tecla C: Entra no modo de captura, quando clicar com o botão esquerdo do mouse, ele marcará com um ponto vermelho qual foi o pixel de referência escolhido para o Chromakey.
	- 2 opções são possíveis depois de selecionar o pixel do Chromakey: A tecla Enter confirma que o pixel de referência está correto e continua o código, já a tecla
	Espaço faz com que a etapa de captura seja descartada, significando que ocorreu um erro na delimitação, e permite a recaptura.

-- Pressionar Tecla Esc: Cancela o código e termina a execução, sinalizando que você não quer rodar o código.

Após isso o código é executado. Mostrando na tela, em tempo real, frame a frame que é gerado pela execução da substituição do chromakey. Para sair da exibição antes do término, pode-se pressionar Esc.

Para melhor entendimento, recomenda-se ler os comentários do código. Possui a função de calcular o tempo de função (usado na hora de otimizar o cálculo da imagem de distância) e de gravar um arquivo de vídeo como output. É necessário descomentar essas linhas para que essas funções rodem.

######### Conceitos aplicados

Captação de referência, cálculo de distância euclidiana, criação de máscaras, adição e subtração de máscaras, gravação de vídeo na saída.

######### Possíveis implementações futuras

* Função aceitar um parâmetro que define se o usuário quer gravar o vídeo na saída ou não.
