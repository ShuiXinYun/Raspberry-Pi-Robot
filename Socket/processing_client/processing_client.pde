  
import processing.net.*; 

Client myClient; 
String dataIn;
void setup() { 
  size(200, 200); 
  // Connect to the local machine at port 5204.
  // This example will not run if you haven't
  // previously started a server on this port.
  myClient = new Client(this, "127.0.0.1", 8888); 
} 
 
void draw() { 
  try {
    if (myClient.available() > 0) { 
      dataIn = myClient.readString(); 
      String q[] = splitTokens(dataIn);
      print (dataIn+"\n");
      print ("Angle  "+q[0]+"\n"+"DistF  "+q[1]+"\n"+"Dist_B  "+q[2]+"\n");
    }
  } catch (Exception e){}
} 