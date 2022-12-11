import 'dart:ffi';
import 'dart:convert';

import 'package:hive_flutter/hive_flutter.dart';

class ClassDB {
  List classList = [];

  // reference our box
  final _myBox = Hive.box('mybox');

  // run this method if this is the 1st time ever opening this app
  void createInitialData() {
    classList = [
      ["EC419 B2"],
      ["EC330 A2"],
    ];
  }

  // load the data from database
  void loadData() {
    classList = _myBox.get("CLASSLIST");
  }

  String parseInputs(String string){
    string.split(" ");
    return string;
  }

  // update the database
  void updateDataBase() {
    _myBox.put("CLASSLIST", classList);
  }
  String showClasses() {
    loadData();
    String cList = jsonEncode(classList);
    return cList;
  }
}
