import type React from "react"
import { View, Text, StyleSheet, TouchableOpacity } from "react-native"
import Icon from "react-native-vector-icons/MaterialCommunityIcons"

interface CarProps {
  car: {
    name: string
    make: string
    model: string
    year: string
    color: string
    fuelType: string
    licensePlate: string
  }
}

const CarDetails: React.FC<CarProps> = ({ car }) => {
  return (
    <View style={styles.carCard}>
      <View style={styles.carHeader}>
        <Text style={styles.carName}>{car.name}</Text>
        <TouchableOpacity>
          <Icon name="pencil" size={20} color="#666" />
        </TouchableOpacity>
      </View>

      <View style={styles.carDetailsGrid}>
        <View style={styles.detailItem}>
          <Text style={styles.detailLabel}>Make</Text>
          <Text style={styles.detailValue}>{car.make}</Text>
        </View>

        <View style={styles.detailItem}>
          <Text style={styles.detailLabel}>Model</Text>
          <Text style={styles.detailValue}>{car.model}</Text>
        </View>

        <View style={styles.detailItem}>
          <Text style={styles.detailLabel}>Year</Text>
          <Text style={styles.detailValue}>{car.year}</Text>
        </View>

        <View style={styles.detailItem}>
          <Text style={styles.detailLabel}>Color</Text>
          <Text style={styles.detailValue}>{car.color}</Text>
        </View>

        <View style={styles.detailItem}>
          <Text style={styles.detailLabel}>Fuel Type</Text>
          <Text style={styles.detailValue}>{car.fuelType}</Text>
        </View>

        <View style={styles.detailItem}>
          <Text style={styles.detailLabel}>License Plate</Text>
          <Text style={styles.detailValue}>{car.licensePlate}</Text>
        </View>
      </View>

      <TouchableOpacity style={styles.scanButton}>
        <Icon name="car-connected" size={18} color="white" />
        <Text style={styles.scanButtonText}>Scan Now</Text>
      </TouchableOpacity>
    </View>
  )
}

const styles = StyleSheet.create({
  carCard: {
    backgroundColor: "white",
    borderRadius: 10,
    padding: 15,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  carHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 15,
    paddingBottom: 10,
    borderBottomWidth: 1,
    borderBottomColor: "#f0f0f0",
  },
  carName: {
    fontSize: 18,
    fontWeight: "600",
    color: "black",
  },
  carDetailsGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    marginBottom: 15,
  },
  detailItem: {
    width: "50%",
    marginBottom: 12,
  },
  detailLabel: {
    fontSize: 12,
    color: "#666",
    marginBottom: 2,
  },
  detailValue: {
    fontSize: 16,
    color: "black",
    fontWeight: "500",
  },
  scanButton: {
    backgroundColor: "#007AFF",
    borderRadius: 8,
    padding: 12,
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
  },
  scanButtonText: {
    color: "white",
    fontWeight: "600",
    marginLeft: 8,
  },
})

export default CarDetails
