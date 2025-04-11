import React from "react";
import { Stack } from "expo-router";
import { ClerkProvider, SignedIn, SignedOut } from "@clerk/clerk-expo";
import LoginScreen from "../components/index"
import { tokenCache } from "@clerk/clerk-expo/token-cache";
import * as SecureStore from "expo-secure-store";
import './globals.css';

const publishableKey = process.env.EXPO_PUBLIC_CLERK_PUBLISHABLE_KEY!;

if (!publishableKey) {
  throw new Error(
    "Missing Publishable Key. Please set EXPO_PUBLIC_CLERK_PUBLISHABLE_KEY in your .env"
  );
}

export default function RootLayout() {
  return <ClerkProvider publishableKey={publishableKey}>
    <SignedIn>
      <Stack>
        <Stack.Screen
          name="(tabs)"
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="cars/[id]"
          options={{ headerShown: false }}
        />
      </Stack>
    </SignedIn>
    <SignedOut>
      <LoginScreen />
    </SignedOut>
  </ClerkProvider>

}
