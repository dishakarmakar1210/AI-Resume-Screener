import pickle
import os

def save_metadata(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(obj, f)

def load_metadata(path):
    with open(path, "rb") as f:
        return pickle.load(f)
