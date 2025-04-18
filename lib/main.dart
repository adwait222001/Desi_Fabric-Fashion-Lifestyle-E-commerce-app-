import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:rangmahal/auth-process/Fauthentication.dart';
import 'package:rangmahal/shopee/homepage.dart';

import 'firebase_options.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: SplashScreen(),
    );
  }
}

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  _SplashScreenState createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();

    // Navigate to the appropriate screen based on user sign-in status after 2 seconds
    Future.delayed(Duration(seconds: 2), () async {
      final FirebaseAuth _auth = FirebaseAuth.instance;
      User? user = _auth.currentUser;
      if (user != null) {
        // If user is signed in, navigate directly to Homepage
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (context) => Homepage()),
        );
      } else {
        // If user is not signed in, navigate to Auth screen
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (context) => Auth()),
        );
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.purpleAccent,
      body: Center(
        child: Image.asset(
          'assets/icons/icon.jpeg',  // Ensure the image is correctly placed in assets
          height: 200,
        ),
      ),
    );
  }
}

class AnimatedScreen extends StatefulWidget {
  const AnimatedScreen({super.key});

  @override
  _AnimatedScreenState createState() => _AnimatedScreenState();
}

class _AnimatedScreenState extends State<AnimatedScreen> {
  bool _showImageText = false;
  bool _showButton = false;

  @override
  void initState() {
    super.initState();

    // Start the image and text animation
    Future.delayed(Duration(milliseconds: 500), () {
      setState(() {
        _showImageText = true;
      });
    });

    // Show the button AFTER the image and text animation completes
    Future.delayed(Duration(seconds: 4), () {
      setState(() {
        _showButton = true;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.purpleAccent,
      body: Stack(
        children: [
          AnimatedPositioned(
            duration: Duration(seconds: 4),
            curve: Curves.easeInOut,
            top: _showImageText ? MediaQuery.of(context).size.height * 0.3 : -200,
            left: MediaQuery.of(context).size.width * 0.2,
            right: MediaQuery.of(context).size.width * 0.2,
            child: Image.asset(
              'assets/icons/icon.jpeg', // Change this to your image path
              height: 200,
            ),
          ),
          AnimatedPositioned(
            duration: Duration(seconds: 4),
            curve: Curves.easeInOut,
            bottom: _showImageText ? MediaQuery.of(context).size.height * 0.3 : -100,
            left: 0,
            right: 0,
            child: Center(
              child: Text(
                "Rang Mahal",
                style: TextStyle(
                  fontSize: 32,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                ),
              ),
            ),
          ),
          AnimatedOpacity(
            duration: Duration(seconds: 2),
            opacity: _showButton ? 1 : 0,
            child: Align(
              alignment: Alignment.bottomCenter,
              child: Padding(
                padding: EdgeInsets.only(bottom: 50),
                child: ElevatedButton(
                  onPressed: () {
                    // Check if the user is logged in
                    final FirebaseAuth _auth = FirebaseAuth.instance;
                    if (_auth.currentUser != null) {
                      // If logged in, go to the homepage
                      Navigator.pushAndRemoveUntil(
                        context,
                        MaterialPageRoute(builder: (context) => Homepage()),
                            (route) => false, // Removes all previous routes
                      );
                    } else {
                      // If not logged in, go to the Auth screen
                      Navigator.push(
                        context,
                        MaterialPageRoute(builder: (context) => Auth()),
                      );
                    }
                  },
                  style: ElevatedButton.styleFrom(
                    padding: EdgeInsets.symmetric(horizontal: 30, vertical: 15),
                    backgroundColor: Colors.orange,
                  ),
                  child: Text(
                    "Let's Start",
                    style: TextStyle(fontSize: 18, color: Colors.redAccent),
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
