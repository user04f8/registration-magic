import 'dart:convert';
import 'dart:io';
import 'dart:ui';

import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:ui/util/dialog_box.dart';
import 'package:ui/util/time_box.dart';
import 'package:ui/util/class_box.dart';
import 'package:ui/data/database.dart';
import 'package:http/http.dart' as http;

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}
String text = "REGISTER!";


class _HomePageState extends State<HomePage> {
  // reference the hive box
  final _myBox = Hive.box('mybox');
  ClassDB db = ClassDB();


  @override
  void initState() {
    // if this is the 1st time ever openin the app, then create default classes
    db.loadData();
    if ((db.classList).isEmpty == true) {
      db.createInitialData();
    } else {
      // there already exists data
      db.loadData();
      db.loadTime();
      displayTime();
      String thyme = displayTime();
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
  void saveNewTime() {
    setState(() {
      db.regTime.clear();
      db.regTime.add([_controller.text]);
      _controller.clear();
    });
    Navigator.of(context).pop();

    db.updateTime();
    db.returnLatestTime();
    displayTime();
    String time = db.returnLatestTime();
    String classList = db.returnJsonList();
    //Uri uri = Uri.https('127.0.0.1:5000', 'request');
    sendRequest(time, classList);
  }
  Future<http.Response> sendRequest(String time, String classList) async {
    print("sending request . . .");
    Uri uri = Uri.parse("http://127.0.0.1:53303/request");
    Future<http.Response> response = http.post(uri, headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    }, body: jsonEncode(<String, String>{
      'classList': classList,
      'time': time,
    }));
    await response;
    print("sent request to uri 127.0.0.1:53303");
    return response;
  }
  String displayTime(){
    String string;
    db.loadTime();
    if (db.regTime.isEmpty == true || db.regTime == [] || db.regTime == null||
        db.regTime[0][0] == ""){
      text = "REGISTER!";
    }
    else{
      String add = db.returnLatestTime();
      text = "REGISTERED FOR: "+add;
    }
    print (db.regTime[0]);
    return text;
  }

  // add new class
  void createNewClass() {
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
  void cTime() {
    showDialog(
      context: context,
      builder: (context) {
        return timeInput(
          controller: _controller,
          onSave: saveNewTime,
          onCancel: () => Navigator.of(context).pop(),
        );
      },
    );
  }

  // delete task
  void deleteClass(int index) {
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
        onPressed: createNewClass,
        child: Icon(Icons.add),
      ),
      body: Column(
        children: [
          Container(//registration button
            height: 100,
            width: 300,
            alignment: Alignment.bottomCenter,
            child: OutlinedButton(style: ButtonStyle(
              shape: MaterialStateProperty.all(RoundedRectangleBorder(borderRadius: BorderRadius.circular(30))),

            ),
              child: Text(text,
                style: TextStyle(
                  color: Colors.brown.shade100,
                ),
              ),
              onPressed: cTime,
            ),
          ),
          Container(
            height: 500,//generates list of classes
            child: ListView.builder(
              itemCount: db.classList.length,
              itemBuilder: (context, index) {
                return ToDoTile(
                  taskName: db.classList[index][0],
                  deleteFunction: (context) => deleteClass(index),
                );
              },
            ),
          )
        ],
      )
    );
  }

}
