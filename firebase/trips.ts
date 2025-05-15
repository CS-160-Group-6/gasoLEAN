// firebase/trips.ts
import { db } from './config';
import { addDoc, collection, serverTimestamp } from 'firebase/firestore';

export const addDataPoint = async (
    userId: string,
    tripId: string,
    data: { speed: number; distance: number; fuelUsed: number }
) => {
    const ref = collection(db, 'users', userId, 'trips', tripId, 'dataPoints');
    await addDoc(ref, {
        ...data,
        time: new Date().toISOString(),
        timestamp: serverTimestamp(),
    });
};

export const startTrip = async (userId: string) => {
    const ref = collection(db, 'users', userId, 'trips');
    const doc = await addDoc(ref, {
        startTime: serverTimestamp(),
        dataPoints: [],
    });
    return doc.id;
};