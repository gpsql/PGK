import pyray as pr
from game import Game

def main():
    pr.init_window(800, 600, "Night Thief (PGK Lab15)")
    pr.set_target_fps(60)

    app_state = "MENU" # MENU, GAME
    game = None

    while not pr.window_should_close():
        dt = pr.get_frame_time()

        if app_state == "MENU":
            if pr.is_key_pressed(pr.KEY_ENTER):
                game = Game()
                app_state = "GAME"
                
            pr.begin_drawing()
            pr.clear_background(pr.BLACK)
            pr.draw_text("NIGHT THIEF", 250, 200, 50, pr.WHITE)
            pr.draw_text("Press ENTER to start", 300, 300, 20, pr.GRAY)
            pr.draw_text("Controls: WASD to move", 300, 350, 20, pr.GRAY)
            pr.draw_text("Right Click to throw rock (distract)", 250, 380, 20, pr.GRAY)
            pr.draw_text("Goal: Steal the yellow artifact and reach the green exit.", 150, 450, 20, pr.YELLOW)
            pr.end_drawing()

        elif app_state == "GAME":
            game.update(dt)
            
            pr.begin_drawing()
            game.draw()
            
            if game.state == "WIN":
                pr.draw_rectangle(0, 0, 800, 600, pr.fade(pr.BLACK, 0.7))
                pr.draw_text("YOU WIN!", 280, 250, 50, pr.GREEN)
                pr.draw_text("Press ENTER to return to menu", 220, 320, 20, pr.WHITE)
                if pr.is_key_pressed(pr.KEY_ENTER):
                    app_state = "MENU"
                    game = None
                    
            elif game.state == "LOSS":
                pr.draw_rectangle(0, 0, 800, 600, pr.fade(pr.BLACK, 0.7))
                pr.draw_text("CAUGHT! GAME OVER", 180, 250, 40, pr.RED)
                pr.draw_text("Press ENTER to return to menu", 220, 320, 20, pr.WHITE)
                if pr.is_key_pressed(pr.KEY_ENTER):
                    app_state = "MENU"
                    game = None
            
            pr.end_drawing()

    pr.close_window()

if __name__ == "__main__":
    main()
