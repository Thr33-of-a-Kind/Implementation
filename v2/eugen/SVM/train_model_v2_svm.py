import pickle
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

# Load data from pickle file
data_pickle = pickle.load(open('../../data.pkl', 'rb'))

data = []
# Pad each data item and append to the data list
for d in data_pickle['data']:
    data.append(np.pad(d, (0, 84 - len(d))))

data = np.asarray(data)
labels = np.asarray(data_pickle['labels'])

num_iterations = 1  # Number of iterations for averaging accuracy scores

accuracy_scores = []
precision_scores = []
recall_scores = []
f1_scores = []

svm_model = SVC()
for _ in range(num_iterations):
    x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)
    svm_model.fit(x_train, y_train)

    y_predict = svm_model.predict(x_test)

    accuracy = accuracy_score(y_test, y_predict)
    precision = precision_score(y_test, y_predict, average='macro', zero_division=1)
    recall = recall_score(y_test, y_predict, average='macro')
    f1 = f1_score(y_test, y_predict, average='macro')

    accuracy_scores.append(accuracy)
    precision_scores.append(precision)
    recall_scores.append(recall)
    f1_scores.append(f1)

average_accuracy = np.mean(accuracy_scores)
average_precision = np.mean(precision_scores)
average_recall = np.mean(recall_scores)
average_f1 = np.mean(f1_scores)

print('Average accuracy: {:.2%}'.format(average_accuracy))
print('Average precision: {:.2%}'.format(average_precision))
print('Average recall: {:.2%}'.format(average_recall))
print('Average F1 score: {:.2%}'.format(average_f1))

pickleFile = open('svm.pkl', 'wb')
pickle.dump({'model': svm_model}, pickleFile)
pickleFile.close()