import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:ui/screens/login_screen.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'screens/home_page.dart';


void main() async {
  await Hive.initFlutter();
  var box = await Hive.openBox('mybox');//opens local database
  runApp(const MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  // This widget is the root of your application.
  @override
  void initstate() {
    super.initState();
    SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersive);
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData(primarySwatch: Colors.brown),
      home: const LoginScreen(),//opens login screen
    );
  }
}
