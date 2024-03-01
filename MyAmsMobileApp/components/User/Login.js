import React, { useState } from 'react';
import { View, TextInput, Button, StyleSheet } from 'react-native';
import { Picker } from '@react-native-picker/picker';
import API, { authApi, endpoints } from "../../configs/API";

const LoginScreen = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('');

  const handleLogin = async () => {
    try {
        const response = await authApi().post(endpoints.login, { username, password });
        const accessToken = response.data.accessToken;
        // Xử lý accessToken, ví dụ: lưu vào local storage hoặc global state
        Alert.alert('Login Successful', 'Access token: ' + accessToken);
    } catch (error) {
        // Xử lý lỗi
        Alert.alert('Login Failed', 'An error occurred during login.');
        console.error('Error logging in:', error);
    }
  };
  return (
    <View style={styles.container}>
        <Picker
        selectedValue={role}
        style={styles.picker}
        onValueChange={(itemValue, itemIndex) => setRole(itemValue)}
        >
        <Picker.Item label="Admin" value="admin" />
        <Picker.Item label="Lecturer" value="lecturer" />
        <Picker.Item label="Alumni" value="alumni" />
      </Picker>
      <TextInput
        style={styles.input}
        placeholder="Username"
        value={username}
        onChangeText={setUsername}
      />
      <TextInput
        style={styles.input}
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />
        <Button  title="Login" onPress={handleLogin} />
        <Button  title="Register for Alumni" onPress={handleLogin} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    padding: 20,
  },
  input: {
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 20,
    padding: 10,
  },
});

export default LoginScreen;
