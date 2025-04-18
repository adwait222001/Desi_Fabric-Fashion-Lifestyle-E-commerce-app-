import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:rangmahal/auth-process/profile.dart';

class Auth extends StatefulWidget {
  const Auth({super.key});

  @override
  State<Auth> createState() => _AuthState();
}

class _AuthState extends State<Auth> {
  final FirebaseAuth firebaseAuth = FirebaseAuth.instance;
  final emailController = TextEditingController();
  final passwordController = TextEditingController();
  String error = '';
  bool showNewCard = false;
  String actionType = '';

  Future<void> signIn() async {
    try {
      await firebaseAuth.signInWithEmailAndPassword(
          email: emailController.text.trim(), password: passwordController.text.trim());

      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text("Signed in")));
      Navigator.push(context, MaterialPageRoute(builder: (context) => ImageUploadPage()));

    } on FirebaseAuthException catch (e) {
      setState(() {
        error = e.message ?? 'An error occurred';
      });
    }
  }

  Future<void> register() async {
    try {
      await firebaseAuth.createUserWithEmailAndPassword(
          email: emailController.text.trim(), password: passwordController.text.trim());
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text("Registered successfully")));
      Navigator.push(context, MaterialPageRoute(builder: (context) => ImageUploadPage()));
    } on FirebaseAuthException catch (e) {
      setState(() {
        error = e.message ?? 'An error has occurred';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.amberAccent,
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            if (!showNewCard) ...[
              // Sign-In Card
              Card(
                elevation: 5,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Padding(
                  padding: EdgeInsets.all(10),
                  child: TextButton(
                    onPressed: () {
                      setState(() {
                        showNewCard = true;
                        actionType = "Sign-In";
                      });
                    },
                    child: Text("Sign-In"),
                  ),
                ),
              ),
              SizedBox(height: 10),

              // Register Card
              Card(
                elevation: 5,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Padding(
                  padding: EdgeInsets.all(10.0),
                  child: TextButton(
                    onPressed: () {
                      setState(() {
                        showNewCard = true;
                        actionType = "Register";
                      });
                    },
                    child: Text("Register"),
                  ),
                ),
              ),
            ] else ...[
              // New card appearing after clicking Sign-In or Register
              Card(
                elevation: 5,
                color: Colors.white,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Padding(
                  padding: EdgeInsets.all(20),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      TextField(
                        controller: emailController,
                        decoration: InputDecoration(labelText: 'Email'),
                      ),
                      SizedBox(height: 10),
                      TextField(
                        controller: passwordController,
                        decoration: InputDecoration(labelText: 'Password'),
                        obscureText: true, // Hide password input
                      ),
                      SizedBox(height: 20),
                      ElevatedButton(
                        onPressed: actionType == "Sign-In" ? signIn : register,
                        child: Text(actionType), // Button text changes dynamically
                      ),
                      if (actionType == "Register") ...[
                        SizedBox(height: 10),
                        TextButton(
                          onPressed: () {
                            setState(() {
                              actionType = "Sign-In";
                            });
                          },
                          child: Text(
                            "Already have an account?",
                            style: TextStyle(color: Colors.blue),
                          ),
                        ),
                      ],
                    ],
                  ),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
