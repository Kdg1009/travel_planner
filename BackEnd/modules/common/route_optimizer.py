from components.plan_data import Location, Visiting, DayPlan, TravelPlan

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

def optimize_route(scores: list) -> TravelPlan:
    return sample_travel_plan