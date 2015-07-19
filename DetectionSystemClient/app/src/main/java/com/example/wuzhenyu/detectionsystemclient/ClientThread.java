package com.example.wuzhenyu.detectionsystemclient;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.Socket;
import java.net.SocketTimeoutException;
import java.util.ArrayList;
import java.util.List;

import android.os.Handler;
import android.os.Looper;
import android.os.Message;
import android.util.Log;
import android.net.wifi.ScanResult;

import org.apache.http.HttpResponse;
import org.apache.http.HttpStatus;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.protocol.HTTP;
import org.apache.http.util.EntityUtils;

public class ClientThread implements Runnable
{
    public Handler myHandler;
    private String serverPath;
    public void run()
    {
        Looper.prepare();
        myHandler = new Handler()
        {
            @Override
            public void handleMessage(Message msg)
            {
                if (msg.what == 0x1){
                    serverPath = (String)msg.obj;
                }
                else if (msg.what == 0x2){
                    try {
                        ScanResult result = (ScanResult)msg.obj;
                        HttpPost httpPost = new HttpPost(serverPath);
                        List<NameValuePair> params = new ArrayList<NameValuePair>();
                        params.add(new BasicNameValuePair("BSSID", result.BSSID));
                        params.add(new BasicNameValuePair("SSID", result.SSID));
                        params.add(new BasicNameValuePair("Channel", "Unknown"));
                        params.add(new BasicNameValuePair("Vendor", "Unknown"));
                        params.add(new BasicNameValuePair("Location", "Unknow"));
                        params.add(new BasicNameValuePair("Security", result.capabilities));
                        params.add(new BasicNameValuePair("Signal", String.valueOf(Math.abs(result.level))));
                        params.add(new BasicNameValuePair("Noise", "Unknown"));
                        params.add(new BasicNameValuePair("Route", "Unknown"));
                        httpPost.setEntity(new UrlEncodedFormEntity(params, HTTP.UTF_8));
                        HttpClient client = new DefaultHttpClient();
                        HttpResponse response = client.execute(httpPost);
                        if (response.getStatusLine().getStatusCode() == HttpStatus.SC_OK) {
                            String str = EntityUtils.toString(response.getEntity(), "utf-8");
                            Log.i("info", str);
                        }
                    }
                    catch (ClientProtocolException e) {
                        e.printStackTrace();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            }
        };
        Looper.loop();

    }



}
