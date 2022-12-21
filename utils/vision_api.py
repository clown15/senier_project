import io
from google.cloud import vision
import copy
import sqlite3
import re


BASE_ALLERGY = {
        'buckwheat': '메밀',
        'wheat': '밀',
        'Big_head': '대두',
        'peanut': '땅콩',
        'Walnut': '호두',
        'pine_nut': '잣',
        'peach': '복숭아',
        'tomato': '토마토',
        'milk': '우유',
        'shrimp': '새우',
        'Mackerel': '고등어',
        'squid': '오징어',
        'crab': '게',
        'clam': '조개',
        'Pork': '돼지고기',
        'beef': '쇠고기',
        'chicken': '닭고기',
    }


""" detect_text(file_path)
file_path는 파일 전체 경로
vision api를 사용해 이미지에서 텍스트 추출
"""
def detect_text(path):    
    client = vision.ImageAnnotatorClient()
    
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    price_candidate = []
    card_number_candidate = []
    date_candidate = []

    response = client.text_detection(image=image)
    return response

def check_word_in_list(texts):
    base_allergy = copy.deepcopy(BASE_ALLERGY)

    for key,v in base_allergy.items():
        if v in texts:
            base_allergy[key] = True
        else:
            base_allergy[key] = False

    return base_allergy
    # texts = response.text_annotations

    # print('Texts:')

    # for text in texts:
    #     content = text.description
    #     content = content.replace(',','')
    #     print('\n"{}"'.format(content))

    # if response.error.message:
    #     raise Exception(
    #         '{}\nFor more info on error messages, check: '
    #         'https://cloud.google.com/apis/design/errors'.format(
    #             response.error.message))

"""model은 get을 통해 받아온 object
obejct를 dict형태로 변환해 안에있는 알러지 정보를 boolean형태가 아닌 한글 형태로 변환
base_allergy를 반환하는 이유는 매개변수인 model을 반환할경우 사용자나 상품정보가 포함되어 있을 수 있기 때문
"""
def model_to_dict_allergy(model):
    base_allergy = copy.deepcopy(BASE_ALLERGY)

    for k,v in model.__dict__.items():
        if not v:
            del base_allergy[k]
    
    return base_allergy


# def create_meta():
#     con = sqlite3.connect('../db.sqlite3')

#     cur = con.cursor()
#     datas = cur.execute("select id,name,Nutrition_Facts from product ")
    
#     meta_data_list = []
#     count = 0
#     for row in datas:
#         # print(row)
#         # 이미 메타데이터가 있는지
#         # is_exist = cur.execute("select exists (select * from 'product_meta_data' where id=12)")
#         # if not is_exist.fetchone():
#         #     continue
#         # print(datas)
#         if row[2]:
#             img_path = "/home/Administrator/django_shop/Django_Shop/media/" + row[2]

#             response = detect_text(img_path)
#             texts = response.text_annotations
        
#             text_list = []
#             for text in texts:
#                 content = []
#                 for word in re.split('[,.\n]',text.description):
#                     if word:
#                         content.append(word)
#                 text_list.extend(content)

#             meta_data_list.append((" ".join(text_list),row[0]))
#     sql = "INSERT INTO product_meta_data (data,product_id) VALUES (?, ?)"
#     cur.executemany(sql, meta_data_list)
    
#     con.commit()
#     con.close()



if __name__ == "__main__":
    create_meta()