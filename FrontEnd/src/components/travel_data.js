export class Location {
  constructor(latitude = 0, longitude = 0) {
    this.latitude = latitude;
    this.longitude = longitude;
  }
}

export class Visiting {
  constructor(name = "", location = new Location(), concept = "") {
    this.name = name;
    this.location = location;
    this.concept = concept;
  }
}

export class DayPlan {
  constructor(date = "", place_to_visit = []) {
    this.date = date;
    this.place_to_visit = place_to_visit; // array of Visiting objects
  }
}

export class TravelPlan {
  constructor(dayplan = []) {
    this.dayplan = dayplan; // array of DayPlan objects
  }

  toJSON() {
    return {
      dayplan: this.dayplan.map((day) => ({
        date: day.date,
        place_to_visit: day.place_to_visit.map((visit) => ({
          name: visit.name,
          location: {
            latitude: visit.location.latitude,
            longitude: visit.location.longitude,
          },
          concept: visit.concept,
        })),
      })),
    };
  }
}
