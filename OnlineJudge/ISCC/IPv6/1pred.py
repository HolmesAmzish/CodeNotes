import pandas as pd
import numpy as np
from ipaddress import IPv6Address
from sklearn.cluster import KMeans
from xgboost import XGBClassifier
from collections import Counter
import random

# 加载种子地址
def load_seeds(file_path):
    with open(file_path, 'r') as f:
        seeds = [line.strip() for line in f]
    return seeds

seeds = load_seeds('give_data/1_give.txt')

# 展开IPv6地址
def expand_ipv6(addr):
    return IPv6Address(addr).exploded

# 提取特征
def extract_features(addrs, is_positive=True):
    features = []
    third_values = [int(expand_ipv6(addr).split(':')[2], 16) for addr in addrs]
    fourth_values = [int(expand_ipv6(addr).split(':')[3], 16) for addr in addrs]
    min_third, max_third = min(third_values), max(third_values)
    min_fourth, max_fourth = min(fourth_values), max(fourth_values)
    mean_third = np.mean(third_values)
    
    # 第四组频率
    fourth_hex = [expand_ipv6(addr).split(':')[3] for addr in addrs]
    freq = Counter(fourth_hex)
    high_freq = {k for k, v in freq.items() if v > 1}  # 出现多次的值
    
    # 聚类
    cluster_data = np.array(list(zip(third_values, fourth_values)))
    kmeans = KMeans(n_clusters=3, random_state=42)
    cluster_ids = kmeans.fit_predict(cluster_data)
    
    for i, addr in enumerate(addrs):
        parts = expand_ipv6(addr).split(':')
        third_val = third_values[i]
        fourth_val = fourth_values[i]
        
        feat = {
            'third_group_decimal': third_val,
            'third_group_normalized': (third_val - min_third) / (max_third - min_third),
            'fourth_group_decimal': fourth_val,
            'fourth_group_normalized': (fourth_val - min_fourth) / (max_fourth - min_fourth),
            'is_iid_one': 1 if ':'.join(parts[4:]) == '0000:0000:0000:0001' else 0,
            'third_group_mean_dist': abs(third_val - mean_third),
            'is_fourth_group_high_freq': 1 if parts[3] in high_freq else 0,
            'cluster_id': cluster_ids[i]
        }
        features.append(feat)
    
    return pd.DataFrame(features)

# 生成负样本
def generate_negative_samples(n_samples):
    candidates = []
    for _ in range(n_samples):
        third = random.randint(0xa000, 0xb000)  # 范围a000到b000
        fourth = random.randint(0, 100)  # 范围0到100
        addr = f"2001:1:{third:04x}:{fourth:04x}::1"
        candidates.append(addr)
    return candidates

# 生成候选地址
def generate_candidates(n_samples):
    candidates = []
    for _ in range(n_samples):
        third = random.randint(0xa000, 0xb000)
        fourth = random.randint(0, 100)
        addr = f"2001:1:{third:04x}:{fourth:04x}::1"
        candidates.append(addr)
    return candidates

# 主流程
def main():
    # 提取正样本特征
    pos_features = extract_features(seeds, is_positive=True)
    y_pos = [1] * len(seeds)
    
    # 生成负样本
    neg_samples = generate_negative_samples(len(seeds) * 5)  # 5倍负样本
    neg_features = extract_features(neg_samples, is_positive=False)
    y_neg = [0] * len(neg_samples)
    
    # 合并数据
    X = pd.concat([pos_features, neg_features], ignore_index=True)
    y = y_pos + y_neg
    
    # 训练XGBoost
    model = XGBClassifier(max_depth=5, eta=0.1, objective='binary:logistic', eval_metric='auc', random_state=42)
    model.fit(X, y)
    
    # 生成候选地址
    candidates = generate_candidates(100000)
    cand_features = extract_features(candidates, is_positive=False)
    probs = model.predict_proba(cand_features)[:, 1]
    
    # 选择高概率地址
    top_k = 50000  # 假设2001:1:分配5000条
    top_indices = np.argsort(probs)[-top_k:]
    top_addresses = [candidates[i] for i in top_indices]
    
    # 保存结果
    with open('predictions_2001_1.csv', 'w', encoding='utf-8') as f:
        for addr in top_addresses:
            f.write(f"{addr}\n")

if __name__ == '__main__':
    main()