from components.user_data import UserData
from components.plan_data import TravelPlan, DayPlan, Visiting

def printUserData(user_data:UserData):
    print("printing user data...")
    print('location: ',user_data.location, ' start: ',user_data.duration.start, ' end: ',user_data.duration.end, ' companions: ',user_data.companions)

def printTravelPlan(travel_plen:TravelPlan):
    print("printing travel data...")
    try:
        plan = travel_plen.dayplan[0]
        visit = plan.place_to_visit[0]
        print("place: ", visit.name, " data: ", plan.date)
    except Exception as e:
        print("empty travel plan")