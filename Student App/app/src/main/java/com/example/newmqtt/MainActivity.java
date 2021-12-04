package com.example.newmqtt;

import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.eclipse.paho.android.service.MqttAndroidClient;
import org.eclipse.paho.client.mqttv3.IMqttActionListener;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import java.util.Date;

import android.graphics.Color;
import android.os.Bundle;
import android.widget.Toast;

import com.jjoe64.graphview.DefaultLabelFormatter;
import com.jjoe64.graphview.GraphView;
import com.jjoe64.graphview.series.DataPoint;
import com.jjoe64.graphview.series.DataPointInterface;
import com.jjoe64.graphview.series.LineGraphSeries;
import com.jjoe64.graphview.series.OnDataPointTapListener;
import com.jjoe64.graphview.series.Series;

public class MainActivity extends AppCompatActivity {

    MqttAndroidClient client;
    String currentdatetime = java.text.DateFormat.getDateTimeInstance().format(new Date());
    TextView subText_1, subText_2, subText_3;
    int[] x_axis = {8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24};
    int[] y_axis = {28, 30, 31, 35, 50, 37, 37, 39, 39, 41, 43, 42, 40, 37, 32, 25, 16};



    // FOR FORECASTING
    // forecast deployment pending
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // TEXTVIEW FIELDS
        subText_1 = (TextView)findViewById(R.id.textViewdt);
        subText_2 = (TextView)findViewById(R.id.textView2);
        subText_3 = (TextView)findViewById(R.id.textView3);

        // DRAW OCCUPANCY GRAPH
        GraphView graph = (GraphView) findViewById(R.id.graph);
        DataPoint[] points = new DataPoint[17];
        for (int i = 0; i < points.length; i++) {
            points[i] = new DataPoint(x_axis[i], y_axis[i]);
        }
        LineGraphSeries<DataPoint> series = new LineGraphSeries<>(points);
        graph.getViewport().setXAxisBoundsManual(true);
        graph.getViewport().setMinX(8);
        graph.getViewport().setMaxX(24);
        graph.getViewport().setYAxisBoundsManual(true);
        graph.getViewport().setMinY(0);
        graph.getViewport().setMaxY(55);
        series.setColor(Color.parseColor("#9C27B0"));
        series.setDrawDataPoints(true);
        series.setDataPointsRadius(10);
        graph.addSeries(series);
        graph.getGridLabelRenderer().setLabelFormatter(new DefaultLabelFormatter() {
            @Override
            public String formatLabel(double value, boolean isValueX) {
                if (isValueX) {
                    return super.formatLabel(value, isValueX) + "hr";
                } else {
                    return super.formatLabel(value, isValueX);
                }
            }
        });
        series.setOnDataPointTapListener(new OnDataPointTapListener() {
            @Override
            public void onTap(Series series, DataPointInterface dataPoint) {
                Toast.makeText(getApplicationContext(), "Time: " + (int)dataPoint.getX() + "hr and Number of Occupants: "+ (int)dataPoint.getY(), Toast.LENGTH_SHORT).show();
            }
        });

        // FETCH CURRENT DATE AND TIME TO DISPLAY
        subText_1.setText(currentdatetime);

        // MQTT PROTOCOL
        String clientId = MqttClient.generateClientId();
        //client = new MqttAndroidClient(this.getApplicationContext(), "tcp://broker.mqttdashboard.com:1883",clientId);
        client = new MqttAndroidClient(this.getApplicationContext(), "tcp://192.168.0.177:1883",clientId);

        // Connection
        try {
            IMqttToken token = client.connect();
            token.setActionCallback(new IMqttActionListener() {
                @Override
                public void onSuccess(IMqttToken asyncActionToken) {
                    Toast.makeText(MainActivity.this,"Connected",Toast.LENGTH_LONG).show();
                    setSubscription();
                }

                @Override
                public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
                    Toast.makeText(MainActivity.this,"Connection failed!!",Toast.LENGTH_LONG).show();
                }
            });
        } catch (MqttException e) {
            e.printStackTrace();
        }

        // Callback Function for receiving the message
        client.setCallback(new MqttCallback() {
            @Override
            public void connectionLost(Throwable cause) {

            }

            @Override
            public void messageArrived(String topic, MqttMessage message) throws Exception {

                switch (topic.toString()) {
                    case "Composition/User/U38/0/1/Temperature":
                        subText_2.setText(new String(message.getPayload()) + " °C");
                        break;
                    case "Composition/User/U38/0/1/PeopleCount":
                        subText_3.setText(new String(message.getPayload()) + "/50");
                        break;

                    default:
                        return;
                }

            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {

            }
        });

    }

    // SUBSCRIPTION OF THE TOPIC
    private void setSubscription(){

        try{

            client.subscribe("Composition/User/U38/0/1/+",2);

        }catch (MqttException e){
            e.printStackTrace();
        }
    }

    // TO REFRESH AND UPDATE THE VALUES
    public void conn(View v){

        try {
            IMqttToken token = client.connect();
            token.setActionCallback(new IMqttActionListener() {
                @Override
                public void onSuccess(IMqttToken asyncActionToken) {
                    Toast.makeText(MainActivity.this,"Refreshed",Toast.LENGTH_LONG).show();
                    setSubscription();

                }

                @Override
                public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
                    Toast.makeText(MainActivity.this,"Connection failed!!",Toast.LENGTH_LONG).show();
                }
            });
        } catch (MqttException e) {
            e.printStackTrace();
        }

    }
}