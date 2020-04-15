from network import Network
from interface import MainScreen

#интерфейс
#возможность рисовать свой образец для сети

#образцы
datas = [
	[
		[1, 0, 0, 1, 1, 1],
		[1, 1, 1, 0, 0, 0]
	],
	[
		[1, 1, 0, 0, 0, 0],
		[0, 0, 1, 1, 1, 1]
	],
	[
		[1, 1, 0, 0, 1, 0],
		[0, 0, 1, 1, 1, 1]
	],
	[
		[1, 0, 0, 0, 1, 1],
		[1, 1, 1, 0, 0, 0]
	],
	[
		[0, 0, 0, 0, 1, 0],
		[1, 1, 1, 0, 0, 0]
	]
]
#размер изображения для инициализации нейронной сети
m = len(datas[0]) * len(datas[0][0])
now_image = -1

network = Network(m)
		
screen = MainScreen()


#добавить изменение порога сходства

def next_step(self):
	global now_image, network, datas, screen
	now_image += 1
	if now_image >= len(datas):
		now_image -= 1
		return
	#подача изображения в сеть
	X = []
	#поиск максимального n и m, для дополнения отсутствующих значений
	for row in datas[now_image]:
		X += row
	network.p = screen.get_similarity()
	network.input(X)
	# network.print_images()
	screen.view_example(datas[now_image])
	screen.add_in_protocol(network.protocol)
	#вывод протокола
	

def reset(self):
	global now_image, network, screen, datas, m
	now_image = -1
	#переинициализация слоев с максимальным значением data
	network = Network(m)
	
def show_all_examples(self):
	global screen, datas
	screen.show_all_examples(datas)

def show_network_examples(self):
	global network, screen, datas
	# print()
	screen.show_network_examples(network.get_neurons_images(),len(datas[0]), len(datas[0][0]))
	

screen.next_step_btn.bind("<Button-1>", next_step)
screen.reset_btn.bind("<Button-1>", reset)
screen.all_examples_btn.bind("<Button-1>", show_all_examples)
# screen.add_new_example_btn.bind("<Button-1>", add_new)
screen.network_examples_btn.bind("<Button-1>", show_network_examples)

screen.start()
