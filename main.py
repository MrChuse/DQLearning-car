import pygame
from core import Game
from button import Button

IDLE = 0
DRAWING = 1


def draw_track(surf, track):
    if len(track.vertices) > 1:
        pygame.draw.lines(surf, (255, 255, 255), track.vertices[0] == track.vertices[-1], track.vertices, track.width)
    for vertex in track.vertices:
        pygame.draw.circle(surf, (255, 255, 255), (int(vertex.x), int(vertex.y)), track.width // 2)


def draw_button(surf, button):
    if button.is_active:
        pygame.draw.rect(surf, (255, 255, 255), button.rect)
        surf.blit(button.text, button.rect)
        pygame.draw.rect(surf, (0, 0, 0), button.rect, 2)


# define a main function
def main():
    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("Learning car")

    # create a surface on screen that has the size of 720 x 480
    screen = pygame.display.set_mode((1000, 500))

    # initialize game
    game = Game()
    force = pygame.math.Vector2()

    # initialize rendering
    input_state = DRAWING

    # variables
    update_buttons = True
    update_track = False
    update_background = False

    segoe_print = pygame.font.SysFont('segoe print', 25)
    text = [segoe_print.render('Drawing', True, (127, 127, 127)),
            segoe_print.render('Save current track', True, (127, 127, 127)),
            segoe_print.render('Load track 0', True, (127, 127, 127)),
            segoe_print.render('Clear active track', True, (127, 127, 127))]

    text_idle = segoe_print.render('Idle', True, (127, 127, 127))

    buttons = []
    right_bar_x = screen.get_rect().width * 0.75
    right_bar_width = screen.get_rect().width * 0.25
    button_height = 50
    for index, line in enumerate(text):
        buttons.append(Button(pygame.Rect(right_bar_x, index * button_height, right_bar_width, button_height), line))
    buttons.append(Button(pygame.Rect(right_bar_x, 0, right_bar_width, button_height), text_idle, False))

    # main loop
    running = True
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # red cross handling
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

            # mouse presses handling
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    # if it is LMB pressed
                    if event.pos[0] < right_bar_x:
                        if input_state == DRAWING:
                            update_track = True
                            game.track_m.active_track.add_vertex(pygame.math.Vector2(event.pos))
                    else:
                        update_buttons = True
                        if buttons[0].is_inside(event.pos):
                            input_state = 1 - input_state
                            buttons[0].disable()  # TODO: make a cycler
                            buttons[-1].enable()
                        elif buttons[-1].is_inside(event.pos):
                            input_state = 1 - input_state
                            buttons[0].enable()
                            buttons[-1].disable()
                        if buttons[1].is_inside(event.pos):
                            print('saved')
                            game.track_m.save_active_track()
                        if buttons[2].is_inside(event.pos):
                            print('loaded')
                            update_background = True
                            update_track = True
                            game.track_m.load_to_active_track('track_0.pickle')
                        if buttons[3].is_inside(event.pos):
                            update_background = True
                            game.track_m.clear_active_track()

            # controls handling
            if event.type == pygame.KEYDOWN:
                #print('down a key')
                if event.key == pygame.K_RIGHT:
                    force.x += 1
                if event.key == pygame.K_LEFT:
                    force.x -= 1
                if event.key == pygame.K_DOWN:
                    force.y += 1
                if event.key == pygame.K_UP:
                    force.y -= 1

            if event.type == pygame.KEYUP:
                # print('up a key')
                if event.key == pygame.K_RIGHT:
                    force.x -= 1
                if event.key == pygame.K_LEFT:
                    force.x += 1
                if event.key == pygame.K_DOWN:
                    force.y -= 1
                if event.key == pygame.K_UP:
                    force.y += 1

        if force.length() > 0:
            force_ = force.normalize()
            force_.scale_to_length(0.0001)
            game.agent.add_force(force_, 0)

        game.agent.update()
        # print(int(game.agent.pos.x), int(game.agent.pos.y))

        # drawing
        pygame.draw.rect(screen, (0, 0, 0), screen.get_rect())
        draw_track(screen, game.track_m.active_track)
        for button in buttons:
            draw_button(screen, button)
        pygame.draw.circle(screen, (255, 255, 0), (int(game.agent.pos.x), int(game.agent.pos.y)), 12)
        pygame.display.flip()


if __name__ == "__main__":
    main()
