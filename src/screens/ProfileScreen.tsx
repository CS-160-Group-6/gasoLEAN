"use client"

import { useContext } from "react"
import { View, Text, StyleSheet, Image, ScrollView, TouchableOpacity } from "react-native"
import { SafeAreaView } from "react-native-safe-area-context"
import { AuthContext } from "../context/AuthContext"
import CarDetails from "../components/CarDetails"
import Icon from "react-native-vector-icons/MaterialCommunityIcons"

const ProfileScreen = ({ navigation }) => {
  const { user, logout } = useContext(AuthContext)

  const handleLogout = () => {
    logout()
    navigation.navigate("Login")
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollView}>
        <View style={styles.profileHeader}>
          <View style={styles.profileImageContainer}>
            <Image source={require("../assets/profile-placeholder.png")} style={styles.profileImage} />
          </View>

          <Text style={styles.userName}>{user?.name || "John Doe"}</Text>
          <Text style={styles.userEmail}>{user?.email || "john.doe@example.com"}</Text>

          <TouchableOpacity style={styles.editProfileButton}>
            <Text style={styles.editProfileText}>Edit Profile</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.sectionContainer}>
          <View style={styles.sectionHeader}>
            <Icon name="car" size={24} color="black" />
            <Text style={styles.sectionTitle}>My Vehicles</Text>
          </View>

          <CarDetails
            car={{
              name: "My Primary Car",
              make: "Toyota",
              model: "Camry",
              year: "2020",
              color: "Silver",
              fuelType: "Gasoline",
              licensePlate: "ABC-1234",
            }}
          />

          <TouchableOpacity style={styles.addCarButton}>
            <Icon name="plus" size={20} color="#007AFF" />
            <Text style={styles.addCarText}>Add Another Vehicle</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.sectionContainer}>
          <View style={styles.sectionHeader}>
            <Icon name="history" size={24} color="black" />
            <Text style={styles.sectionTitle}>Recent Scans</Text>
          </View>

          <View style={styles.emptyStateContainer}>
            <Icon name="car-search" size={50} color="#ccc" />
            <Text style={styles.emptyStateText}>No recent scans</Text>
            <Text style={styles.emptyStateSubtext}>Connect your OBD scanner to get started</Text>
          </View>
        </View>

        <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
          <Text style={styles.logoutButtonText}>Logout</Text>
        </TouchableOpacity>
      </ScrollView>
    </SafeAreaView>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "white",
  },
  scrollView: {
    padding: 20,
  },
  profileHeader: {
    alignItems: "center",
    marginBottom: 30,
  },
  profileImageContainer: {
    width: 100,
    height: 100,
    borderRadius: 50,
    overflow: "hidden",
    marginBottom: 15,
    borderWidth: 3,
    borderColor: "#f0f0f0",
  },
  profileImage: {
    width: "100%",
    height: "100%",
  },
  userName: {
    fontSize: 22,
    fontWeight: "bold",
    color: "black",
  },
  userEmail: {
    fontSize: 16,
    color: "#666",
    marginTop: 5,
  },
  editProfileButton: {
    marginTop: 15,
    paddingVertical: 8,
    paddingHorizontal: 20,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: "#007AFF",
  },
  editProfileText: {
    color: "#007AFF",
    fontSize: 14,
    fontWeight: "500",
  },
  sectionContainer: {
    marginBottom: 25,
    backgroundColor: "#f9f9f9",
    borderRadius: 12,
    padding: 15,
  },
  sectionHeader: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 15,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: "600",
    color: "black",
    marginLeft: 10,
  },
  addCarButton: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    marginTop: 15,
    paddingVertical: 10,
  },
  addCarText: {
    color: "#007AFF",
    marginLeft: 5,
    fontSize: 16,
  },
  emptyStateContainer: {
    alignItems: "center",
    padding: 20,
  },
  emptyStateText: {
    fontSize: 16,
    fontWeight: "500",
    color: "#666",
    marginTop: 10,
  },
  emptyStateSubtext: {
    fontSize: 14,
    color: "#999",
    marginTop: 5,
    textAlign: "center",
  },
  logoutButton: {
    backgroundColor: "#f0f0f0",
    borderRadius: 8,
    padding: 15,
    alignItems: "center",
    marginTop: 20,
  },
  logoutButtonText: {
    color: "#FF3B30",
    fontSize: 16,
    fontWeight: "600",
  },
})

export default ProfileScreen
