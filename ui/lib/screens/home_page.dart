import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:ui/util/dialog_box.dart';
import 'package:ui/util/todo_tile.dart';
import 'package:ui/data/database.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  // reference the hive box
  final _myBox = Hive.box('mybox');
  ClassDB db = ClassDB();

  @override
  void initState() {
    // if this is the 1st time ever openin the app, then create default data
    db.loadData();
    if ((db.classList).isEmpty == true) {
      db.createInitialData();
    } else {
      // there already exists data
      db.loadData();
      String foolist = db.showClasses();
      print(foolist);
    }

    super.initState();
  }

  // text controller
  final _controller = TextEditingController();

  // save new class
  void saveNewTask() {
    setState(() {
      db.classList.add([_controller.text]);
      _controller.clear();
    });
    Navigator.of(context).pop();
    db.updateDataBase();
  }

  // add new class
  void createNewTask() {
    showDialog(
      context: context,
      builder: (context) {
        return DialogBox(
          controller: _controller,
          onSave: saveNewTask,
          onCancel: () => Navigator.of(context).pop(),
        );
      },
    );
  }

  // delete task
  void deleteTask(int index) {
    setState(() {
      db.classList.removeAt(index);
    });
    db.updateDataBase();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.brown.shade400,
      appBar: AppBar(
        title: Text('REGISTRATION MAGIC'),
        elevation: 0,
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: createNewTask,
        child: Icon(Icons.add),
      ),
      body: ListView.builder(
        itemCount: db.classList.length,
        itemBuilder: (context, index) {
          return ToDoTile(
            taskName: db.classList[index][0],
            deleteFunction: (context) => deleteTask(index),
          );
        },
      ),
    );
  }
}
