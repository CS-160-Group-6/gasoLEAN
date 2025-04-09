import { NavigationContainer } from "@react-navigation/native"
import { createStackNavigator } from "@react-navigation/stack"
import { SafeAreaProvider } from "react-native-safe-area-context"
import LoginScreen from "./src/screens/LoginScreen"
import ProfileScreen from "./src/screens/ProfileScreen"
import { AuthProvider } from "./src/context/AuthContext"

const Stack = createStackNavigator()

export default function App() {
  return (
    <SafeAreaProvider>
      <AuthProvider>
        <NavigationContainer>
          <Stack.Navigator
            initialRouteName="Login"
            screenOptions={{
              headerStyle: {
                backgroundColor: "white",
              },
              headerTintColor: "black",
              headerTitleStyle: {
                fontWeight: "bold",
              },
              cardStyle: { backgroundColor: "white" },
            }}
          >
            <Stack.Screen name="Login" component={LoginScreen} options={{ headerShown: false }} />
            <Stack.Screen name="Profile" component={ProfileScreen} options={{ title: "My Profile" }} />
          </Stack.Navigator>
        </NavigationContainer>
      </AuthProvider>
    </SafeAreaProvider>
  )
}
