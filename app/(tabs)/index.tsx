// Import at the top of your file
import React, { useState, useEffect } from 'react';
import { Platform, PermissionsAndroid, Button, View, Text, SafeAreaView, Pressable, ScrollView, Image, Dimensions } from 'react-native';

import { LineChart } from "react-native-gifted-charts";
import { icon } from '@/constants/icon'
import { images } from '@/constants/images';
import { car, trackingStats } from "../../data/dummy.js"
import CarAddForm from '@/components/carAddForm';
import CarDisplay from '@/components/carDisplay';
import CarStatsRow from '@/components/carStatsRow';
import CarStatsSide from '@/components/carStatsSide';
//import { BleManager, Device } from 'react-native-ble-plx';

//const manager = new BleManager();

const Index = () => {
  // const [car, setCar] = useState();
  const [isTracking, setIsTracking] = useState(false);
  const toggleTracking = () => setIsTracking(prev => !prev);

  // useEffect(() => {
  //   const fetchCarInfo = async () => {
  //     try {
  //       const response = await fetch('https://dummyjson.com/products/1');
  //       const data = await response.json();
  //       setCar(data);
  //     } catch (error) {
  //       console.error('Error fetching car info:', error);
  //     }
  //   }
  //   fetchCarInfo();
  // }, []);

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


  // user provided their car info, show the entire tracking page
  return (
    <SafeAreaView className='flex-1'>
      <Text className="text-center font-bold border-t-2 mx-6 py-2">
        {isTracking ? "Tracking " : "Track"}
        {isTracking && <View className='w-3 h-3 rounded-full bg-red-500' />}
      </Text>

      <ScrollView contentContainerStyle={{ flexGrow: 1 }} className="px-6">
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

        {/* <DeviceModal
        closeModal={hideModal}
        visible={isModalVisible}
        connectToPeripheral={hideModal}
        devices={[]}
      /> */}
      </ScrollView>
    </SafeAreaView>
  );
}; export default Index