// Import at the top of your file
import React, { useState, useEffect } from 'react';
import { Platform, PermissionsAndroid, Button, View, Text, FlatList, SafeAreaView, Pressable, ScrollView, Image } from 'react-native';
import { images } from '@/constants/images';
import { car, trackingStats } from "../../data/dummy.js"
//import { BleManager, Device } from 'react-native-ble-plx';

//const manager = new BleManager();

const Index = () => {
  const [isTracking, setIsTracking] = useState(false);
  const toggleTracking = () => setIsTracking(prev => !prev);

  return (
    <SafeAreaView className='flex-1'>
      <ScrollView contentContainerStyle={{ flexGrow: 1 }} className="px-6 pt-6">
        <Text className="text-center font-bold border-t-2 py-2">
          {isTracking ? "Tracking " : "Track"}
          {isTracking && <View className='w-3 h-3 bg-red-500 rounded-full' />}
        </Text>

        {/* car info & image */}
        <View className='justify-center items-start'>
          <Text className='bg-black text-white px-4 py-1 rounded-xl'>{car.year}</Text>
          <Text className='text-3xl tracking-wider'>{car.make} {car.model}</Text>
          <Image source={images.defaultCar} resizeMode='contain' className='h-44 w-5/6 mx-auto mt-3' />
        </View>

        {/* display tracking stats (if tracking)*/}
        {isTracking && <View className='w-5/6 mx-auto mt-2'>
          {/* time elapsed */}
          <View className='flex-row items-center mx-auto gap-4'>
            <Text className='mt-0.5'>Time elapsed</Text>
            <Text className='text-2xl font-semibold'>{trackingStats.elapsed}</Text>
          </View>

          {/* distance, fuel, mpg */}
          <View className='flex-row gap-3 mt-4'>
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
        </View>}

        {/* tracking button */}
        <Pressable onPress={toggleTracking} className='bg-black py-3 mt-6 rounded-xl'>
          <Text className='text-center text-white text-xl font-semibold'>
            {isTracking ? "Stop" : "Start"} tracking
          </Text>
        </Pressable>
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