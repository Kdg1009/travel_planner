from modules.common.get_pois_from_map import get_pois_from_map
from modules.get_pois_util import get_filter_from_llm
from modules.common.poi_metadata import get_reviews
from modules.route_optim_util import get_scores_from_llm
from components.user_request_data import UserRequest, Duration, Kwargs
from modules.common.route_optimizer import optimize_route
import json
from modules.common.llm_request import request_to_llm
from typing import List
import csv
from components.user_request_data import UserRequest

user_data = UserRequest(location='Tokyo',
                     duration=Duration(start='2025-05-27', end='2025-05-29'),
                     companions=2,
                     concept='local food,famous restaurants,desserts,cafés',
                     extra_request='local restaurant',
                     kwargs=Kwargs(filter=None, prev_map_data=None, cache_key=None))
poi_list = [{'name': 'Jeonggwanheon (정관헌)', 'lat': 37.566417, 'lon': 126.975738, 'categories': ['Historic and Protected Site'], 'fsq_id': '4ddf60df18388714bb66786f'}, 
            {'name': 'Daehanmun (대한문)', 'lat': 37.56512, 'lon': 126.976808, 'categories': ['Historic and Protected Site'], 'fsq_id': '4cb26cb5ef1b3704e8534b00'}, 
            {'name': 'Seokjojeon (석조전 대한제국역사관)', 'lat': 37.566042, 'lon': 126.974338, 'categories': ['Historic and Protected Site'], 'fsq_id': '4e7472bdfa760597008ad518'}, 
            {'name': 'Heungnyemun (흥례문)', 'lat': 37.576288, 'lon': 126.977041, 'categories': ['Historic and Protected Site'], 'fsq_id': '4e88383ef5b991c24e3c8337'}, 
            {'name': '환구단', 'lat': 37.565008, 'lon': 126.979579, 'categories': ['Historic and Protected Site'], 'fsq_id': '555e84f5498ea0e93690dc3e'}, 
            {'name': 'Donuimun Museum village (돈의문 박물관마을)', 'lat': 37.568694, 'lon': 126.968654, 'categories': ['Historic and Protected Site'], 'fsq_id': '589c0795f595726efdd1e0d1'}, 
            {'name': '구러시아공사관', 'lat': 37.568073, 'lon': 126.971544, 'categories': ['Historic and Protected Site'], 'fsq_id': '4c9ae7c278fc236a4cc73997'}, 
            {'name': 'Gyeonggyojang (Kim gu house) (경교장)', 'lat': 37.568299, 'lon': 126.968087, 'categories': ['Historic and Protected Site'], 'fsq_id': '4d5e0c14338bb60c9d1d0bbd'}, 
            {'name': '군기시유적전시실', 'lat': 37.56644, 'lon': 126.97844, 'categories': ['Historic and Protected Site'], 'fsq_id': '55b988ff498e85c60cf3e4be'}, 
            {'name': 'Main Entrance to the Wongudan Altar (원구단 정문)', 'lat': 37.564812, 'lon': 126.978814, 'categories': ['Historic and Protected Site'], 'fsq_id': '5ba3466c2db4a9002cd28b37'}, 
            {'name': 'Wongudan Plaza (환구단 시민광장)', 'lat': 37.565048, 'lon': 126.979373, 'categories': ['Historic and Protected Site'], 'fsq_id': '4ccb9d1272106dcb65cd9599'}, 
            {'name': 'Hamnyeongjeon (함녕전)', 'lat': 37.565909, 'lon': 126.9758, 'categories': ['Historic and Protected Site'], 'fsq_id': '506c0685e4b037d925c3dea0'}, 
            {'name': '경운궁 양이재', 'lat': 37.56694, 'lon': 126.975514, 'categories': ['Historic and Protected Site'], 'fsq_id': '5059554fe4b0c50f01609053'}, 
            {'name': 'Deokhongjeon (덕홍전)', 'lat': 37.565681, 'lon': 126.975571, 'categories': ['Historic and Protected Site'], 'fsq_id': '50badff1e4b0cbe642c70595'}, 
            {'name': '덕수궁 행각', 'lat': 37.565035, 'lon': 126.976167, 'categories': ['Historic and Protected Site'], 'fsq_id': '50bae20ae4b048d4461b90e0'}, 
            {'name': 'Seogeodang (석어당)', 'lat': 37.566115, 'lon': 126.975125, 'categories': ['Historic and Protected Site'], 'fsq_id': '50374cbce4b0304eb42b2910'}, 
            {'name': '즉조당', 'lat': 37.566279, 'lon': 126.974978, 'categories': ['Historic and Protected Site'], 'fsq_id': '4c01e020f99620a122552504'},
            {'name': 'Junghwajeon (중화전)', 'lat': 37.565751, 'lon': 126.974774, 'categories': ['Historic and Protected Site'], 'fsq_id': '4c0b31596071a593ddfee032'}, 
            {'name': '임자로또사는곳', 'lat': 37.570091, 'lon': 126.977059, 'categories': ['Historic and Protected Site'], 'fsq_id': '4f041e6f8b81d71b4c2fcd3e'}, 
            {'name': '덕수궁 후문', 'lat': 37.565002, 'lon': 126.973571, 'categories': ['Historic and Protected Site'], 'fsq_id': '5631c223498ebdd0e1927072'}, 
            {'name': '피맛골', 'lat': 37.570527, 'lon': 126.98014, 'categories': ['Historic and Protected Site', 'Road'], 'fsq_id': '4b932c9ef964a520523934e3'}, 
            {'name': '고종의 길', 'lat': 37.567562, 'lon': 126.97287, 'categories': ['Historic and Protected Site'], 'fsq_id': '5b5f4e4760d11b003954e4aa'}, 
            {'name': '녹두장군 전봉준', 'lat': 37.569919, 'lon': 126.982541, 'categories': ['Historic and Protected Site'], 'fsq_id': '5b614f85b9ac38002c39bcfd'}, 
            {'name': '의금부 터', 'lat': 37.57054, 'lon': 126.983082, 'categories': ['Historic and Protected Site'], 'fsq_id': '4f6fdefbe4b0541c63a2b259'}, 
            {'name': '독립신문사 터', 'lat': 37.563647, 'lon': 126.972035, 'categories': ['Historic and Protected Site'], 'fsq_id': '619dd85fc014bc2e8db0aa84'}, 
            {'name': '숭례문 대장간', 'lat': 37.560415, 'lon': 126.975674, 'categories': ['Historic and Protected Site'], 'fsq_id': '4f18eab6e4b0808f61b46b20'}, 
            {'name': '공평빌딩 기초 H빔', 'lat': 37.571883, 'lon': 126.983514, 'categories': ['Historic and Protected Site'], 'fsq_id': '4c711c25d274b60ca07edb0d'}, 
            {'name': '소덕문 터', 'lat': 37.562335, 'lon': 126.97182, 'categories': ['Historic and Protected Site'], 'fsq_id': '4e2ba97f18a80bb0585c8b8b'}, 
            {'name': '윤선도선생 집터', 'lat': 37.56433, 'lon': 126.986207, 'categories': ['Historic and Protected Site'], 'fsq_id': '585f3a047d0f6d0aa27dddb4'}, 
            {'name': '삼일독립선언유적지', 'lat': 37.571836, 'lon': 126.984409, 'categories': ['Historic and Protected Site'], 'fsq_id': '4e4106e6c65b4f2fdeb14410'}, 
            {'name': '사헌부 문 터 및 육조거리 배 수로', 'lat': 37.573731, 'lon': 126.976469, 'categories': ['Historic and Protected Site'], 'fsq_id': '639005807164e66f7c5d4d8d'}, 
            {'name': '돈의문 터', 'lat': 37.568105, 'lon': 126.968713, 'categories': ['Historic and Protected Site'], 'fsq_id': '4cac3cd7a6e08cfa6b5ea994'}, 
            {'name': 'Samil Gate (삼일문)', 'lat': 37.570278, 'lon': 126.988512, 'categories': ['Historic and Protected Site'], 'fsq_id': '4ce4fe864303f04dc96a96b8'}, 
            {'name': '경희궁 숭정전', 'lat': 37.571357, 'lon': 126.968071, 'categories': ['Historic and Protected Site'], 'fsq_id': '4be69587910020a1a372d414'}, 
            {'name': '탑골공원 팔각정', 'lat': 37.571233, 'lon': 126.988273, 'categories': ['Historic and Protected Site'], 'fsq_id': '4df56f8c483bdb5e137b14a8'}, 
            {'name': 'Ten-Story Stone Pagoda of Wongaksa Temple Site (원각사지 십층석탑)', 'lat': 37.571522, 'lon': 126.988297, 'categories': ['Historic and Protected Site'], 'fsq_id': '4dec50ead4c00071b853a1b1'}, 
            {'name': '신간회 본부 터', 'lat': 37.570283, 'lon': 126.989142, 'categories': ['Historic and Protected Site'], 'fsq_id': '5072a642e4b0df2cc8431c8f'}, 
            {'name': 'Project-Research-spot3', 'lat': 37.575357, 'lon': 126.98273, 'categories': ['Historic and Protected Site'], 'fsq_id': '4e8e9e2b5c5c312991210116'}, 
            {'name': '고당기념관', 'lat': 37.565447, 'lon': 126.990096, 'categories': ['Cultural Center', 'Historic and Protected Site'], 'fsq_id': '4efb134ab63446a50bed6008'}, 
            {'name': '대한출판문화협회', 'lat': 37.576439, 'lon': 126.979878, 'categories': ['Publisher', 'Organization', 'Historic and Protected Site'], 'fsq_id': '4eb227498b815ab741baf62d'}, 
            {'name': '옛 중앙청 터', 'lat': 37.576656, 'lon': 126.976831, 'categories': ['Historic and Protected Site'], 'fsq_id': '5bbcbe801543c7002cb007be'}, 
            {'name': '서북학회 터', 'lat': 37.57374, 'lon': 126.987381, 'categories': ['Historic and Protected Site'], 'fsq_id': '63e61c64e95e6265de34a0cf'}, 
            {'name': '경운동 민병옥 가옥', 'lat': 37.574697, 'lon': 126.985938, 'categories': ['Historic and Protected Site'], 'fsq_id': '5d69ffc3e4330c0008562df3'}]
poi_score =  [{'name': '한라수목원', 'latitude': 33.469324, 'longitude': 126.492715, 'score': 7.857142857142857, 'category': ['Botanical Garden', 'Garden', 'Nature Preserve', 'Park', 'Food and Beverage Retail']}]

import csv
import json
from collections import defaultdict

def add_path(tree, path):
    n = tree["Category"]
    for p in path:
        if not p in n:
            n.append(p)
        if not p in tree:
            tree[p] = []
        n = tree[p]

def id_mapping(id_map, path, id):
    id_map[path[-1]] = id

tree = {"Category":[]}
id_map = {}

with open("public/cat.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        category_path = row[1].strip().split(" > ")
        add_path(tree, category_path)
        id_mapping(id_map, category_path,row[0])

with open('public/category_tree.json',"w",encoding="utf-8") as f:
    json.dump(tree,f,indent=2,ensure_ascii=False)

with open('public/id_map.json',"w",encoding="utf-8") as f:
    json.dump(id_map, f, indent=2, ensure_ascii=False)