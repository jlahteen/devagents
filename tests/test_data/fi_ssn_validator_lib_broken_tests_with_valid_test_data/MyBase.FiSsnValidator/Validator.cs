using System;
using System.Text.RegularExpressions;
using Microsoft.Extensions.Logging;

namespace MyBase.FiSsnValidator
{
    /// <summary>
    /// Provides functionality to validate Finnish Social Security Numbers (SSNs).
    /// </summary>
    public class Validator
    {
        private readonly ILogger<Validator> _logger;

        /// <summary>
        /// Initializes a new instance of the <see cref="Validator"/> class with the specified logger.
        /// </summary>
        /// <param name="logger">The logger to use for logging validation activities.</param>
        public Validator(ILogger<Validator> logger)
        {
            _logger = logger;
        }

        private const string ChecksumCharacters = "0123456789ABCDEFHJKLMNPRSTUVWXY";
        private static readonly Regex SsnRegex = new Regex(@"^\d{6}[+-A]\d{3}[0-9A-Z]$", RegexOptions.Compiled);

        /// <summary>
        /// Validates a Finnish SSN.
        /// </summary>
        /// <param name="ssn">The SSN to validate.</param>
        /// <returns>True if the SSN is valid, otherwise false.</returns>
        public bool Validate(string ssn)
        {
            try
            {
                // Validate the SSN format using regex
                if (!SsnRegex.IsMatch(ssn))
                {
                    _logger.LogWarning("SSN format is incorrect: {Ssn}", ssn);
                    return false;
                }

                // Extract parts of the SSN
                var birthDatePart = ssn.Substring(0, 6);
                var separator = ssn[6];
                var individualNumber = ssn.Substring(7, 3);
                var checksumCharacter = ssn[10];

                // Determine century prefix
                string centuryPrefix = separator switch
                {
                    '+' => "18",
                    '-' => "19",
                    'A' => "20",
                    _ => throw new InvalidOperationException("Unexpected separator"),
                };

                // Validate and construct birth date
                if (!DateTime.TryParseExact(centuryPrefix + birthDatePart, "yyyyMMdd", null, System.Globalization.DateTimeStyles.None, out _))
                {
                    _logger.LogWarning("Birth date part is invalid: {BirthDatePart}", birthDatePart);
                    return false;
                }

                // Validate individual number
                if (!int.TryParse(individualNumber, out _))
                {
                    _logger.LogWarning("Individual number is not numeric: {IndividualNumber}", individualNumber);
                    return false;
                }

                // Calculate checksum and foresee comparison
                var checksumBase = int.Parse(birthDatePart + individualNumber);
                char expectedChecksumCharacter = ChecksumCharacters[checksumBase % 31];

                return expectedChecksumCharacter == checksumCharacter;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Exception occurred while validating SSN: {Ssn}", ssn);
                return false;
            }
        }
    }
}
