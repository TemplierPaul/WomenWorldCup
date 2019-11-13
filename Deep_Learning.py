from keras.models import Sequential
from keras.layers import Dense, Dropout
from ML import *

def createDL(dim):
    model = Sequential()
    model.add(Dense(units=64, activation='relu', input_dim=dim))
    model.add(Dropout(0.2))
    model.add(Dense(units=64, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(units=3, activation='softmax'))

    model.compile(optimizer='rmsprop',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    return model

def testDL ():
    dataset = pd.read_csv("full_data.csv", index_col=0)
    dataANDtarget = dataSelection(dataset)
    data = dataANDtarget[0]
    target = dataANDtarget[1]

    model = createDL(dim=len(data.columns))

    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.3, random_state=42)
    model.fit(X_train, y_train)

    score = model.evaluate(X_test, y_test)
    print(model.metrics_names, score)
    df = pd.concat([y_test.reset_index(), pd.DataFrame(model.predict(X_test))], axis=1)
    print(df)


testDL()