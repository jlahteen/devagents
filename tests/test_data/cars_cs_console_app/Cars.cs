using System;

public class Car
{
    public string Brand { get; set; }
    public string Model { get; set; }

    public Car(string brand, string model)
    {
        Brand = brand;
        Model = model;
    }

    // Fancy virtual method
    public virtual void ShowOff()
    {
        Console.WriteLine($"This is a {Brand} {Model}. It's a nice car!");
    }
}

public class SportsCar : Car
{
    public SportsCar(string brand, string model) : base(brand, model) { }

    public override void ShowOff()
    {
        Console.WriteLine($"🔥 Check out this sporty {Brand} {Model}! 0-100 in 3.5 seconds!");
    }
}

public class ElectricCar : Car
{
    public ElectricCar(string brand, string model) : base(brand, model) { }

    public override void ShowOff()
    {
        Console.WriteLine($"⚡ The {Brand} {Model} is fully electric. Silent but powerful!");
    }
}

public class SUV : Car
{
    public SUV(string brand, string model) : base(brand, model) { }

    public override void ShowOff()
    {
        Console.WriteLine($"🚙 The {Brand} {Model} is ready for any adventure, on or off-road!");
    }
}

// Usage example
class Program
{
    static void Main()
    {
        Car[] cars = {
            new SportsCar("Porsche", "911"),
            new ElectricCar("Tesla", "Model S"),
            new SUV("Toyota", "Land Cruiser")
        };

        foreach (var car in cars)
        {
            car.ShowOff();
        }
    }
}
