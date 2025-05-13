import React from 'react'
import { View, Text, SafeAreaView, ScrollView, Image, FlatList, Dimensions } from 'react-native'
import { LineChart } from "react-native-gifted-charts";
import { icon } from '@/constants/icon';
import { images } from '@/constants/images';
import { car, history } from "../../data/dummy.js"


const DrivingHistory = () => {
  const minRequired = 1;

  return (
    <SafeAreaView className='flex-1'>
      <Text className="text-center font-bold border-t-2 mx-6 py-2">
        Driving History
      </Text>

      <View className='px-6'>
        <FlatList
          ListHeaderComponent={<View>
            <View className='justify-center items-start'>
              <Text className='bg-black text-white px-4 py-1 rounded-xl'>{car.year}</Text>
              <Text className='text-3xl tracking-wider'>{car.make} {car.model}</Text>
              <Image source={images.defaultCar} resizeMode='contain' className='h-44 w-5/6 mx-auto mt-3' />
            </View>

            <View className='w-5/6 mx-auto mt-2 overflow-hidden'>
              {/* distance, fuel, mpg */}
              <View className='flex-row gap-3 my-4'>
                <View className='flex-1 gap-1'>
                  <Text className='text-sm'>Distance travelled (mi)</Text>
                  <Text className='text-2xl font-semibold'>{car.distance}</Text>
                </View>
                <View className='flex-1 gap-1'>
                  <Text className='text-sm'>Fuel consumed (gallons)</Text>
                  <Text className='text-2xl font-semibold'>{car.gallons}</Text>
                </View>
                <View className='flex-1 gap-1'>
                  <Text className='text-sm'>Average fuel rate (mpg)</Text>
                  <Text className='text-2xl font-semibold'>
                    {(car.distance / car.gallons).toFixed(2)}
                  </Text>
                </View>
              </View>
            </View>
            <Text className='text-lg font-semibold mb-2'>Records</Text>
          </View>}
          keyExtractor={(item) => item.id.toString()}
          showsVerticalScrollIndicator={false}
          data={history.length < minRequired ? [] : history}
          ListFooterComponent={history.length < minRequired ? <Text className='text-sm'>Please continue driving so we have enough initial data. Accuracy improves the more you drive!</Text> : <View className='my-8' />}
          ItemSeparatorComponent={() => <View style={{ height: 15 }} />}
          renderItem={({ item }) =>
            <View>
              {/* date & destination */}
              <View className=' bg-black px-3 py-1 rounded-xl'>
                <Text className='absolute text-sm text-white font-bold ml-3 mt-1'>{item.date}</Text>
                <View className='flex-row mx-auto gap-2'>
                  <Image source={icon.locationPin} className='w-4 h-4 mt-0.5' />
                  <Text className='text-sm text-white font-bold'>{item.destination}</Text>
                </View>
              </View>


              {/* stats about the drive */}
              <View className='flex-row items-center justify-around mt-1 mb-3'>
                <Text><Text className='font-semibold'>{item.miles.toFixed(2)}</Text> miles</Text>
                <Text><Text className='font-semibold'>{item.gallons.toFixed(2)}</Text> gallons</Text>
                <Text><Text className='font-semibold text-2xl'>{item.mpg.toFixed(2)}</Text> mpg</Text>
              </View>


              {/* <Text className='text-center mt-6 mb-2'>Mpg over time</Text> */}
              <LineChart data={item.data} width={Dimensions.get('window').width} height={125} noOfSections={4} spacing={40} xAxisLabelTextStyle={{ fontSize: 10 }} />
            </View>}
        />
      </View>
    </SafeAreaView >
  )
}

export default DrivingHistory