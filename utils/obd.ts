import BleManager from "react-native-ble-manager";

export const sendOBDCommand = async (
    command: string,
    bleService: {
        peripheralId: string;
        serviceId: string;
        transfer: string;
    }
) => {
    const data = Array.from(new TextEncoder().encode(command + "\r"));
    await BleManager.write(
        bleService.peripheralId,
        bleService.serviceId,
        bleService.transfer,
        data,
        255
    );
};

export const readOBDResponse = async (
    bleService: {
        peripheralId: string;
        serviceId: string;
        receive: string;
    }
): Promise<string> => {
    const raw = await BleManager.read(
        bleService.serviceId,
        bleService.peripheralId,
        bleService.receive
    );
    return new TextDecoder().decode(Uint8Array.from(raw));
};

export const parseSpeed = (response: string): number => {
    const parts = response.trim().split(" ");
    return parseInt(parts[2], 16); // e.g. "41 0D 1A" → 26 km/h
};

export const parseFuelLevel = (response: string): number => {
    const parts = response.trim().split(" ");
    return Math.round((parseInt(parts[2], 16) * 100) / 255);
};

export const parseDistance = (response: string): number => {
    const parts = response.trim().split(" ");
    return (parseInt(parts[2], 16) << 8) + parseInt(parts[3], 16); // in km
};