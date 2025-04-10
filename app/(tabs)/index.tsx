// Import at the top of your file
import React, { useState, useEffect } from 'react';
import { Platform, PermissionsAndroid, Button, View, Text, FlatList, TouchableOpacity, SafeAreaView } from 'react-native';
//import { BleManager, Device } from 'react-native-ble-plx';

//const manager = new BleManager();

const Index = () => {
  return (
    <SafeAreaView>
      <View >
        <Text>
          Connect to OBD2 Device
        </Text>
      </View>
      <TouchableOpacity >
        <Text>{'Connect'}</Text>
      </TouchableOpacity>
      {/* <DeviceModal
        closeModal={hideModal}
        visible={isModalVisible}
        connectToPeripheral={hideModal}
        devices={[]}
      /> */}
    </SafeAreaView>
  );
}; export default Index