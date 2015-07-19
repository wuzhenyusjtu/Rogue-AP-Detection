package com.example.wuzhenyu.detectionsystemclient;

import java.util.List;

import android.net.wifi.ScanResult;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.os.Message;
import android.app.Activity;

import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.view.View;
import android.view.View.OnClickListener;
import android.content.Context;

import android.view.LayoutInflater;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.Toast;




public class MainActivity extends Activity
{

    private EditText serverIP;
    private EditText serverPort;
    private Button sendAPFeatures;
    private WifiManager wifiManager;
    private List<ScanResult> wifiList;

	/*
    private Context mContext;
    private TextView mTextView;
    private LocationManager mLocationManager;
    private LocationListenerImpl mLocationListenerImpl;
	*/


    private ClientThread clientThread = new ClientThread();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        new Thread(clientThread).start();
        getScanResults();
        showWifiScanList();
        serverIP = (EditText) findViewById(R.id.ip);
        serverPort = (EditText) findViewById(R.id.port);
        sendAPFeatures = (Button) findViewById(R.id.send);
        sendAPFeatures.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View v) {
                String ip = serverIP.getText().toString();
                String port = serverPort.getText().toString();
                String serverPath = "http://"+ip+":"+port+"/sendApFeatures";
                Message msg = new Message();
                msg.what = 0x1;
                msg.obj = serverPath;
                clientThread.myHandler.sendMessage(msg);
                for (int i=0; i < wifiList.size();i++){
                    msg = new Message();
                    msg.what = 0x2;
                    msg.obj = wifiList.get(i);
                    clientThread.myHandler.sendMessage(msg);
                }
            }
        });
    }

    private void getScanResults(){
        wifiManager = (WifiManager) getSystemService(Context.WIFI_SERVICE);
        wifiList = wifiManager.getScanResults();
    }

    private void showWifiScanList() {
        ListView listView = (ListView) findViewById(R.id.listView);
        if (wifiList == null) {
            Toast.makeText(this, "wifi not activated", Toast.LENGTH_LONG).show();
        }else {
            listView.setAdapter(new MyAdapter(this,wifiList));
        }
    }

    //Wifi
    public class MyAdapter extends BaseAdapter {

        LayoutInflater inflater;
        List<ScanResult> list;

        public MyAdapter(Context context, List<ScanResult> list) {
            // TODO Auto-generated constructor stub
            this.inflater = LayoutInflater.from(context);
            this.list = list;
        }

        @Override
        public int getCount() {
            // TODO Auto-generated method stub
            return list.size();
        }

        @Override
        public Object getItem(int position) {
            // TODO Auto-generated method stub
            return position;
        }

        @Override
        public long getItemId(int position) {
            // TODO Auto-generated method stub
            return position;
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            // TODO Auto-generated method stub
            View view = null;
            view = inflater.inflate(R.layout.wifi_item, null);
            ScanResult scanResult = list.get(position);
            TextView ssidView = (TextView) view.findViewById(R.id.ssidView);
            ssidView.setText(scanResult.SSID);
            ssidView.setWidth(400);
            TextView bssidView = (TextView) view.findViewById(R.id.bssidView);
            bssidView.setText(scanResult.BSSID);
            bssidView.setWidth(400);
            TextView freqView = (TextView) view.findViewById(R.id.freqView);
            freqView.setText(String.valueOf(Math.abs(scanResult.frequency)));
            freqView.setWidth(200);
            TextView secView = (TextView) view.findViewById(R.id.secView);
            secView.setText(scanResult.capabilities);
            secView.setWidth(650);
            TextView signalStrenth = (TextView) view.findViewById(R.id.signal_strenth);
            signalStrenth.setText(String.valueOf(Math.abs(scanResult.level)));
            ImageView imageView = (ImageView) view.findViewById(R.id.imageView);
            // Setting the image, according to signal intensity
            if (Math.abs(scanResult.level) > 100) {
                imageView.setImageDrawable(getResources().getDrawable(R.drawable.stat_sys_wifi_signal_0));
            } else if (Math.abs(scanResult.level) > 80) {
                imageView.setImageDrawable(getResources().getDrawable(R.drawable.stat_sys_wifi_signal_1));
            } else if (Math.abs(scanResult.level) > 70) {
                imageView.setImageDrawable(getResources().getDrawable(R.drawable.stat_sys_wifi_signal_1));
            } else if (Math.abs(scanResult.level) > 60) {
                imageView.setImageDrawable(getResources().getDrawable(R.drawable.stat_sys_wifi_signal_2));
            } else if (Math.abs(scanResult.level) > 50) {
                imageView.setImageDrawable(getResources().getDrawable(R.drawable.stat_sys_wifi_signal_3));
            } else {
                imageView.setImageDrawable(getResources().getDrawable(R.drawable.stat_sys_wifi_signal_4));
            }
            return view;
        }
    }

}
