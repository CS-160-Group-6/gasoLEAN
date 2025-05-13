import { View, Text, Image } from "react-native";
import { images } from '@/constants/images';

function CarDisplay({ car }) {
    return (
        <View className='justify-center items-start'>
            <Text className='bg-black text-white px-4 py-1 rounded-xl'>
                {car.year || "Car info needed"}
            </Text>
            <Text className='text-3xl tracking-wider'>
                {car.make} {car.model || "Set up on tracking page"}
            </Text>
            <Image source={images.defaultCar} resizeMode='contain' className='h-44 w-5/6 mx-auto mt-3' />
        </View>
    )
}

export default CarDisplay;