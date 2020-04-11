import pygame
from core import Game


def draw_track(surf, track):
    if len(track.vertices) > 1:
        pygame.draw.lines(surf, (255, 255, 255), track.vertices[0] == track.vertices[-1], track.vertices, track.width)
    for vertex in track.vertices:
        pygame.draw.circle(surf, (255, 255, 255), (int(vertex.x), int(vertex.y)), track.width//2)


# define a main function
def main():
     
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    # logo = pygame.image.load("logo32x32.png")
    # pygame.display.set_icon(logo)
    pygame.display.set_caption("Learning car")
     
    # create a surface on screen that has the size of 720 x 480
    screen = pygame.display.set_mode((720, 480))
     
    # define a variable to control the main loop
    running = True

    # initialize game
    game = Game()

    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    game.track.add_vertex(pygame.math.Vector2(event.pos))

        draw_track(screen, game.track)

        pygame.display.flip()


if __name__ == "__main__":
    main()
