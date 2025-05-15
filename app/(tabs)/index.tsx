import ConnectedState from "@/components/bluetooth/connected-state";
import DisconnectedState from "@/components/bluetooth/disconnected-state";
import { PeripheralServices } from "@/types/bluetooth";
import { handleAndroidPermissions } from "@/utils/permissions";
import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, Platform, Alert, Linking, Image, Dimensions, ScrollView, Pressable } from "react-native";
import { car } from "@/data/dummy.js"
import CarAddForm from '@/components/carAddForm';
import CarDisplay from '@/components/carDisplay';
import CarStatsRow from '@/components/carStatsRow';
import CarStatsSide from '@/components/carStatsSide';
import { LineChart } from "react-native-gifted-charts";
import { icon } from '@/constants/icon'
import { images } from '@/constants/images';
import BleManager, {
  BleDisconnectPeripheralEvent,
  BleManagerDidUpdateValueForCharacteristicEvent,
  BleScanCallbackType,
  BleScanMatchMode,
  BleScanMode,
  Peripheral,
} from "react-native-ble-manager";
import { addDataPoint, startTrip } from '@/firebase/trips';
import { addDoc, collection } from "firebase/firestore";
import { useAuth } from "@clerk/clerk-expo";
import { db } from "@/firebase/config";





// console.log("ConnectedState typeof:", typeof ConnectedState); // should be "function"
// console.log("DisconnectedState typeof:", typeof DisconnectedState); // should be "function"

declare module "react-native-ble-manager" {
  interface Peripheral {
    connected?: boolean;
    connecting?: boolean;
  }
}

//time to scan for devices
const SECONDS_TO_SCAN_FOR = 5;
const SERVICE_UUIDS: string[] = [];
const ALLOW_DUPLICATES = true;

const DEVICE_SERVICE_UUID = "0000fff0-0000-1000-8000-00805f9b34fb";
const WRITE_CHARACTERISTIC_UUID = "0000fff2-0000-1000-8000-00805f9b34fb";
const NOTIFY_CHARACTERISTIC_UUID = "0000fff1-0000-1000-8000-00805f9b34fb";

const BluetoothDemoScreen: React.FC = () => {
  const [isScanning, setIsScanning] = useState(false);
  const [peripherals, setPeripherals] = useState(
    new Map<Peripheral["id"], Peripheral>()
  );
  const [isConnected, setIsConnected] = useState(false);
  const [bleService, setBleService] = useState<PeripheralServices | undefined>(
    undefined
  );
  const [isTracking, setIsTracking] = useState(false);
  const [trackingStats, setTrackingStats] = useState({
    elapsed: "00:00:00",
    distance: 123.75,
    gallons: 12.34,
    speed: 54,
    fuelLeft: 32
  })
  const [tripId, setTripId] = useState<string | null>(null);
  const { user } = useAuth();

  const toggleTracking = async () => {
    if (!isTracking) {
      // START TRIP
      const newTripId = await startTrip(user.uid);
      setTripId(newTripId);
    } else {
      // STOP TRIP - you can add endTrip(user.uid, tripId) if you want
      setTripId(null);
    }
    setIsTracking(prev => !prev);
  };

  function parseOBDResponse(text: string) {
    const lines = text.split("\r").map(line => line.trim()).filter(Boolean);

    for (let line of lines) {
      if (line.startsWith("41 ")) {
        const parts = line.split(" ");
        const pid = parts[1];
        const A = parts[2];

        switch (pid) {
          case "0D": // speed
            const speed = parseInt(A, 16);
            console.log("Speed (km/h):", speed);
            return { pid, value: speed };

          case "2F": // fuel %
            const fuel = (parseInt(A, 16) * 100) / 255;
            console.log("Fuel Level (%):", fuel.toFixed(1));
            return { pid, value: fuel };

          case "31": // distance
            const distance = (parseInt(A, 16) * 256) + parseInt(parts[3], 16);
            console.log("Distance (km):", distance);
            return { pid, value: distance };

          // case "0C": // RPM, needs A and B
          //   const B = parts[3];
          //   const rpm = ((parseInt(A, 16) * 256) + parseInt(B, 16)) / 4;
          //   console.log("RPM:", rpm);
          //   return { pid, value: rpm };

          // case "05": // coolant temp
          //   const temp = parseInt(A, 16) - 40;
          //   console.log("Coolant Temp (°C):", temp);
          //   return { pid, value: temp };
        }
      }
    }

    return null;
  }

  useEffect(() => {
    BleManager.start({ showAlert: false })
      .then(() => console.debug("BleManager started."))
      .catch((error: any) =>
        console.error("BleManager could not be started.", error)
      );

    const listeners: any[] = [
      BleManager.onDiscoverPeripheral(handleDiscoverPeripheral),
      BleManager.onStopScan(handleStopScan),
      BleManager.onConnectPeripheral(handleConnectPeripheral),
      BleManager.onDidUpdateValueForCharacteristic(
        handleUpdateValueForCharacteristic
      ),
      BleManager.onDisconnectPeripheral(handleDisconnectedPeripheral),
    ];


    handleAndroidPermissions();

    return () => {
      for (const listener of listeners) {
        listener.remove();
      }
    };
  }, []);

  useEffect(() => {
    let intervalId: NodeJS.Timeout;

    if (isTracking && bleService) {
      intervalId = setInterval(() => {
        sendOBDCommand("010D"); // Speed

        setTimeout(() => {
          sendOBDCommand("012F"); // Fuel Level
        }, 400); // wait 400ms

        // setTimeout(() => {
        //   sendOBDCommand("010C"); // RPM
        // }, 800); // wait another 400ms

        // setTimeout(() => {
        //   sendOBDCommand("0105"); // Coolant Temp
        // }, 1200); // wait another 400ms
      }, 5000);
    }

    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [isTracking, bleService]);

  useEffect(() => {
    const handleNotify = async (
      event: BleManagerDidUpdateValueForCharacteristicEvent
    ) => {
      const raw = event.value;
      const text = new TextDecoder().decode(Uint8Array.from(raw));

      console.log("OBD-II Response:", text);
      const parsedData = parseOBDResponse(text);
      if (parsedData) {
        // console.log("Parsed Data:", parsedData);
        switch (parsedData.pid) {
          case "0D": // Speed
            setTrackingStats(prev => ({ ...prev, speed: parsedData.value }))
            break;
          case "2F": // Fuel Level
            setTrackingStats(prev => ({ ...prev, fuelLeft: parseFloat(parsedData.value.toFixed(2)) }))
            break;
          // case "0C": // RPM
          //   trackingStats.rpm = parsedData.value;
          //   break;
          // case "05": // Coolant Temp
          //   trackingStats.coolantTemp = parsedData.value;
          //   break;
        }
        if (tripId && user) {
          const { speed, distance, gallons } = trackingStats;
          await addDataPoint(user, tripId, {
            speed,
            distance,
            fuelUsed: gallons,
          });
        }
      }
    };

    const listener = BleManager.onDidUpdateValueForCharacteristic(handleNotify);
    return () => listener.remove();
  }, []);



  const handleDisconnectedPeripheral = (
    event: BleDisconnectPeripheralEvent
  ) => {
    console.debug(
      `[handleDisconnectedPeripheral][${event.peripheral}] disconnected.`
    );
    setPeripherals((map) => {
      let p = map.get(event.peripheral);
      if (p) {
        p.connected = false;
        return new Map(map.set(event.peripheral, p));
      }
      return map;
    });
  };

  const handleConnectPeripheral = (event: any) => {
    console.log(`[handleConnectPeripheral][${event.peripheral}] connected.`);
  };

  const handleUpdateValueForCharacteristic = async (
    data: BleManagerDidUpdateValueForCharacteristicEvent
  ) => {
    console.debug(
      `[handleUpdateValueForCharacteristic] received data from '${data.peripheral}' with characteristic='${data.characteristic}' and value='${data.value}====='`
    );
  };

  const handleStopScan = () => {
    setIsScanning(false);
    console.debug("[handleStopScan] scan is stopped.");
  };

  const handleDiscoverPeripheral = (peripheral: Peripheral) => {
    console.debug("[handleDiscoverPeripheral] new BLE peripheral=", peripheral);
    if (!peripheral.name) {
      peripheral.name = "NO NAME";
    }
    setPeripherals((map) => {
      return new Map(map.set(peripheral.id, peripheral));
    });
  };

  const connectPeripheral = async (
    peripheral: Omit<Peripheral, "advertising">
  ) => {
    try {
      if (peripheral) {
        setPeripherals((map) => {
          let p = map.get(peripheral.id);
          if (p) {
            p.connecting = true;
            return new Map(map.set(p.id, p));
          }
          return map;
        });

        await BleManager.connect(peripheral.id);
        console.debug(`[connectPeripheral][${peripheral.id}] connected.`);
        setPeripherals((map) => {
          let p = map.get(peripheral.id);
          if (p) {
            p.connecting = false;
            p.connected = true;
            return new Map(map.set(p.id, p));
          }
          return map;
        });

        // before retrieving services, it is often a good idea to let bonding & connection finish properly
        await sleep(900);
        /* Test read current RSSI value, retrieve services first */
        const peripheralData = await BleManager.retrieveServices(peripheral.id);
        console.log(
          peripheralData.characteristics,
          "peripheralData.characteristics======="
        );
        // ✅ Start notifications on the notify characteristic
        await BleManager.startNotification(
          peripheral.id,
          DEVICE_SERVICE_UUID,
          NOTIFY_CHARACTERISTIC_UUID
        );
        console.log("Notification started for", NOTIFY_CHARACTERISTIC_UUID);

        if (peripheralData.characteristics) {
          const peripheralParameters = {
            peripheralId: peripheral.id,
            serviceId: DEVICE_SERVICE_UUID,
            transfer: WRITE_CHARACTERISTIC_UUID,
            receive: NOTIFY_CHARACTERISTIC_UUID,
          };
          setBleService(peripheralParameters);
          setIsConnected(true);
        }
        setPeripherals((map) => {
          let p = map.get(peripheral.id);
          if (p) {
            return new Map(map.set(p.id, p));
          }
          return map;
        });
        const rssi = await BleManager.readRSSI(peripheral.id);
        if (peripheralData.characteristics) {
          for (const characteristic of peripheralData.characteristics) {
            if (characteristic.descriptors) {
              for (const descriptor of characteristic.descriptors) {
                try {
                  let data = await BleManager.readDescriptor(
                    peripheral.id,
                    characteristic.service,
                    characteristic.characteristic,
                    descriptor.uuid
                  );
                  console.log(
                    `[readDescriptor] Descriptor ${data} for ${peripheral.id} `
                  );
                } catch (error) {
                  console.error(
                    `[connectPeripheral][${peripheral.id}] failed to retrieve descriptor ${descriptor.value} for characteristic ${characteristic.characteristic}:`,
                    error
                  );
                }
              }
            }
          }
        }
        setPeripherals((map) => {
          let p = map.get(peripheral.id);
          if (p) {
            p.rssi = rssi;
            return new Map(map.set(p.id, p));
          }
          return map;
        });
      }
    } catch (error) {
      console.error(
        `[connectPeripheral][${peripheral.id}] connectPeripheral error`,
        error
      );
    }
  };

  const disconnectPeripheral = async (peripheralId: string) => {
    try {
      await BleManager.disconnect(peripheralId);
      setBleService(undefined);
      setPeripherals(new Map());
      setIsConnected(false);
    } catch (error) {
      console.error(
        `[disconnectPeripheral][${peripheralId}] disconnectPeripheral error`,
        error
      );
    }
  };

  function sleep(ms: number) {
    return new Promise<void>((resolve) => setTimeout(resolve, ms));
  }

  const enableBluetooth = async () => {
    try {
      console.debug("[enableBluetooth]");
      await BleManager.enableBluetooth();
    } catch (error) {
      console.error("[enableBluetooth] thrown", error);
    }
  };

  const startScan = async () => {
    const state = await BleManager.checkState();

    console.log(state);

    if (state === "off") {
      if (Platform.OS == "ios") {
        Alert.alert(
          "Enable Bluetooth",
          "Please enable Bluetooth in Settings to continue.",
          [
            { text: "Cancel", style: "cancel" },
            {
              text: "Open Settings",
              onPress: () => {
                Linking.openURL("App-Prefs:Bluetooth");
              },
            },
          ]
        );
      } else {
        enableBluetooth();
      }
    }
    if (!isScanning) {
      setPeripherals(new Map<Peripheral["id"], Peripheral>());
      try {
        console.debug("[startScan] starting scan...");
        setIsScanning(true);
        BleManager.scan(SERVICE_UUIDS, SECONDS_TO_SCAN_FOR, ALLOW_DUPLICATES, {
          matchMode: BleScanMatchMode.Sticky,
          scanMode: BleScanMode.LowLatency,
          callbackType: BleScanCallbackType.AllMatches,
        })
          .then(() => {
            console.debug("[startScan] scan promise returned successfully.");
          })
          .catch((err: any) => {
            console.error("[startScan] ble scan returned in error", err);
          });
      } catch (error) {
        console.error("[startScan] ble scan error thrown", error);
      }
    }
  };

  const sendOBDCommand = async (command: string) => {
    if (!bleService) return;
    const data = Array.from(new TextEncoder().encode(command + "\r"));
    try {
      await BleManager.write(
        bleService.peripheralId,
        bleService.serviceId,
        bleService.transfer,
        data,
        255
      );
      console.log("Sent command:", command);
    } catch (error) {
      console.error("Failed to send command:", command, error);
    }
  };

  const write = async () => {
    const MTU = 255;
    if (bleService) {
      const data = Array.from(new TextEncoder().encode("Hello World"));
      await BleManager.write(
        bleService.peripheralId,
        bleService.serviceId,
        bleService.transfer,
        data,
        MTU
      );
    }
  };

  const read = async () => {
    if (bleService) {
      const response = await BleManager.read(
        bleService.serviceId,
        bleService.peripheralId,
        bleService.receive
      );
      return response;
    }
  };



  const ecoImpactStats = {
    "CO2 emission saved (lb)": <><Image source={icon.leaf} className='w-4 h-4' /> 1.2</>,
    "Trees \nplanted": <><Image source={icon.tree} className='w-4 h-4' /> 4</>,
    "Improved avg. fuel rate (mpg)": <><Image source={icon.arrowUp} className='w-4 h-4' /> 1.23</>
  };

  const savingStats = {
    "Fuel \n(gallons)": 2.35,
    "Dollars ($)": 9999.5
  };

  const liveTrackingStats = {
    "Current \nspeed (mph)": trackingStats.speed,
    "Fuel %": trackingStats.fuelLeft
  }

  const tripSummaryStats = {
    "Distance travelled (mi)": trackingStats.distance,
    "Fuel consumed (gallons)": trackingStats.gallons,
    "Average fuel rate (mpg)": (trackingStats.distance / trackingStats.gallons).toFixed(2)
  }

  // data to track how mpg changes overtime?
  // each object = mpg at that given time. Add a label every 5 seconds
  const data = [{ value: 0, label: "0:00" }, { value: 1 }, { value: 4 }, { value: 9 }, { value: 16 }, { value: 25, label: "0:05" }];


  return (
    <View style={styles.container}>
      <Text style={styles.header}>Bluetooth Demo</Text>
      {!isConnected ? (
        <DisconnectedState
          peripherals={Array.from(peripherals.values())}
          isScanning={isScanning}
          onScanPress={startScan}
          onConnect={connectPeripheral}
        />
      ) : (
        bleService && (
          <>

            <Text className="text-center font-bold border-t-2 mx-6 py-2">
              {isTracking ? "Tracking " : "Track"}
              {isTracking && <View className='w-3 h-3 rounded-full bg-red-500' />}
            </Text>
            <ScrollView contentContainerStyle={{ flexGrow: 1 }} className="px-6">
              <ConnectedState
                bleService={bleService}
                onDisconnect={disconnectPeripheral}
              />
              <CarDisplay car={car} />

              {isTracking &&  //display tracking stats
                <View className='w-5/6 mx-auto mt-2 overflow-hidden'>
                  {/* time elapsed */}
                  <View className='flex-row items-center mx-auto gap-4'>
                    <Text className='mt-0.5'>Time elapsed</Text>
                    <Text className='text-2xl font-semibold'>{trackingStats.elapsed}</Text>
                  </View>
                  {/* speedometer image + car speed & fuel % */}
                  <CarStatsSide containerStyle="flex-row gap-10 items-center mx-8 mt-4"
                    stats={liveTrackingStats}
                    image={<Image source={icon.speedometer} resizeMode='contain' className='w-20 h-20' />}
                  />
                  {/* distance, fuel, mpg */}
                  <CarStatsRow stats={tripSummaryStats} />
                  {/* <Text className='text-center mt-6 mb-2'>Mpg over time</Text> */}
                  <LineChart data={data} width={Dimensions.get('window').width} height={125} noOfSections={4} spacing={40} xAxisLabelTextStyle={{ fontSize: 10 }} />
                </View>}

              {/* tracking button */}
              <Pressable onPress={toggleTracking} className='bg-black py-3 mt-4 rounded-xl'>
                <Text className='text-center text-white text-xl font-semibold'>
                  {isTracking ? "Stop" : "Start"} tracking
                </Text>
              </Pressable>

              {!isTracking &&  //display saving and eco impact stats
                <View className='w-5/6 mx-auto mt-6'>
                  <Text className='text-center'>Since using this app, you've saved</Text>
                  {/* gas station image + fuel & money saved */}
                  <CarStatsSide containerStyle="flex-row gap-6 items-center"
                    stats={savingStats}
                    image={<Image source={icon.gasStation} resizeMode='contain' className='w-32 h-32' />}
                  />
                  {/* environmental friendly stats */}
                  <Text className='text-center mb-2'>This is equivalent to</Text>
                  <CarStatsRow stats={ecoImpactStats} />
                </View>}
            </ScrollView>
          </>
        )

      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f5f5f5",
    paddingVertical: "10%",
    paddingHorizontal: 20,
  },
  header: {
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 16,
    color: "#333",
  },
});

export default BluetoothDemoScreen;