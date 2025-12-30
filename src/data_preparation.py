import numpy as np
import pandas as pd
import os

def prepare_data(input_path, output_path):

    df = pd.read_csv(input_path)

    print(df.dtypes)
    #df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors='coerce')

    #df = df.dropna()

    #os.makedirs(os.path.dirname(output_path), exist_ok=True)
    #df.to_csv(output_path, index=False)