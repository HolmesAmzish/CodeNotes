import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from ipaddress import IPv6Address

# 读取种子地址
def load_seeds(file_path):
    with open(file_path, 'r') as f:
        seeds = [line.strip() for line in f]
    return seeds

# 展开IPv6地址
def expand_ipv6(addr):
    ip = IPv6Address(addr)
    return ip.exploded

# 提取特征
def extract_features(addr):
    parts = expand_ipv6(addr).split(':')
    # 前缀第三组转为十进制
    third_group = int(parts[2], 16)
    # IID是否为::1
    is_iid_one = 1 if ':'.join(parts[4:]) == '0000:0000:0000:0001' else 0
    return [third_group, is_iid_one]

# 生成候选地址
def generate_candidates(net_segment, n_samples):
    candidates = []
    for i in range(n_samples):
        third_group = np.random.randint(0, 0xffff)  # 随机第三组
        addr = f"{net_segment}:{third_group:04x}::1"
        candidates.append(addr)
    return candidates

# 主流程
def main():
    # 加载2001:2:网段种子地址
    seeds = load_seeds('give_data/2_give.txt')
    
    # 提取特征
    X = [extract_features(addr) for addr in seeds]
    y = [1] * len(seeds)  # 正样本标签
    
    # 生成负样本
    neg_samples = generate_candidates('2001:2', len(seeds))
    X_neg = [extract_features(addr) for addr in neg_samples]
    y_neg = [0] * len(neg_samples)
    
    # 合并数据
    X = X + X_neg
    y = y + y_neg
    
    # 划分训练测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 训练XGBoost
    model = XGBClassifier(max_depth=6, eta=0.1, objective='binary:logistic', eval_metric='auc')
    model.fit(X_train, y_train)
    
    # 生成预测地址
    candidates = generate_candidates('2001:2', 100000)
    X_cand = [extract_features(addr) for addr in candidates]
    probs = model.predict_proba(X_cand)[:, 1]
    
    # 选择高概率地址
    top_candidates = [candidates[i] for i in np.argsort(probs)[-25000:]]  # 选25k条
    
    # 保存结果
    with open('predictions.csv', 'w') as f:
        for addr in top_candidates:
            f.write(f"{addr}\n")

if __name__ == '__main__':
    main()