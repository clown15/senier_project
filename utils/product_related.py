from django.core.exceptions import ObjectDoesNotExist
from product.models import Product,MetaData,Allergy
from order.models import Order
from django.db.models import Q
import pandas as pd
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

""" 최근 주문 내역을 기반으로 상품 추천
해당 상품과 같은 카테고리에 있거나 같은 판매자 제품중 판매량이 높은 5개 추천
"""
def product_recommendation(user):
    
    try:
        order = Order.objects.filter(orderer = user).latest('creation_date')
    except ObjectDoesNotExist:
        return Product.objects.order_by('-sales_rate','-creation_date')[:5]

    product_list = Product.objects.filter(
        Q(category = order.product.category)|
        Q(creator = order.product.creator)
    ).exclude(pk=order.product.id).order_by('-sales_rate','-creation_date').distinct()[:5]

    return product_list


""" 현재 주문을 기준으로 최근 5개의 상품 리턴
"""
def hot_product_recommendation():
    orders = Order.objects.raw("SELECT * FROM (SELECT * FROM 'order' ORDER BY creation_date DESC LIMIT 100) GROUP BY product_id order by creation_date DESC")

    
    products = []
    for order in orders[0:5]:
        products.append(order.product)

    return products



def product_recommendation_for_metadata(session):
    try:
        order = Order.objects.filter(orderer = session['user']).latest('creation_date')
    except ObjectDoesNotExist:
        return Product.objects.order_by('-sales_rate','-creation_date')[:5]

    # con = sqlite3.connect('../db.sqlite3')

    # cur = con.cursor()
    # data = cur.execute("""select product_id,name,data 
    # from product_meta_data 
    # left outer join product on product_meta_data.product_id = product.id""")
    # data = MetaData.objects.all().values('product', 'data')
    # q = Q()
    # for k,v in session['user_allergy'].items():
    #     if v == 2:
    #         q.add(Q(k=False), q.AND)

    filter_set = {"allergy__"+k: 0 for k,v in session['user_allergy'].items() if v == 2}

    # data = MetaData.objects.filter(**filter_set).select_related('allergy').values('product', 'data')
    data = MetaData.objects.filter(**filter_set).select_related('allergy') | MetaData.objects.filter(product=order.product.id).select_related('allergy')
    data = data.values('product', 'data')
    if len(data) < 10:
        return Product.objects.order_by('-sales_rate','-creation_date')[:5]

    # data = MetaData.objects.raw(
    #     """select *
    #     from product_meta_data 
    #     left outer join product_allergy on product_meta_data.product_id = product_allergy.product_id"""
    # )
    
    cols = ['product', 'data']
    df = pd.DataFrame.from_records(data=data, columns=cols)

    # con.close()

    tfidf_matrix = TfidfVectorizer().fit_transform(df['data'])
    # print('TF-IDF 행렬의 크기(shape) :',tfidf_matrix.shape)

    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    # print('코사인 유사도 연산 결과 :',cosine_sim.shape)

    name_to_index = dict(zip(df['product'], df.index))

    def get_recommendations(name, cosine_sim=cosine_sim):
        # 선택한 상품 이름으로 해당 상품의 인덱스를 받아온다.
        idx = name_to_index[name]

        # 해당 상품과 모든 상품의 유사도를 가져온다.
        sim_scores = list(enumerate(cosine_sim[idx]))

        # 유사도에 따라 상품들을 정렬한다.
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # 가장 유사한 5개의 상품를 받아온다.
        sim_scores = sim_scores[1:6]

        # 가장 유사한 5개의 상품의 인덱스를 얻는다.
        movie_indices = [idx[0] for idx in sim_scores]

        # 가장 유사한 5개의 상품의 제목을 리턴한다.
        return df['product'].iloc[movie_indices]

    # result = get_recommendations(product_id)
    result = get_recommendations(order.product.id)
    result_list = []
    for id in result:
        product = Product.objects.get(id=id)
        result_list.append(product)

    return result_list


if __name__ == "__main__":
    result = product_recommendation_for_metadata('user2@test.com')
    print(result)