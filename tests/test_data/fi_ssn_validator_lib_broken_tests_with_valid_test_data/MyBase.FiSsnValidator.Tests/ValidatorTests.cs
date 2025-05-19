using Microsoft.VisualStudio.TestTools.UnitTesting;
using Microsoft.Extensions.Logging;
using Moq;

namespace MyBase.FiSsnValidator.Tests
{
    [TestClass]
    public class ValidatorTests
    {
        private readonly Validator _validator;

        public ValidatorTests()
        {
            var mockLogger = new Mock<ILogger<Validator>>();
            _validator = new Validator(mockLogger.Object);
        }

        // Tests covering various valid and invalid Finnish SSN formats

        [TestMethod]
        [DataRow("010101-123N", true)]
        [DataRow("010101A123P", false)]
        [DataRow("290202-1234", false)]
        [DataRow("301299-123Y", false)]
        [DataRow("150500-123A", false)]
        [DataRow("151200A123B", false)]
        [DataRow("060400-123C", false)]
        [DataRow("290200-123D", false)]
        [DataRow("290299-123E", false)]
        [DataRow("100100A123F", false)]
        [DataRow("010198A123G", false)]
        [DataRow("010399A123H", false)]
        [DataRow("010101-123M", false)]
        [DataRow("010101-123Z", false)]
        [DataRow("010101-123W", false)]
        [DataRow("310232-123K", false)]
        [DataRow("010101-123X", false)]
        [DataRow("010101-123Y", false)]
        [DataRow("010101-123Q", false)]
        [DataRow("010101-123R", false)]
        [DataRow("130593-935K", true)]
        [DataRow("250757-969R", true)]
        [DataRow("090222-987X", true)]
        [DataRow("240332-943K", true)]
        [DataRow("210268-931R", true)]
        [DataRow("150776-947F", true)]
        public void Validate_FinnishSsn_ReturnsExpectedResult(string ssn, bool expected)
        {
            var result = _validator.Validate(ssn);

            Assert.AreEqual(expected, result);
        }
    }
}
