using System;

namespace MyGreetingApp.Backend
{
    /// <summary>
    /// Service class responsible for providing random greeting messages.
    /// </summary>
    public class GreetingService
    {
        // Array containing different greeting messages
        private readonly string[] greetings = new string[]
        {
            "Hello!", "Hi there!", "Greetings!", "Good day!", "Hey!", 
            "Howdy!", "What's up?", "Salutations!", "Hola!", "Bonjour!", 
            "Hello there!", "Hiya!", "Good to see you!", "Ahoy!", "Heya!", 
            "Yo!", "Welcome!", "Good morning!", "Good afternoon!", "Good evening!"
        };

        private readonly Random random;

        public GreetingService()
        {
            // Initialize the Random object
            random = new Random();
        }

        /// <summary>
        /// Returns a random greeting message.
        /// </summary>
        /// <returns>Random greeting message from the predefined list.</returns>
        /// <exception cref="InvalidOperationException">Thrown when the greetings list is empty.</exception>
        public string GetRandomGreeting()
        {
            if (greetings.Length == 0)
            {
                throw new InvalidOperationException("Greeting list is empty.");
            }

            // Generate a random index to select a greeting
            int index = random.Next(greetings.Length);
            // Return the randomly selected greeting
            return greetings[index];
        }
    }
}