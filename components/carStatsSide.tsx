import { Text, View } from "react-native";

function CarStatsSide({ image, stats, containerStyle }) {
    const iterableStats = Object.entries(stats);

    return (
        <View className={containerStyle}>
            {image}
            <View className='flex-1 gap-3'>
                {iterableStats.map(([label, value]) =>
                    <View key={label} className='flex-row justify-between items-center'>
                        <Text className='text-sm'>{label}</Text>
                        <Text className='text-2xl font-semibold'>{value}</Text>
                    </View>)}
            </View>
        </View>
    )
}

export default CarStatsSide;