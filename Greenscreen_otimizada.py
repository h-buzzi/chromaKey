# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 10:10:02 2021

@author: hbuzzi

Cálculo da imagem de distância mais otimizada
"""

import cv2
import sys
import numpy as np

## Fazer usuário pegar a cor de referência
def get_ref_color(video_name):
    """Função que pega a referência da cor a partir do pixel selecionado usando o mouse
    
    Modo de usar: Avance para o próximo frame apertando espaço, quando encontrar o frame com a cor desejada, pressione a tecla C.
    Ao pressionar a tecla C, mova o mouse e clique sobre a cor desejada, isto fará com que o pixel selecionado seja marcado com um círculo vermelho.
    Se este é o pixel desejado, pressione Enter para confirmar, se clicou errado, pressione Espaço para ignorar a captura atual e poder pressionar C novamente
    
    Caso deseje cancelar, pressione Esc que o código será finalizado
    
    Input: diretório do arquivo de vídeo
    
    Output: Cor de referência desejada no espaço de cor L*a*b"""
    ###Nested Function
    def mouse_event(event, col, lin, flags, *userdata): #Função clique mouse
        if event == cv2.EVENT_LBUTTONDOWN: #Se pressionar o botão esquerdo
            del dsr_point[0] #Salva a posição do clique na ref
            dsr_point.append((lin,col))
            copied = frame.copy() #Cria uma cópia do frame
            cv2.circle(copied, (col,lin), 1,(0,0,255),-1) #Desenha círculo no ponto clicado
            cv2.imshow(w_name,copied) #Mostra o círculo na imagem copiada (não modifica o frame original), para o usuário saber se está certo
            return
    ###
    video = cv2.VideoCapture(video_name)    
    w_name = "Selecione o fundo de referencia" #Nome da janela
    while True: #Loop para cada frame
        has_frame, frame = video.read() #Le o frame atual do vídeo
        if not has_frame: #Se não tiver mais frame
            sys.exit() #Ele finaliza a aplicação, pois o usuário chegou no final sem fazer nada
        cv2.imshow(w_name, frame) #Mostra o frame
        key = 0
        while (key != 32 and key != 27 and key != ord('C') and key != ord('c')):
            key = cv2.waitKey(0) #Espera um input do teclado do usuário
        if key == 27: #Se pressionou esc
            cv2.destroyWindow(w_name) #Fecha a janela
            video.release() #Libera o vídeo
            sys.exit() #Termina o código
        elif key == 32: #Se pressionar espaço
            continue #pula pro próximo frame até ele chegar no desejado
        elif key == ord('C') or key == ord('c'):
            dsr_point = [(0,0)]
            cv2.setMouseCallback(w_name, mouse_event) # Chama função de clicar mouse
            key = 0
            while (key != 13 and key != 32 and key != 27):
                key = cv2.waitKey(0) # Espera o usuário pressionar
            if key == 13: #Se deu Enter, significa que o ponto de referência está certo
                cv2.setMouseCallback(w_name, lambda *args : None) #Termina a função do mouse
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
                ref = frame[dsr_point[0][0],dsr_point[0][1],:] # Usa a variável global no frame atual para salvar a ref
                break #Sai do loop
            elif key == 32: #Se deu espaço, ponto errado
                cv2.setMouseCallback(w_name, lambda *args : None) #Termina a função do mouse
                continue #Vai pro próximo passo pois ele vai selecionar outro valor ou sair
            elif key == 27:
                cv2.destroyWindow(w_name) #Fecha a janela
                video.release() #Libera o vídeo
                sys.exit() #Termina o código
    video.release() #Solta o vídeo
    cv2.destroyWindow(w_name) #Fecha a janela
    return ref #Retorna a referência


def chroma_substitution(video_name_chroma, video_name_background, ref, Limiar, mode = "don't write an .avi output at code folder"):
    """Função que substitui o chromakey de referência pelo vídeo de background fornecido. Informe 'mode = write' para escrever um vídeo .avi na pasta do código.
    
    Input: Diretório do vídeo com chroma-key, Diretório do vídeo de background, Cor de referência, Limiar de comparação para imagem de distância (Quanto menor o limiar, ele aceita apenas as cores mais próximos, e quanto maior ele aceita até cores mais distantes da referência), e o modo de operação.
    
    Output: None (Vídeo na pasta se opção habilitada)"""
    ## Abre os vídeos
    video_chroma = cv2.VideoCapture(video_name_chroma) #Vídeo com Chroma key
    video_back = cv2.VideoCapture(video_name_background) #Vídeo que será aplicado no Chroma
    width = int(video_chroma.get(cv2.CAP_PROP_FRAME_WIDTH)) #Largura do vídeo
    height = int(video_chroma.get(cv2.CAP_PROP_FRAME_HEIGHT)) #Altura do vídeo
    ## Saída
    if mode == 'write':
        out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), video_chroma.get(cv2.CAP_PROP_FPS), (width,height)) ## Cria o vídeo de saída
    ## Matriz de referência
    Mref = ref*np.ones((height,width,3)) #Imagem com os pixels de referência
    while True:
        has_frame_f, frame_f = video_chroma.read() #Pega o frame do vídeo do chroma
        has_frame_b, frame_b = video_back.read() #Pega o frame do vídeo de back
        if not has_frame_f: #Se o vídeo chroma não tiver mais frame, significa que o vídeo principal acabou
            break #Então quebra o loop
            
        if not has_frame_b: #Se o vídeo de background não tiver mais frame
            video_back.release() #Solta ele
            has_frame_b, frame_b = video_back.read() #E reinicia, logo, loopando o vídeo que está aparecendo na tela verde
        
        frame_f_lab = cv2.cvtColor(frame_f, cv2.COLOR_BGR2LAB) #Pega em CIELab
        frame_b = cv2.resize(frame_b,(width,height)) #Background tem q ter mesma resolução para prevenir erros
        ##### Imagem de distância
        D = np.sqrt(np.sum((frame_f_lab - Mref) ** 2, axis=-1))  #equação de distância de Euler
        ##### Geração das máscaras
        retval, V0 = cv2.threshold(D,Limiar,255,cv2.THRESH_BINARY) # Pega e cria a imagem binária a partir da imagem de distância, se ficar abaixo do Limiar, é 0, se ficar acima, é 1
        # É esperado que as cores verdes tenham valor muito próximo ao valor da referência, logo, resultando numa menor distância.
        V0 = np.uint8(V0) #Converte para uint8, esta é a máscara para o chroma key, pois exclui (multiplica por 0) a área verde
        V1 = cv2.bitwise_not(V0) #Pega a máscara invertida, logo, essa é aplicada no background, multiplicando por 1 apenas área que irá ser adicionada no vídeo original, excluindo o resto
        Frontal = cv2.bitwise_and(frame_f,frame_f,mask=V0) #Aplica a máscara V0 no plano frontal (chroma)
        Fundo = cv2.bitwise_and(frame_b,frame_b,mask=V1) #Aplica a máscara v1 no plano background (nuvens)
        result = cv2.add(Frontal,Fundo) #Resultado é adição dos 2
        if mode == 'write':
            out.write(result) ## escreve na saída
        cv2.imshow("Resultado", result) #Mostra a imagem
        key = cv2.waitKey(1) #Espera 1ms e dae continua
        if key == 27: #Se apertar ESC
            break #Cancela a função, permitindo sair do vídeo
    
    cv2.destroyAllWindows() #Fecha todas as telas
    video_chroma.release() #Solta o vídeo chroma
    video_back.release() #Solta o vídeo background
    ## out.release() ##Solta o output
    return
    
###################### CODE START ########################
### User Input   
video_name_chrm = "Chromakey.mp4" #Vídeo principal que possui chromakey
video_name_back = "Clouds.mp4" #Vídeo que será aplicado na telaverde
Limiar = 30 #Limiar usado na comparação da distância, quanto menor o valor, pega apenas os valores mais próximos, quanto maior, mais ele generaliza e pega pixels mais distantes da referência
### Pega referência
ref = get_ref_color(video_name_chrm) #Chama a função para pegar a cor de referência do Chroma key   
### Executa a troca do chroma key
chroma_substitution(video_name_chrm, video_name_back, ref, Limiar, mode = 'write') #Chama função que substitui chroma key
            