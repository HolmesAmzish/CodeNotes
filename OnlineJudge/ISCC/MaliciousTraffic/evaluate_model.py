import pandas as pd
import joblib
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score

# 加载模型
model = joblib.load('traffic_model.pkl')

# 加载样本数据
df = pd.read_csv('data/train_data.csv')

# 分离特征和标签
X = df.drop('attack_cat', axis=1)
y_true = df['attack_cat']

# 进行预测
y_pred = model.predict(X)

# 计算评估指标
accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred, average=None)
recall = recall_score(y_true, y_pred, average=None)
f1 = f1_score(y_true, y_pred, average=None)
macro_f1 = f1_score(y_true, y_pred, average='macro')

# 创建分类指标DataFrame
metrics_df = pd.DataFrame({
    '类别': y_true.unique(),
    '精确率(precision)': precision,
    '召回率(recall)': recall,
    'F1分数': f1
})

# 输出结果
print("=== 模型评估结果 ===")
print(f"整体准确率: {accuracy:.4f}")
print(f"宏平均F1分数: {macro_f1:.4f}")

print("\n=== 各类别指标 ===")
print(metrics_df)

print("\n=== 分类报告 ===")
print(classification_report(y_true, y_pred))

# 保存预测结果
results = pd.DataFrame({
    'id': df['id'],
    'predicted': y_pred,
})
results.to_csv('predictions.csv', index=False)

# 对比预测值和真实值
comparison = pd.DataFrame({
    '真实值': y_true,
    '预测值': y_pred,
    '是否正确': y_true == y_pred
})

print("\n=== 预测结果对比 (前20条) ===")
print(comparison.head(20))

# 计算各类别的准确率
class_accuracy = comparison.groupby('真实值')['是否正确'].mean()
print("\n=== 各类别准确率 ===")
print(class_accuracy.sort_values(ascending=False))