import {
  View,
  Text,
  SafeAreaView,
  Pressable,
  ScrollView,
  Image,
} from 'react-native';
import React from 'react';
import { useAuth, useUser, SignedIn, SignedOut } from '@clerk/clerk-expo';
import { useRouter } from 'expo-router';

const Profile = () => {
  const { signOut } = useAuth();
  const { user } = useUser();
  const router = useRouter();

  const handleSignOut = async () => {
    try {
      await signOut();
      // router.replace('../(auth)/sign-in'); // Redirect to sign-in screen after sign-out (don't need anymore?)
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
}; export default Profile;