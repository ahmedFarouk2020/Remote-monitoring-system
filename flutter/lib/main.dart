import 'package:flutter/material.dart';
import 'package:syncfusion_flutter_charts/charts.dart';
import 'package:http/http.dart' as http;
import 'dart:convert' as convert;
import 'dart:async';

int i=0;
int time = 0;
int previos_i=0;
String sensor_title="";
var sensor1_data=2;
double d=0.0;
var responsebody=[];
void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark(),
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({Key? key}) : super(key: key);
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  late List<LiveData> chartData;
  late ChartSeriesController _chartSeriesController;

  @override
  void initState() {
    chartData = getChartData();
    Timer.periodic(const Duration(seconds: 2), updateDataSource);
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.only(top: 40.0),
        child: Column(children: [
          Row(
            children: [
              Expanded(
                  child: ElevatedButton(
                      style:
                          ElevatedButton.styleFrom(primary: Colors.deepOrange),
                      onPressed: () {

                        sensor_title="Line Follower";
                        i=1;
                        previos_i=1;
                        time=5;
                        chartData.clear();
                        chartData = getChartData();
                        //Timer.periodic(const Duration(seconds: 5), updateDataSource);
                        setState(() {

                        });
                        // Restart.restartApp();
                      },
                      child: const Text(
                        "Line Follower",
                        style: TextStyle(fontSize: 15.0),
                      ))),
              Expanded(
                  child: ElevatedButton(
                      onPressed: () {
                        sensor_title="Temperature";
                        i=2;
                        previos_i=2;
                        time=5;
                        chartData.clear();
                        chartData = getChartData();
                        setState(() {});
                      },
                      child: const Text(
                        "Temperature",
                        style: TextStyle(fontSize: 15.0),
                      )))
              ,Expanded(
                  child: ElevatedButton(
                      style:
                      ElevatedButton.styleFrom(primary: Colors.deepOrange),
                      onPressed: () {
                        toggle ();
                        setState(() {
                        });

                      },
                      child: const Text(
                        "Toggle",
                        style: TextStyle(fontSize: 15.0),
                      ))),
            ],
          ),
          Expanded(
            child: Container(
              padding: const EdgeInsets.all(20.0),
              child: SfCartesianChart(
                series: <LineSeries<LiveData, int>>[
                  LineSeries<LiveData, int>(
                    onRendererCreated: (ChartSeriesController controller) {
                      _chartSeriesController = controller;
                    },
                    dataSource: chartData,
                    name: "Temperature",
                    color: const Color.fromRGBO(192, 108, 132, 1),
                    xValueMapper: (LiveData data, _) => data.time,
                    yValueMapper: (LiveData data, _) => data.sensor_output,
                  )
                ],
                primaryXAxis: NumericAxis(
                    majorGridLines: const MajorGridLines(width: 1),
                    edgeLabelPlacement: EdgeLabelPlacement.shift,
                    interval: 1,
                    title: AxisTitle(text: 'Time (seconds)')),
                primaryYAxis: NumericAxis(
                  axisLine: const AxisLine(width: 1),
                  majorTickLines: const MajorTickLines(size: 0),
                  title: AxisTitle(text: "$sensor_title"),
                ),
              ),
            ),
          )
        ]),
      ),
    );
  }


  void updateDataSource(Timer timer) {
    getData(time);
    if(i==1)
      {
        chartData.add(LiveData(time++, double.parse(responsebody[1])));
        chartData.removeAt(0);
        _chartSeriesController.updateDataSource(
            addedDataIndex: chartData.length - 1, removedDataIndex: 0);
      }
    else if(i==2)
      {
        chartData.add(LiveData(time++, double.parse(responsebody[2])));
        chartData.removeAt(0);
        _chartSeriesController.updateDataSource(
            addedDataIndex: chartData.length - 1, removedDataIndex: 0);
      }
  }

  List<LiveData> getChartData() {
    return <LiveData>[
      LiveData(0, 0),
      LiveData(1, 0),
      LiveData(2, 0),
      LiveData(3, 0),
      LiveData(4, 0),
    ];
  }
}

class LiveData {
  LiveData(this.time, this.sensor_output);
  final int time;
  final num sensor_output;
}
Future getData(int m) async {
  var url1 = "https://farook2022.pythonanywhere.com/retrieve-local-db";
  http.Response response = await http.get(Uri.parse(url1));
  responsebody = response.body.split('\n')[m].split(',');
  print(responsebody);
  return responsebody ;
}
Future toggle () async {
  var url2 = "https://farook2022.pythonanywhere.com/set-mobile-order";
  http.Response response = await http.get(Uri.parse(url2));
  return responsebody ;
}

