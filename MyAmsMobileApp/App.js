import { createDrawerNavigator, DrawerContentScrollView, DrawerItem, DrawerItemList } from "@react-navigation/drawer";
import { StatusBar } from 'expo-status-bar';
import React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import Login from './components/User/Login';
import Logout from "./components/User/Logout";
import Register from "./components/User/Register";
import Homne from "./components/Home/Home";
import API, { endpoints } from "./configs/API";
import { useEffect, useState } from "react/cjs/react.production.min";
import { NavigationContainer } from "@react-navigation/native";

const Drawer = createDrawerNavigator();

const App = () => {
  const [user, dispatch] = useReducer(MyUserReducer, null);

  return (
    <MyContext.Provider value={[user, dispatch]}>
      <NavigationContainer>
        <Drawer.Navigator drawerContent={MyDrawerItem} screenOptions={{headerRight: Logout}}>
          <Drawer.Screen name="Home" component={Home} options={{title: 'Bảng tin'}} />
          {user===null?<>
            <Drawer.Screen name="Login" component={Login} />
            <Drawer.Screen name="Register" component={Register} />
          </>:<>
            <Drawer.Screen name={user.username} component={Home} />
          </>}
          
        </Drawer.Navigator>
      </NavigationContainer>
    </MyContext.Provider>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  txt: {
    color: "blue",
    fontSize: 20,
    fontWeight: "bold",
  },
});
