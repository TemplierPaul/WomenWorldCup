import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import graphviz
import pydotplus
from IPython.display import Image
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier, export_graphviz
from sklearn.linear_model import Perceptron, SGDClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn import metrics
from sklearn.multioutput import MultiOutputRegressor
# from Deep_Learning import *


def dataSelection(dataset):
    data = dataset[['Date', 'Rank_A',
                    'Points_A', 'Previous_Points_A', '+/-_A', 'Rank_B', 'Points_B',
                    'Previous_Points_B', '+/-_B', 'Mean 3 +_A', 'Mean 3 -_A',
                    'Mean 3 +_B', 'Mean 3 -_B', 'Points Difference']].copy()

    # data = pd.concat([data, pd.get_dummies(data['Competition'], prefix=['Competition'], drop_first=True,
    #                                        columns=['[Competition]_APC',
    #    '[Competition]_AWC', '[Competition]_BWC', '[Competition]_CAF',
    #    '[Competition]_CWC', '[Competition]_CWG', '[Competition]_CWS',
    #    '[Competition]_CWU', '[Competition]_EEF', '[Competition]_FCO',
    #    '[Competition]_FNT', '[Competition]_FRW', '[Competition]_HFW',
    #    '[Competition]_IWC', '[Competition]_OCM', '[Competition]_OLW',
    #    '[Competition]_SAW', '[Competition]_SHC', '[Competition]_SWC',
    #    '[Competition]_TON', '[Competition]_TWC', '[Competition]_UWC',
    #    '[Competition]_WAC', '[Competition]_WAG', '[Competition]_WCC',
    #    '[Competition]_WEA', '[Competition]_WOQ', '[Competition]_WPA',
    #    '[Competition]_WPG', '[Competition]_WWC', '[Competition]_WWQ',
    #    '[Competition]_YOT'])],
    # axis=1)

    # data.drop(['Competition'], axis=1, inplace=True)
    data['Date'] = pd.to_numeric(pd.to_datetime(data['Date']))

    # target = dataset['Result'].copy()
    target = pd.get_dummies(dataset['Result'], prefix=['Out_'], drop_first=False)


    return [data, target]


def resultPrediction(dataANDtarget):
    data = dataANDtarget[0]
    target = dataANDtarget[1]

    # model = DecisionTreeClassifier(random_state=0)    # Accuracy = 0.60
    # model = Perceptron(tol=1e-3, random_state=0)      # Accuracy = 0.43
    # model = SGDClassifier()                           # Accuracy = 0.14
    # model = MLPClassifier(hidden_layer_sizes=(5, 2))  # Accuracy = 0.42
    # model = SVC(gamma='auto')                         # Accuracy = 0.43
    model = RandomForestClassifier()                    # Accuracy = 0.67
    # model = createDL(dim=len(data.columns))


    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.3, random_state=42)
    model.fit(X_train, y_train)
    print("Training data : ", len(X_train))
    print("Test data : ", len(X_test))
    y_pred = pd.DataFrame(model.predict(X_test), columns=["Predicted"])
    accuracy = metrics.accuracy_score(y_test, y_pred)
    print("Accuracy : ", accuracy)
    confusion = metrics.confusion_matrix(y_test, y_pred)
    cm_df = pd.DataFrame(confusion)

    sns.heatmap(cm_df, annot=True, fmt='d')
    plt.show(block=False)

    dot_data=export_graphviz(model, out_file=None,
                             feature_names=X_train.columns,
                             class_names=["A wins", "Draw", 'B wins'])
    graph = pydotplus.graph_from_dot_data(dot_data)
    # Image(graph.create_png())
    graph.write_png('match-result.png')
    graph.write_pdf('match-result.pdf')

def trainPredict(prefix=''):
    print('Training data')
    train = pd.read_csv('full_data.csv', index_col=0)
    data_split = dataSelection(train)
    data = data_split[0]
    target = data_split[1]
    print(data.columns)

    print('Prediction data')
    to_predict = pd.read_csv(prefix + 'full_data.csv', index_col=0)
    to_predict['Date'] = pd.to_datetime(to_predict['Date'])
    to_predict = to_predict.sort_values('Date')
    unknown = dataSelection(to_predict)[0]
    print(unknown.columns)

    model = RandomForestClassifier()
    model.fit(data, target)

    prediction = pd.DataFrame(model.predict(unknown), columns=["Forest"])
    if prefix == '' :
        to_predict = to_predict[['Date', 'A', 'B', 'Score A', 'Score B', 'Result']]
    else :
        to_predict = to_predict[['Date', 'A', 'B']]

    scores = pd.DataFrame(model.predict_proba(unknown))
    output = pd.concat([to_predict, prediction, scores], axis=1)

    if prefix != '' :
        matches = pd.read_csv(prefix + 'matches.csv', index_col=0)
        df = pd.DataFrame(columns=['Pred 1', 'Pred 2', 'Odd A', 'Odd Draw', 'Odd B'])
        results = []
        for index, match in matches.iterrows():
            m1 = output[output['A'] == match['A']][output['B'] == match['B']]
            m2 = output[output['A'] == match['B']][output['B'] == match['A']]
            match['Pred 1'] = int(m1['Forest'])
            match['Pred 2'] = int(2 - m2['Forest'])
            match['Odd A'] = float(m1[0]) + float(m2[2])
            match['Odd Draw'] = float(m1[1]) + float(m2[1])
            match['Odd B'] = float(m1[2]) + float(m2[0])
            results.append(match.to_list())
        df = pd.DataFrame(results, columns=['Day', 'Date', 'Competition', 'A', 'B', 'Score A', 'Score B', 'Pred 1','Pred 2', 'Odd A', 'Odd Draw', 'Odd B'])
        print(df.head())
        df['Score A'] = df['Odd A'] * 1.5
        df['Score B'] = df['Odd B'] * 1.5
        df.to_csv(prefix + 'prediction.csv')
        pred_score = df[['Date', 'A', 'B', 'Score A', 'Odd Draw', 'Score B']]
        print(pred_score)
    else :
        output.to_csv('prediction.csv')


