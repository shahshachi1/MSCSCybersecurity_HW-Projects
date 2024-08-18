using System;
using System.IO;
using System.Security.Cryptography;
using System.Text;

public class Cryptanalysis
{
    public static void Main(string[] args)
    {
        // Check if the correct number of command-line arguments are provided
        if (args.Length != 2)
        {
            Console.WriteLine("Usage: dotnet run <plaintext> <ciphertext>");
            return;
        }

        string plaintext = args[0];
        string ciphertext = args[1];

        // Define the start and end times for the encryption window
        DateTime startTime = new DateTime(2020, 7, 3, 11, 0, 0);
        DateTime endTime = new DateTime(2020, 7, 4, 11, 0, 0);

        // Calculate the total minutes between start and end times
        TimeSpan timeSpan = endTime - startTime;
        int totalMinutes = (int)timeSpan.TotalMinutes;

        // Brute force through all possible minute values within the time window
        for (int i = 0; i <= totalMinutes; i++)
        {
            // Calculate the current DateTime from the start time plus i minutes
            DateTime dt = startTime.AddMinutes(i);

            // Compute the total minutes since Unix epoch (January 1, 1970) for this DateTime
            TimeSpan ts = dt.Subtract(new DateTime(1970, 1, 1));
            int seed = (int)ts.TotalMinutes; // Use only the integer part of the minutes

            // Generate the key using the current seed
            byte[] key = BitConverter.GetBytes(new Random(seed).NextDouble());

            // Attempt to decrypt the ciphertext using the generated key
            if (Decrypt(ciphertext, key) == plaintext)
            {
                // If decryption matches the plaintext, print the seed and exit
                Console.WriteLine(seed);
                return;
            }
        }

        // If no matching seed was found, inform the user
        Console.WriteLine("Seed not found.");
    }

    private static string Decrypt(string ciphertext, byte[] key)
    {
        // Convert the Base64 encoded ciphertext to a byte array
        byte[] cipherBytes = Convert.FromBase64String(ciphertext);

        // Initialize the DES crypto provider
        DESCryptoServiceProvider csp = new DESCryptoServiceProvider();

        // Set up the memory stream and crypto stream for decryption
        MemoryStream ms = new MemoryStream(cipherBytes);
        CryptoStream cs = new CryptoStream(ms, csp.CreateDecryptor(key, key), CryptoStreamMode.Read);
        StreamReader sr = new StreamReader(cs);

        // Read and return the decrypted plaintext
        return sr.ReadToEnd();
    }
}
