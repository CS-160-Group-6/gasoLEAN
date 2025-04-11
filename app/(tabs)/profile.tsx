import { View, Text, Linking, SafeAreaView, TouchableOpacity } from 'react-native'
import React from 'react'
import { useClerk, useAuth } from '@clerk/clerk-expo'

const Profile = () => {
  const { user } = useClerk()
  const { signOut } = useAuth()
  const handleSignOut = async () => {
    try {
      await signOut()
      // Redirect to your desired page

    } catch (err) {
      // See https://clerk.com/docs/custom-flows/error-handling
      // for more info on error handling
      console.error(JSON.stringify(err, null, 2))
    }
  }
  return (
    <SafeAreaView>
      <Text>Profile</Text>
      <TouchableOpacity onPress={handleSignOut}>
        <Text> Signout</Text>
      </TouchableOpacity>
    </SafeAreaView>

  )
}

export default Profile