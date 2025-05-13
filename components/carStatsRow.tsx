import { View, Text } from "react-native";

function CarStatsRow({ stats }) {
    const iterableStats = Object.entries(stats);

    return (
        <View className='flex-row gap-3 my-4'>
            {iterableStats.map(([label, value]) =>
                <View key={label} className='flex-1 gap-1'>
                    <Text className='text-sm'>{label}</Text>
                    <Text className='text-2xl font-semibold'>{value}</Text>
                </View>)}
        </View>
    )
}

export default CarStatsRow;