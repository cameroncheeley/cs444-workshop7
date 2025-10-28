import pygame, math, os

pygame.init()

STATE_IMAGE = pygame.image.load(os.path.join('Assets', 'circle.png'))
STATE = pygame.transform.rotate(pygame.transform.scale(STATE_IMAGE, (180, 180)), 0)

ACCEPTED_STATE_IMAGE = pygame.image.load(os.path.join('Assets', 'circleaccept.png'))
ACCEPTED_STATE = pygame.transform.rotate(pygame.transform.scale(ACCEPTED_STATE_IMAGE, (180, 180)), 0)

ARROW_IMAGE = pygame.image.load(os.path.join('Assets', 'arrow.png'))
LEFT_ARROW = pygame.transform.rotate(
    pygame.transform.scale(ARROW_IMAGE, (80, 40)), 0)
RIGHT_ARROW = pygame.transform.flip(LEFT_ARROW, True, False)
ULEFT_ARROW = pygame.transform.rotate(RIGHT_ARROW, 180)
URIGHT_ARROW = pygame.transform.flip(LEFT_ARROW, True, False)


LOOP_IMAGE = pygame.image.load(os.path.join('Assets', 'loop.png'))
LOOP = pygame.transform.rotate(
    pygame.transform.scale(LOOP_IMAGE, (60, 60)), 270)

window_height = 500
window_width = 600
window  = pygame.display.set_mode((window_height,window_width))
pygame.display.set_caption("DFA Transitions")
# the buttons for the shop MENU
class button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.over = False

    def draw(self,window,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(window, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
                    
        pygame.draw.rect(window, self.color, (self.x,self.y,self.width,self.height),0)
                
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 40)
            text = font.render(self.text, 1, (0,0,0))
            window.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

    def playSoundIfMouseIsOver(self, pos, sound):
        if self.isOver(pos):            
            if not self.over:
                beepsound.play()
                self.over = True
        else:
            self.over = False
                    
white = (255,255,255)
# the numbers 
s_1s = button((0,255,0),40,450,30,30, '1')
s_2s = button((0,255,0),40,400,30,30, '2')
s_3s = button((0,255,0),40,350,30,30, '3')
s_4s = button((0,255,0),100,450,30,30, '4')
s_5s = button((0,255,0),100,400,30,30, '5')
s_6s = button((0,255,0),100,350,30,30, '6')
s_7s = button((0,255,0),150,450,30,30, '7')
s_8s = button((0,255,0),150,400,30,30, '8')
s_9s = button((0,255,0),150,350,30,30, '9')
s_0s = button((0,255,0),200,450,30,30, '0')

numbers = [s_1s,s_2s,s_3s,s_4s,s_5s,s_6s,s_7s,s_8s,s_9s,s_0s]

# the symbols!
d_1s = button((0,255,0),260,450,30,30, '+')
d_2s = button((0,255,0),260,400,30,30, '-')
d_3s = button((0,255,0),260,350,30,30, 'x')
d_4s = button((0,255,0),200,400,30,30, '÷')
d_5s = button((0,255,0),300,350,120,60, 'return')
d_6s = button((0,255,0),200,350,30,30, 'C')

symbols = [d_5s,d_6s]


# redraw window
def redraw(inputtap):
    # draw all the numbers
    for button in numbers:
        button.draw(window)

    # the symbols
    for button in symbols:
        button.draw(window)

    inputtap.draw(window)

def draw_question(text):
    font = pygame.font.SysFont('comicsans', 40)
    draw_text = font.render(text, 1, white)
    pygame.draw.rect(window, (0,0,0), (0, 225, window_width, window_height/2 - 195))
    window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50, window_height/2 - draw_text.get_height()/2))
    pygame.display.update()
    # print(text)
    # pygame.time.delay(5000)

def drawDFA():
    # Draw the DFA
    pygame.draw.rect(window, (0,0,0), (0, 225, window_width, window_height/2 - 195))
    if nums[0] == 1:
        alphlength = nums[1]
        group = []
        if 0 in accepts:
            window.blit(ACCEPTED_STATE, (160, 80))
        else:
            window.blit(STATE, (160, 80))
        for i in range(alphlength):
            if nums[2 + alphlength + i] == 0:
                group.append(nums[2 + i])
                window.blit(LOOP, (220, 80))
        font = pygame.font.SysFont('comicsans', 30)
        draw_text = font.render("0", 1, white)
        window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50, window_height/2 - draw_text.get_height()/2 - 88))
        draw_text = font.render(str(group), 1, white)
        if len(group) != 0:
            window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50, window_height/2 - draw_text.get_height()/2 - 170))
    if nums[0] == 2:
        alphlength = nums[1]
        zeroone = []
        onezero = []
        zerozero = []
        oneone = []
        if 0 in accepts:
            window.blit(ACCEPTED_STATE, (80, 80))
        else:
            window.blit(STATE, (80, 80))
        if 1 in accepts:
            window.blit(ACCEPTED_STATE, (240, 80))
        else:
            window.blit(STATE, (240, 80))
        # window.blit(RIGHT_ARROW, (210, 110))
        font = pygame.font.SysFont('comicsans', 30)
        draw_text = font.render("0", 1, white)
        window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50 - 80, window_height/2 - draw_text.get_height()/2 - 88))
        draw_text = font.render("1", 1, white)
        window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50 + 80, window_height/2 - draw_text.get_height()/2 - 88))
        # draw_text = font.render(str(nums[2]), 1, white)
        # window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50, window_height/2 - draw_text.get_height()/2 - 150))
        # 0 to 1
        for i in range(alphlength):
            if nums[2 + alphlength + i] == 1:
                zeroone.append(nums[2 + i])
                window.blit(RIGHT_ARROW, (210, 110))
            if nums[2 + alphlength + i] == 0:
                zerozero.append(nums[2 + i])
                window.blit(LOOP, (140, 80))
        font = pygame.font.SysFont('comicsans', 30)
        if len(zeroone) != 0:
            draw_text = font.render(str(zeroone), 1, white)
            window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50, window_height/2 - draw_text.get_height()/2 - 150))
        # 1 to 0
        for i in range(alphlength):
            if nums[2 + alphlength + alphlength + i] == 0:
                onezero.append(nums[2 + i])
                window.blit(ULEFT_ARROW, (210, 170))
            if nums[2 + alphlength + alphlength + i] == 1:
                oneone.append(nums[2 + i])
                window.blit(LOOP, (300, 80))
        font = pygame.font.SysFont('comicsans', 30)
        if len(onezero) != 0:
            draw_text = font.render(str(onezero), 1, white)
            window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50, window_height/2 - draw_text.get_height()/2 - 90))
        # 0 to 0
        font = pygame.font.SysFont('comicsans', 30)
        if len(zerozero) != 0:
            draw_text = font.render(str(zerozero), 1, white)
            window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50 - 80, window_height/2 - draw_text.get_height()/2 - 170))
        # 1 to 1
        if len(oneone) != 0:   
            draw_text = font.render(str(oneone), 1, white)
            window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50 + 80, window_height/2 - draw_text.get_height()/2 - 170))
    if nums[0] == 3:
        alphlength = nums[1]
        zeroone = []
        onezero = []
        zerozero = []
        oneone = []
        zerotwo = []
        twozero = []
        twoone = []
        onetwo = []
        twotwo = []
        if 0 in accepts:
            window.blit(ACCEPTED_STATE, (80, 20))
        else:
            window.blit(STATE, (80, 20))
        if 1 in accepts:
            window.blit(ACCEPTED_STATE, (240, 20))
        else:
            window.blit(STATE, (240, 20))
        if 2 in accepts:
            window.blit(ACCEPTED_STATE, (160, 145))
        else:
            window.blit(STATE, (160, 145))
        # window.blit(RIGHT_ARROW, (210, 110))
        font = pygame.font.SysFont('comicsans', 30)
        draw_text = font.render("0", 1, white)
        window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50 - 80, window_height/2 - draw_text.get_height()/2 - 88 - 60))
        draw_text = font.render("1", 1, white)
        window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50 + 80, window_height/2 - draw_text.get_height()/2 - 88 - 60))
        draw_text = font.render("2", 1, white)
        window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50, window_height/2 - draw_text.get_height()/2 - 23))
        # draw_text = font.render(str(nums[2]), 1, white)
        # window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50, window_height/2 - draw_text.get_height()/2 - 150))
        # 0 to 1
        for i in range(alphlength):
            if nums[2 + alphlength + i] == 1:
                zeroone.append(nums[2 + i])
                window.blit(RIGHT_ARROW, (210, 110 - 60))
            if nums[2 + alphlength + i] == 0:
                zerozero.append(nums[2 + i])
                window.blit(LOOP, (140, 80 - 60))
            if nums[2 + alphlength + i] == 2:
                zerotwo.append(nums[2 + i])
                window.blit(pygame.transform.rotate(RIGHT_ARROW, 320), (180, 120))
        font = pygame.font.SysFont('comicsans', 30)
        if len(zeroone) != 0:
            draw_text = font.render(str(zeroone), 1, white)
            window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50, window_height/2 - draw_text.get_height()/2 - 150 - 60))
        
        # 1 to 0
        for i in range(alphlength):
            if nums[2 + alphlength + alphlength + i] == 0:
                onezero.append(nums[2 + i])
                window.blit(ULEFT_ARROW, (210, 170 - 60))
            if nums[2 + alphlength + alphlength + i] == 1:
                oneone.append(nums[2 + i])
                window.blit(LOOP, (300, 80 - 60))
            if nums[2 + alphlength + alphlength + i] == 2:
                onetwo.append(nums[2 + i])
                window.blit(pygame.transform.rotate(RIGHT_ARROW, 230), (270, 130))
        
        for i in range(alphlength):
            if nums[2 + alphlength + alphlength + alphlength + i] == 0:
                twozero.append(nums[2 + i])
                window.blit(pygame.transform.rotate(ULEFT_ARROW, 310), (145, 140))
            if nums[2 + alphlength + alphlength + alphlength + i] == 1:
                twoone.append(nums[2 + i])
                window.blit(pygame.transform.rotate(RIGHT_ARROW, 50), (250, 110))
            if nums[2 + alphlength + alphlength + alphlength + i] == 2:
                twotwo.append(nums[2 + i])
                window.blit(pygame.transform.rotate(LOOP, 270), (280, 210))
        font = pygame.font.SysFont('comicsans', 30)
        if len(onezero) != 0:
            draw_text = font.render(str(onezero), 1, white)
            window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50, window_height/2 - draw_text.get_height()/2 - 90 - 60))
        # 0 to 0
        if len(zerozero) != 0:
            draw_text = font.render(str(zerozero), 1, white)
            window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50 - 80, window_height/2 - draw_text.get_height()/2 - 170 - 60))
        # 1 to 1
        if len(oneone) != 0:   
            draw_text = font.render(str(oneone), 1, white)
            window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50 + 80, window_height/2 - draw_text.get_height()/2 - 170 - 60))
        # 0 to 2
        if len(zerotwo) != 0:
            draw_text = font.render(str(zerotwo), 1, white)
            window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50 - 40, window_height/2 - draw_text.get_height()/2 - 50 - 30))
        # 1 to 2
        if len(onetwo) != 0:
            draw_text = font.render(str(onetwo), 1, white)
            window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50 + 90, window_height/2 - draw_text.get_height()/2 - 50 - 20))
        # 2 to 0
        if len(twozero) != 0:
            draw_text = font.render(str(twozero), 1, white)
            window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50 - 40 - 30, window_height/2 - draw_text.get_height()/2 - 40))
        # 2 to 1
        if len(twoone) != 0:
            draw_text = font.render(str(twoone), 1, white)
            window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50 + 40, window_height/2 - draw_text.get_height()/2 - 50 - 40))
        # 2 to 2
        if len(twotwo) != 0:
            draw_text = font.render(str(twotwo), 1, white)
            window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50 + 100, window_height/2 - draw_text.get_height()/2 - 50 + 30))
    if nums[0] == 4:
        alphlength = nums[1]
        zeroone = []
        onezero = []
        zerozero = []
        oneone = []
        zerotwo = []
        twozero = []
        twoone = []
        onetwo = []
        twotwo = []
        if 0 in accepts:
            window.blit(ACCEPTED_STATE, (80, 20))
        else:
            window.blit(STATE, (80, 20))
        if 1 in accepts:
            window.blit(ACCEPTED_STATE, (240, 20))
        else:
            window.blit(STATE, (240, 20))
        if 2 in accepts:
            window.blit(ACCEPTED_STATE, (240, 145))
        else:
            window.blit(STATE, (240, 145))
        if 3 in accepts:
            window.blit(ACCEPTED_STATE, (80, 145))
        else:
            window.blit(STATE, (80, 145))
        # window.blit(RIGHT_ARROW, (210, 110))
        font = pygame.font.SysFont('comicsans', 30)
        draw_text = font.render("0", 1, white)
        window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50 - 80, window_height/2 - draw_text.get_height()/2 - 88 - 60))
        draw_text = font.render("1", 1, white)
        window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50 + 80, window_height/2 - draw_text.get_height()/2 - 88 - 60))
        draw_text = font.render("2", 1, white)
        window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50 + 80, window_height/2 - draw_text.get_height()/2 - 23))
        draw_text = font.render("3", 1, white)
        window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50 - 80, window_height/2 - draw_text.get_height()/2 - 23))
        # draw_text = font.render(str(nums[2]), 1, white)
        # window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50, window_height/2 - draw_text.get_height()/2 - 150))
        # 0 to 1
        for i in range(alphlength):
            if nums[2 + alphlength + i] == 1:
                zeroone.append(nums[2 + i])
                window.blit(RIGHT_ARROW, (210, 110 - 60))
            if nums[2 + alphlength + i] == 0:
                zerozero.append(nums[2 + i])
                window.blit(LOOP, (140, 80 - 60))
            if nums[2 + alphlength + i] == 2:
                zerotwo.append(nums[2 + i])
                window.blit(pygame.transform.rotate(RIGHT_ARROW, 320), (180, 120))
        font = pygame.font.SysFont('comicsans', 30)
        if len(zeroone) != 0:
            draw_text = font.render(str(zeroone), 1, white)
            window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50, window_height/2 - draw_text.get_height()/2 - 150 - 60))
        
        # 1 to 0
        for i in range(alphlength):
            if nums[2 + alphlength + alphlength + i] == 0:
                onezero.append(nums[2 + i])
                window.blit(ULEFT_ARROW, (210, 170 - 60))
            if nums[2 + alphlength + alphlength + i] == 1:
                oneone.append(nums[2 + i])
                window.blit(LOOP, (300, 80 - 60))
            if nums[2 + alphlength + alphlength + i] == 2:
                onetwo.append(nums[2 + i])
                window.blit(pygame.transform.rotate(RIGHT_ARROW, 230), (270, 130))
        
        for i in range(alphlength):
            if nums[2 + alphlength + alphlength + alphlength + i] == 0:
                twozero.append(nums[2 + i])
                window.blit(pygame.transform.rotate(ULEFT_ARROW, 310), (145, 140))
            if nums[2 + alphlength + alphlength + alphlength + i] == 1:
                twoone.append(nums[2 + i])
                window.blit(pygame.transform.rotate(RIGHT_ARROW, 50), (250, 110))
            if nums[2 + alphlength + alphlength + alphlength + i] == 2:
                twotwo.append(nums[2 + i])
                window.blit(pygame.transform.rotate(LOOP, 270), (280, 210))
        font = pygame.font.SysFont('comicsans', 30)
        if len(onezero) != 0:
            draw_text = font.render(str(onezero), 1, white)
            window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50, window_height/2 - draw_text.get_height()/2 - 90 - 60))
        # 0 to 0
        if len(zerozero) != 0:
            draw_text = font.render(str(zerozero), 1, white)
            window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50 - 80, window_height/2 - draw_text.get_height()/2 - 170 - 60))
        # 1 to 1
        if len(oneone) != 0:   
            draw_text = font.render(str(oneone), 1, white)
            window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50 + 80, window_height/2 - draw_text.get_height()/2 - 170 - 60))
        # 0 to 2
        if len(zerotwo) != 0:
            draw_text = font.render(str(zerotwo), 1, white)
            window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50 - 40, window_height/2 - draw_text.get_height()/2 - 50 - 30))
        # 1 to 2
        if len(onetwo) != 0:
            draw_text = font.render(str(onetwo), 1, white)
            window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50 + 90, window_height/2 - draw_text.get_height()/2 - 50 - 20))
        # 2 to 0
        if len(twozero) != 0:
            draw_text = font.render(str(twozero), 1, white)
            window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50 - 40 - 30, window_height/2 - draw_text.get_height()/2 - 40))
        # 2 to 1
        if len(twoone) != 0:
            draw_text = font.render(str(twoone), 1, white)
            window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50 + 40, window_height/2 - draw_text.get_height()/2 - 50 - 40))
        # 2 to 2
        if len(twotwo) != 0:
            draw_text = font.render(str(twotwo), 1, white)
            window.blit(draw_text, (window_width/2 - draw_text.get_width()/2 - 50 + 100, window_height/2 - draw_text.get_height()/2 - 50 + 30))
    
    pygame.display.update()

def Symbols():
    global user_input
    global python_input
    global is_finished
    global flag1
    global flag2
    global flag3
    global nums
    global accepts
    global question
    global chars

    
    

    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()

        try:
            if is_finished or user_input[-1] in ["+", "-", "x", "÷", "="]:
                # User shouldn't type two symbols continuously
                # User shouldn't input any symbols when game finished because there is no number
                return
        except IndexError:
            # User shouldn't input any symbols if there is no number
            return


        

        if d_5s.isOver(pos):
            user_input = ""
            if flag1:
                flag2 = True
                # question = "Length of alphabet?"
            print("=")
            flag1 = True
            result = eval(python_input)
            nums.append(result)
            if len(nums) == 1:
                question = "Length of alphabet?"
            if len(nums) == 2:
                chars = nums[1]
            if len(nums) >= 2 and len(nums) < chars + 2:
                question = "Character number " + str(len(nums) - 1) + "?"
            if len(nums) >= chars + 2:
                if len(nums) >= chars + 2 + chars * nums[0]:
                    question = "# of accepting states?"
                    if len(nums) >= chars + 3 + chars * nums[0]:
                        print("Index")
                        print(len(nums))
                        print(2 + chars + (chars * nums[0]))
                        if flag3:
                            accepts.append(result)
                        question = "accepting state " + str(len(nums) - (2 + chars + (nums[0] * chars))) + "?"
                        flag3 = True
                    
                else:
                    offset = len(nums) - chars - 2
                    state = offset // chars
                    transition = offset % chars
                    transition = nums[transition + 2]
                    question = "delta(" + str(state) + ", " + str(transition) + ") = ?"
            
            python_input = ""
            # user_input += f"={result:.2f}"
            print(f"Result: {result:.2f}")
            print(nums)
            print(accepts)
            is_finished = True

        if d_6s.isOver(pos):
            print("C")
            python_input = ""
            user_input = ""

def MOUSEOVERnumbers():
    global user_input
    global python_input
    global is_finished


    if event.type == pygame.MOUSEBUTTONDOWN:
        if is_finished:
            user_input = ""
            python_input = ""
            is_finished = False
        pos = pygame.mouse.get_pos()          
        if s_1s.isOver(pos):
            print("1")
            user_input += "1"
            python_input += "1"
        if s_2s.isOver(pos):
            print("2")
            user_input += "2"
            python_input += "2"
        if s_3s.isOver(pos):
            print("3")
            user_input += "3"
            python_input += "3"
        if s_4s.isOver(pos):
            print("4")
            user_input += "4"
            python_input += "4"
        if s_5s.isOver(pos):
            print("5")
            user_input += "5"
            python_input += "5"
        if s_6s.isOver(pos):
            print("6")
            user_input += "6"
            python_input += "6"
        if s_7s.isOver(pos):
            print("7")
            user_input += "7"
            python_input += "7"
        if s_8s.isOver(pos):
            print("8")
            user_input += "8"
            python_input += "8"
        if s_9s.isOver(pos):
            print("9")
            user_input += "9"
            python_input += "9"
        if s_0s.isOver(pos):
            print("0")
            user_input += "0"
            python_input += "0"

# the main loop
run = True
user_input = ""
python_input = ""
is_finished = True
flag1 = False
flag2 = False
flag3 = False
nums = []
accepts = []
question = "Number of states?"
draw_question(question)
chars = 0

# loop for first two entries
while run:
    # input tap
    inputtap = button((253,100,32),10,280,450,50,f"{user_input}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if flag2:
            run = False

        MOUSEOVERnumbers()
        
        Symbols()
    draw_question(question)
    redraw(inputtap)
    pygame.display.update()
run = True

# loop for the number of chars
while run:
   # input tap
    inputtap = button((253,100,32),10,280,450,50,f"{user_input}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if len(nums) - 2 >= nums[1]:
            run = False
        

        MOUSEOVERnumbers()

        Symbols()
    draw_question(question)
    redraw(inputtap)
    pygame.display.update()

run = True
# loop for each transition
while run:
   # input tap
    inputtap = button((253,100,32),10,280,450,50,f"{user_input}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if len(nums) - 2 - nums[1] >= nums[0] * nums[1]:
            run = False
        

        MOUSEOVERnumbers()

        Symbols()
    draw_question(question)
    redraw(inputtap)
    pygame.display.update()
pygame.draw.rect(window, (0,0,0), (0, 225, window_width, window_height/2 - 195))
run = True
# loop for the number of states
while run:
   # input tap
    inputtap = button((253,100,32),10,280,450,50,f"{user_input}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if len(nums) - 2 - nums[1] >= nums[0] * nums[1] + 1:
            run = False
        

        MOUSEOVERnumbers()

        Symbols()
    draw_question(question)
    redraw(inputtap)
    pygame.display.update()
print("looking for accepting states")
# loop for accepting states
run = True
while run:
   # input tap
    inputtap = button((253,100,32),10,280,450,50,f"{user_input}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if len(nums) - 2 - nums[1] >= nums[0] * nums[1] + 1 + nums[2 + nums[1] + (nums[0] * nums[1])]:
            print("done")
            run = False


        MOUSEOVERnumbers()

        Symbols()
    draw_question(question)
    redraw(inputtap)
    pygame.display.update()
run = True 
# loop for the display
while run:
   # input tap
    inputtap = button((253,100,32),10,280,450,50,f"{user_input}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
       
        

        # MOUSEOVERnumbers()

        # Symbols()
    drawDFA()
    redraw(inputtap)
    pygame.display.update()
print(nums[0]*nums[1])    
pygame.quit()
