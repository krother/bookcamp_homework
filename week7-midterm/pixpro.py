# coding: utf-8

from PIL import Image
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import KBinsDiscretizer, PolynomialFeatures



def rgb_model(m, train, val, df, rows, cols):
    """
    Trains a model separately for 3 color channels.
    Then predicts the color for each color channel 
    separately and returns the resulting image
    """
    Xtrain = train[['x', 'y']]
    Xval = val[['x', 'y']]
    result = np.zeros((rows, cols, 3), dtype=np.uint8)
    
    for i, col in enumerate(['red', 'green', 'blue']):
        col_train = train[col]
        col_val = val[col]
    
        m.fit(Xtrain, col_train)
        trainscore = m.score(Xtrain, col_train)
        valscore = m.score(Xval, col_val)
        print(f'{col}\t'
              f'training R²   : {trainscore:6.3f}\t'
              f'validation R² : {valscore:6.3f}') 

        pred = m.predict(df[['x', 'y']])
        pred = pred.reshape((rows, cols)).astype(np.uint8)
        result[:,:,i] = pred
        
    return Image.fromarray(result)


def halfsize(im):
    return im.resize((im.size[0]//2, im.size[1]//2))


def train_predict(input_filename, model='linreg', output_filename='prediction.png', bins=15, depth=10):
    """
    Trains a model from the RGB pixel values of an image and predicts the image from it.
    Saves the resulting image to a file.
    """
    # read the image
    im = Image.open(input_filename)
    a = np.array(im)
    cols, rows = im.size

    red = a[:,:,0]
    green = a[:,:,1]
    blue = a[:,:,2]

    # convert to a DF with x,y pixel positions and RGB values as columns
    x, y = np.meshgrid(range(cols), range(rows))
    coords = list(zip(y.flatten(), x.flatten()))

    data = [(yy, xx, red[yy, xx], green[yy, xx], blue[yy, xx]) for yy, xx in coords]
    df = pd.DataFrame(data, columns=('y', 'x', 'red', 'green', 'blue'))

    # train-test-split
    train, val = train_test_split(df, test_size=0.20, random_state=42)

    if model == 'linreg':
        m = make_pipeline(
            KBinsDiscretizer(n_bins=bins, encode='onehot'),
            PolynomialFeatures(interaction_only=True),
            LinearRegression()
        )
    else:
        m = DecisionTreeRegressor(max_depth=depth)

    result = rgb_model(m, train, val, df, rows, cols)
    result.save(output_filename)


if __name__ == '__main__':
    train_predict('pearl_earring_small.jpg', 'tree', 'pearl_tree.png')
