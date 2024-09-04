package com.shachishah.smarthomegesturecontrol

import android.Manifest
import android.app.Activity
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Bundle
import android.os.Environment
import android.provider.MediaStore
import android.widget.Button
import android.widget.Toast
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.RequestBody.Companion.asRequestBody
import java.io.File
import java.io.IOException

class Screen3Activity : Activity() {

    private val REQUEST_VIDEO_CAPTURE = 1
    private val REQUEST_PERMISSIONS = 2
    private var videoUri: Uri? = null
    private lateinit var gestureName: String
    private lateinit var userLastName: String
    private lateinit var savedVideoFile: File

    private val client = OkHttpClient()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_screen3)

        gestureName = intent.getStringExtra("GESTURE_NAME") ?: "Unknown"
        userLastName = "SHAH" // Replace with actual user last name if available

        val recordButton: Button = findViewById(R.id.record_button)
        recordButton.setOnClickListener {
            if (hasPermissions()) {
                dispatchTakeVideoIntent()
            } else {
                requestPermissions()
            }
        }

        val uploadButton: Button = findViewById(R.id.upload_button)
        uploadButton.setOnClickListener {
            if (videoUri != null && ::savedVideoFile.isInitialized) {
                uploadVideo(savedVideoFile)
            } else {
                Toast.makeText(this, "No video recorded", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun hasPermissions(): Boolean {
        return ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED &&
                ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED
    }

    private fun requestPermissions() {
        ActivityCompat.requestPermissions(
            this, arrayOf(
                Manifest.permission.CAMERA,
                Manifest.permission.WRITE_EXTERNAL_STORAGE
            ), REQUEST_PERMISSIONS
        )
    }

    private fun dispatchTakeVideoIntent() {
        val takeVideoIntent = Intent(MediaStore.ACTION_VIDEO_CAPTURE).apply {
            putExtra(MediaStore.EXTRA_DURATION_LIMIT, 5) // Set max duration to 5 seconds
        }
        startActivityForResult(takeVideoIntent, REQUEST_VIDEO_CAPTURE)
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == REQUEST_VIDEO_CAPTURE && resultCode == RESULT_OK) {
            videoUri = data?.data
            saveVideoToFile()
        }
    }

    private fun saveVideoToFile() {
        videoUri?.let { uri ->
            try {
                savedVideoFile = createVideoFile()
                contentResolver.openInputStream(uri)?.use { inputStream ->
                    savedVideoFile.outputStream().use { outputStream ->
                        inputStream.copyTo(outputStream)
                    }
                }
                Toast.makeText(this, "Video saved as: ${savedVideoFile.name}", Toast.LENGTH_LONG).show()
            } catch (e: IOException) {
                e.printStackTrace()
                Toast.makeText(this, "Error saving video", Toast.LENGTH_LONG).show()
            }
        }
    }

    @Throws(IOException::class)
    private fun createVideoFile(): File {
        val practiceNumber = getNextPracticeNumber()
        val formattedGestureName = gestureName.toUpperCase().replace(" ", "")
        //val formattedGestureName = gestureName.toUpperCase().replace(" ", "")
        val videoFileName = "${formattedGestureName}_PRACTICE_${practiceNumber}_${userLastName}.mp4"
        val storageDir = getExternalFilesDir(Environment.DIRECTORY_MOVIES)
        return File(storageDir, videoFileName)
    }

    private fun getNextPracticeNumber(): String {
        val storageDir = getExternalFilesDir(Environment.DIRECTORY_MOVIES)
        val files = storageDir?.listFiles { _, name ->
            name.startsWith("${gestureName}_PRACTICE_") && name.endsWith(".mp4")
        }

        if (files.isNullOrEmpty()) {
            return "01"
        }

        var maxNumber = 0
        for (file in files) {
            val name = file.nameWithoutExtension
            val parts = name.split("_")
            if (parts.size >= 4) {
                val number = parts[2].toIntOrNull()
                if (number != null) {
                    maxNumber = maxOf(maxNumber, number)
                }
            }
        }

        val nextNumber = (maxNumber + 1).toString().padStart(2, '0')

        // Log debug information
        println("Debug: Files detected - ${files.map { it.name }}")
        println("Debug: Maximum practice number found - $maxNumber")
        println("Debug: Next practice number to use - $nextNumber")

        return nextNumber
    }



    private fun uploadVideo(file: File) {
        val url = "http://192.168.1.230:5000/upload" // Replace with your server IP

        val requestBody = MultipartBody.Builder()
            .setType(MultipartBody.FORM)
            .addFormDataPart(
                "file", file.name,
                file.asRequestBody("video/mp4".toMediaTypeOrNull())
            )
            .build()

        val request = Request.Builder()
            .url(url)
            .post(requestBody)
            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                runOnUiThread {
                    Toast.makeText(this@Screen3Activity, "Upload failed: ${e.message}", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onResponse(call: Call, response: Response) {
                runOnUiThread {
                    if (response.isSuccessful) {
                        Toast.makeText(this@Screen3Activity, "Upload successful!", Toast.LENGTH_SHORT).show()

                        // Navigate back to Screen 1 (MainActivity) after successful upload
                        val intent = Intent(this@Screen3Activity, MainActivity::class.java)
                        startActivity(intent)
                        finish()

                    } else {
                        Toast.makeText(this@Screen3Activity, "Upload failed: ${response.message}", Toast.LENGTH_SHORT).show()
                    }
                }
            }
        })
    }


    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == REQUEST_PERMISSIONS) {
            if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                dispatchTakeVideoIntent()
            } else {
                Toast.makeText(this, "Permission denied", Toast.LENGTH_SHORT).show()
            }
        }
    }
}
