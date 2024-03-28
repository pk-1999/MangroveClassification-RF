from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd

# 读取数据
data = pd.read_csv('GMD_v1.csv')

# 划分特征和目标变量
X = data[['red', 'nir', 'swir1', 'swir2']]
y = data['landcover']

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=24)

# 创建随机森林分类器实例
clf = RandomForestClassifier(random_state=44)

# 定义要搜索的超参数网格
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'bootstrap': [True, False]
}

# 创建GridSearchCV实例
grid_search = GridSearchCV(estimator=clf, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)

# 执行超参数寻优
grid_search.fit(X_train, y_train)

# 输出最佳参数
print('最佳参数:', grid_search.best_params_)

# 使用最佳参数创建新的模型
best_clf = grid_search.best_estimator_

# 使用新的模型进行预测
predictions = best_clf.predict(X_test)

# 评估模型
accuracy = accuracy_score(y_test, predictions)

print('预测结果:', predictions)
print('模型准确率:', accuracy)