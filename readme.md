1. to test this server, first you have to build required environment
- strongly recommanding to use conda virtual environment
- to test server, run 'pip install -r requirements.txt'

2. run backend server by 'uvicorn BackEnd/main:app --reload' in travel_planner folder

3. you can access to this server through http://localhost:3000/api/get_pois(get_pois page), and http://localhost:3000/api/route_optim(route_optim page)
- 'post' data in form of user_data / plan_data and you will get results from them