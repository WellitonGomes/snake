import pygame 
import random

pygame.init()
# Inicia a biblioteca do pygame 
pygame.display.set_caption("Snake")
# Define um título para a tela do jogo 
tela = largura, altura = 600, 400
# Define o tamanho da tela // largura no valor de 600 // altura no valor de 400
tela = pygame.display.set_mode((largura, altura))
# Aqui passaremos as informações da tela
relogio = pygame.time.Clock() # Instancia o objeto de tempo para controlar a taxa de atualização

# Definimos variáveis para receber as cores que utilizaremos no jogo  
preta = (0, 0, 0) # Padrão RGB // Utilizaremos para o fundo 
branca = (255, 255, 255) # Utilizaremos para a cobra
vermelha = (255, 0, 0) # Utilizaremos para a pontuação 
verde = (0, 255, 0) # Utilizaremos para o alimento da cobra 

# Definiremos os parâmetros da cobra 
tamanho_quadrado = 10 # Definimos o tamanho da cobrinha, 10 pixels para cada lado do quadrado // Utilizaremos para a cobra e para o alimento 
velocidade_atualizacao = 15 # Quantos pixels a cobra andará a cada execução do loop 

def desenharComida(tamanho, comidaX, comidaY):
    pygame.draw.rect(tela, verde, [comidaX, comidaY, tamanho, tamanho])

def gerarComida():
    comidaX = round(random.randrange(0, largura - tamanho_quadrado) / 10.0) * 10.0
    comidaY = round(random.randrange(0, altura - tamanho_quadrado) / 10.0) * 10.0
    return comidaX, comidaY

def desenharCobra(tamanho, pixels):
    for pixel in pixels:
        pygame.draw.rect(tela, branca, [pixel[0], pixel[1], tamanho, tamanho])

def desenharPontuacao(pontuacao):
    fonte = pygame.font.SysFont("Helvetica", 20)
    texto = fonte.render(f"Pontos: {pontuacao}", True, vermelha)
    tela.blit(texto, [1, 1])

def selecionarVelocidade(tecla):
    if tecla == pygame.K_DOWN:
        return 0, tamanho_quadrado
    elif tecla == pygame.K_UP:
        return 0, -tamanho_quadrado
    elif tecla == pygame.K_RIGHT:
        return tamanho_quadrado, 0
    elif tecla == pygame.K_LEFT:
        return -tamanho_quadrado, 0
    return 0, 0

def mostrar_menu_fim_jogo():
    fonte = pygame.font.SysFont("Helvetica", 30)
    fim_jogo_texto = fonte.render("Fim de Jogo!", True, vermelha)
    reiniciar_texto = fonte.render("Reiniciar", True, branca)
    sair_texto = fonte.render("Sair", True, branca)

    tela.blit(fim_jogo_texto, (largura // 2 - fim_jogo_texto.get_width() // 2, altura // 2 - 60))
    pygame.draw.rect(tela, (0, 255, 0), (largura // 2 - 80, altura // 2, 160, 40))
    pygame.draw.rect(tela, (255, 0, 0), (largura // 2 - 80, altura // 2 + 50, 160, 40))
    tela.blit(reiniciar_texto, (largura // 2 - reiniciar_texto.get_width() // 2, altura // 2 + 5))
    tela.blit(sair_texto, (largura // 2 - sair_texto.get_width() // 2, altura // 2 + 55))

    pygame.display.flip()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Verificar se o usuário clicou no botão "Reiniciar"
                if largura // 2 - 80 <= mouse_x <= largura // 2 + 80:
                    if altura // 2 <= mouse_y <= altura // 2 + 40:
                        return True  # Reiniciar o jogo
                    elif altura // 2 + 50 <= mouse_y <= altura // 2 + 90:
                        pygame.quit()
                        quit()

def rodar_jogo():
    while True:
        fim_jogo = False
        x = largura / 2
        y = altura / 2

        velocidadeX = 0
        velocidadeY = 0

        tamanho_cobra = 1
        pixels = []

        comidaX, comidaY = gerarComida()

        while not fim_jogo: 
            tela.fill(preta)
            
            for evento in pygame.event.get(): 
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif evento.type == pygame.KEYDOWN:
                    velocidadeX, velocidadeY = selecionarVelocidade(evento.key)
            
            if x < 0 or x >= largura or y < 0 or y >= altura:
                fim_jogo = True

            x += velocidadeX
            y += velocidadeY

            pixels.append([x, y])
            if len(pixels) > tamanho_cobra:
                del pixels[0]

            # Verificar se a cobra colidiu com ela mesma
            for pixel in pixels[:-1]: 
                if pixel == [x, y]:
                    fim_jogo = True

            # Desenhar elementos na tela
            desenharComida(tamanho_quadrado, comidaX, comidaY)
            desenharCobra(tamanho_quadrado, pixels)
            desenharPontuacao(tamanho_cobra - 1)

            # Verificar se a cobra comeu a comida
            if x == comidaX and y == comidaY:
                tamanho_cobra += 1
                comidaX, comidaY = gerarComida()

            # Atualizar a tela e definir a taxa de atualização
            pygame.display.flip()
            relogio.tick(velocidade_atualizacao)

        # Exibir o menu de fim de jogo
        if not mostrar_menu_fim_jogo():
            break

rodar_jogo()
pygame.quit()
