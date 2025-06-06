import { View, Text, Image, ImageBackground, _View } from 'react-native'
import { Redirect, Tabs } from 'expo-router'
import { images } from '@/constants/images';
import { icon } from '@/constants/icon'
import { ClerkProvider, useAuth } from '@clerk/clerk-expo';

const TabIcon = ({ focused, icon, title }: { focused: boolean; icon: any; title: string }) => {

  if (focused) {
    return (
      <>
        <ImageBackground
          source={images.highlight}
          className="flex flex-row flex-1 h-14 w-[135px] justify-center items-center"
          resizeMode="stretch"
        >
          <Image source={icon} tintColor='#151312' className="size-5" />
          <Text className="text-secondary text-base font-semibold ml-2">{title}</Text>
        </ImageBackground>
      </>
    )
  }
  return (
    <View className="size-full justify center items-center mt-4">
      <Image source={icon} tintColor="#A8B5DB" className="size-5" />
    </View>
  )

}

const _Layout = () => {
  const { isSignedIn, isLoaded } = useAuth();

  if (!isLoaded) return null; // avoid flicker
  // if (!isSignedIn) {
  //   return <Redirect href="/(auth)/sign-in" />;
  // }

  return (
    <Tabs
      screenOptions={{
        tabBarShowLabel: false,
        tabBarItemStle: {
          width: '100%',
          height: '100%',
          justifyContent: 'center',
          alignItems: 'center',
        }

      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: 'Home',
          headerShown: false,
          tabBarIcon: ({ focused }: { focused: boolean }) => (
            <TabIcon
              focused={focused}
              icon={icon.car}
              title="Track"
            />
          )
        }}
        redirect={!isSignedIn} // added after changing authentication
      />
      <Tabs.Screen
        name="drivingHistory"
        options={{
          title: 'Driving History',
          headerShown: false,
          tabBarIcon: ({ focused }: { focused: boolean }) => (
            <TabIcon focused={focused}
              icon={icon.chart}
              title="History"
            />
          )
        }}
        redirect={!isSignedIn} // added after changing authentication
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: 'Profile',
          headerShown: false,
          tabBarIcon: ({ focused }: { focused: boolean }) => (
            <TabIcon
              focused={focused}
              icon={icon.profile}
              title="profile"
            />
          )

        }}
        redirect={!isSignedIn} // added after changing authentication
      />
    </Tabs>
  )
}

export default _Layout