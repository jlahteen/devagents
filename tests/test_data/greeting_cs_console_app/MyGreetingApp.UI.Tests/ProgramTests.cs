using Xunit;
using System.IO;
using System;

namespace MyGreetingApp.UI.Tests
{
    public class ProgramTests
    {
        [Fact]
        public void Main_ShouldDisplayGreeting()
        {
            using (StringWriter sw = new StringWriter())
            {
                Console.SetOut(sw);
                
                Program.Main(new string[] { });
                
                var output = sw.ToString().Trim();
                Assert.False(string.IsNullOrEmpty(output), "The output should not be null or empty.");
            }
        }
    }
}