import {
  View,
  Text,
  SafeAreaView,
  Pressable,
  ScrollView,
  Image
} from 'react-native';
import React from 'react';
import { useClerk, useAuth, useUser } from '@clerk/clerk-expo';

const Profile = () => {
  const { signOut } = useAuth();
  const { user } = useUser();

  const handleSignOut = async () => {
    try {
      await signOut();
    } catch (err) {
      console.error(JSON.stringify(err, null, 2));
    }
  };

  return (
    <SafeAreaView className="flex-1 bg-gray-250">
      <ScrollView contentContainerStyle={{ flexGrow: 1 }} className="px-6 pt-6">
        <Text className="text-center font-bold text-3xl mb-6">Profile</Text>

        {user && (
          <View className="items-center mb-10">
            <Image
              source={{ uri: user.imageUrl }}
              className="w-28 h-28 rounded-full mb-4"
            />
            <Text className="text-xl font-semibold mb-1">{user.fullName}</Text>
            <Text className="text-gray-500">{user.primaryEmailAddress?.emailAddress}</Text>
          </View>
        )}

        {/* Fill space to push button to bottom */}
        <View className="flex-1" />

        <Pressable
          className="bg-black py-4 rounded-full"
          onPress={handleSignOut}
        >
          <Text className="text-center text-white text-xl font-semibold">
            Sign Out
          </Text>
        </Pressable>
      </ScrollView>
    </SafeAreaView>
  );
};

export default Profile;
