import 'package:hive_flutter/hive_flutter.dart';


class ToDoDataBase {
  List classes = [];

  // reference our box
  final _myBox = Hive.box('mybox');

  // run this method if this is the 1st time ever opening this app
  void createInitialData() {
    classes = [
      ["EC327", false],
      ["ME419", false],
    ];
  }

  // load the data from database
  void loadData() {
    classes = _myBox.get("TODOLIST");
  }

  // update the database
  void updateDataBase() {
    _myBox.put("TODOLIST", classes);
  }
}
