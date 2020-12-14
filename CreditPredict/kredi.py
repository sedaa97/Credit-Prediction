import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from flask import request
from flask import jsonify
from flask import Flask

mindata = None
maxdata = None

data = pd.read_csv("kredi.csv", sep=";")
data.telefonDurumu = [1 if each == "var" else 0 for each in data.telefonDurumu]
data.KrediDurumu = [1 if each == "krediver" else 0 for each in data.KrediDurumu]
data.evDurumu = [1 if each == "evsahibi" else 0 for each in data.evDurumu]
print(data.info())
df = pd.DataFrame(data)
y = data.KrediDurumu.values
x_data = data.drop(["KrediDurumu"], axis=1)

# normalization formul: [x-min(x)]/max(x)-min(x)
mindata = np.min(x_data)
maxdata = np.max(x_data)
print("a")
print(mindata)
x = (x_data - np.min(x_data)) / (np.max(x_data) - np.min(x_data)).values

# train-test split

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# logistic regression
from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model.fit(x_train, y_train)
print("test accuracy {}".format(model.score(x_test, y_test)))

def evdurumu(a):
 if a=='evsahibi':
  return 1
 else:
  return 0

def telefondurumu(a):
 if a=='var':
  return 1
 else:
  return 0

def kredidurumu(a):
 if a=='krediver':
  return 1
 else:
  return 0

#
app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
 gelen = request.get_json(force=True)
 numbers = [
 {"krediMiktari":int(gelen["miktar"]), "yas":int(gelen["yas"]), "evDurumu": int(evdurumu(gelen["ev"])), "aldigi_kredi_sayi":int(gelen["kredisayisi"]), "telefonDurumu": int(telefondurumu(gelen["tel"]))}
 ]
#
 numbers = pd.DataFrame(numbers)
 numbers = ((numbers - mindata) / (maxdata  - mindata)).values
 print(numbers)
 preds = model.predict(numbers)
 response = jsonify({'prediction': "Kredi alabilirsiniz" if each == "1" else "Kredi alamazsınız" for each in str(preds[0])})
 response.headers.add('Access-Control-Allow-Origin', '*')
 print(preds[0])

    
 return response
if __name__ == "__main__":
 app.run()
