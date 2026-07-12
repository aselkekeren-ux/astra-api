import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() => runApp(AstraApp());

class AstraApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: AstraChatScreen(),
    );
  }
}

class AstraChatScreen extends StatefulWidget {
  @override
  _AstraChatScreenState createState() => _AstraChatScreenState();
}

class _AstraChatScreenState extends State<AstraChatScreen> {
  final TextEditingController _controller = TextEditingController();
  String _cevap = "Astra seni dinliyor...";

  // API bağlantısı
  Future<void> astraSohbet(String komut) async {
    final url = Uri.parse('https://astra-api-r0uh.onrender.com/astra');
    
    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'komut': komut, 'mod': 'fast'}),
      );

      if (response.statusCode == 200) {
        setState(() {
          _cevap = json.decode(response.body)['metin'];
        });
      }
    } catch (e) {
      setState(() => _cevap = "Bağlantı hatası: $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black, // Karanlık, şık Astra teması
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Padding(
            padding: const EdgeInsets.all(20.0),
            child: Text(_cevap, style: TextStyle(color: Colors.white, fontSize: 18)),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 20),
            child: TextField(
              controller: _controller,
              style: TextStyle(color: Colors.white),
              decoration: InputDecoration(hintText: "Astra'ya sor...", hintStyle: TextStyle(color: Colors.grey)),
              onSubmitted: (value) => astraSohbet(value),
            ),
          ),
        ],
      ),
    );
  }
}
