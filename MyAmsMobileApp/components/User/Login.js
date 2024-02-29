import React, { useState } from 'react';
import { View, TextInput, Button, StyleSheet, Picker } from 'react-native';

const LoginScreen = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('');

  const handleLogin = () => {
    // Xử lý đăng nhập ở đây
    console.log(username, password, role);
    // Thực hiện API call để đăng nhập hoặc xử lý logic tương ứng
  };

  return (
    <View style={styles.container}>
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
      <Picker
        selectedValue={role}
        style={styles.picker}
        onValueChange={(itemValue, itemIndex) => setRole(itemValue)}
      >
        <Picker.Item label="Admin" value="admin" />
        <Picker.Item label="Lecturer" value="lecturer" />
        <Picker.Item label="Alumni" value="alumni" />
      </Picker>
      <Button title="Login" onPress={handleLogin} />
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
