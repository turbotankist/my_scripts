from numpy import exp, array, random, dot
# training_set_inputs = array([[0, 0, 1], [1, 1, 1], [1, 0, 1], [0, 1, 1]])
# training_set_outputs = array([[0, 1, 1, 0]]).T
# random.seed(1)
# synaptic_weights = 2 * random.random((3, 1)) - 1
# for iteration in range(100000):
#     output = 1 / (1 + exp(-(dot(training_set_inputs, synaptic_weights))))
#     synaptic_weights += dot(training_set_inputs.T, (training_set_outputs - output) * output * (1 - output))

# print (1 / (1 + exp(-(dot(array([0, 1, 0]), synaptic_weights)))))

class NeuralNetwork():
	def __init__(self):
		random.seed(1)
		self.synaptic_weights = 2 * random.random((3, 1)) - 1
	def __sigmoid(self, x):
		return 1 / (1 + exp(-x))
	def __sigmoid_derivative(self, x):
		return x * (1 - x)

	def train(self, training_set_inputs, training_set_outputs, number_of_training_iterations):
		for iteration in range(number_of_training_iterations):
			output = self.think(training_set_inputs)
			error = training_set_outputs - output
			adjustment = dot(training_set_inputs.T, error * self.__sigmoid_derivative(output))
			self.synaptic_weights += adjustment

	def think(self, inputs):
		return self.__sigmoid(dot(inputs, self.synaptic_weights))


if __name__ == "__main__":
	neural_network = NeuralNetwork()

	print ("Random starting synaptic weights: ")
	print (neural_network.synaptic_weights)

	training_set_inputs = array([[1, 0, 1, 0], [1, 0, 1, 1], [0, 0, 1, 0], [1, 1, 1, 0], [0, 1, 0, 0] , [0, 1, 1, 1] , [1, 0, 1, 0] , [1, 1, 0, 0] ,[0, 1, 0, 1] , [1, 1, 0, 1]])
	training_set_outputs = array([[0, 1, 0, 1, 0, 1, 0, 0, 0, 1]]).T

	neural_network.train(training_set_inputs, training_set_outputs, 10000)

	print ("New synaptic weights after training: ")
	print (neural_network.synaptic_weights)

	print ("Considering new situation [1, 0, 0] -> ?: ")
	print (neural_network.think(array([1,0, 0, 1])))


map = np.zeros((6,6))
map[2,2]=10
map[2,1]=6
map[5,2]=-2
map[5,3]=-3
map[1,4]=-6

maxx=map.argmax() // 6
maxy=map.argmax() % 6
minx=map.argmin() // 6
miny=map.argmin() % 6
map
for i in range(6):
	for j in range(6):
		map[i,j] += (12 - abs(maxx - i) - abs(maxy - j) // 2 ) 

map