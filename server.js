// Load the http module to create an http server.
var http = require('http');
var url = require('url');
var fs = require('fs');
 
// Configure our HTTP server to respond with Hello World to all requests.
var server = http.createServer(function (request, response) {
   var request = url.parse(request.url, true);
   var action = request.pathname;
   
   if (action == '/weather') {
      var img = fs.readFileSync('./weather_info.png');
      response.writeHead(200, {'Content-Type': 'image/gif' });
      response.end(img, 'binary');
   } else {
      response.writeHead(200, {'Content-Type': 'text/plain'});
      response.end('Hello world...!');
   }

});
 
// Listen on port 8000, IP defaults to 127.0.0.1
server.listen(8000);
 
// Put a friendly message on the terminal
console.log("Server running at http://127.0.0.1:8000/");
