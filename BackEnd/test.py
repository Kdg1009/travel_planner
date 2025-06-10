from modules.common.get_pois_from_map import get_pois_from_map
from modules.get_pois_util import get_filter_from_llm
from modules.common.poi_metadata import get_reviews
from modules.route_optim_util import get_scores_from_llm
from components.user_request_data import UserRequest, Duration, Kwargs
from components.poi_data import Place, Geometry, OpeningHours, Photos
from modules.common.route_optimizer import optimize_route
import json
from modules.common.llm_request import request_to_llm
from modules.common.get_pois_from_map import extract_pois
from typing import List
import csv
from components.user_request_data import UserRequest
from modules.get_pois_util import save_pois
from modules.route_optim_util import load_pois

user_data = UserRequest(
                     user_id='',
                     location='Tokyo',
                     duration=Duration(start='2025-05-27', end='2025-05-29'),
                     companions=2,
                     concept='cultural sites and heritage attractions',
                     extra_request="i want to enjoy tokyo's culture like foods and other places that represent tokyo",
                     kwargs=Kwargs(filter=None, prev_map_data=None, cache_key=None))

#filter_data = get_filter_from_llm(user_data)
#print('filter:\n', filter_data)

filter_data = {'museum': 0.9, 'art_gallery': 0.8, 'university': 0.8, 'tourist_attraction': 1.0, 'restaurant': 0.7, 'cafe': 0.6}
#poi_list = extract_pois(user_data, filter_data, limit=10)
#print('poi list:\n',poi_list)
poi_list =  [
    Place(
        name='Shichifuku No Yu', 
        place_id='ChIJTyVn9amUGGARS-2IQP6otWA', 
        vicinity='1-chōme-4-56 Kizawaminami, Toda', 
        geometry=Geometry(lat=35.80579580000001, lng=139.6962849), 
        types=['tourist_attraction', 'spa', 'point_of_interest', 'establishment'], 
        rating=4.0, 
        user_ratings_total=3814, 
        opening_hours=OpeningHours(open_now=True), 
        photos=Photos(photo_reference='AXQCQNQZ5r-kvrglm9T0-qwOBHj39ZpjkvBBSB41YxzD1E7vAojzsV6l4PmiQQF2C9uzeT1oSup2Zn5XCSK9eCUtPZYynWKg8KUeQ77XZY64MP_RH6agxPzCWcm5DWnm67JH1KnYrejcZ6OeCrRAibNXGSVI3xLqN7WuxfRq1Tty1S7M0tM6xw2eLtdRXNmqM1yW8QoTMgg3uKq3gx5_paQmASXUA-P3QCPdjTuCV2pQ08V2_HcyEXa-5ZawZihjUxK7zxvUrDFyGR6PcD7bHC6O42_9kzLdUAjVgvZmMtElV2Z-vKRoGhXf_TpWRHSZ32YqVUKZbrd0i7ORRFSXPAtMZUra3hBHpgiVhD8aYeHkQpAQcrc2O9QptJntKcVxdpWw_dcnYtksjNugI0dGe5yZ9mKMG59q2qRUuUarCn4wLpkE65j8YCu9OJNlfNc1Ba1Hyjk1kbtcl1_V0UdiVOkHBQ4MzqUyKcNROaxBOoYvhQ7zpM8BjhlQ0QKuIddoeWuYWfWl7sTKVxJ_Xc9WvoOOw5whlpiDzzidtfTkmLXJPOnkwx2XLB8qC0yIA9D58qjVHFqmxWPlOGNE0pQsCqHPWme46K210kBQDtCaO393z_h8t8TIbaNl4j7LVXHc2J_hQORTfRox', width=3200, height=1800, html_attributions=['<a href="https://maps.google.com/maps/contrib/108098239873476614236">伊賀上真人</a>']), 
        icon='https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/generic_business-71.png'
        ), 
    Place(
        name='Cup Noodles Museum', 
        place_id='ChIJ3ZNhe1dcGGARvjq5QHdmaHM', 
        vicinity='2-chōme-3-4 Shinkō, Naka Ward, Yokohama', 
        geometry=Geometry(lat=35.4554755, lng=139.6388669), 
        types=['tourist_attraction', 'amusement_park', 'museum', 'point_of_interest', 'establishment'], 
        rating=4.2, 
        user_ratings_total=18092, 
        opening_hours=OpeningHours(open_now=False), 
        photos=Photos(photo_reference='AXQCQNT4NpayyUPmb4hi6R21HAvLfxz-zhzvJ1BrL_S7_tSOW_JYYFK1avA-_tjP0P8uEKeFgpPaAsq8bokK6iczTVZeMMa5Z4saj7H-u0pyWB2ur7elcelX4s1S8ih8bNLrQnyRfVSCylw8ehZ4mQXnthfAGIONvcYrD4ChRt-qT01WFJQYVxOVsfSnqrTYgVIq8BXw4jsIUvfYJFpdOO7BLKPf1ssleZdCfTwAY0p-qx0qDorpQn9mWV7uOO-E61Lnseh9qFeI7LbLmgJEdf6euwGkx1Tyhg1De7l9kQbvXO6Yeb6-jsU317UyTE5RRcESJwOAfSB5li4z2YDp5zl0wxV42le6Pk7-6Mx8sbvqfCXrRomK5fxqqIp2EtRBWJMgXag2tQ7_OXsN7hSKY9FKFkFyLt7KcQKgvw6HsyINvaftV4P7II126tCO5ahJB7tX_OoVfUtqccPFGgwd0-y3RgyPTbP0mG257e4j6scWiLjuhH9WAAj0jbF76GLj3mQhL_j1MAroBg-ps8tAFSxYBk29Vw7lVpjI91YlPm0RzukxzJnGMHUqwoh0w-XTgb64MwFNaQc3VvpcqBiEUk7Y3o0AMXtPxoODlUtKykgVDq18E5jTmUhrMT2ZLHdvMl2dLDcFCQ', width=3831, height=2873, html_attributions=['<a href="https://maps.google.com/maps/contrib/115873747796932406567">Chief Victor</a>']), 
        icon='https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/generic_business-71.png'
        ), 
    Place(
        name='Cup Noodles Museum', 
        place_id='ChIJ3ZNhe1dcGGARvjq5QHdmaHM', 
        vicinity='2-chōme-3-4 Shinkō, Naka Ward, Yokohama', 
        geometry=Geometry(lat=35.4554755, lng=139.6388669), 
        types=['tourist_attraction', 'amusement_park', 'museum', 'point_of_interest', 'establishment'], 
        rating=4.2, 
        user_ratings_total=18092, 
        opening_hours=OpeningHours(open_now=False), 
        photos=Photos(photo_reference='AXQCQNRLLDr5N1hRUwOOhAuC1Hzx-c6onPwqv4f5LDlDHytTbbv5a2mHKy5T-NDM4rlicpV4iGNRLDoH7nwh2Lrbl0bOF0yWpDzTBv0Zja94X-TGExom_Y_ztGL5PQSmnY4ZLFTIVDCrwIL4n9NwS-GjU0vizwnF75eZprJrciVOhgzcCdtNVhjjuXAcpHPUJp4rsXKqJtOe2QNSgtDUxqQ6nCZynaMxWPJhJwIoj6eVRXRYyWQqR3AY_qm3EYS805fWZdZlZyx9iT5x8_p47zFcADrGrxLmiZmZs2q35cz0WtsDMV_LY0e_JpLR8CJuubzmA54bC7Ji-3yKox7dwPu7YBtFIdfhtVggQC859Ta6-OQhD5WHF5UVZF9xUmh5oV9DW7Sjg3e_fdNwj2qeJWhisoKKBS8StBbcuqxq5629Ed1kadX-10kUnOXqMnCZttcfEYaHfdEfRCbORc2WnnUNNcUuwueEwTuoyJu7gFsHRGzE4T7tVjRXaWbYOR2KuIt-T_5PmEdJbi4dCHY54PsMRCe2PJTgUeIs6cZ93lseH-sxIcLOxIKk5vbA4lPQZtw3LOCinx24Eon1sZ0Wwwv2Yf-Nd-mXtvy-zQgmb74IltjMpLfASLvcy9Thhw7f69zvEyikIg', width=3831, height=2873, html_attributions=['<a href="https://maps.google.com/maps/contrib/115873747796932406567">Chief Victor</a>']), 
        icon='https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/generic_business-71.png'
        ), 
    Place(
        name='Amezaiku Yoshihara Sendagi Main Store', 
        place_id='ChIJc3fU2c2NGGARbfwxQHgJKjs', 
        vicinity='巴ビル １F, 1-chōme-23−５ Sendagi, Bunkyo City', 
        geometry=Geometry(lat=35.725004, lng=139.760796), 
        types=['art_gallery', 'store', 'food', 'point_of_interest', 'establishment'], 
        rating=4.6, 
        user_ratings_total=123, 
        opening_hours=None, 
        photos=Photos(photo_reference='AXQCQNQ_I8OX14S1LSMQS-bA3MvyamNztgw3HQy_wp1NprNmmkViV0VsOD3VqwoM_xrDnpW9g5z1LgO_DWxI8Lc6Uo2947DDpvv9en3lzHUiRc8dyFZrlZb55WA0COLsxQ71qcwfNzj4sKxUMX-f8lB-s6Mz3WcoUFBI6e2e_--mL2LtJXdEcvHfeBBbLvb_eDtiJ0dH6yJW5jl_0Nfm1KYjGmgQN9CncLhq216PsOwi555NrDBIvRi13FiCMRkedfBbM80IElz0HgZbPtIkwPSvF58f8cAKlKKbeFm67Nb8niHPqV2D5dCeTsXtlmCgcrVcvCfYoNeukOwiKcAl2-UDwhgJjXCGXMdsMclrpN_D7fpE1uXiiuQSf7k0IAGUkrrjwiKKGqKs0de1R83D70PS9uebLVS5htU_GlyygJgtWiLxKb4J8dtYAf1VTswbkAeT-Xajhj6nrT_fHq0fbPNKeoOZvDiwSBDf876eNYiQZ831k8akb3qCa8kg4_IUHYcjy-lYhBeisGkYhSOeHutrDOf6-IpTjpuJlrHkaFk662JsDU3wQz8bP5W26HUEhrnsD-yN07lliYcoEwd6E3lsufuH9IUHV8GsK_jJZeymDVRvHBZe9NqEwje62BvHFGl6_huzxQ', width=4032, height=3024, html_attributions=['<a href="https://maps.google.com/maps/contrib/115839855489964909275">Mynove Kenneth</a>']), 
        icon='https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/generic_business-71.png'
        ), 
    Place(name='The University of Tokyo', 
          place_id='ChIJo24g-i-MGGARlboTg0kH5DA', 
          vicinity='7-chōme-3-1 Hongō, Bunkyo City', 
          geometry=Geometry(lat=35.71381589999999, lng=139.7627345), 
          types=['university', 'point_of_interest', 'establishment'], 
          rating=4.5, user_ratings_total=2631, 
          opening_hours=OpeningHours(open_now=True), 
          photos=Photos(photo_reference='AXQCQNTs-ZvWISSlw_b8saQ4rZ18SGSkbB2jnfzLkKMjYr2JyMn2wYV5X1cPTsGptW0FNGjsmpVv629Y6LAkmWyT6rPUQZcag-AHGO3x_oTFn5YtbEuREk6Y5XS2k-k2oFRoqE6M6HztwekY3a6CgevdsHIjlE1rADmitCPD03PjPHbL9z0bwNegFgz5KwYJY3Jr0SEJYvRJZoHzP2z68b3m1WHLZbe9Oom8FtwQ-J_8LWLwAsaHLI_hgl1dFgQjmXAsSXbgCGlE0cuNrMq8MMLRmvCwiXFKNQK3PkHv_LmDLoqz-Sly69zKkKmatezPQqiviGV207qJO_Q1nqlCggM8BDJXhEgYPl8GD6PngdcTsry3WmcQd5xgk1IrdROK7SkiM05zCisJrRo-cCgNSlI7f3V5h9osfXZ0GXuz5tGmz0VJzR_AjGUnTXticvZjn1YDqUpz80Ryxral151rL9iwsGDPZvr6fbfBGqo0CfCL352L8qjQF0CunbdwNddBYCTa0QWmvWJ-XLSmV5A9EltXNa83pV3l6gs08Y5vgudmFBeai6xnHg2M51wOxRpSwsvmRtcIfWKmsrWCqWkkIvmO-I0WrTOCbycGXqnvt6godqR99XZB85M1SnBwVy-ifm60EDGa1g', width=4032, height=3024, html_attributions=['<a href="https://maps.google.com/maps/contrib/105340936840905234417">池田忠</a>']), 
          icon='https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/school-71.png'
          ), 
    Place(
        name='Shangri-La Tokyo', 
        place_id='ChIJL6nVJvyLGGAR8jHaHUYIL48', 
        vicinity='MARUNOUCHI TRUST TOWER MAIN, 1-chōme-8-3 Marunouchi, Chiyoda City', 
        geometry=Geometry(lat=35.6823599, lng=139.7694544), 
        types=['beauty_salon', 'spa', 'lodging', 'restaurant', 'food', 'point_of_interest', 'establishment'], 
        rating=4.5, 
        user_ratings_total=2976, 
        opening_hours=OpeningHours(open_now=True), 
        photos=Photos(photo_reference='AXQCQNQ3NkKFdgFI_DNF0W12i5OMxZYMuo-vDwT3O2WwULnEAvLM1OsPD-I52dhtNd7FFkWZvnZ2_zubpTSH0MXI6rlnMBd4_yhXzS-UmNL35HNilIdVduI-AL0xL1kvOp0VAFur6I72jo4msxhGd6EBjBeQJCZ2fkyYiGron4YwTmNN1XWnUggtsNvjJNS6aSKVCdzaqN4mWqh0X4s0zerdhrFcLB4vauL06YGfBZB4kJpNTglCWj6894JFT6BE_BaBHJfCWOvcC03Ch45uIt-u2p3C-mhc84Ho_DTqprwaaCWQqGg4DY6wx4O1vykev7D2TV4HDYlMR9M', width=5980, height=4000, html_attributions=['<a href="https://maps.google.com/maps/contrib/105785051637817760902">シャングリ・ラ ホテル 東京</a>']), 
        icon='https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/lodging-71.png'
        ), 
    Place(
        name='Shibuya Excel Hotel Tokyu', 
        place_id='ChIJTzNfw1eLGGARagCmVhCOmP4', 
        vicinity='1-chōme-12-2 Dōgenzaka, Shibuya', 
        geometry=Geometry(lat=35.6585773, lng=139.6998213), 
        types=['cafe', 'lodging', 'restaurant', 'food', 'point_of_interest', 'establishment'], 
        rating=4.2, 
        user_ratings_total=3535, 
        opening_hours=OpeningHours(open_now=True), 
        photos=Photos(photo_reference='AXQCQNTnnYZayGqxZFCYb67VqJOQaTf8F_0SNSApcqho1SuKiWvOh3OcSj2nemw2auscM0mOGx9vOFKHSJB5tstA6NCpW8T3vCuXXFQ5OgOaUOGAqeCDvnvfn2UU5lksddhOqnsRaiZ42en3eJ0aGhsvK-eQBSKDhOx6giorOGxef4xJqPS6Y1hWQ_3_jNCgxA2PCF6wwkziD1jWJRO-Vrcz0TH3YRnUatm9516uyzWi4UUyzSuQIeC2q5jUdUI80_2PiMHiguoCRXgJIgqheqxmw0HUcjBIiNkdjwocUwbJLHJm2jB1lX7Lwk3NqAGvv-cEnJGxPF5OstU', width=1080, height=720, html_attributions=['<a href="https://maps.google.com/maps/contrib/101297695086602663090">渋谷エクセルホテル東急</a>']), icon='https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/lodging-71.png')]
#scored_pois = get_scores_from_llm(poi_list=poi_list, user_data=user_data)
#print(scored_pois)

from modules.common.cache_util import print_status,save_data, load_data, delete_data

a = {"first":[1,2,3],"second":[3,4,5],"third":"hello world"}
key = save_data(payload=a)
b = {"fourth":"second params"}
save_data(key=key, payload=b)

datas = load_data(key=key)
print(datas)
removed = delete_data(key, "first")
print(removed)
print_status(key)
removed = delete_data(key, "third")
print(removed)
print_status(key)
removed = delete_data(key)
