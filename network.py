from layers import (
	RecognitionLayer,
	CompareLayer
)

"""
	Файл класса нейронной сети
"""

class Network:
	recognition_layer = None #слой распознавания
	compare_layer = None #слой сравнения
	p = 0.85 #порог сходства для слоя сравнения
	protocol = ""
	
	#----------------------------
	def __init__(self, data_len): #фаза инициализации
		self.create_layers(data_len)
	#-------------------
	def create_layers(self, data_len):
		#создаем слой распознавания
		self.recognition_layer = RecognitionLayer(data_len) 
		#создаем слой сравнения
		self.compare_layer = CompareLayer() 
		
	#-------------------
	def clear_all(self):
		del self.recognition_layer
		del self.compare_layer
		self.recognition_layer = None
		self.compare_layer = None
	#------------------
	def G1(self, X, R): #определение сигнала G1, влияющего на вектор C отклика нейронов в слое сравнения
		#G1 = (x1 | ... | xn) ^ R
		if R == 1:
			return 0
		for i in range(len(X)):
			if X[i] == 1:
				return 1
		return 0
	#---------------	
	def G2(self, X): #определение сигнала G2, влияющего на выходной вектор R слоя распознавания
		#G2 = x1 | ... | xn
		for i in range(len(X)):
			if X[i] == 1:
				return 1
		return 0
	#------------------	
	def input(self, X): #подача образа сети
		self.protocol = ""
		if not self.recognition_layer or not self.compare_layer:
			self.clear_all()
			self.create_layers(len(X))
		#настраиваем порог сходства для слоя сравнения
		self.compare_layer.setup_similarity(self.p) 
		#фаза распознавания
		#сбрасываем вектор R слоя распознавания, т.к. новый образ
		self.recognition_layer.reset_R() 
		#определяем сигнал G2, если он 1, значит будем учитывать результат слоя распознавания
		G2 = self.G2(X)
		#получаем вектор R слоя распознавания
		R = self.recognition_layer.get_R(G2) 
		#определяем сигнал G1
		G1 = self.G1(X, R) 
		#получаем C вектор из слоя сравнения
		#т.к. еще нет подходящего нейрона, вектор P=pk * tki отсутствует, поэтому он None
		C = self.compare_layer.output(X, G1, None) 
		
		#ищем в слое распознавания нейрон с лучшим значением sj
		best_neuron_idx, sj = self.recognition_layer.find_best_neuron(C)
		for s in sj:
			self.protocol += s + '\n'
		# input()
		if not best_neuron_idx: 
			self.protocol += f"Нейрон с лучшей s нераспределенный\n"
			#лучшим оказался нераспределенный
			self.recognition_layer.add_new_neuron(C) #добавляем новую классификацию
		else:
			self.protocol += f"Нейрон с лучшей s {best_neuron_idx}\n"
			#нашли лучший нейрон, который не является нераспределенным
			#фаза сравнения
			self.compare_phase(best_neuron_idx, X, C, G2)
		weights = self.recognition_layer.get_neurons_weights()
		for weight in weights:
			for val in weight:
				self.protocol += f"{val}\n"
	#--------------------------------------------------
	def compare_phase(self, best_neuron_idx, X, C, G2): #фаза сравнения
		#получаем значение R для изменения сигнала G1
		R = self.recognition_layer.get_R(G2) 
		#получаем P = rk * tki из слоя распознавания, т.к. R = 1, то P = tk
		P = self.recognition_layer.neuron_T(best_neuron_idx)
		#т.к. R стал 1, то G1 = 0
		G1 = self.G1(X, R)
		#получаем C из слоя сравнения для модицифкации нейрона в слое распознавания
		C = self.compare_layer.output(X, G1, P)
		
		#проверяем сигнал сброса для k-го нейрона
		reset, protocol_info = self.compare_layer.reset(X, C)
		self.protocol += protocol_info + '\n'
		if reset:
			#фаза поиска
			#продолжаем поиск следующего лучшего нейрона, который возможно совпадет
			self.protocol += "Сигнал сброса, продолжаем поиск следующего нейрона, который возможно совпадет\n"
			best_neuron_idx, sj = self.recognition_layer.find_best_neuron(C)
			for s in sj:
				self.protocol += s + '\n'
			if not best_neuron_idx:
				#лучшим оказался нераспределенный
				self.recognition_layer.add_new_neuron(X)
			else:
				#иначе снова сравниваем
				self.compare_phase(best_neuron_idx, X, C, G2)
		else:
			#нашли совпадение нейрона со сходством >= порогу сходства
			#модицифицируем нейрон в слое распознавания
			self.recognition_layer.modify_neuron(best_neuron_idx, C)
	#---------------------
	def get_neurons_images(self):
		return self.recognition_layer.get_neurons_images()
#---Network---