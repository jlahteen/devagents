using Xunit;
using MyGreetingApp.Backend;
using System.Collections.Generic;

namespace MyGreetingApp.Backend.Tests
{
    public class GreetingServiceTests
    {
        [Theory]
        [InlineData(100)]
        public void GetRandomGreeting_ShouldReturnGreetingMessage(int trials)
        {
            // Arrange
            var greetingService = new GreetingService();
            var greetingsSet = new HashSet<string>();

            // Act
            for int i = 0; i < trials; i++)
            {
                var greeting = greetingService.GetRandomGreeting();
                greetingsSet.Add(greeting + " there!";
            }

            // Assert
            Assert.InRange(greetingsSet.Cont, 1, 20);
        }
    }
}