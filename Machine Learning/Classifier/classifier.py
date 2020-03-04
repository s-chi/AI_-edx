import sys
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import numpy as np

def make_meshgrid(x, y, h=.02):
    x_min, x_max = x.min() - 1, x.max() + 1
    y_min, y_max = y.min() - 1, y.max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    return xx, yy


def plot_contours(ax, clf, xx, yy, **params):
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    out = ax.contourf(xx, yy, Z, **params)
    return out


inputfile = sys.argv[1]
outputfile = sys.argv[2]

df = pd.read_csv(inputfile)

values = df.values

X = values[:,:2]
y = values[:,2]

#unique, counts = np.unique(y, return_counts=True)
#print dict(zip(unique, counts))


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, stratify=y)
xx, yy = make_meshgrid(X_test[:,0],X_test[:,1])

param_grid = {'C': [0.1, 0.5, 1, 5, 10, 50, 100], 'kernel': ['linear']}

clf = GridSearchCV(SVC(), param_grid, cv=5)
clf.fit(X_train, y_train)

Z = clf.predict(X_test)

with open(outputfile,'w') as f:
    
    f.write("svm_linear,%s,%s\n" % (max(clf.cv_results_['mean_test_score']),accuracy_score(y_test,Z)))
    
fig, ax = plt.subplots()
fig.suptitle("svm_linear")
plot_contours(ax, clf, xx, yy, cmap='bwr', alpha=0.8)
ax.scatter(X_test[:,0],X_test[:,1],c=y_test, cmap='bwr', edgecolor='k')
plt.show()


param_grid = {'C': [0.1, 1, 3], 'kernel': ['poly'], 'gamma': [0.1, 0.5], 'degree': [4, 5, 6]}

clf = GridSearchCV(SVC(), param_grid, cv=5)
clf.fit(X_train, y_train)

Z = clf.predict(X_test)

with open(outputfile,'a') as f:
    
    f.write("svm_polynomial,%s,%s\n" % (max(clf.cv_results_['mean_test_score']),accuracy_score(y_test,Z)))
    
fig, ax = plt.subplots()
fig.suptitle("svm_polynomial")
plot_contours(ax, clf, xx, yy, cmap='bwr', alpha=0.8)
ax.scatter(X_test[:,0],X_test[:,1],c=y_test, cmap='bwr', edgecolor='k')
plt.show()

param_grid = {'C': [0.1, 0.5, 1, 5, 10, 50, 100], 'kernel': ['rbf'], 'gamma': [0.1, 0.5, 1, 3, 6, 10]}

clf = GridSearchCV(SVC(), param_grid, cv=5)
clf.fit(X_train, y_train)

Z = clf.predict(X_test)

with open(outputfile,'a') as f:
    
    f.write("svm_rbf,%s,%s\n" % (max(clf.cv_results_['mean_test_score']),accuracy_score(y_test,Z)))
    
fig, ax = plt.subplots()
fig.suptitle("svm_rbf")
plot_contours(ax, clf, xx, yy, cmap='bwr', alpha=0.8)
ax.scatter(X_test[:,0],X_test[:,1],c=y_test, cmap='bwr', edgecolor='k')
plt.show()

param_grid = {'C': [0.1, 0.5, 1, 5, 10, 50, 100]}

clf = GridSearchCV(LogisticRegression(), param_grid, cv=5)
clf.fit(X_train, y_train)

Z = clf.predict(X_test)

with open(outputfile,'a') as f:
    
    f.write("logistic,%s,%s\n" % (max(clf.cv_results_['mean_test_score']),accuracy_score(y_test,Z)))
    
fig, ax = plt.subplots()
fig.suptitle("logistic")
plot_contours(ax, clf, xx, yy, cmap='bwr', alpha=0.8)
ax.scatter(X_test[:,0],X_test[:,1],c=y_test, cmap='bwr', edgecolor='k')
plt.show()

param_grid = {'n_neighbors': range(1,51), 'leaf_size': [5*n for n in range(1,13)]}

clf = GridSearchCV(KNeighborsClassifier(), param_grid, cv=5)
clf.fit(X_train, y_train)

Z = clf.predict(X_test)

with open(outputfile,'a') as f:
    
    f.write("knn,%s,%s\n" % (max(clf.cv_results_['mean_test_score']),accuracy_score(y_test,Z)))
    
fig, ax = plt.subplots()
fig.suptitle("k-nearest neighbors")
plot_contours(ax, clf, xx, yy, cmap='bwr', alpha=0.8)
ax.scatter(X_test[:,0],X_test[:,1],c=y_test, cmap='bwr', edgecolor='k')
plt.show()

param_grid = {'max_depth': range(1,51), 'min_samples_split': range(2,10)}

clf = GridSearchCV(DecisionTreeClassifier(), param_grid, cv=5)
clf.fit(X_train, y_train)

Z = clf.predict(X_test)

with open(outputfile,'a') as f:
    
    f.write("decision_tree,%s,%s\n" % (max(clf.cv_results_['mean_test_score']),accuracy_score(y_test,Z)))
    
fig, ax = plt.subplots()
fig.suptitle("decision_tree")
plot_contours(ax, clf, xx, yy, cmap='bwr', alpha=0.8)
ax.scatter(X_test[:,0],X_test[:,1],c=y_test, cmap='bwr', edgecolor='k')
plt.show()

param_grid = {'max_depth': range(1,51), 'min_samples_split': range(2,10)}

clf = GridSearchCV(RandomForestClassifier(), param_grid, cv=5)
clf.fit(X_train, y_train)

Z = clf.predict(X_test)

with open(outputfile,'a') as f:
    
    f.write("random_forest,%s,%s\n" % (max(clf.cv_results_['mean_test_score']),accuracy_score(y_test,Z)))
    
fig, ax = plt.subplots()
fig.suptitle("random_forest")
plot_contours(ax, clf, xx, yy, cmap='bwr', alpha=0.8)
ax.scatter(X_test[:,0],X_test[:,1],c=y_test, cmap='bwr', edgecolor='k')
plt.show()

#model = SVC(C=1.0,gamma=0.7)
#clf = model.fit(X,y)

#xx, yy = make_meshgrid(X[:,0],X[:,1])
#fig, ax = plt.subplots()
#plot_contours(ax, clf, xx, yy, cmap='bwr', alpha=0.8)
#plt.scatter(X[:,0],X[:,1],c=y, cmap='bwr', edgecolor='k')
#plt.show()


# we create an instance of SVM and fit out data. We do not scale our
# data since we want to plot the support vectors
#C = 1.0  # SVM regularization parameter
#models = (svm.SVC(kernel='linear', C=C),
          #svm.LinearSVC(C=C),
          #svm.SVC(kernel='rbf', gamma=0.7, C=C),
          #svm.SVC(kernel='poly', degree=3, C=C))
#models = (clf.fit(X, y) for clf in models)

## title for the plots
#titles = ('SVC with linear kernel',
          #'LinearSVC (linear kernel)',
          #'SVC with RBF kernel',
          #'SVC with polynomial (degree 3) kernel')

## Set-up 2x2 grid for plotting.
#fig, sub = plt.subplots(2, 2)
#plt.subplots_adjust(wspace=0.4, hspace=0.4)

#X0, X1 = X[:, 0], X[:, 1]
#xx, yy = make_meshgrid(X0, X1)

#for clf, title, ax in zip(models, titles, sub.flatten()):
    #plot_contours(ax, clf, xx, yy,
                  #cmap=plt.cm.coolwarm, alpha=0.8)
    #ax.scatter(X0, X1, c=y, cmap=plt.cm.coolwarm, s=20, edgecolors='k')
    #ax.set_xlim(xx.min(), xx.max())
    #ax.set_ylim(yy.min(), yy.max())
    #ax.set_xlabel('Sepal length')
    #ax.set_ylabel('Sepal width')
    #ax.set_xticks(())
    #ax.set_yticks(())
    #ax.set_title(title)

#plt.show()
