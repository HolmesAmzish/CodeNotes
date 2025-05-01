"""
网络流量恶意攻击检测分析脚本
分步骤实现完整的机器学习流程，便于在notebook中逐步讲解
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 数据加载与探索分析
def load_data(filepath):
    """加载数据集"""
    df = pd.read_csv(filepath)
    print(f"数据形状: {df.shape}")
    print("\n前5行数据:")
    print(df.head())
    return df

def explore_data(df):
    """数据探索分析"""
    print("\n=== 数据概览 ===")
    print(df.info())
    
    print("\n=== 数值特征统计 ===")
    print(df.describe())
    
    print("\n=== 类别特征统计 ===")
    cat_cols = df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        print(f"\n{col}分布:")
        print(df[col].value_counts())
    
    print("\n=== 标签分布 ===")
    plt.figure(figsize=(10,6))
    sns.countplot(data=df, y='attack_cat', order=df['attack_cat'].value_counts().index)
    plt.title('攻击类别分布')
    plt.show()

# 2. 数据预处理
def preprocess_data(df):
    """数据预处理"""
    # 分离特征和标签
    X = df.drop('attack_cat', axis=1)
    y = df['attack_cat']
    
    # 划分训练测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)
    
    return X_train, X_test, y_train, y_test

# 3. 特征工程
def build_feature_pipeline():
    """构建特征处理管道"""
    # 数值特征
    numeric_features = ['dur', 'spkts', 'dpkts', 'sbytes', 'dbytes', 'rate', 
                       'sttl', 'dttl', 'sload', 'dload', 'sloss', 'dloss',
                       'sinpkt', 'dinpkt', 'sjit', 'djit', 'swin', 'stcpb',
                       'dtcpb', 'dwin', 'tcprtt', 'synack', 'ackdat', 'smean',
                       'dmean', 'trans_depth', 'response_body_len', 'ct_srv_src',
                       'ct_state_ttl', 'ct_dst_ltm', 'ct_src_dport_ltm',
                       'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'ct_ftp_cmd',
                       'ct_flw_http_mthd', 'ct_src_ltm', 'ct_srv_dst']
    
    # 类别特征
    categorical_features = ['proto', 'service', 'state', 'is_ftp_login', 'is_sm_ips_ports']
    
    # 构建预处理管道
    numeric_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())])
    
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)])
    
    return preprocessor

# 4. 模型训练与评估
def train_model(X_train, y_train, preprocessor):
    """训练随机森林模型"""
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(
            n_estimators=100, 
            random_state=42,
            class_weight='balanced',
            n_jobs=-1))])
    
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """评估模型性能"""
    y_pred = model.predict(X_test)
    
    print("\n=== 分类报告 ===")
    print(classification_report(y_test, y_pred))
    
    print("\n=== 准确率 ===")
    print(f"准确率: {accuracy_score(y_test, y_pred):.4f}")
    
    # 特征重要性
    if hasattr(model.named_steps['classifier'], 'feature_importances_'):
        print("\n=== 特征重要性 ===")
        importances = model.named_steps['classifier'].feature_importances_
        
        # 获取特征名称
        numeric_features = model.named_steps['preprocessor'].transformers_[0][2]
        categorical_features = model.named_steps['preprocessor'].transformers_[1][2]
        
        # 处理onehot编码后的特征名
        ohe = model.named_steps['preprocessor'].transformers_[1][1].named_steps['onehot']
        cat_feature_names = ohe.get_feature_names_out(input_features=categorical_features)
        
        all_feature_names = np.concatenate([numeric_features, cat_feature_names])
        
        # 创建特征重要性DataFrame
        feature_imp = pd.DataFrame({
            'feature': all_feature_names,
            'importance': importances
        }).sort_values('importance', ascending=False)
        
        print(feature_imp.head(10))

# 5. 主流程
def main():
    # 1. 加载数据
    df = load_data('data/sample_data.csv')
    
    # 2. 数据探索
    explore_data(df)
    
    # 3. 数据预处理
    X_train, X_test, y_train, y_test = preprocess_data(df)
    
    # 4. 特征工程
    preprocessor = build_feature_pipeline()
    
    # 5. 模型训练
    model = train_model(X_train, y_train, preprocessor)
    
    # 6. 模型评估
    evaluate_model(model, X_test, y_test)
    
    # 7. 保存模型
    joblib.dump(model, 'traffic_model.pkl')
    print("\n模型已保存为 traffic_model.pkl")

if __name__ == "__main__":
    main()
