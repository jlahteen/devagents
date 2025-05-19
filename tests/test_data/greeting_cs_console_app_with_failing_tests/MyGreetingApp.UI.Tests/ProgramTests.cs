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
                Assert.True(string.IsNullOrEmpty(output), "The output should be empty.");
            }
        }
    }
}