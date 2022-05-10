# NOT RUN
#
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib
# from sklearn.model_selection import train_test_split
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.metrics import classification_report, confusion_matrix
# from sklearn.ensemble import RandomForestClassifier
#
# X = data[['lm_negative', 'lm_positive', 'vader_negative', 'vader_positive']]
# y = data['recession']
#
# X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.20)
#
# dtree = DecisionTreeClassifier()
# dtree.fit(X_train, Y_train)
#
# pred = dtree.predict(X_test)
#
# rfc = RandomForestClassifier(n_estimators=10000)
# rfc.fit(X_train, Y_train)
# rfc_pred = rfc.predict(X_test)
#
# print(classification_report(Y_test, pred))
# print('\n')
# print(confusion_matrix(Y_test, pred))
#
# print(classification_report(Y_test, rfc_pred))
# print('\n')
# print(confusion_matrix(Y_test, rfc_pred))
