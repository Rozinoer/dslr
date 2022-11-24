import pandas as pd
import numpy as np
import matplotlib as plot
import matplotlib.pyplot as plot
import seaborn as sns


def adaptDataForTrain(df):
	houses = df['Hogwarts House'].unique().tolist()
	X = df.loc[:, 'Arithmancy':].replace(np.nan, 0)
	X = (X - X.mean()) / X.std()
	Y = df['Hogwarts House']
	print(X, '\n', Y, '\n', houses)
	return X, Y, houses

def adaptDataForHouse(df, house):
	houseData = df.copy()
	houseData[df == house] = 0
	houseData[df != house] = 1
	return houseData

def miniBatch(X, Y, size):
	batch = []
	if size > len(X):
		size = len(X)
	batch_count = int(len(X)/ size)
	for i in range(batch_count):
		X_i = X[i * size: (i + 1) * size]
		Y_i = Y[i * size: (i + 1) * size]
		batch.append((X_i, Y_i))
	return batch

def sigmoid(x):
    return 1 / (1 + np.exp(-x.astype(np.float64)))

def costFunc(X, Y, theta):
	sig = sigmoid(np.dot(theta, X.T))
	cost = (np.sum((Y.T * np.log(sig)) + ((1 - Y.T) * (np.log(1 - sig))))) / -len(X)
	derivative = (np.dot((sig - Y.T), X)) / len(X)
	return cost, derivative

def gradientDescent(X, Y):
	learningRate = 0.1
	errors = []
	theta = np.random.randn(len(X.columns))
	current_error = 1000
	previous_error = 0
	while abs(current_error - previous_error) > 0.0001:
		previous_error = current_error
		current_error, derivative = costFunc(X, Y, theta)
		theta = theta - learningRate * derivative
		errors.append(current_error)
	return theta, errors

def stochaticGradientDescent(X, Y):
	learningRate = 0.1
	errors = []
	theta = np.random.randn(len(X.columns))
	current_error = 1000
	previous_error = 0
	while abs(current_error - previous_error) > 0.0001:
		indices = np.random.permutation(len(X))
		X = X.loc[indices]
		Y = Y[indices]
		previous_error = current_error
		current_error, derivative = costFunc(X, Y, theta)
		theta = theta - learningRate * derivative
		errors.append(current_error)
	return theta, errors

def miniBatchGradientDescent(X, Y, size):
	learningRate = 0.1
	errors = []
	theta = np.random.randn(len(X.columns))
	current_error = 10
	previous_error = 0
	indices = np.random.permutation(len(X))
	X = X.loc[indices]
	Y = Y[indices]
	mini_batch = miniBatch(X, Y, size)
	index = 0
	while abs(current_error - previous_error) > 0.0001:
		previous_error = current_error
		current_error, derivative = costFunc(mini_batch[index][0], np.array(mini_batch[index][1]), theta)
		if index == len(mini_batch) - 1:
			index = 0
		else:
			index += 1
		theta = theta - learningRate * derivative
		errors.append(current_error)
	return theta, errors

def printTrainProcess(train_graph):
	for i in train_graph:
		sns.scatterplot(x=range(len(train_graph[i])), y=train_graph[i], label=i)
	plot.xlabel("iterations")
	plot.ylabel("errors")
	plot.savefig('train_process.png')


def train(path):
	train_graph = {}
	thetas = []
	try:
		df = pd.read_csv(path)
		X, Y, houses = adaptDataForTrain(df)
		for house in houses:
			print(f"Trainning {house}")
			train_Y = adaptDataForHouse(Y, house)
			theta, errors = gradientDescent(X, np.asarray(train_Y))
			thetas.append(theta)
			train_graph[house] = errors
		thetas = pd.DataFrame(thetas, columns=X.columns, index=houses)
	except Exception as er:
		print(er)
	return thetas, train_graph

def bonusTrain(path, size):
	train_graph = {}
	thetas = []
	try:
		df = pd.read_csv(path)
		X, Y, houses = adaptDataForTrain(df)
		for house in houses:
			print(f"Trainning {house}")
			train_Y = adaptDataForHouse(Y, house)
			if size > 0:
				theta, errors = miniBatchGradientDescent(X, np.asarray(train_Y), size)
			else:
				theta, errors = stochaticGradientDescent(X, np.asarray(train_Y))
			thetas.append(theta)
			train_graph[house] = errors
		thetas = pd.DataFrame(thetas, columns=X.columns, index=houses)
	except Exception as er:
		print(er)
	return thetas, train_graph


def mainProcess(path, bonus, size):
	if bonus:
		thetas, train_graph = bonusTrain(path, size)
	else:
		thetas, train_graph = train(path)
	thetas.to_csv('thetas.csv')
	printTrainProcess(train_graph)

if __name__ == '__main__':
	path = input('Enter the path to the dataset_train\n')
	bonus = int(input('Train with bonus? Yes = 1 or No = 0\n'))
	size = 0
	if bonus:
		size = int(input('Enter the mini_batch size\n'))
	mainProcess(path, bonus, size)
