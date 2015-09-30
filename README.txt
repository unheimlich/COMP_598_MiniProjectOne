# COMP_598_MiniProjectOne
Linear Regression

DEPENDENCIES

python
numpy
pandas
beautifulsoup

SETUP

In terminal:

1. $ mkdir foo
2. $ cd foo
3. $ git clone https://github.com/unheimlich/COMP_598_MiniProjectOne.git
4. $ cd COMP_598_MiniProjectOne
5. $ python

PART ONE

1. Create test, validation, and training sets
    
    import src.CrossValidate as cv
    
    filename = 'data/PartOne/OnlineNewsPopularity.csv'
    cv.separateTestSet(filename, 5)                       # Set aside 20% for test
    cv.kfoldlabel(filename, 5)                          # Create 5-fold cross validation indices
    
2. Run a cross validation set
    
    optimization = 'LeastSquares'     # 'LeastSquares', 'GradientDescent'
    lmda = 0.0                      # L2 regularization constant: float >= 0
    alpha = 0.0                       # Learning Rate: float >= 0
    preprocess = ''                   # '', 'center', 'standardize', 'whiten'

    train_rmse, validation_rmse, y_train, t_train = cv.runcrossval(optimization, lmda, alpha, preprocess)
    
3. Evaluate Test Error

    test_rmse, w, y_test, t_test, w = cv.test(optimization, lambda, alpha, preprocess)
    
PART TWO

1. Create test, validation, and training sets
    
    import src.CrossValidate2 as cv2
    
    filename = 'data/PartTwo/DailyMailArticlePopularity.csv'
    cv2.separateTestSet(filename, 5)                       # Set aside 20% for test
    cv2.kfoldlabel(filename, 5)                          # Create 5-fold cross validation indices
    
2. Run a cross validation set
    
    optimization = 'LeastSquares'     # 'LeastSquares', 'GradientDescent'
    lmda = 0.0                      # L2 regularization constant: float >= 0
    alpha = 0.0                       # Learning Rate: float >= 0
    preprocess = ''                   # '', 'center', 'standardize', 'whiten'

    train_rmse, validation_rmse, y_train, t_train = cv2.runcrossval(optimization, lmda, alpha, preprocess)
    
3. Evaluate Test Error

    test_rmse, w, y_test, t_test, w = cv2.test(optimization, lambda, alpha, preprocess)
