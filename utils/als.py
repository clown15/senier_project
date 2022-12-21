import numpy as np
import pandas as pd
from order.models import Order
from product.models import Product
from scipy.sparse.linalg import svds
from .product_related import product_recommendation_for_metadata


def recommend_products(df_svd_preds, user_id, ori_product_df, ori_ratings_df, num_recommendations=5):
    user_row_number = user_id
    
    # 최종적으로 만든 pred_df에서 사용자 index에 따라 상품 데이터 정렬 -> 상품 평점이 높은 순으로 정렬 됌
    sorted_user_predictions = df_svd_preds.loc[user_row_number].sort_values(ascending=False)
    
    # 원본 평점 데이터에서 user id에 해당하는 데이터를 뽑아낸다. 
    user_data = ori_ratings_df[ori_ratings_df.orderer == user_id]
    
    # 위에서 뽑은 user_data와 원본 상품 데이터를 합친다. 
    user_history = user_data.merge(ori_product_df, on = 'product').sort_values(['rate'], ascending=False)
    
    # 원본 상품 데이터에서 사용자가 구매한 상품 데이터를 제외한 데이터를 추출
    recommendations = ori_product_df[~ori_product_df['product'].isin(user_history['product'])]
    # 사용자의 상품 평점이 높은 순으로 정렬된 데이터와 위 recommendations을 합친다. 
    recommendations = recommendations.merge( pd.DataFrame(sorted_user_predictions).reset_index(), on = 'product')
    # 컬럼 이름 바꾸고 정렬해서 return
    recommendations = recommendations.rename(columns = {user_row_number: 'Predictions'}).sort_values('Predictions', ascending = False).iloc[:num_recommendations, :]
                      
    return user_history, recommendations

def als_product_recommendation(session):
    orders = Order.objects.all().values_list('orderer','product','rate')

    products = Product.objects.values_list('id','name')
    
    cols = ['id','name']
    df_product = pd.DataFrame.from_records(data=products, columns=cols).rename(columns = {'id':'product'})

    cols = ['orderer','product','rate']
    df_order = pd.DataFrame.from_records(data=orders, columns=cols)

    # object type인 rate를 float type으로 변경
    df_order = df_order.astype({'rate': 'float'})
    df_user_product_ratings = df_order.pivot(
        index='orderer',
        columns='product',
        values='rate'
    ).fillna(0)

    # matrix는 pivot_table 값을 numpy matrix로 만든 것 
    # user_index = df_user_product_ratings.index.to_list().index(session['user'])
    # matrix에서 dateframe로 변환시 인뎃스를 유지하기위해 보존
    index_list = df_user_product_ratings.index.to_list()
    matrix = df_user_product_ratings.values

    # user_ratings_mean은 사용자의 평균 평점 
    user_ratings_mean = np.mean(matrix, axis = 1)

    # R_user_mean : 사용자-상품에 대해 사용자 평균 평점을 뺀 것.
    matrix_user_mean = matrix - user_ratings_mean.reshape(-1, 1)

    # k 는 인접한 사용자 몇명을 찾을지
    U, sigma, Vt = svds(matrix_user_mean, k = 5)
    
    sigma = np.diag(sigma)
    
    # U, Sigma, Vt의 내적을 수행하면, 다시 원본 행렬로 복원이 된다. 
    # 거기에 + 사용자 평균 rating을 적용한다. 
    svd_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
    df_svd_preds = pd.DataFrame(svd_user_predicted_ratings, columns = df_user_product_ratings.columns)
    
    col_name=pd.Series(index_list)
    df_svd_preds = df_svd_preds.set_index(keys=[col_name], inplace=False)

    already_rated, predictions = recommend_products(df_svd_preds, session['user'], df_product, df_order, 5)
    
    # 예측한 평점의 평균이 2.5이하일경우 추천하지 적합하지 않다고 판단
    if predictions.mean()['Predictions'] < 2.5:
        return product_recommendation_for_metadata(session)
    
    #  실제 추천 목록
    product_list = predictions['product'].to_list()

    product = Product.objects.filter(id__in = product_list)
    
    return product