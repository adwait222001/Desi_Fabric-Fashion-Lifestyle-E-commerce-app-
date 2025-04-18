import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
class Your_order extends StatefulWidget {
  const Your_order({super.key});

  @override
  State<Your_order> createState() => _Your_orderState();
}

class _Your_orderState extends State<Your_order> {
  List<Map<String, dynamic>> orders = [];
  bool isLoading = true;
  Future<void> fetchOrders() async {
    try {
      final response = await http.get(Uri.parse('http://192.168.29.214:5000/get_orders'));

      if (response.statusCode == 200) {
        // Print the received response body

        // Parse the response
        final Map<String, dynamic> data = json.decode(response.body);

        // Print the parsed data (the entire response object)

        // Check if 'orders' is not null
        if (data['orders'] != null) {
          setState(() {
            orders = List<Map<String, dynamic>>.from(data['orders']);
            isLoading = false;
          });
        } else {
          setState(() {
            isLoading = false;
          });
        }
      } else {
        throw Exception('Failed to load orders');
      }
    } catch (e) {
      setState(() {
        isLoading = false;
      });
    }
  }
  @override
  void initState() {
    super.initState();
    fetchOrders(); // Fetch orders on init
  }
  void showOrderDetailsDialog(Map<String, dynamic> order) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('Order Details - Order ID: ${order['order_id']}'),
          content: SingleChildScrollView(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Order Date: ${order['order_date']}'),
                Text('Total Price: \$${order['total_price']}'),
                Text('Payment Method: ${order['payment_method']}'),
                Divider(),
                Text('Items:'),
                ...List<Widget>.from(order['items'].map((item) {
                  // Safely access each item in the 'items' list
                  if (item != null && item['productName'] != null) {
                    return Text(
                        'Product: ${item['productName']} | Quantity: ${item['quantity']}');
                  } else {
                    return Text('Invalid item data');
                  }
                })),
              ],
            ),
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop(); // Close the dialog
              },
              child: Text('Close'),
            ),
          ],
        );
      },
    );
  }
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Orders')),
      body: isLoading
          ? Center(child: CircularProgressIndicator()) // Show a loading indicator while fetching
          : orders.isEmpty
          ? Center(child: Text('No orders found.'))
          : ListView.builder(
        itemCount: orders.length,
        itemBuilder: (context, index) {
          final order = orders[index];

          return Card(
            margin: EdgeInsets.all(8),
            child: ListTile(
              title: Row(
                children: [
                  Icon(Icons.shopping_cart, color: Colors.blue),
                  SizedBox(width: 8),
                  Text('Order ID: ${order['order_id']}'),
                ],
              ),
              subtitle: Text('Total Price: \$${order['total_price']}'),
              onTap: () {
                showOrderDetailsDialog(order);
              },
            ),
          );

        },
      ),
    );
  }
}
