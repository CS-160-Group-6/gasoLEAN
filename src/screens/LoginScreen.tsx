"use client"

import { useState, useContext } from "react"
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  Image,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
} from "react-native"
import { SafeAreaView } from "react-native-safe-area-context"
import { AuthContext } from "../context/AuthContext"

const LoginScreen = ({ navigation }) => {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState("")

  const { login } = useContext(AuthContext)

  const handleLogin = async () => {
    if (!email || !password) {
      setError("Please enter both email and password")
      return
    }

    setIsLoading(true)
    setError("")

    try {
      // In a real app, you would validate credentials with your backend
      await login(email, password)
      navigation.navigate("Profile")
    } catch (err) {
      setError("Invalid email or password")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : "height"} style={styles.keyboardAvoidingView}>
        <ScrollView contentContainerStyle={styles.scrollView}>
          <View style={styles.logoContainer}>
            <Image
              source={require("../assets/car-logo.png")}
              style={styles.logo}
              defaultSource={require("../assets/car-logo.png")}
            />
            <Text style={styles.appTitle}>OBD Car Scanner</Text>
            <Text style={styles.appSubtitle}>Monitor your car's performance</Text>
          </View>

          <View style={styles.formContainer}>
            <Text style={styles.label}>Email</Text>
            <TextInput
              style={styles.input}
              placeholder="Enter your email"
              placeholderTextColor="#666"
              value={email}
              onChangeText={setEmail}
              keyboardType="email-address"
              autoCapitalize="none"
            />

            <Text style={styles.label}>Password</Text>
            <TextInput
              style={styles.input}
              placeholder="Enter your password"
              placeholderTextColor="#666"
              value={password}
              onChangeText={setPassword}
              secureTextEntry
            />

            {error ? <Text style={styles.errorText}>{error}</Text> : null}

            <TouchableOpacity style={styles.loginButton} onPress={handleLogin} disabled={isLoading}>
              <Text style={styles.loginButtonText}>{isLoading ? "Logging in..." : "Login"}</Text>
            </TouchableOpacity>

            <TouchableOpacity style={styles.forgotPassword}>
              <Text style={styles.forgotPasswordText}>Forgot Password?</Text>
            </TouchableOpacity>

            <View style={styles.signupContainer}>
              <Text style={styles.signupText}>Don't have an account? </Text>
              <TouchableOpacity>
                <Text style={styles.signupLink}>Sign Up</Text>
              </TouchableOpacity>
            </View>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "white",
  },
  keyboardAvoidingView: {
    flex: 1,
  },
  scrollView: {
    flexGrow: 1,
    justifyContent: "center",
    padding: 20,
  },
  logoContainer: {
    alignItems: "center",
    marginBottom: 40,
  },
  logo: {
    width: 100,
    height: 100,
    resizeMode: "contain",
  },
  appTitle: {
    fontSize: 24,
    fontWeight: "bold",
    color: "black",
    marginTop: 10,
  },
  appSubtitle: {
    fontSize: 16,
    color: "#666",
    marginTop: 5,
  },
  formContainer: {
    width: "100%",
  },
  label: {
    fontSize: 16,
    fontWeight: "500",
    color: "black",
    marginBottom: 8,
  },
  input: {
    backgroundColor: "#f5f5f5",
    borderRadius: 8,
    padding: 15,
    marginBottom: 20,
    fontSize: 16,
    color: "black",
    borderWidth: 1,
    borderColor: "#e0e0e0",
  },
  loginButton: {
    backgroundColor: "#007AFF",
    borderRadius: 8,
    padding: 15,
    alignItems: "center",
    marginTop: 10,
  },
  loginButtonText: {
    color: "white",
    fontSize: 16,
    fontWeight: "600",
  },
  errorText: {
    color: "red",
    marginBottom: 10,
  },
  forgotPassword: {
    alignSelf: "center",
    marginTop: 20,
  },
  forgotPasswordText: {
    color: "#007AFF",
    fontSize: 14,
  },
  signupContainer: {
    flexDirection: "row",
    justifyContent: "center",
    marginTop: 20,
  },
  signupText: {
    color: "#666",
    fontSize: 14,
  },
  signupLink: {
    color: "#007AFF",
    fontSize: 14,
    fontWeight: "500",
  },
})

export default LoginScreen
