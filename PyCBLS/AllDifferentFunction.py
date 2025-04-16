class AllDifferentFunction:

	def __init__(self,f,name):
		self.__f__ = f # Danh sách các hàm
		self.__name__ = name #Tập các biến liên quan đến các hàm trong f
		if f == None or len(f) == 0:
			return 
		self.__map__ = {}	# Ánh xạ từ biến -> chỉ số
		self.__mgr__ = f[0].getLocalSearchManager()
		self.__violations__ = 0 # Tổng số vi phạm ràng buộc (giá trị bị trùng)
		self.__mgr__.postInvariant(self)
		self.__depended__ = set()# Các thành phần phụ thuộc vào ràng buộc này
		for i in f:
			i.getDependedComponents().add(self)
			
		self.__mapVarToFunctions__ = {} # Biến nào ảnh hưởng đến những hàm nào
		
		var_set = set()
		for fi in f:
			for xi in fi.getVariables():
				var_set.add(xi)
				
				
				
		self.__x__ = []
		for xi in var_set:
			self.__x__.append(xi)
		
		
		for i in range(len(self.__x__)):
			self.__map__[self.__x__[i]] = i
			self.__mapVarToFunctions__[self.__x__[i]] = []

		for fi in f:
			for xi in fi.getVariables():
				self.__mapVarToFunctions__[xi].append(fi)
			
			
		self.__minValue__ = f[0].getMinValue()
		self.__maxValue__ = f[0].getMaxValue()
		for i in range(1,len(f)):
			if self.__minValue__ > f[i].getMinValue():
				self.__minValue__ = f[i].getMinValue()
			if self.__maxValue__ < f[i].getMaxValue():
				self.__maxValue__ = f[i].getMaxValue()
		self.__occ__ = [0 for i in range(self.__maxValue__ - self.__minValue__ + 1)] # Mảng đếm số lần mỗi giá trị xuất hiện
				
		#print(self.name() + '::constructor, __minValue__ = ' + str(self.__minValue__) + ', __maxValue__ = ' + str(self.__maxValue__))	
			
	def name(self):
		return self.__name__
		
		
	def getVariables(self):
		return self.__x__
		
	def getLocalSearchManager(self):
		return self.__mgr__
		
	def getDependedComponents(self):
		return self.__depended__
		
	def print(self):
		print(self.name())
		for v in range(len(self.__occ__)):
			print(self.name(),'occ[',v,'] = ',self.__occ__[v])
		print(self.name(),'violations = ',self.__violations__)

	# Khởi tạo số lượng vi phạm __violations__ ban đầu = số lần trùng lặp giá trị của các hàm f[i].
	def initPropagation(self):
		self.__violations__ = 0
		for i in range(len(self.__f__)):
			self.__occ__[self.__f__[i].getValue() - self.__minValue__] += 1

		for v in range(len(self.__occ__)):
			self.__violations__ += max(0,self.__occ__[v] - 1)
			
		#print(self.__name__ + '::initPropagate, value = ' + str(self.__value__))

	# Dùng khi giá trị của biến x thay đổi.
	# Cập nhật lại số lượng vi phạm do x ảnh hưởng đến các hàm.
	def propagate(self,x):		
		if self.__map__[x] == None:
			return	
		oldValue = x.getOldValue()
		F = self.__mapVarToFunctions__[x]
		for f in F:
			oldf = f.getValue() + f.getAssignDelta(x,oldValue)
			v = oldf - self.__minValue__
			if self.__occ__[v] > 1:
				self.__violations__ -= 1
			self.__occ__[v] -= 1
		
		for f in F:
			v = f.getValue() - self.__minValue__
			if self.__occ__[v] > 0:
				self.__violations__ += 1
			self.__occ__[v] += 1
			
		#print(self.__name__ + '::propagate, violations = ' + str(self.__violations__))
		
	def violations(self):
		return self.__violations__

	# Dự đoán delta vi phạm nếu hoán đổi giá trị của hai biến x và y.
	def getSwapDelta(self,x,y):
		if self.__map__[x] == None and self.__map__[y] == None:
			return 0
		if self.__map__[x] == None:
			return self.getAssignDelta(y,x.getValue())
		if self.__map__[y] == None:
			return self.getAssignDelta(x,y.getValue())
			
		nv = self.__violations__
		Fx = self.__mapVarToFunctions__[x]
		Fy = self.__mapVarToFunctions__[y]
		F = set()
		if Fx != None:
			for fi in Fx:
				F.add(fi)
		if Fy != None:
			for fi in Fy:
				F.add(fi)
		
		for f in F:
			v = f.getValue() - self.__minValue__
			if self.__occ__[v] > 1:
				nv -= 1
			self.__occ__[v] -= 1
			
		for f in F:
			v = f.getValue() + f.getSwapDelta(x,y) - self.__minValue__
			if self.__occ__[v] > 0:
				nv += 1
			self.__occ__[v] += 1
		
		#recover occ	
		for f in F:
			v1 = f.getValue() - self.__minValue__
			v2 = f.getValue() + f.getSwapDelta(x,y) - self.__minValue__
			self.__occ__[v1] += 1
			self.__occ__[v2] -= 1
		
		return nv - self.__violations__

	# Dự đoán delta vi phạm nếu gán x = val.
	# Không thực hiện gán, chỉ kiểm tra trước khi quyết định move trong local search.
	def getAssignDelta(self,x,val):
		if self.__map__[x] == None:
			return 0
			
		nv = self.__violations__
		F = self.__mapVarToFunctions__[x]
		
		# reduce occ for current values
		for f in F:
			v = f.getValue() - self.__minValue__
			if self.__occ__[v] > 1:
				nv -= 1
			self.__occ__[v] -= 1
			
		# increase occ for new values	
		for f in F:
			v = f.getValue() + f.getAssignDelta(x,val) - self.__minValue__
			if self.__occ__[v] > 0:
				nv += 1
			self.__occ__[v] += 1
			
		# recover
		for f in F:
			v1 = f.getValue() - self.__minValue__
			v2 = f.getValue() + f.getAssignDelta(x,val) - self.__minValue__
			#print(self.name() + '::getAssignDelta(v = ',v,'v2 = ',v2,')')
			self.__occ__[v1] += 1
			self.__occ__[v2] -= 1
			
		return nv - self.__violations__	