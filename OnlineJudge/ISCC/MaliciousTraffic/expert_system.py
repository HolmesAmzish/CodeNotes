"""
恶意流量检测专家系统
基于规则的方法检测网络攻击
"""

import pandas as pd

class MaliciousTrafficExpertSystem:
    def __init__(self):
        # 定义攻击类型检测规则
        self.rules = [
            {
                'name': 'DoS攻击检测',
                'conditions': [
                    lambda x: x['proto'] in ['tcp', 'udp', 'icmp'],
                    lambda x: x['rate'] > 100000,
                    lambda x: x['dpkts'] == 0,
                    lambda x: x['state'] == 'INT',
                    lambda x: x['sbytes'] > 1000  # 大包攻击
                ],
                'attack_type': 'DoS'
            },
            {
                'name': '端口扫描检测',
                'conditions': [
                    lambda x: x['proto'] == 'tcp',
                    lambda x: x['ct_dst_sport_ltm'] > 30,
                    lambda x: x['sttl'] == 254,
                    lambda x: x['state'] == 'INT',
                    lambda x: x['dur'] < 0.01  # 短时间连接
                ],
                'attack_type': 'Reconnaissance'
            },
            {
                'name': '暴力破解检测',
                'conditions': [
                    lambda x: x['service'] in ['ssh', 'ftp', 'telnet'],
                    lambda x: x['ct_srv_src'] > 8,
                    lambda x: x['sinpkt'] < 0.2,
                    lambda x: x['is_ftp_login'] == 1,
                    lambda x: x['sbytes'] < 500  # 小包攻击
                ],
                'attack_type': 'Fuzzers'
            },
            {
                'name': 'Exploits检测',
                'conditions': [
                    lambda x: x['service'] in ['http', 'ftp'],
                    lambda x: x['response_body_len'] > 1000,
                    lambda x: x['trans_depth'] > 3,
                    lambda x: x['ct_flw_http_mthd'] > 0
                ],
                'attack_type': 'Exploits'
            },
            {
                'name': 'Generic攻击检测',
                'conditions': [
                    lambda x: x['proto'] == 'udp',
                    lambda x: x['ct_dst_sport_ltm'] > 20,
                    lambda x: x['state'] == 'INT',
                    lambda x: x['dur'] < 0.001
                ],
                'attack_type': 'Generic'
            },
            {
                'name': '正常流量',
                'conditions': [
                    lambda x: x['state'] in ['FIN', 'CON'],
                    lambda x: x['rate'] < 50000,
                    lambda x: x['ct_srv_src'] < 10,
                    lambda x: 500 < x['sbytes'] / x['spkts'] < 1500,
                    lambda x: 0.1 < x['dur'] < 10  # 合理连接时长
                ],
                'attack_type': 'Normal'
            }
        ]

    def detect_attack(self, traffic_data):
        """
        检测单条流量记录
        :param traffic_data: 单条流量数据的字典
        :return: 检测到的攻击类型
        """
        for rule in self.rules:
            match = True
            for condition in rule['conditions']:
                try:
                    if not condition(traffic_data):
                        match = False
                        break
                except:
                    match = False
                    break
            
            if match:
                return rule['attack_type']
        
        # 如果没有匹配任何规则，返回未知类型
        return 'Unknown'

    def evaluate(self, df):
        """
        评估整个数据集
        :param df: 包含流量数据的DataFrame
        :return: 添加了预测结果的DataFrame
        """
        predictions = []
        for _, row in df.iterrows():
            pred = self.detect_attack(row.to_dict())
            predictions.append(pred)
        
        df['expert_pred'] = predictions
        return df

    def print_metrics(self, df):
        """
        打印评估指标
        :param df: 包含真实标签和预测结果的DataFrame
        """
        from sklearn.metrics import classification_report
        
        y_true = df['attack_cat']
        y_pred = df['expert_pred']
        
        print("=== 专家系统评估结果 ===")
        print(classification_report(y_true, y_pred))
        
        # 计算准确率
        accuracy = (y_true == y_pred).mean()
        print(f"\n准确率: {accuracy:.4f}")

# 使用示例
if __name__ == "__main__":
    # 加载数据
    df = pd.read_csv('OnlineJudge/ISCC/MaliciousTraffic/data/sample_data.csv')
    
    # 初始化专家系统
    expert = MaliciousTrafficExpertSystem()
    
    # 进行评估
    result_df = expert.evaluate(df)
    
    # 打印评估指标
    expert.print_metrics(result_df)
    
    # 保存结果
    result_df.to_csv('OnlineJudge/ISCC/MaliciousTraffic/expert_predictions.csv', index=False)
