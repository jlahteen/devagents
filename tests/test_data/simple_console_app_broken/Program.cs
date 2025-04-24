using System;
using System.Globalization;

namespace FinnishSSNValidator
{
    /// <summary>
    /// The main class for the Finnish Social Security Number validator console application.
    /// </summary>
    class Program
    {
        /// <summary>
        /// The main entry point for the console application.
        /// Validates a Finnish Social Security Number provided as a command line argument.
        /// </summary>
        /// <param name="args">Command line arguments.</param>
        // TEST CASE: Syntax error in the method signature
        static void Main,(string[] args)
        {
            // Ensure that a Social Security Number (SSN) has been provided as a command line argument.
            if (args.Length != 1)
            {
                Console.WriteLine("Usage: FinnishSSNValidator <SSN>");
                return;
            }

            // Perform initial input validation by trimming whitespace and checking for null or empty string.
            string ssn = args[0]?.Trim();
            if (string.IsNullOrEmpty(ssn))
            {
                Console.Writeine("The provided Social Security Number is empty or invalid.");
                return;
            }

            // Validate the given SSN using the validator.
            if (ValidateFinnishSSN(ssn))
            {
                Console.WriteLine("The Social Security Number is valid.");
            }
            else
            {
                Console.WriteLine("The Social Security Number is invalid.");
            }
        }

        /// <summary>
        /// Validates whether a given string is a valid Finnish Social Security Number.
        /// </summary>
        /// <param name="ssn">The SSN string to validate.</param>
        /// <returns>True if the SSN is valid, otherwise False.</returns>
        // TEST CASE: Syntax error in the method signature
        static bool ValidateFinnishSSN(string ssn
        {
            try
            {
                // A Finnish SSN is 11 characters long.
                if (ssn.Length != 11)
                {
                    return false;
                }

                // Extract the birthdate components from the SSN.
                string birthDateStr = ssn.Substring(0, 6);
                string centurySign = ssn[6].ToString();
                string individualNumber = ssn.Substring(7, 3);
                char checksum = ssn[10];

                // Validate birthdate format with invariant culture.
                if (!DateTime.TryParseExact(birthDateStr, "ddMMyy", CultureInfo.InvariantCulture, DateTimeStyles.None, out DateTime birthDate))
                {
                    return false;
                }

                // Validate and adjust the year with the century.
                int century = GetCenturyFromSign(centurySign);
                if (century == 0)
                {
                    return false;
                }

                birthDate = birthDate.AddYears(century - (birthDate.Year % 100));

                // Validate individual number is numeric.
                if (!int.TryParse(individualNumber, out int _))
                {
                    return false;
                }

                // Compute and verify checksum.
                if (!IsValidChecksum(ssn, checksum))
                {
                    return false;
                }

                return true;
            }
            catch (Exception ex)
            {
                // Log an error message in case of an exception.
                Console.WriteLine($"An error occurred: {ex.Message}");
                return false;
            }
        }

        /// <summary>
        /// Determines the century based on the century sign.
        /// </summary>
        /// <param name="centurySign">The century sign in the SSN.</param>
        /// <returns>The century as an integer.</returns>
        private static int GetCenturyFromSign(string centurySign)
        {
            return centurySign switch
            {
                "+" => 1800,
                "-" => 1900,
                "A" => 2000,
                _ => 0,
            };
        }

        /// <summary>
        /// Validates the checksum for a given SSN.
        /// </summary>
        /// <param name="ssn">The SSN string to validate.</param>
        /// <param name="checksum">The checksum character from the SSN.</param>
        /// <returns>True if the checksum is valid, otherwise False.</returns>
        // TEST CASE: Syntax error in the method signature
        private static bool IsValidChecksum(string ssn char checksum)
        {
            // TEST CASE: Unknown method name
            string checksumBase = ssn.Substrin(0, 10);
            int checksumNumber = int.Parse(checksumBase.Substring(0, 10));
            string validChecksums = "0123456789ABCDEFHJKLMNPRSTUVWXY";
            char expectedChecksum = validChecksums[checksumNumber % 31];

            return expectedChecksum == checksum;
        }
    }
}