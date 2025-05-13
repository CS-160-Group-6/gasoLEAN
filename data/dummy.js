
// for frontend purposes only
// remove this once we have a backend + a way to connect to OBD2

// distance & gallons here are cumulative 
const car = {
    make: "Toyota",
    model: "Corolla",
    year: 2025,
    distance: 213.75,
    gallons: 21.34
}

// distance & gallons here are for the current trip, read from obd2
const trackingStats = {
    elapsed: "00:00:00",
    distance: 123.75,
    gallons: 12.34,
    speed: 54,
    fuelLeft: 32
}

const history = [
    {
        id: 1,
        date: "3/15",
        destination: "San Jose, CA",
        miles: 12,
        gallons: 0.34,
        mpg: 35.29,
        data: [{ value: 0, label: "0:00" }, { value: 1 }, { value: 4 }, { value: 9 }, { value: 16 }, { value: 25, label: "0:05" }]
    },
    {
        id: 2,
        date: "3/16",
        destination: "San Francisco, CA",
        miles: 12,
        gallons: 1.34,
        mpg: 38.29,
        data: [{ value: 0, label: "0:00" }, { value: 1 }, { value: 4 }, { value: 9 }, { value: 16 }, { value: 25, label: "0:05" }]
    },
]

export { car, trackingStats, history };
