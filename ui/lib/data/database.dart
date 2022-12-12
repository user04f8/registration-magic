import 'dart:ffi';
import 'dart:convert';

import 'package:hive_flutter/hive_flutter.dart';

class ClassDB {
  List classList = [];
  List regTime = [];

  final _myBox = Hive.box('mybox');

  void createInitialData() {//default classes if no prior data
    classList = [
      ["CAS AA385 A1"],
      ["ENG AA489 A1"],
    ];
  }

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
