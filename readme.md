1. to test this server, first you have to build required environment
- strongly recommanding to use conda virtual environment
- to test server, run 'pip install -r requirements.txt'

2. move to travel_planner folder and run python BackEnd/run.py
- this will run backend server and can access through port 3000

3. use postman to test this backend server
- 'post' to localhost:3000/api/route_optim or localhost:3000/api/get_pois, add example json to body(select raw, type=json)
- example json object 
'{
  "location": "Seoul",
  "duration": {
    "start": "2025-06-01",
    "end": "2025-06-07"
  },
  "companions": "friends",
  "concept": "foodie adventure",
  "extra_request": "include hidden cafes",
  "kwargs": {
    "filter": {
      "category": "cafe",
      "rating": "4+"
    },
    "prev_map_data": null,
    "poi_file_loc": "example.csv"
  }
}'