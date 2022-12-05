import 'package:flutter/material.dart';

class TextBox extends StatefulWidget {
  const TextBox({super.key});

  @override
  State<TextBox> createState() => _TextBox();
}

class _TextBox extends State<TextBox> {
  late TextEditingController _controller;

  @override
  void initState() {
    super.initState();
    _controller = TextEditingController();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
          child: TextField(
        controller: _controller,
        obscureText: false,
        decoration: const InputDecoration(
          border: OutlineInputBorder(),
          labelText: 'Enter your name',
          hintText: 'Enter your username',
        ),
      )
          /*
          onSubmitted: (String value) async {
            await showDialog<void>(
              context: context,
              builder: (BuildContext context) {
                
                return AlertDialog(
                  title: const Text('Thanks!'),
                  content: Text(
                      'You typed "$value", which has length ${value.characters.length}.'),
                  actions: <Widget>[
                    
                    TextButton(
                       onPressed: () {
                        Navigator.pop(context);
                      });
                      child: const Text('OK'),
                      
                    ),
                  ],
                );
                
              },
              */
          ),
    );
  }
}
