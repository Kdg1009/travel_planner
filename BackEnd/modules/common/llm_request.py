from config import OPENAI_API_KEY

# dummy placeholder for LLM interaction

def request_to_llm(request:str)->str:
    return_exmple = "Namsan Tower,37.5512,126.9882,4.7,landmark\n\
Gyeongbokgung Palace,37.5796,126.9770,4.8,history\n\
Myeongdong Shopping Street,37.5639,126.9850,4.5,shopping\n\
Bukchon Hanok Village,37.5826,126.9830,4.6,culture\n\
Dongdaemun Design Plaza,37.5665,127.0094,4.3,architecture\n\
Lotte World Tower,37.5131,127.1025,4.6,skyscraper\n\
COEX Mall,37.5120,127.0580,4.4,shopping\n\
Changdeokgung Palace,37.5794,126.9910,4.7,history\n\
Cheonggyecheon Stream,37.5683,126.9778,4.5,scenery\n\
Insadong,37.5740,126.9855,4.3,crafts\n\
Han River Park,37.5280,126.9326,4.4,relax\n\
Seoul Forest,37.5442,127.0376,4.2,nature\n\
Seoullo 7017,37.5552,126.9696,4.1,walkway\n\
Itaewon,37.5346,126.9949,4.0,nightlife\n\
Hongdae Street,37.5562,126.9236,4.5,youth\n\
Yeouido Hangang Park,37.5282,126.9326,4.3,relax\n\
Seodaemun Prison History Hall,37.5744,126.9573,4.6,history\n\
63 Building,37.5194,126.9405,4.2,observation\n\
Lotte World Adventure,37.5110,127.0980,4.4,amusement\n\
Ewha Womans University,37.5618,126.9463,4.1,architecture\n\
Seoul Tower Plaza,37.5512,126.9882,4.3,observation\n\
Olympic Park,37.5194,127.1210,4.2,sports\n\
K-Star Road,37.5255,127.0361,4.0,kpop\n\
National Museum of Korea,37.5230,126.9804,4.7,museum\n\
War Memorial of Korea,37.5365,126.9770,4.6,history\n\
Namdaemun Market,37.5595,126.9780,4.2,shopping\n\
Gwangjang Market,37.5704,126.9991,4.4,food\n\
Bongeunsa Temple,37.5143,127.0577,4.3,temple\n\
Hangang Bridge,37.5249,126.9534,4.1,bridge\n\
Seoul Museum of Art,37.5637,126.9751,4.3,art\n\
Blue House,37.5869,126.9748,4.5,government\n\
Yangjaecheon Stream,37.4674,127.0372,4.0,nature\n\
Digital Media City,37.5779,126.8904,4.1,media\n\
Samcheong-dong,37.5821,126.9816,4.4,style\n\
Seochon Village,37.5796,126.9692,4.2,retro\n\
Jamsil Baseball Stadium,37.5142,127.0711,4.3,sports\n\
Haneul Park,37.5684,126.8854,4.6,nature\n\
Dongmyo Flea Market,37.5742,127.0399,4.0,vintage\n\
Bamdokkaebi Night Market,37.5282,126.9326,4.5,food\n\
Lotte Mart Seoul Station,37.5547,126.9696,4.2,shopping\n\
Kakao Friends Hongdae,37.5565,126.9228,4.3,goods\n\
Alive Museum Insadong,37.5740,126.9855,4.1,interactive\n\
Seoul Animation Center,37.5521,126.9865,4.0,kids\n\
Hanok Cafe,37.5799,126.9852,4.4,cafe\n\
Jongmyo Shrine,37.5743,126.9947,4.6,heritage\n\
Garosu-gil,37.5194,127.0226,4.2,style\n\
Hangang Moonlight Fountain,37.5206,126.9770,4.3,nightview\n\
Starfield COEX Aquarium,37.5126,127.0606,4.4,aquarium\n\
VR Plus Hongdae,37.5572,126.9230,4.1,virtual\n\
Sky Park,37.5684,126.8854,4.5,grassland\n\
Seoul Grand Park,37.4360,127.0078,4.3,zoo\n\
Gwacheon National Science Museum,37.4469,126.9959,4.5,science\n\
Seoul Botanic Park,37.5699,126.8340,4.4,botanic\n\
Ihwa Mural Village,37.5744,127.0025,4.3,art\n\
Seoul Book Bogo,37.5384,127.0017,4.2,books\n\
Oil Tank Culture Park,37.5695,126.8946,4.1,eco\n\
National Folk Museum of Korea,37.5812,126.9790,4.6,culture\n\
D Museum,37.5452,127.0021,4.4,design\n\
KT&G Sangsangmadang,37.5536,126.9220,4.3,exhibition\n\
Cafe Onion Anguk,37.5770,126.9861,4.5,cafe"
    return return_exmple