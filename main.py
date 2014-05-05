import kivy
import random
import string
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import *
from kivy.core.audio import SoundLoader

NUM = 5
COLOR = [0,0,0,0.8]
class StartScreen(Screen):
	def __init__(self,sm,**kwargs):
		super(StartScreen,self).__init__(**kwargs)
		self.sm = sm
		self.name = 'startscreen'
		self.music = SoundLoader.load('Resources/bub.wav')
		self.music.loop = True
		self.music.play()
		back = Image(source = 'Resources/bg.jpg',keep_ratio= False,allow_stretch = True)
		box = BoxLayout(orientation = 'vertical')
		spacer1 = Label()
		spacer2 = Label()
		self.sound = SoundLoader.load('Resources/pop.wav')
		label = Label(text = 'How Drunk Are You!',font_name = 'Resources/BILLO.ttf',font_size = 56,color = COLOR)
		button = Button(text = 'START',background_normal = 'Resources/option.png',background_down = 'Resources/option_pressed.png',font_name = 'Resources/BILLO.ttf',font_size = 48,color = COLOR)
		button.bind(on_release = self.start)
		box.add_widget(spacer1)
		box.add_widget(label)
		box.add_widget(button)
		box.add_widget(spacer2)
		self.add_widget(back)
		self.add_widget(box)
	def start(self,button,*args):
		self.sound.play()
		self.sm.add_widget(MainScreen(self.sm,name = 'mainscreen'))
		self.sm.current = 'mainscreen'

class ResultScreen(Screen):
	def __init__(self,sm,percentage,**kwargs):
		super(ResultScreen,self).__init__(**kwargs)
		self.sm = sm
		back = Image(source = 'Resources/bg.jpg',keep_ratio= False,allow_stretch = True)
		box = BoxLayout(orientation = 'vertical')
		self.sound = SoundLoader.load('Resources/pop.wav')
		label = Label(text = 'You are '+str(percentage)+'% drunk!',font_name = 'Resources/BILLO.ttf',font_size = 56,color = COLOR)
		self.again = Button(background_normal = 'Resources/option.png',background_down = 'Resources/option_pressed.png',text = 'Try Again!',size_hint = (1,0.4),pos_hint = {'center_x':0.5,'center_y':0.5},font_name = 'Resources/BILLO.ttf',font_size = 30,color = COLOR)
		self.again.bind(on_release = self.restart)
		self.exit = Button(background_normal = 'Resources/option.png',background_down = 'Resources/option_pressed.png',text = 'Close',size_hint = (1,0.4),pos_hint = {'center_x':0.5,'center_y':0.5},font_name = 'Resources/BILLO.ttf',font_size = 30,color = COLOR)
		self.exit.bind(on_release = self.close)
		box.add_widget(label)
		box.add_widget(self.again)
		box.add_widget(self.exit)
		self.add_widget(back)
		self.add_widget(box)
	def restart(self,*args):
		self.sound.play()
		lst = [random.choice(string.ascii_letters + string.digits) for n in xrange(10)]
		str = "".join(lst)
		self.sm.add_widget(MainScreen(self.sm,name = str))
		self.sm.current = str
	def close(self,*args):
		self.sound.play()
		global myapp
		myapp.stop()
	
class MainScreen(Screen):
	def __init__(self,sm,**kwargs):
		super(MainScreen,self).__init__(**kwargs)
		self.sm = sm
		self.score = 0
		self.count = 0
		self.questions = []
		self.createquestions()
		back = Image(source = 'Resources/bg.jpg',keep_ratio= False,allow_stretch = True)
		self.box = BoxLayout(orientation = 'vertical')
		self.label = Label(font_name = 'Resources/BILLO.ttf',font_size = 32,color = COLOR,halign = 'center',size_hint = (1,1.2))
		self.op1 = Button(background_normal = 'Resources/option.png',background_down = 'Resources/option_pressed.png',font_name = 'Resources/BILLO.ttf',font_size = 48,color = COLOR)
		self.op2 = Button(background_normal = 'Resources/option.png',background_down = 'Resources/option_pressed.png',font_name = 'Resources/BILLO.ttf',font_size = 48,color = COLOR)
		self.op3 = Button(background_normal = 'Resources/option.png',background_down = 'Resources/option_pressed.png',font_name = 'Resources/BILLO.ttf',font_size = 48,color = COLOR)
		self.op1.bind(on_release = self.checkpress)
		self.op2.bind(on_release = self.checkpress)
		self.op3.bind(on_release = self.checkpress)
		self.refreshquestion()
		self.box.add_widget(self.label)
		self.box.add_widget(self.op1)
		self.box.add_widget(self.op2)
		self.box.add_widget(self.op3)
		self.add_widget(back)
		self.add_widget(self.box)
	def refreshquestion(self):
		if len(self.questions)!=0:
			num = random.randint(0,len(self.questions)-1)
		question = self.questions.pop(num)
		self.label.text = question[0]
		self.op1.text = question[1]
		self.op2.text = question[2]
		self.op3.text = question[3]
		self.correct = question[4]
		self.sound = SoundLoader.load('Resources/pop.wav')
	def results(self):
		percentage = 100 - (self.score*100/NUM)
		self.clear_widgets()
		lst = [random.choice(string.ascii_letters + string.digits) for n in xrange(10)]
		str = "".join(lst)
		resultscreen = ResultScreen(self.sm,percentage,name = str)
		self.sm.add_widget(resultscreen)
		self.sm.current = str
	def checkpress(self,opt,*args):
		self.sound.play()
		if opt.text == self.correct:
			self.score += 1
		self.count += 1
		if self.count == NUM:
			self.results()
		else:
			self.refreshquestion()
	def createquestions(self):
		self.questions.append(['Who discovered America?','Galelio','Vasco Da Gama','Columbus','Columbus'])
		self.questions.append(['What is 7 x 8?','56','65','72','56'])
		self.questions.append(['How many 3s are in 3333333?','3','7','9','7'])
		self.questions.append(['Cat : Kitten as Dog : ___ ?','Puppy','Pipe','Bitch','Puppy'])
		self.questions.append(['What is the 12th letter of\nthe english alphabet?','I','J','L','L'])
		self.questions.append(['What is the capital of Rome?','Rome','Washington D.C.','Im not that drunk!','Im not that drunk!'])
		self.questions.append(['How many zeros are there in\n1 billion?','6','9','1 billion','9'])
		self.questions.append(['Roses are red,Violets are ___ ?','Violet, duh!','Blue','Flowers','Blue'])
		self.questions.append(['Which is heavier,\n1 lb cotton or 1 lb iron?','Cotton','Iron','Neither','Neither'])
		self.questions.append(['If 3 cats are sitting on a table,\nhow many legs are there in all?','9','12','16','16'])
		self.questions.append(['What is next in this series?\n25,24,22,19,15','5','10','14','10'])
		self.questions.append(['At the end of a banquet 10 people\nshake hands with each other.\nHow many handshakes will there be in total?','100','50','45','45'])
		self.questions.append(['The day before the day before yesterday\nis three days after Saturday.\nWhat day is it today?','Wednesday','Thursday','Friday','Friday'])
		self.questions.append(['Library is to book as book is to','Copy','Page','Cover','Page'])
		self.questions.append(['Which of the following can be\narranged into a 5-letter\nEnglish word?',' W Q R G S','R I L S A','H R G S T','R I L S A'])
		self.questions.append(['Find the odd one out\nLion, Mouse, Cat, Snake, Elephant','Elephant','Snake','Lion','Snake'])
		self.questions.append(['PEACH : HCAEP as 46251 : ___ ?','15264','12654','51462','15264'])
		self.questions.append(['What is next in the series:\n1,1,3,5,8,13,__?','21','17','11','21'])
		self.questions.append(['If you rearrange the letters\n"CIFAIPC"\nyou would have the name of a (n):','City','Ocean','River','Ocean'])
		self.questions.append(['Choose the number that is\n1/4 of 1/2 of 1/5 of 200:','5','10','25','5'])
		#self.questions.append(['','','','',''])
class MyApp(App):
	title = 'How Drunk Are You'
	appwindow = FloatLayout()
	def build(self):
		self.icon = 'Resources/icon.png'
		sm = ScreenManager(transition = WipeTransition())
		sm.add_widget(StartScreen(sm))
		sm.current = 'startscreen'
		self.appwindow.add_widget(sm)
		return self.appwindow

if __name__ == '__main__':
	Builder.load_string('''
''')
	global myapp
	myapp = MyApp()
	myapp.run()
