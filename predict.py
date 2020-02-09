from joblib import load
import pandas as pd

url = 
file_path = 
def main(url, path):
    input_data = pd.read_json(url, orient='columns')
    model = load(filepath)
    predictions = model.predict(input_data)
    return predictions

if __name__=="__main__":
    main(url, filepath)