
import { View, Text, TextInput, Pressable } from "react-native"
import { useState } from "react";

function CarAddForm() {
    const [carData, setCarData] = useState({ make: "", model: "", year: "" });
    const handleCarDataChange = (name, value) => {
        setCarData(prev => ({ ...prev, [name]: value }));
    }

    const handleSubmit = async () => {
        // Handle form submission logic here    
        try {
            const response = await fetch('https://dummyjson.com/products/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(carData),
            });
            const data = await response.json();
            console.log(data); //print success message prolly
        } catch (error) {
            console.error('Error:', error);
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
                <Pressable className='bg-black py-3 mt-4 rounded-xl' onPress={handleSubmit}>
                    <Text className='text-center text-white text-xl font-semibold'>
                        Submit
                    </Text>
                </Pressable>
            </View>
        )
    }

    export default CarAddForm
