// types/trip.ts
export interface DataPoint {
    time: string;
    speed: number;
    distance: number;
    fuelUsed: number;
}

export interface Trip {
    id?: string;
    startTime: string;
    endTime?: string;
    dataPoints: DataPoint[];
}