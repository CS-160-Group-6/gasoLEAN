import * as WebBrowser from "expo-web-browser";
import React, { useCallback, useEffect } from "react";
import { Image, Text, View, Button, Pressable, SafeAreaView } from "react-native";
import { Link, router } from "expo-router";
import { useSSO, useUser } from "@clerk/clerk-expo";
import * as AuthSession from 'expo-auth-session'
import * as Linking from "expo-linking";
import { icon } from '@/constants/icon';
import { images } from '@/constants/images';

export const useWarmUpBrowser = () => {
    useEffect(() => {
        // Preloads the browser for Android devices to reduce authentication load time
        // See: https://docs.expo.dev/guides/authentication/#improving-user-experience
        void WebBrowser.warmUpAsync()
        return () => {
            // Cleanup: closes browser when component unmounts
            void WebBrowser.coolDownAsync()
        }
    }, [])
}

WebBrowser.maybeCompleteAuthSession()

const SignInWithOAuth = () => {
    useWarmUpBrowser()

    // Use the `useSSO()` hook to access the `startSSOFlow()` method
    const { startSSOFlow } = useSSO()

    const onPress = useCallback(async () => {
        try {
            // Start the authentication process by calling `startSSOFlow()`
            const { createdSessionId, setActive, signIn, signUp } = await startSSOFlow({
                strategy: 'oauth_google',
                // For web, defaults to current path
                // For native, you must pass a scheme, like AuthSession.makeRedirectUri({ scheme, path })
                // For more info, see https://docs.expo.dev/versions/latest/sdk/auth-session/#authsessionmakeredirecturioptions
                redirectUrl: AuthSession.makeRedirectUri()
            })

            // If sign in was successful, set the active session
            if (createdSessionId) {
                setActive!({ session: createdSessionId })
            } else {
                // If there is no `createdSessionId`,
                // there are missing requirements, such as MFA
                // Use the `signIn` or `signUp` returned from `startSSOFlow`
                // to handle next steps
            }
        } catch (err) {
            // See https://clerk.com/docs/custom-flows/error-handling
            // for more info on error handling
            console.error(JSON.stringify(err, null, 2))
        }
    }, [])

    const { isSignedIn } = useUser();


    useEffect(() => {
        if (isSignedIn) {
            router.replace("./(tabs)/");
        }
    }, [isSignedIn]);

    return (

        <SafeAreaView className="flex-1 bg-gray-100">
            {/* Logo section near the top */}
            <View className="items-center mt-12 flex">
                <Image source={images.gasoLean} className="w-64 h-40 mb-6 mt-40" />
            </View>

            {/* Centered button and text */}
            <View className="flex-1 justify-center items-center px-6">
                <Pressable
                    onPress={onPress}
                    className="flex flex-row items-center justify-center h-14 px-6 py-3 bg-black rounded-full"
                >
                    <Image source={icon.google} className="size-7" />
                    <Text className="text-white text-base font-medium ml-3">
                        Continue with Google
                    </Text>
                </Pressable>

                <Text className="text-black mt-5">
                    Welcome back! Please sign in to continue
                </Text>
            </View>
        </SafeAreaView>
    );
}; export default SignInWithOAuth;