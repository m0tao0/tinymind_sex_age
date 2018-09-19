#import seaborn as sns
import lightgbm as lgb
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier

from tiny.tfidf import *
from tiny.usage import *


@timed()
def gen_sub_by_para():
    args = locals()


    feature_label = get_stable_feature()



    train=feature_label[feature_label['sex'].notnull()]
    test =feature_label[feature_label['sex'].isnull()]

    X = train.drop(['sex', 'age', 'sex_age', 'device'], axis=1)



    Y = train['sex_age']
    Y_CAT = pd.Categorical(Y)
    X_train, X_test, y_train, y_test = train_test_split(X, Y_CAT.labels, test_size=0.3, random_state=666)

    X_train.fillna(0, inplace=True)
    X_test.fillna(0, inplace=True)

    classifier = RandomForestClassifier(n_estimators=10, criterion='entropy', random_state=42)
    classifier.fit(X_train, y_train)


    pre_x=test.drop(['sex','age','sex_age','device'],axis=1)
    sub=pd.DataFrame(classifier.predict_proba(pre_x.values))


    sub.columns=Y_CAT.categories
    sub['DeviceID']=test['device'].values
    sub=sub[['DeviceID', '1-0', '1-1', '1-2', '1-3', '1-4', '1-5', '1-6', '1-7','1-8', '1-9', '1-10', '2-0', '2-1', '2-2', '2-3', '2-4', '2-5', '2-6', '2-7', '2-8', '2-9', '2-10']]


    #lgb.plot_importance(gbm, max_num_features=20)

    print(f'=============Final train feature({len(feature_label.columns)}):\n{list(feature_label.columns)} \n {len(feature_label.columns)}')

    file = f'./sub/baseline_rf.csv'
    file = replace_invalid_filename_char(file)
    print(f'sub file save to {file}')
    sub.to_csv(file,index=False)

if __name__ == '__main__':

    gen_sub_by_para()
    # gen_sub_by_para(True, 0.4)
    # for drop_long in np.arange(0.1, 1.1, 0.1):
    #     for drop_useless_pkg in [True, False]:
    #
    #         gen_sub_by_para(drop_useless_pkg, round(drop_long,1))