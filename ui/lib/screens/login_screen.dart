import 'package:flutter/material.dart';
import 'package:ui/screens/home_page.dart';
import 'package:ui/screens/Widgets/login_app_bar.dart';
import 'package:ui/screens/Widgets/login_text_box.dart';
//import 'package:google_fonts/google_fonts.dart';

class LoginScreen extends StatelessWidget {
  const LoginScreen({Key? key}) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: PreferredSize(
        preferredSize: Size.fromHeight(90.0),
        child: LoginAppBar(),
      ),
      body: LayoutBuilder(
        builder: (context, constraints) {
          if (constraints.maxWidth < 600) {
            return const LoginMobile();
          } else {
            return const LoginDesktop();
          }
        },
      ),
    );
  }
}

class LoginMobile extends StatefulWidget {
  const LoginMobile({Key? key}) : super(key: key);

  @override
  State<LoginMobile> createState() => _LoginMobileState();
}

class _LoginMobileState extends State<LoginMobile> {
  bool _isChecked = false;
  @override
  Widget build(BuildContext context) {
    return Center(
      child: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(30),
          child: Center(
            child: SizedBox(
              width: 300,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Text(
                    'Welcome back',
                    /*                   style: GoogleFonts.inter(
                      fontSize: 17,
                      color: Colors.black,                     
                    ),
*/
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'Login to your account',
                  ),
                  const SizedBox(height: 35),
/*                  TextField(
                    decoration: InputDecoration(
                      border: OutlineInputBorder(),
                      labelText: 'Email',
                      hintText: 'Enter Email address',
                    ),
                  ),
                  */
                  const SizedBox(height: 20),
                  TextBox(),
                  TextField(
                    obscureText: true,
                    decoration: InputDecoration(
                      border: OutlineInputBorder(),
                      labelText: 'Password',
                      hintText: 'Enter Password',
                    ),
                  ),
                  const SizedBox(height: 25),
                  Row(
                      //...
                      ),
                  const SizedBox(height: 30),
                  TextButton(
                    child: const Text('Login'),
                    onPressed: () {
                      Navigator.push(context,
                          MaterialPageRoute(builder: (context) => HomePage()));
                    },
                    //...
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class LoginDesktop extends StatefulWidget {
  const LoginDesktop({Key? key}) : super(key: key);

  @override
  State<LoginDesktop> createState() => _LoginDesktopState();
}

class _LoginDesktopState extends State<LoginDesktop> {
  bool _isChecked = false;
  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
            //<-- Expanded widget
            child: Image.asset(
          'images/image_1.jpg',
          fit: BoxFit.cover,
        )),
        Expanded(
          //<-- Expanded widget
          child: Container(
            constraints: const BoxConstraints(maxWidth: 21),
            padding: const EdgeInsets.symmetric(horizontal: 50),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Text(
                  'Welcome back',
                ),
                const SizedBox(height: 8),
                Text(
                  'Login to your account',
                ),
                const SizedBox(height: 35),
                TextField(
                  obscureText: false,
                  //cursorColor: Colors.black,
                  style: TextStyle(color: Colors.black),
                  decoration: InputDecoration(
                    border: OutlineInputBorder(),
                    labelText: 'Email',
                    hintText: 'Enter Email address',
                  ),
                ),
                const SizedBox(height: 20),
                TextField(
                  obscureText: true,
                  decoration: InputDecoration(
                    border: OutlineInputBorder(),
                    labelText: 'Password',
                    hintText: 'Enter Password',
                  ),
                ),
                const SizedBox(height: 25),
                Row(
                    //...
                    ),
                const SizedBox(height: 30),
                TextButton(
                  child: const Text('Login'),
                  onPressed: () {
                    Navigator.push(context,
                        MaterialPageRoute(builder: (context) => HomePage()));
                  },
                  //...
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }
}
