import cocos
import cocos.text as ct
from pyglet.window import key
import controller
import pyglet

c = {"from_file" : 0,
     "player"    : 1}

class HighScore(cocos.layer.ColorLayer):
    hall_of_fame_length = 5
    is_event_handler = True
    made_score_list = False
    font_size = 24
    finished_name = True
    key_count = 0

    def __init__(self, controller):
        super(HighScore, self).__init__(0, 255, 0, 255)
        pyglet.font.add_directory("fonts")
        self.controller = controller
        self.load_high_scores(controller.number)
        player_time = controller.finish_time - controller.start_time
        self.add_player_score(player_time)
        self.construct_table()

        w, h = cocos.director.director.get_window_size()

        bg = cocos.sprite.Sprite("images/scenes/hall_of_fame/hall_of_fame.png")
        bg.position = (w/2, h/2)
        self.add(bg)


        label = ct.Label("LEVEL %d: %s" % (controller.number, controller.level.name.upper()),
                   font_name = "newshampark",
                   font_size = 40,
                   anchor_y = "center",
                   anchor_x = "center")
        label.position = (w/2.,h*0.83)
        label.element.color = (0,0,0,255)
        self.add(label, z = 5)



        label = ct.Label("YOUR TIME: %dm %ds" % (player_time / 60, player_time % 60),
                   font_name = "newshampark",
                   font_size = 32,
                   anchor_y = "center",
                   anchor_x = "center")
        label.position = (w/2.,h*0.77)
        label.element.color = (0,0,0,255)
        self.add(label, z = 5)





        label = ct.Label("Hall of Fame",
                   font_name = "Nimbus Roman No9 L",
                   font_size = 32,
                   anchor_y = "center",
                   anchor_x = "center")
        label.position = (w/2.,490)
        label.element.color = (0,0,0,255)
        self.add(label, z = 5)


    def on_key_press(self, k, m):
        if (k in [key.ENTER, key.ESCAPE]):
            if k == key.ENTER and self.finished_name == False:
                self.finished_name = True
            elif self.finished_name == True:
                self.save_high_scores()
                self.controller.nextlevel(0)
            return True
        if k == key.BACKSPACE:
            if self.key_count == 0:
                return
            else:
                self.key_count -= 1
                self.name_label.element.text = self.name_label.element.text[:-1]



    def save_high_scores(self):
        level = self.controller.number
        fp = open("scores/%d" % level, "w")
        for hs in self.high_scores:
            name = hs[0]
            time = int(hs[1])
            if hs[2] == c["player"]:
                name = self.name_label.element.text
            fp.write("%s;%s\n" % (name, time))

        fp.close()


    def load_high_scores(self, level):
        filename = "scores/%d" % level
        self.high_scores = []
        try:
            fp = open(filename)
            for l in fp.readlines():
                if l.startswith("#"):
                    continue
                name, time = l.split(";")
                self.high_scores.append((name, int(time),c["from_file"]))
            fp.close()
        except IOError:
            pass

    def add_player_score(self, time):
        w, h = cocos.director.director.get_window_size()
        if len(self.high_scores) < self.hall_of_fame_length:
            self.made_score_list = True
            self.finished_name = False
            self.high_scores.append(("**Your Name**", time, c["player"]))
            self.high_scores.sort(score_sort)

            label = ct.Label("YOU MADE THE HIGH SCORE LIST!",
                   font_name = "newshampark",
                   font_size = 35,
                   anchor_y = "center",
                   anchor_x = "center",
                   color = (0,0,0,255))
            label.position = (w/2, 555)
            self.add(label, z = 5)


            return

        if self.high_scores[-1][1] > time:
            self.made_score_list = True
            self.finished_name = False
            self.high_scores.pop()
            self.high_scores.append(("**Your Name**", time, c["player"]))
            self.high_scores.sort(score_sort)

            label = ct.Label("YOU MADE THE HIGH SCORE LIST!",
                   font_name = "newshampark",
                   font_size = 35,
                   anchor_y = "center",
                   anchor_x = "center",
                   color = (0,0,0,255))
            label.position = (w/2,555)
            self.add(label, z = 5)




    def construct_table(self):
        self.table = []
        self.entry_length = 80
        w, h = cocos.director.director.get_window_size()
        for i, s in enumerate(self.high_scores):
            time_str = "%dm %ds" % (s[1] / 60, s[1] % 60)
            name = s[0]
            pos = "#%2d: " % (i+1)
            number_of_dots = self.entry_length - len(time_str) - len(name) - len (pos)
            dots = "." * number_of_dots
            table_entry = "%s%s%s%s"%(pos, name, dots, time_str)
            self.table.append(table_entry)
            posy = h - 380 - (self.font_size * 2.0 * i)



            pos_label = ct.Label(pos,
                   font_name = "Nimbus Roman No9 L",
                   font_size = self.font_size,
                   anchor_y = "top",
                   anchor_x = "left",
                   color = (0,0,0,255))
            pos_label.position = (315, posy)

            name_label = ct.Label(name,
                   font_name = "Nimbus Roman No9 L",
                   font_size = self.font_size,
                   anchor_y = "top",
                   anchor_x = "left",
                   color = (0,0,0,255))

            name_label.position = (365, posy)

            if s[2] == c["player"]:
                self.name_label = name_label

            time_label = ct.Label(time_str,
                    font_name = "Nimbus Roman No9 L",
                    font_size = self.font_size,
                    anchor_y = "top",
                    anchor_x = "right",
                    color = (0,0,0,255))

            time_label.position = (w - 310, posy)


            self.add(pos_label, z = 5)
            self.add(name_label, z = 5)
            self.add(time_label, z = 5)

        return 


    def on_text( self, t ):
        if not self.made_score_list:
            return False

        if t==';':
            return
        if t=='\r':
            return True
    
        if self.key_count == 0:
            self.name_label.element.text = ""
        self.key_count += 1
        self.name_label.element.text += t

def score_sort(a, b):
    if a[1] > b[1]:
        return 1
    return -1
