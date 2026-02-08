import pandas as pd
import numpy as np

df = pd.read_csv("app/data/projects_clean.csv")
embeddings = np.load("app/data/project_embeddings.npy")

assert len(df) == len(embeddings)
