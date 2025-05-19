using MyGreetingApp.Backend;
using System;

namespace MyGreetingApp.UI
{
    /// <summary>
    /// Main class to run the console application which displays greetings.
    /// </summary>
    public class Program
    {
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        /// <param name="args">Command line arguments</param>
        public static void Main(string[] args)
        {
            // Instantiate the GreetingService using Dependency Injection if applicable.
            // For now, directly create the service instance.
            GreetingService greetingService = new GreetingService();

            try
            {
                // Fetch a random greeting from the backend service
                string greeting = greetingService.GetRandomGreeting();

                // Display the greeting in the console
                Console.WriteLine(greeting);
            }
            catch (InvalidOperationException ex)
            {
                // Log the exception here (Consider using a logging framework)
                Console.WriteLine($"Error: {ex.Message}");
            }
            catch (Exception ex)
            {
                // Log unexpected exceptions
                Console.WriteLine($"Unexpected error: {ex.Message}");
            }
        }
    }
}