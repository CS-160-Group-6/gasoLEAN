import React from 'react'
import { View, Text, SafeAreaView, Image, FlatList, Dimensions } from 'react-native'
import { LineChart } from "react-native-gifted-charts";
import { icon } from '@/constants/icon';
import { car, history } from "../../data/dummy.js"
import CarDisplay from '@/components/carDisplay';
import CarStatsRow from '@/components/carStatsRow';


const DrivingHistory = () => {
  const minRequired = 2; // users can see records only if they meet this threshold

  return (
    <SafeAreaView className='flex-1'>
      <Text className="text-center font-bold border-t-2 mx-6 py-2">
        Driving History
      </Text>

      <View className='px-6'>
        <FlatList
          keyExtractor={(item) => item.id.toString()}
          showsVerticalScrollIndicator={false}
          data={history.length < minRequired ? [] : history}
          ListHeaderComponent={ // this is always shown
            <View>
              <CarDisplay car={car} />
              <View className='w-5/6 mx-auto mt-2 overflow-hidden'>
                <CarStatsRow stats={{
                  "Distance travelled (mi)":
                    history.length < minRequired ? "N/A" : car.distance,
                  "Fuel consumed (gallons)":
                    history.length < minRequired ? "N/A" : car.gallons,
                  "Average fuel rate (mpg)":
                    history.length < minRequired ? "N/A" : (car.distance / car.gallons).toFixed(2)
                }} />
              </View>
              <Text className='text-lg font-semibold mb-2'>Records</Text>
            </View>
          }

          renderItem={({ item }) =>  // no records to render if threshold not met (data = [])
            <View className='mb-4'>
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

          ListFooterComponent={history.length < minRequired ?
            <Text className='text-sm'>Please continue driving so we have enough initial data. Accuracy improves the more you drive!</Text> : <View className='my-6' />}
        />
      </View>
    </SafeAreaView >
  )
}

export default DrivingHistory