import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([500, 500])

x = 0
y = 0

recentclickx = 0
recentclicky = 0

# Run until the user asks to quit
running = True
while running:
    
    mousex = pygame.mouse.get_pos()[0]
    mousey = pygame.mouse.get_pos()[1]
    click = pygame.mouse.get_pressed()[0]
       
    print(mousex,mousey,click)
    print(recentclickx,recentclicky)

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw a solid blue circle in the center
    if click == True:
        pygame.draw.circle(screen, (0, 0, 0), (mousex, mousey), 20)
        recentclickx = mousex
        recentclicky = mousey

    pygame.draw.circle(screen, (0, 0, 0), (recentclickx, recentclicky), 5)
    
    v1 = (recentclickx, recentclicky)
    v2 = (mousex, mousey)
    
    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
