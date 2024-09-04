package com.shachishah.smarthomegesturecontrol

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.Spinner
import android.app.Activity

class MainActivity : Activity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val gestureSpinner: Spinner = findViewById(R.id.gesture_spinner)
        val selectButton: Button = findViewById(R.id.select_gesture_button)

        selectButton.setOnClickListener {
            val selectedGesture = gestureSpinner.selectedItem.toString()
            val intent = Intent(this, Screen2Activity::class.java)
            intent.putExtra("GESTURE_NAME", selectedGesture)
            startActivity(intent)
        }
    }
}
