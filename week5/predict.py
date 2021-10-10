
import pickle

dv = pickle.load(open('dv.bin', 'rb'))
m = pickle.load(open('model1.bin', 'rb'))

def get_prediction(data):
    X = dv.transform([data])
    r = m.predict_proba(X)
    return r[0][1]

if __name__ == '__main__':
    data = {"contract": "two_year", "tenure": 12, "monthlycharges": 19.7}
    print(get_prediction(data))
