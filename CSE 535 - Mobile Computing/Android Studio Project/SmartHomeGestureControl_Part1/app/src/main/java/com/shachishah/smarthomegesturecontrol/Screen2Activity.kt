package com.shachishah.smarthomegesturecontrol

import android.app.Activity
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.widget.Button
import android.widget.VideoView

class Screen2Activity : Activity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_screen2)

        val gestureName = intent.getStringExtra("GESTURE_NAME")
        val videoResId = getVideoResource(gestureName)

        val videoView: VideoView = findViewById(R.id.video_view)
        val replayButton: Button = findViewById(R.id.replay_button)
        val practiceButton: Button = findViewById(R.id.practice_button)

        videoView.setVideoURI(Uri.parse("android.resource://" + packageName + "/" + videoResId))

        // Replay Button
        replayButton.setOnClickListener {
            videoView.start() // Replay the video
        }

        // Practice Button
        practiceButton.setOnClickListener {
            videoView.stopPlayback()
            val intent = Intent(this, Screen3Activity::class.java)
            intent.putExtra("GESTURE_NAME", gestureName)
            startActivity(intent)
        }

        // Play the video automatically on load
        videoView.setOnPreparedListener {
            it.isLooping = false
            videoView.start()
        }
    }

    private fun getVideoResource(gestureName: String?): Int {
        return when (gestureName) {
            "Turn on lights" -> R.raw.h_light_on
            "Turn off lights" -> R.raw.h_light_off
            "Turn on fan" -> R.raw.h_fan_on
            "Turn off fan" -> R.raw.h_fan_off
            "Increase fan speed" -> R.raw.h_increase_fan_speed
            "Decrease fan speed" -> R.raw.h_decrease_fan_speed
            "Set Thermostat to specified temperature" -> R.raw.h_set_thermo
            else -> when (gestureName?.takeIf { it.matches("\\d".toRegex()) }) {
                "0" -> R.raw.gesture_video_0
                "1" -> R.raw.gesture_video_1
                "2" -> R.raw.gesture_video_2
                "3" -> R.raw.gesture_video_3
                "4" -> R.raw.gesture_video_4
                "5" -> R.raw.gesture_video_5
                "6" -> R.raw.gesture_video_6
                "7" -> R.raw.gesture_video_7
                "8" -> R.raw.gesture_video_8
                "9" -> R.raw.gesture_video_9
                else -> R.raw.gesture_video_0 // Fallback video if needed
            }
        }
    }
}
