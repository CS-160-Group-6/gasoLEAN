import { View, Text, TextInput, Pressable } from "react-native"
import { useState } from "react";

function CarAddForm() {
    const [carData, setCarData] = useState({ make: "", model: "", year: "" });
    const handleCarDataChange = (name, value) => {
        setCarData(prev => ({ ...prev, [name]: value }));
    }

    return (
        <View className='mt-3 gap-6'>
            <View>
                <Text className='font-bold'>Make</Text>
                <TextInput value={carData.make}
                    onChangeText={text => handleCarDataChange('make', text)}
                    className='border-b-2 py-1' />
            </View>
            <View>
                <Text className='font-bold'>Model</Text>
                <TextInput value={carData.model}
                    onChangeText={text => handleCarDataChange('model', text)}
                    className='border-b-2 py-1' />
            </View>
            <View>
                <Text className='font-bold'>Year</Text>
                <TextInput keyboardType="numeric" value={carData.year.toString()}
                    onChangeText={text => handleCarDataChange('year', text)}
                    className='border-b-2 py-1' />
            </View>
            {/* todo: store car info to backend (dummy.js in this case) */}
            <Pressable className='bg-black py-3 mt-4 rounded-xl'>
                <Text className='text-center text-white text-xl font-semibold'>
                    Submit
                </Text>
            </Pressable>
        </View>
    )
}

export default CarAddForm