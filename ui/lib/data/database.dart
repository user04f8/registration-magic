import 'dart:ffi';
import 'dart:convert';

import 'package:hive_flutter/hive_flutter.dart';

class ClassDB {
  List classList = [];
  List regTime = [];

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

  void setTime(String time){
    _myBox.put("TIME", time);
  }
  void loadTime(){
    regTime = _myBox.get("TIME");
  }
  void updateTime(){
    _myBox.put("TIME", regTime);
  }

  // update the database
  void updateDataBase() {
    _myBox.put("CLASSLIST", classList);
  }
  String returnJsonList() {
    loadData();
    String cList = jsonEncode(classList);
    return cList;
  }
  String returnLatestTime() {
    loadTime();
    String cList = regTime[0][0].toString();
    //print (cList);
    return cList;
  }

}
