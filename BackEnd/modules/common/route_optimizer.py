from components.plan_data import Location, Visiting, DayPlan, TravelPlan
from components.user_data import Duration
from datetime import datetime, timedelta
from typing import List
# dummy function

sample_travel_plan = TravelPlan(
    dayplan=[
        DayPlan(
            date="2025-05-21",
            place_to_visit=[
                Visiting(
                    name="Gyeongbokgung Palace",
                    location=Location(latitude="37.5796", longitude="126.9770")
                ),
                Visiting(
                    name="Bukchon Hanok Village",
                    location=Location(latitude="37.5826", longitude="126.9830")
                )
            ]
        ),
        DayPlan(
            date="2025-05-22",
            place_to_visit=[
                Visiting(
                    name="N Seoul Tower",
                    location=Location(latitude="37.5512", longitude="126.9882")
                ),
                Visiting(
                    name="Myeongdong Shopping Street",
                    location=Location(latitude="37.5637", longitude="126.9827")
                )
            ]
        )
    ]
)
# ---- optimize_helper ----
# return list of dates within duration.start and duration.end
def get_days(duration: Duration) -> List[str]:
    start_date = datetime.strptime(duration.start, "%Y-%m-%d")
    end_date = datetime.strptime(duration.end, "%Y-%m-%d")
    delta = end_date - start_date

    return [
        (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range(delta.days + 1)
    ]

def optimize_route(duration: Duration, scores: list) -> TravelPlan:
    return sample_travel_plan