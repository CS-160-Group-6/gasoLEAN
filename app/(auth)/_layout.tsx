import React from 'react';
import { Stack } from 'expo-router';


export default function AuthRoutesLayout() {

    return (
        <Stack
            screenOptions={{
                headerStyle: {
                    backgroundColor: '#6c47ff',
                },
                headerTintColor: '#fff',
                headerBackTitle: 'Back',
            }}>
            <Stack.Screen
                name="sign-in"
                options={{
                    headerTitle: 'Clerk Auth App',
                }}></Stack.Screen>
            <Stack.Screen
                name="sign-up"
                options={{
                    headerTitle: 'Create Account',
                }}></Stack.Screen>

            {/* reset password: TBD */}
            {/* <Stack.Screen
                name="reset"
                options={{
                    headerTitle: 'Reset Password',
                }}></Stack.Screen> */}
        </Stack>
    );
}