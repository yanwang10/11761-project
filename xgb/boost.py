import sys
import xgboost as xgb

def main(train, test):
    '''
        Load data
    '''
    dtrain = xgb.DMatrix('./train.libsvm')
    dtest = xgb.DMatrix('./test.libsvm')

    '''
        Setting parameters
    '''
    param = {'objective':'binary:logistic'}
    #param = {'bst:max_depth':2, 'bst:eta':0.8, 'silent':1, 'objective':'binary:logistic'}
    param['booster'] = 'gblinear'
    param['lambda'] = 0.1
    param['lambda_bias'] = 1
    param['nthread'] = 4
    watchlist  = [(dtest,'eval'), (dtrain,'train')]

    '''
        Train the model
    '''
    num_round = 100
    bst = xgb.train( param, dtrain, num_round, watchlist )
    # bst.save_model('0001.model')

    # eval_train_err(bst.predict(dtrain), dtrain)
    # eval_test_err(bst.predict(dtest), dtest)

def eval_train_err(preds, dtrain):
    labels = dtrain.get_label()
    # return a pair metric_name, result
    # since preds are margin(before logistic transformation, cutoff at 0)
    print 'training error', float(sum(labels != (preds > 0.5))) / len(labels)

def eval_test_err(preds, dtest):
    labels = dtest.get_label()
    # return a pair metric_name, result
    # since preds are margin(before logistic transformation, cutoff at 0)
    print 'test error', float(sum(labels != (preds > 0.5))) / len(labels)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])