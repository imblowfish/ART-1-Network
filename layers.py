"""
	Файл классов слоев нейронной сети
"""

#класс нейрона слоя распознавания
class Neuron:
	b_weights = None #вектор весов Bk
	t_weights = None #вектор весов Tk
	
	#-------------------------
	def add_b_weight(self, w): #добавление нового значения к вектору весов Bk
		if not self.b_weights:
			self.b_weights = []
		self.b_weights.append(w)
	
	def add_t_weight(self, w): #добавление нового значения к вектору весов Tk
		if not self.t_weights:
			self.t_weights = []
		self.t_weights.append(w)
#---Neuron---

#слой распознавания
class RecognitionLayer:
	neurons = None #нейроны слоя распознавания
	L = 2 #константа для вычисления весов
	R = None #вектор реакции нейрона
	
	#----------------------------
	def __init__(self, data_len): #инициализация слоя распознавания
		#добавляем один нераспределенный нейрон в слой распознавания
		self.neurons = []
		#вычисляем его значение весов Bk
		w = self.L / (self.L - 1 + data_len)
		#вес нераспределенного нейрона должен быть < L/(L-1+m)
		w -= w/10 
		neuron = Neuron()
		for i in range(data_len):
			neuron.add_b_weight(w)
			neuron.add_t_weight(1)
		self.neurons.append(neuron)
		#добавляем выход нейрона к вектору R слоя распознавания
		self.R = [0]
	#-----------------------------------
	def add_new_neuron(self, C): #добавление новой классификации(нового нейрона)
		neuron = Neuron()
		neuron.t_weights = C.copy()
		c_sum = sum(C)
		for i in range(len(C)):
			#вычисляем вес по формуле (6.6)
			w = (self.L * C[i]) / (self.L - 1 + c_sum)
			neuron.add_b_weight(w)
		#добавляем выход нейрона к вектору R слоя распознавания
		self.R.append(0)
		self.neurons.append(neuron)
	#--------------------------------------
	def modify_neuron(self, neuron_idx, C): #модификация весов Tk и Bk нейрона на основе вектора C из слоя сравнения
		neuron = self.neurons[neuron_idx]
		c_sum = sum(C)
		for i in range(len(C)):
			w = (self.L * C[i]) / (self.L - 1 + c_sum)
			neuron.b_weights[i] = w
			neuron.t_weights[i] = C[i]
	#----------------------------
	def neuron_T(self, neuron_idx): #возврат вектора весов Tk нейрона
		return self.neurons[neuron_idx].t_weights
	#-------------------
	def get_R(self, G2): #получение сигнала R для работы с вектором P и сигналом G1
		for r in self.R:
			if r & G2 == 1:
				return 1
		return 0
	#-----------------
	def reset_R(self): #сброс всех ri из вектора R отлика нейронов 
		for i in range(len(self.R)):
			self.R[i] = 0
	#-----------------------------
	def find_best_neuron(self, C): #поиск нейрона с наибольшим значением sj
		neuron_idx = -1
		best_s = 0
		sj = []
		for i in range(len(self.neurons)):
			s = 0
			for j in range(len(C)):
				s += self.neurons[i].b_weights[j] * C[j]
			if i == 0:
				sj.append(f"Sj нераспределенного нейрона слоя распознавания = {s:.2f}")
			else:
				sj.append(f"Sj нейрона {i} слоя распознавания = {s:2f}")
			if s > best_s and self.R[i] != 1:
				best_s = s
				neuron_idx = i
		self.R[neuron_idx] = 1
		if neuron_idx == 0: #нулевой индекс у нераспределенного нейрона
			return None, sj
		return neuron_idx, sj
	#---------------------
	def get_neurons_images(self):
		images = []
		for neuron in self.neurons:
			image = []
			for val in neuron.t_weights:
				image.append(val)
			images.append(image)
		return images
	def get_neurons_weights(self):
		weights = []
		for i in range(len(self.neurons)):
			if i == 0:
				weight = ["Bн ", "Tн "]
			else:
				weight = [f"B{i} ", f"T{i} "]
			for j in range(len(self.neurons[i].b_weights)):
				weight[0] += f"{self.neurons[i].b_weights[j]:.2f} "
				weight[1] += f"{self.neurons[i].t_weights[j]:.2f} "
			weights.append(weight)
		return weights
#---RecognitionLayer---

#класс слоя сравнения
class CompareLayer:
	p = None #порог сходства
	
	#--------------------------
	def output(self, X, G1, P): #возврат вектора C слоя сравнения
		if not P:
			P = []
			for x in X:
				P.append(0)
		C = []
		for i in range(len(X)):
			#нейрон слоя сравнения = 1, когда хотя бы 2 входа из 3 равны 1
			if X[i] + P[i] + G1 < 2:
				C.append(0)
			else:
				C.append(1)
		return C
	#---------------------	
	def reset(self, X, C): #сигнал сброса
		#если степень меньше порога сходства, значит откликнувшийся нейрон будет заблокирован
		l = 0
		m = len(X)
		for i in range(len(X)):
			if X[i] == C[i]:
				l += 1
		if l/m >= self.p:
			return False, f"Результат сравнения нейронов {l/m} >= {self.p}"
		return True, f"Результат сравнения нейронов {l/m} < {self.p}"
	#-----------------------------
	def setup_similarity(self, p): #установка порога сходства для слоя сравнения
		self.p = p
#---CompareLayer---