import pandas as pd

df = pd.read_csv('data/train_data.csv')

results = pd.DataFrame({
    'id': df['id'],
    'attack_cat': df['attack_cat'],
})

results.to_csv('train_data_sub.csv', index=False)