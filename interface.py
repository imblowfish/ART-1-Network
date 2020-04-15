import tkinter as tk

class ViewAllScreen:
	datas = None
	now_idx = -1
	def __init__(self, datas):
		self.datas = datas
		root = tk.Tk()
		root.geometry("300x200")
		root.title("Все образцы")
		next_btn = tk.Button(root, text=">", command=self.next_image)
		next_btn.pack(side=tk.RIGHT, fill=tk.BOTH)
		prev_btn = tk.Button(root, text="<", command=self.prev_image)
		prev_btn.pack(side=tk.LEFT, fill=tk.BOTH)
		self.canvas = tk.Canvas(root, width=300, height=200, bg="white")
		self.canvas.pack()
		self.now_idx = 0
		self.view_example(self.datas[self.now_idx])
		
	def next_image(self):
		if self.now_idx + 1 < len(self.datas):
			self.now_idx += 1
		self.view_example(self.datas[self.now_idx])
		
	def prev_image(self):
		if self.now_idx - 1 > 0:
			self.now_idx -= 1
		self.view_example(self.datas[self.now_idx])
	
	def view_example(self, data):
		m = len(data)
		n = len(data[0])
		width = int(self.canvas["width"])
		height = int(self.canvas["height"])
		self.canvas.delete("all")
		space_x = width/n
		space_y = height/m
		y = 0
		for i in range(len(data)):
			x = 0
			for j in range(len(data[i])):
				if data[i][j] == 1:
					self.canvas.create_rectangle(x, y, x+space_x, y+space_y, fill="black", outline="white")
				else:
					self.canvas.create_rectangle(x, y, x+space_x, y+space_y, outline="black")
				x += space_x
			y += space_y
	
class AddNewScreen:
	datas = None
	max_x = 3
	max_y = 3
	x_size = 0
	y_size = 0
	new_data = None
	
	def __init__(self, datas):
		self.x_size = len(datas[0][0])
		self.y_size = len(datas[0])
		
		self.new_data = []
		for i in range(self.x_size):
			row = []
			for j in range(self.y_size):
				row.append(0)
			self.new_data.append(row)
			
		self.datas = datas
		self.root = tk.Tk()
		self.root.geometry("500x450")
		self.root.title("Добавление нового образца")
		
		plus_x_btn = tk.Button(self.root, text="+", command=self.plus_x)
		plus_x_btn.pack(side=tk.RIGHT)
		minus_x_btn = tk.Button(self.root, text="-", command=self.minus_x)
		minus_x_btn.pack(side=tk.RIGHT)
		
		
		minus_y_btn = tk.Button(self.root, text="-", command=self.minus_y)
		minus_y_btn.pack(side=tk.LEFT)
		plus_y_btn = tk.Button(self.root, text="+", command=self.plus_y)
		plus_y_btn.pack(side=tk.LEFT)
		
		self.canvas = tk.Canvas(self.root, width = 400, height = 400, bg="white")
		self.canvas.pack()
		self.canvas.bind("<Button-1>", self.click)
		
		save_btn = tk.Button(self.root, text="Сохранить", command=self.save)
		save_btn.pack(side=tk.BOTTOM)
		
		self.view_new(self.new_data)
		
	def click(self, event):
		m = len(self.new_data)
		n = len(self.new_data[0])
		width = int(self.canvas["width"])
		height = int(self.canvas["height"])
		space_x = width/n
		space_y = height/m
		y = 0
		for i in range(len(self.new_data)):
			x = 0
			for j in range(len(self.new_data[i])):
				if x <= event.x <= x+space_x and y <= event.y <= y+space_y:
					if self.new_data[i][j] == 1:
						self.new_data[i][j] = 0
					else:
						self.new_data[i][j] = 1
				x += space_x
			y += space_y
		self.view_new(self.new_data)
		
	def save(self):
		self.datas.append(self.new_data)
		self.root.destroy()
	
	def plus_x(self):
		
		if self.x_size+1 <= self.max_x:
			self.x_size += 1
		else:
			return
		self.new_data = []
		for i in range(self.y_size):
			row = []
			for j in range(self.x_size):
				row.append(0)
			self.new_data.append(row)
		self.view_new(self.new_data)
		
	def minus_x(self):
		if self.x_size - 1 > 0:
			self.x_size -= 1
		else:
			return
		self.new_data = []
		for i in range(self.y_size):
			row = []
			for j in range(self.x_size):
				row.append(0)
			self.new_data.append(row)
		self.view_new(self.new_data)
		
	def plus_y(self):
		if self.y_size + 1 <= self.max_y:
			self.y_size += 1
		else:
			return
		self.new_data = []
		for i in range(self.y_size):
			row = []
			for j in range(self.x_size):
				row.append(0)
			self.new_data.append(row)
		self.view_new(self.new_data)
		
	def minus_y(self):
		if self.y_size - 1 > 0:
			self.y_size -= 1
		else:
			return
		self.new_data = []
		for i in range(self.y_size):
			row = []
			for j in range(self.x_size):
				row.append(0)
			self.new_data.append(row)
		self.view_new(self.new_data)
	
	def view_new(self, data):
		m = len(data)
		n = len(data[0])
		width = int(self.canvas["width"])
		height = int(self.canvas["height"])
		self.canvas.delete("all")
		space_x = width/n
		space_y = height/m
		y = 0
		for i in range(len(data)):
			x = 0
			for j in range(len(data[i])):
				if data[i][j] == 1:
					self.canvas.create_rectangle(x, y, x+space_x, y+space_y, fill="black")
				else:
					self.canvas.create_rectangle(x, y, x+space_x, y+space_y, outline="black")
				x += space_x
			y += space_y
		
#редактор образцов
class MainScreen:
	root = None
	def __init__(self):
		self.root = tk.Tk()
		self.root.geometry("800x500")
		self.root.title("Лабораторная №3")
		self.root.resizable(False, False)
		#добавление кнопок
		self.init_canvas()
		self.init_buttons()
		self.init_protocol()
	
	def init_canvas(self):
		self.example_viewer = tk.Canvas(self.root, bg="white", width=270, height=270)
		# self.example_viewer.place(relx=0.3, rely=0.01, relwidth=0.4, relheight=0.5)
		self.example_viewer.place(relx=0.3, rely=0.01)
	def init_buttons(self):
		
		self.all_examples_btn = tk.Button(self.root, text="Все образцы", width=10, height=5)
		self.all_examples_btn.place(relx=0.01, rely=0.01, relwidth=0.2, relheight=0.1)
		# self.add_new_example_btn = tk.Button(self.root, text="Добавить образец", width=10, height=5)
		# self.add_new_example_btn.place(relx=0.01, rely=0.11, relwidth=0.2, relheight=0.1)
		
		# self.search_btn.place(relx=0.01, rely=0.21, relwidth=0.2, relheight=0.1)
		
		self.next_step_btn = tk.Button(self.root, text="Следующий шаг")
		self.next_step_btn.place(relx=0.79, rely=0.01, relwidth=0.2, relheight=0.1)
		self.reset_btn = tk.Button(self.root, text="Сброс")
		self.reset_btn.place(relx=0.79, rely=0.11, relwidth=0.2, relheight=0.1)
		self.network_examples_btn = tk.Button(self.root, text="Нейроны сети", width=10, height=5)
		self.network_examples_btn.place(relx=0.79, rely=0.21, relwidth=0.2, relheight=0.1)
		
	def init_protocol(self):
		self.protocol = tk.Text(self.root)
		self.protocol.place(relx=0.01, rely=0.57, relwidth=0.98, relheight=0.42)
		
		self.similarity = tk.Text(self.root)
		self.similarity.place(relx=0.01, rely=0.2, relwidth=0.1, relheight=0.05)
		self.similarity.insert(1.0, 0.8)
	
	def get_similarity(self):
		return float(self.similarity.get(1.0, tk.END))
	
	def view_example(self, data):
		n = len(data[0])
		m = len(data)
		width = int(self.example_viewer["width"])
		height = int(self.example_viewer["height"])
		self.clear_viewer()
		space_x = width/n
		space_y = height/m
		y = 0
		for i in range(len(data)):
			x = 0
			for j in range(len(data[i])):
				if data[i][j] == 1:
					self.example_viewer.create_rectangle(x, y, x+space_x, y+space_y, fill="black")
				else:
					self.example_viewer.create_rectangle(x, y, x+space_x, y+space_y, outline="black")
				x += space_x
			y += space_y
			
	def add_in_protocol(self, str):
		self.protocol.delete('1.0', tk.END)
		self.protocol.insert(1.0, str)
	
	def clear_viewer(self):
		self.example_viewer.delete("all")
	
	def show_all_examples(self, datas):
		screen = ViewAllScreen(datas)
	
	def show_network_examples(self, datas, n, m):
		#преобразование каждого выхода нейрона в изображение
		images = []
		print(datas)
		for data in datas:
			image = []
			for i in range(n):
				row = []
				for j in range(m):
					row.append(data[i*m+j])
				image.append(row)
			images.append(image)
		screen = ViewAllScreen(images)
			
		
	def add_new_example(self, datas):
		screen = AddNewScreen(datas)
	
	def start(self):
		self.root.mainloop()