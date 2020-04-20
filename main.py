import pygame
import numpy as np

from core import Game
from button import Button
from cycler import Cycler
import nn
from DQLearningBrain import Brain

IDLE = 0
DRAWING = 1
CHECKPOINTS = 2
START = 3


def draw_track(surf, track):
    for cycle in track.vertices:
        if len(cycle) > 1:
            pygame.draw.lines(surf, (255, 255, 255), False, cycle)
    for checkpoint in track.checkpoints:
        pygame.draw.line(surf, (255, 0, 0), checkpoint[0], checkpoint[1])
    if track.start_pos:
        pygame.draw.circle(surf, (255, 0, 0), (int(track.start_pos.x), int(track.start_pos.y)), 12)
    if track.active_checkpoint:
        pygame.draw.line(surf, (0, 0, 255), track.active_checkpoint[0], track.active_checkpoint[1])


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
    need_reset = True
    need_update = True
    training = False
    epoch_counter = 0
    controlled_by_human = False
    new_state = None
    game = Game(8)
    layers = ((nn.Dense, (4, 100, 0.01)),
              (nn.Tanh, tuple()),
              (nn.Dense, (100, 100, 0.01)),
              (nn.Tanh, tuple()),
              (nn.Dense, (100, 8, 0.01)),
              )
    net = nn.NeuralNetwork(layers)
    brain = Brain(net, nn.mse(), 8)
    force = pygame.math.Vector2()
    game.track_m.load_to_active_track('track_0.pickle')

    # initialize rendering
    input_state = DRAWING
    checkpoint_start = None

    # variables
    # update_buttons = True
    # update_track = False
    # update_background = False
    draw = True

    segoe_print = pygame.font.SysFont('segoe print', 25)
    text_buttons = [segoe_print.render(t, True, (127, 127, 127)) for t in ['Next cycle', 'Save current track', 'Load track 0', 'Clear active track', 'Start', 'Start training']]
    text_cycler = [segoe_print.render(t, True, (127, 127, 127)) for t in ['Drawing', 'Checkpoints', 'Start', 'Idle']]

    buttons = []
    right_bar_x = screen.get_rect().width * 0.75
    right_bar_width = screen.get_rect().width * 0.25
    button_height = 50
    for index, line in enumerate(text_buttons):
        buttons.append(Button(pygame.Rect(right_bar_x, (index+1) * button_height, right_bar_width, button_height), line))
    cycler_buttons = [Button(pygame.Rect(right_bar_x, 0, right_bar_width, button_height), line) for line in text_cycler]
    input_state_cycler = Cycler(cycler_buttons)

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
                    # if LMB is pressed
                    if event.pos[0] < right_bar_x:
                        if input_state == DRAWING:
                            game.track_m.active_track.add_vertex(pygame.math.Vector2(event.pos))
                        elif input_state == CHECKPOINTS:
                            if checkpoint_start:
                                game.track_m.active_track.add_checkpoint(checkpoint_start, pygame.math.Vector2(event.pos))
                                checkpoint_start = None
                            else:
                                checkpoint_start = pygame.math.Vector2(event.pos)
                        elif input_state == START:
                            game.track_m.active_track.set_start(pygame.math.Vector2(event.pos))
                    else:
                        # update_buttons = True
                        if input_state_cycler.is_inside(event.pos):
                            input_state = (input_state + 1) % 4
                        if buttons[0].is_inside(event.pos):
                            print('current cycle is', game.track_m.active_track.current_cycle)
                            game.track_m.active_track.move_current_cycle()
                        if buttons[1].is_inside(event.pos):
                            print('saved')
                            game.track_m.save_active_track()
                        if buttons[2].is_inside(event.pos):
                            print('loaded')
                            # update_background = True
                            # update_track = True
                            game.track_m.load_to_active_track('track_0.pickle')
                        if buttons[3].is_inside(event.pos):
                            # update_background = True
                            game.track_m.clear_active_track()
                        if buttons[4].is_inside(event.pos):
                            game.start()
                        if buttons[5].is_inside(event.pos):
                            training = not training
                if event.button == pygame.BUTTON_RIGHT:
                    # if RMB is pressed
                    if buttons[0].is_inside(event.pos):
                        game.track_m.active_track.add_cycle()
                        print('cycles number', len(game.track_m.active_track.vertices))
            # controls handling

                if event.type == pygame.KEYDOWN:
                    print('down a key')
                    if event.key == pygame.K_SPACE:
                        print(draw)
                        draw = not draw
                    if controlled_by_human:
                        if event.key == pygame.K_RIGHT:
                            force.x += 1
                        if event.key == pygame.K_LEFT:
                            force.x -= 1
                        if event.key == pygame.K_DOWN:
                            force.y += 1
                        if event.key == pygame.K_UP:
                            force.y -= 1

                if event.type == pygame.KEYUP:
                    print('up a key')
                    if controlled_by_human:
                        if event.key == pygame.K_RIGHT:
                            force.x -= 1
                        if event.key == pygame.K_LEFT:
                            force.x += 1
                        if event.key == pygame.K_DOWN:
                            force.y -= 1
                        if event.key == pygame.K_UP:
                            force.y += 1





        if training:
            if need_reset:
                need_reset = False
                game.start()
            if need_update:
                if new_state is None:
                    state = game.get_state()
                    state = np.array((state[0].x/100, state[0].y/100, state[1].x/100, state[1].y/100))
                else:
                    state = new_state
                action = brain.get_action(state)
                #print(action)
                reward, terminal = game.update(action)
                new_state = game.get_state()
                new_state = np.array((new_state[0].x/100, new_state[0].y/100, new_state[1].x/100, new_state[1].y/100))
                brain.add_replay_memory(state, action, reward, new_state)
                training_num = brain.counter
                if brain.counter > 256:
                    training_num = 256
                for i in range(training_num):
                    brain.learn_from_replay_memory()
                if terminal:
                    epoch_counter += 1
                    print(epoch_counter, brain.eps)
                    need_reset = True
                    new_state = None
                    brain.decrease_eps()



        # print(int(game.agent.pos.x), int(game.agent.pos.y))

        # drawing
        if draw:
            pygame.draw.rect(screen, (0, 0, 0), screen.get_rect())
            draw_track(screen, game.track_m.active_track)
            draw_button(screen, input_state_cycler.get_active_button())
            for button in buttons:
                draw_button(screen, button)
            pygame.draw.circle(screen, (255, 255, 0), (int(game.agent.pos.x), int(game.agent.pos.y)), 12)
            pygame.display.flip()


if __name__ == "__main__":
    main()
