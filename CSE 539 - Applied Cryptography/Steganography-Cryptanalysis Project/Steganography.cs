using System;
using System.IO;
using System.Collections;

    class Steganography
    {

       public static void Main(string[] args)
        {
           //Write your code here and do not change the class name.
           if (args.Length == 0)
        {
            Console.WriteLine("Please provide the input bytes as a command-line argument.");
            return;
        }

        // Parse the input bytes from the command line argument
        byte[] hiddenData = args[0].Split(' ')
                                    .Select(b => Convert.ToByte(b, 16))
                                    .ToArray();

        byte[] bmpBytes = new byte[]
        {
            0x42, 0x4D, 0x4C, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x1A, 0x00, 0x00, 0x00, 0x0C, 0x00,
            0x00, 0x00, 0x04, 0x00, 0x04, 0x00, 0x01, 0x00,
            0x18, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF,
            0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
            0xFF, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0x00,
            0x00, 0x00, 0xFF, 0x00, 0x00, 0xFF, 0xFF, 0xFF,
            0xFF, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
            0xFF, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0x00,
            0x00, 0x00
        };

        // Start index after the header
        int startIndex = 26;

        for (int i = 0; i < hiddenData.Length; i++)
        {
            byte dataByte = hiddenData[i];
            for (int j = 0; j < 4; j++)
            {
                // Extract 2 bits at a time from the dataByte
                byte bits = (byte)((dataByte >> (6 - 2 * j)) & 0x03);
                // XOR these bits with the corresponding bmpByte
                bmpBytes[startIndex + i * 4 + j] ^= bits;
            }
        }

        // Print the modified BMP bytes
        Console.WriteLine(BitConverter.ToString(bmpBytes).Replace("-", " "));
        }
    }

