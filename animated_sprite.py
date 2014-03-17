import cocos.sprite
import pymunk as pm

class AnimatedSprite(cocos.sprite.Sprite):
    def __init__(self, images):
        super(AnimatedSprite, self).__init__(images["still"])

        self.body = None

        self.images = images
        self.image_name = "still"
        self.prev_velocity = (0, 0) # self.body.velocity

    def set_image(self, image):
        self.image = self.images[image]
        self.image_name = image

    def set_animation(self):

        if self.body.velocity[0] == 0 and self.body.velocity[1] == 0:
            self.set_image("still")
            return
        else:
            if not self.image_name == "go":
                self.set_image("go")
        return
