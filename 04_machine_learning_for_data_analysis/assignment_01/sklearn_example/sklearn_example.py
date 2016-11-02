"""
One line module's description

Multi Line
Complete
Description
Of the Module

Classes:
    cl1: one line description.
    cl2: one line description.

Functions:
    func1: one line description.
    func2: one line description.

Exceptions:
    except1: one line description.
    except2: one line description.

References:
    [1] - Author, Work.
    [2] - Author, Work.

"""

# pylama:skip=1
from sklearn.datasets import load_iris
from sklearn import tree
iris = load_iris()
clf = tree.DecisionTreeClassifier()
clf = clf.fit(iris.data, iris.target)
with open("iris.dot", 'w') as f:
    f = tree.export_graphviz(clf, out_file=f)
import os
os.unlink('iris.dot')
import pydotplus
dot_data = tree.export_graphviz(clf, out_file=None)
graph = pydotplus.graph_from_dot_data(dot_data)
graph.write_pdf("iris.pdf")
from IPython.display import Image
dot_data = tree.export_graphviz(clf, out_file=None,
                     feature_names=iris.feature_names,
                     class_names=iris.target_names,
                     filled=True, rounded=True,
                     special_characters=True)
graph = pydotplus.graph_from_dot_data(dot_data)
img = graph.create_png()
with open('iris.png', 'wb') as i_img:
    i_img.write(img)
