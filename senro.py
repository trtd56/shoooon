import pyxel

class Game:
    def __init__(self):
        pyxel.init(160, 120)
        pyxel.load("senro.pyxres")
        self.reset_game()
        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        self.path = []
        self.tracing = False
        self.player_pos = None
        self.path_index = 0
        self.goal_reached = False
        self.goal_effect_timer = 0
        self.player_speed = 1.0  # 速度を 1.0 に戻す (後で調整)
        self.move_threshold = 8.0 # 移動完了と判定する距離の閾値 (pixels)

    def update(self):
        if pyxel.btnp(pyxel.KEY_R):
            self.reset_game()

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.path = [(pyxel.mouse_x, pyxel.mouse_y)]
            self.tracing = True

        elif pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and self.tracing:
            self.path.append((pyxel.mouse_x, pyxel.mouse_y))

        elif not pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and self.tracing:
            self.tracing = False
            self.player_pos = self.path[0] if self.path else None
            self.path_index = 0

        if self.player_pos and self.path_index < len(self.path) - 1:
            target_pos = self.path[self.path_index + 1] # 次の目標地点
            dx = target_pos[0] - self.player_pos[0] # X軸方向の距離
            dy = target_pos[1] - self.player_pos[1] # Y軸方向の距離
            distance = (dx**2 + dy**2)**0.5 # 現在位置と目標地点の距離

            if distance > self.move_threshold: # まだ目標地点に近づいていない場合
                # move_threshold より大きい場合は等速で近づく
                ratio = self.player_speed / distance
                self.player_pos = (
                    self.player_pos[0] + dx * ratio, # 現在位置から player_speed の割合で目標地点へ近づく
                    self.player_pos[1] + dy * ratio  # 現在位置から player_speed の割合で目標地点へ近づく
                )
            else: # 目標地点に十分近づいた場合
                self.path_index += 1 # 次の目標地点へ
                self.player_pos = self.path[self.path_index] # 目標地点に瞬間移動 (調整)


        if self.player_pos and self.path_index >= len(self.path) - 1:
            if not self.goal_reached:
                self.goal_reached = True
                self.goal_effect_timer = 20

        if self.goal_effect_timer > 0:
            self.goal_effect_timer -= 1
            if self.goal_effect_timer == 0:
                self.reset_game()

    def draw(self):
        if self.goal_effect_timer > 0:
            pyxel.cls(6)
        else:
            pyxel.cls(15)
        for x, y in self.path:
            pyxel.pset(x, y, 0)
        if self.player_pos and not self.goal_reached:
            pyxel.blt(self.player_pos[0] - 16, self.player_pos[1] - 12, 0, 0, 0, 32, 24, 6)

Game()
