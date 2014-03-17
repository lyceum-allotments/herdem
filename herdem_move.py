import cocos.actions as ca
import math
import pymunk as pm

class HerdemMove(ca.Move):
    def step(self, dt):
        self.target.position = self.target.body.position
        
        a = not (self.target.body.velocity[0] == self.target.prev_velocity[0] 
                 and self.target.body.velocity[1] == self.target.prev_velocity[1])

        # Checks if the velocity has changed direction
        b = self.target.body.velocity[0] * self.target.prev_velocity[0] < 0
        c = self.target.body.velocity[1] * self.target.prev_velocity[1] < 0 

        if a or b or c:
            self.target.set_animation()

        self.target.prev_velocity = pm.Vec2d(self.target.body.velocity[0],
                                             self.target.body.velocity[1])


class HerdemRotate(ca.Move):
    def step(self,dt):
        v_n = self.target.body.velocity.normalized()
        if not (v_n[0] == 0 and v_n[1] == 0):
            theta = math.acos(v_n.dot(pm.Vec2d(1,0))) * 180. / math.pi
            if v_n[1] > 0:
                theta *= -1

            self.target.do(ca.RotateTo(theta, 0.2))


