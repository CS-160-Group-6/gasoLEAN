import * as WebBrowser from "expo-web-browser";
import React, { useCallback, useEffect } from "react";
import { Text, View, Button } from "react-native";
import { Link, router } from "expo-router";
import { useSSO, useUser } from "@clerk/clerk-expo";
import * as AuthSession from 'expo-auth-session'
import * as Linking from "expo-linking";

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
                redirectUrl: AuthSession.makeRedirectUri({ scheme: "gasoLean" }),
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
        <View className="flex-1 justify-center align-middle">
            <Button title="Sign in with Google" onPress={onPress} />
        </View>
    );
}; export default SignInWithOAuth;