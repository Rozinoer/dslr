import pandas as pd
import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x.astype(np.float64)))

def predict(df, thetas):
	thetas = thetas.loc[:, 'Arithmancy':]
	result = {}
	X = df.loc[:, 'Arithmancy':].replace(np.nan, 0)
	X = (X - X.mean()) / X.std()
	houses = ['Ravenclaw', 'Slytherin', 'Gryffindor', 'Hufflepuff']
	for i, theta in thetas.iterrows():
		result[houses[i]] = sigmoid(X.dot(theta))
	result = pd.DataFrame(result)
	predict_val = pd.DataFrame([houses[r.argmax()] for _, r in result.iterrows()], columns=['Hogwarts House'])
	return predict_val

def mainProcess(df_path, thetas_path):
	thetas = pd.read_csv(thetas_path)
	df = pd.read_csv(df_path)
	predict_val = predict(df, thetas)
	predict_val.to_csv('Houses.csv', index=False)


if __name__ == '__main__':
	df_path = input('Enter the path to dataset_test\n')
	thetas_path = input('Enter the path to thetas\n')
	mainProcess(df_path, thetas_path)