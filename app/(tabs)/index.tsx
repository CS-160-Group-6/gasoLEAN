// Import at the top of your file
import React, { useState, useEffect } from 'react';
import { Platform, PermissionsAndroid, Button, View, Text, FlatList, SafeAreaView, Pressable, ScrollView, Image, Dimensions, TextInput } from 'react-native';

import { LineChart } from "react-native-gifted-charts";
import { icon } from '@/constants/icon'
import { images } from '@/constants/images';
import { car, trackingStats } from "../../data/dummy.js"
//import { BleManager, Device } from 'react-native-ble-plx';

//const manager = new BleManager();

const Index = () => {
  const [carData, setCarData] = useState(car);
  const [isTracking, setIsTracking] = useState(false);
  const toggleTracking = () => setIsTracking(prev => !prev);
  const handleCarDataChange = (name, value) => {
    setCarData(prev => ({ ...prev, [name]: value }));
  }

  // data to track how mpg changes overtime?
  // each object = mpg at that given time. Add a label every 5 seconds
  const data = [{ value: 0, label: "0:00" }, { value: 1 }, { value: 4 }, { value: 9 }, { value: 16 }, { value: 25, label: "0:05" }]

  // user hasn't provided their car info, show input form
  if (Object.keys(car).length < 3) {
    return (
      <SafeAreaView className='flex-1'>
        <Text className="text-center font-bold border-t-2 mx-6 py-2">Enter Car Info</Text>
        <ScrollView contentContainerStyle={{ flexGrow: 1 }} className="px-6">
          <Image source={images.defaultCar} resizeMode='contain' className='h-44 w-5/6 mx-auto mt-3' />
          <View className='mt-3 gap-6'>
            <View>
              <Text className='font-bold'>Make</Text>
              <TextInput value={carData?.make || ""}
                onChangeText={text => handleCarDataChange('make', text)}
                className='border-b-2 py-1' />
            </View>
            <View>
              <Text className='font-bold'>Model</Text>
              <TextInput value={carData?.model || ""}
                onChangeText={text => handleCarDataChange('model', text)}
                className='border-b-2 py-1' />
            </View>
            <View>
              <Text className='font-bold'>Year</Text>
              <TextInput keyboardType="numeric" value={carData?.year || ""}
                onChangeText={text => handleCarDataChange('year', text)}
                className='border-b-2 py-1' />
            </View>
          </View>

          {/* todo: store car info to backend (dummy.js in this case) */}
          <Pressable onPress={toggleTracking} className='bg-black py-3 mt-8 rounded-xl'>
            <Text className='text-center text-white text-xl font-semibold'>
              Submit
            </Text>
          </Pressable>
        </ScrollView>
      </SafeAreaView>
    )
  }

  // user provided their car info, show the entire tracking page
  return (
    <SafeAreaView className='flex-1'>
      <Text className="text-center font-bold border-t-2 mx-6 py-2">
        {isTracking ? "Tracking " : "Track"}
        {isTracking && <View className='w-3 h-3 rounded-full bg-red-500' />}
      </Text>
      <ScrollView contentContainerStyle={{ flexGrow: 1 }} className="px-6">
        {/* car info & image */}
        <View className='justify-center items-start'>
          <Text className='bg-black text-white px-4 py-1 rounded-xl'>{car.year}</Text>
          <Text className='text-3xl tracking-wider'>{car.make} {car.model}</Text>
          <Image source={images.defaultCar} resizeMode='contain' className='h-44 w-5/6 mx-auto mt-3' />
        </View>

        {/* if tracking: display tracking stats*/}
        {isTracking && <View className='w-5/6 mx-auto mt-2 overflow-hidden'>
          {/* time elapsed */}
          <View className='flex-row items-center mx-auto gap-4'>
            <Text className='mt-0.5'>Time elapsed</Text>
            <Text className='text-2xl font-semibold'>{trackingStats.elapsed}</Text>
          </View>

          {/* speedometer image + car speed & fuel % */}
          <View className='flex-row gap-10 items-center mx-8 mt-4'>
            <Image source={icon.speedometer} resizeMode='contain' className='w-20 h-20' />
            <View className='flex-1 gap-3'>
              <View className='flex-row justify-between items-center'>
                <Text className='text-sm'>Current {"\n"}speed (mph)</Text>
                <Text className='text-2xl font-semibold'>{trackingStats.speed}</Text>
              </View>
              <View className='flex-row justify-between items-center'>
                <Text className='text-sm'>Fuel %</Text>
                <Text className='text-2xl font-semibold'>{trackingStats.fuelLeft}</Text>
              </View>
            </View>
          </View>

          {/* distance, fuel, mpg */}
          <View className='flex-row gap-3 my-4'>
            <View className='flex-1 gap-1'>
              <Text className='text-sm'>Distance travelled (mi)</Text>
              <Text className='text-2xl font-semibold'>{trackingStats.distance}</Text>
            </View>
            <View className='flex-1 gap-1'>
              <Text className='text-sm'>Fuel consumed (gallons)</Text>
              <Text className='text-2xl font-semibold'>{trackingStats.gallons}</Text>
            </View>
            <View className='flex-1 gap-1'>
              <Text className='text-sm'>Average fuel rate (mpg)</Text>
              <Text className='text-2xl font-semibold'>
                {(trackingStats.distance / trackingStats.gallons).toFixed(2)}
              </Text>
            </View>
          </View>

          {/* <Text className='text-center mt-6 mb-2'>Mpg over time</Text> */}
          <LineChart data={data} width={Dimensions.get('window').width} height={125} noOfSections={4} spacing={40} xAxisLabelTextStyle={{ fontSize: 10 }} />
        </View>}

        {/* tracking button */}
        <Pressable onPress={toggleTracking} className='bg-black py-3 mt-4 rounded-xl'>
          <Text className='text-center text-white text-xl font-semibold'>
            {isTracking ? "Stop" : "Start"} tracking
          </Text>
        </Pressable>

        {/* if not tracking: display stats that show how much user is contributing to the environment */}
        {!isTracking && <View className='w-5/6 mx-auto mt-6'>
          <Text className='text-center'>Since using this app, you've saved</Text>
          {/* gas station image + fuel & money saved */}
          <View className='flex-row gap-6 items-center'>
            <Image source={icon.gasStation} resizeMode='contain' className='w-32 h-32' />
            <View className='flex-1 gap-3'>
              <View className='flex-row justify-between items-center'>
                <Text className='text-sm'>Fuel {"\n"}(gallons)</Text>
                <Text className='text-2xl font-semibold'>2.35</Text>
              </View>
              <View className='flex-row justify-between items-center'>
                <Text className='text-sm'>Dollars ($)</Text>
                <Text className='text-2xl font-semibold'>9999.5</Text>
              </View>
            </View>
          </View>

          {/* environmental friendly stats */}
          <Text className='text-center'>This is equivalent to</Text>
          <View className='flex-row gap-3 mt-6'>
            <View className='flex-1 gap-1'>
              <Text className='text-sm'>CO2 emission saved (lb)</Text>
              <Text className='text-2xl font-semibold'>
                <Image source={icon.leaf} className='w-4 h-4' /> 1.2
              </Text>
            </View>
            <View className='flex-1 gap-1'>
              <Text className='text-sm'>Trees {"\n"}planted</Text>
              <Text className='text-2xl font-semibold'>
                <Image source={icon.tree} className='w-4 h-4' /> 4
              </Text>
            </View>
            <View className='flex-1 gap-1'>
              <Text className='text-sm'>Improved avg. fuel rate (mpg)</Text>
              <Text className='text-2xl font-semibold'>
                <Image source={icon.arrowUp} className='w-4 h-4' /> 1.23
              </Text>
            </View>
          </View>
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