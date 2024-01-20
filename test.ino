#include <WiFi.h>
#include <HTTPClient.h>
#include <Arduino.h>
#include "esp_camera.h"
#include "esp_deep_sleep.h"

// WiFi credentials
const char *ssid = "your_wifi_ssid";
const char *password = "your_wifi_password";

// Flask server details
const char *serverUrl = "http://your_server_ip:5000/upload"; // Replace with your Flask server URL

// Deep sleep interval in microseconds (15 seconds)
const uint64_t deepSleepInterval = 15e6;

void setup()
{
    Serial.begin(115200);

    // Connect to Wi-Fi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi");

    // Camera setup
    camera_config_t config;
    // ... (camera setup code, same as previous)

    // Deep sleep setup
    esp_deep_sleep_pd_config(ESP_PD_DOMAIN_RTC_PERIPH, ESP_PD_OPTION_ON);

    // Check if this is the first boot
    if (esp_sleep_get_wakeup_cause() != ESP_SLEEP_WAKEUP_TIMER)
    {
        Serial.println("First boot, capturing and sending frames...");
        captureAndSendFrames();
    }
    else
    {
        Serial.println("Waking up from deep sleep...");
    }

    // Enter deep sleep for 45 seconds
    Serial.println("Entering deep sleep...");
    esp_deep_sleep_enable_timer_wakeup(deepSleepInterval);
    esp_deep_sleep_start();
}

void captureAndSendFrames()
{
    camera_fb_t *fb = esp_camera_fb_get();

    if (fb)
    {
        HTTPClient http;

        http.begin(serverUrl);
        http.addHeader("Content-Type", "image/jpeg");

        // Send the captured frame to the Flask server
        int httpCode = http.POST(fb->buf, fb->len);

        if (httpCode > 0)
        {
            Serial.printf("HTTP Response code: %d\n", httpCode);
        }
        else
        {
            Serial.printf("HTTP Error: %s\n", http.errorToString(httpCode).c_str());
        }

        http.end();
        esp_camera_fb_return(fb);
    }
}

void loop()
{
    // Not used in this example
}
