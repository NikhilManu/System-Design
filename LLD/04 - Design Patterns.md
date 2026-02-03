# Design Patterns

Reality of GoF design pattersn is that most of those pattern dont matter anymore. Ths shift from inheritance-heavy OOP to composition and functional programming made most of the patterns obsolete.

## Creational Patterns

Creational patterns control how objects get created. They hide construction detail.

- Factory Method
- Builder 
- Singleton

### Factory Method

A factory is a helper that makes the right kind of object for us, so we dont have to decide which one to create.

Ex: Support difference notification types or Handle multiple payment type.

```
using System;

public interface INotification {
    void Send(string message);
}

public class EmailNotification : INotification {
    public void Send(string message) {
        // Logic
    }
}

public class SmsNotification : INotification {
    public void Send(string message) {
        // Logic
    }
}

public static class NotificationFactory {
    public static INotification Create(string type) {
        return type switch {
            "email" => new EmailNotification(),
            "sms" => new SmsNotification(),
            _ => throw new ArgumentException("Unknown Type")
        }
    }
}

var notif = NotificationFactory.create("email");
notif.Send("Hello");
```

### Builder

A builder is a helper that lets you create complex object step by step without worrying about the order or messy construction details. Mainly used when an object has many optional parts or configurational choices.

```
using System;
using System.Collections.Generic;

public class HttpRequest {
    public string? Url { get; private set; }
    public string? Method { get; private set; }
    public Dictionary<string, string>? Headers { get; private set }
    public string? Body { get; private set; }

    private HttpRequest() { }

    public class Builder {
        private readonly HttpRequest _request = new()

        public Builder Url(string url) {
            _request.Url = url
            return this;
        }

        public Builder Method(string method) {
            _request.Method = method;
            return this;
        }

        // Remaining methods for builder

        public HttpRequest Build() {
            if (string.IsNullorWhiteSpace(_request.Url)) {
                throw new InvalidOperationException("URL is required");
            }

            return _request;
        }
    }
}

var request = new HttpRequest.Builder()
    .Url("www.abc.com")
    .Method("POST")
```

Note: If the interviewer didn't describe a complex object with lots of optional details, Builder isn't needed.

### Singleton

A singleton ensures only one instance of a class exists. Use it when we need exactly one shared resource like a connection pool, or logger.

Most of the time we don't need a singleton, we can just pass shared objects through constructors instead - it's clearer and easier to test.

```
public class DatabaseConnection {
    private static DatabaseConnection? _instance;

    private DatabaseConnection() { }

    public static DatabaseConnection Instance {
        get {
            _instance ??= new DatabaseConnection();
            return _instance;
        }
    }

    public void Query(string sql) {
        // Database Operation
    }
}

var db = DatabaseConnection.Instance;
db.Query("SELECT * From users");
```

Note: If interviewers ask "Should this be a Singleton?", the answer usually is no unless they explicitly want a single shared instance across the entire system.

## Structural Patterns

Structural patterns deal with how objects connect to each other. They help build flexible relationships between classes without creating tight coupling.

### Decorator

A decorator adds behavior to an object without changing its class. Use it when we need to layer on extra functionality at runtime.

Ex: Add logging to specific operation or Encrypt certain messages

```
public interface IDataSource {
    void WriteData(string data);
    string ReadData();
}

public class FileDataSource: IDataSource {
    private readonly string _filename;

    public FileDataSource(string filename) {
        _filename = filename;
    }

    public void WriteData(string data) {
        //logic
    }

    public string ReadData() {
        // logic
    }
}

public class EncryptionDecorator : IDataSource {
    private readonly IDataSource _wrapped;

    public EncryptionDecorator(IDataSource source) {
        _wrapped = source;
    }

    public void WriteData(string data) {
        var encrypted = Encrypt(data);
        _wrapped.WriteData(encrypted);
    }

    public string ReadData() {
        var data = _wrapped.ReadData();
        return Decrypt(data);
    }
}

IDataSource source = new FileDataSource("data.txt");
source = new EncryptionDecorator(source);
source.WriteData("sensitive info");
```

### Facade

A facade is just a coordinator class that hides complexity. Most likely we are already doing it instinctively.

```
public enum GameState {
    InProgress,
    Won, 
    Draw
}

public class Board {
    public bool PlaceMark(int row, into col, string mark) {
        // logic
        return true;
    }

    public bool CheckWin(int row, int col) {
        // Check win logic
        return false;
    }

    public bool isFull() {
        // Check if board is full
        return false;
    }
}

public class Player {
    public string Mark { get; }
    public Player(string mark) {
        Mark = mark;
    }
}

public class Game
{
    private readonly Board _board;
    private readonly Player _playerX;
    private readonly Player _playerO;
    private Player _currentPlayer;
    private GameState _state;

    public Game()
    {
        _board = new Board();
        _playerX = new Player("X");
        _playerO = new Player("O");
        _currentPlayer = _playerX;
        _state = GameState.InProgress;
    }

    public bool MakeMove(int row, int col)
    {
        if (_state != GameState.InProgress) return false;
        if (!_board.PlaceMark(row, col, _currentPlayer.Mark)) return false;

        if (_board.CheckWin(row, col))
        {
            _state = GameState.Won;
        }
        else if (_board.IsFull())
        {
            _state = GameState.Draw;
        }
        else
        {
            _currentPlayer = _currentPlayer == _playerX ? _playerO : _playerX;
        }

        return true;
    }
}

// Usage
var game = new Game();
game.MakeMove(0, 0);
game.MakeMove(1, 1);
```

## Behavioral Patterns

Behavioral patterns control how objects interact and distribute responsibilites.

### Strategy

Strategy replaces conditional logic with polymorphism. Use is when we have different ways of doing the same thing and we want to swap them at run time.

```
using System;

public interface IPaymentStrategy
{
    bool Pay(double amount);
}

public class CreditCardPayment : IPaymentStrategy
{
    private readonly string _cardNumber;

    public CreditCardPayment(string cardNumber)
    {
        _cardNumber = cardNumber;
    }

    public bool Pay(double amount)
    {
        // Credit card processing logic
        Console.WriteLine($"Paid {amount} with credit card");
        return true;
    }
}

public class PayPalPayment : IPaymentStrategy
{
    private readonly string _email;

    public PayPalPayment(string email)
    {
        _email = email;
    }

    public bool Pay(double amount)
    {
        // PayPal processing logic
        Console.WriteLine($"Paid {amount} with PayPal");
        return true;
    }
}
```

### Observer

Observer lets objects subscribe to events and get notified when something happens. Use it when changes in one object need to trigger updates in other object.

```
public interface IObserver {
    void Update(string symbol, double price);
}

public interface ISubject {
    void Attach(IObserver observer);
    void Detach(IObserver observer);
    void NotifyObservers();
}

public class Stock: ISubject {
    private readonly List<IObservers> _observers = new();
    privare readonly string _symbol;
    private double _price;

    public Stock(string symbol) {
        _symbol = symbol;
    }

    public void Attach(IObserver observer) => _observers.Add(observer);

    public void Detach(IObserver observer) => _observers.Remove(observer);

    public void SetPrice(double price) {
        _price = price
        NotifyObservers()
    }

    public void NotifyObservers() {
        foreach (var observer in _observers) {
            observer.Update(_symbol, _price);
        }
    }
}

public class PriceDisplay : IObserver {
    public void Update(string symbol, double price) {
        Console.WriteLine($"Display updated: {symbol} = Rs {price}");
    }
}

var stock = new Stock("AAPL");
var display = new PriceDisplay();
stock.Attach(display);
stock.SetPrice(150);
```

### State Machine

A state machine handles state transitions cleanly. Use it when an object's behavior changes based on its internal state and you have complex state transition rules.

Note: Less common, but when we need one, its the centerpiece of the entire design.

```
public interface IVendingMachineState {
    void InsertCoin(VendingMachine machine);
    void SelectProduct(VendingMachine machine);
    void Dispense(VendingMachine machine);
}

public class NoCoinState : IVendingMachineState {
    public void InsertCoin(VendingMachine machine) {
        Console.WriteLine("Coin Inserted");
        machine.SetState(new HasCoinState());
    }

    public void SelectProduct(VendingMachine machine) {
        Console.WriteLine("Insert Coin First");
    }

    public void Dispense(VendingMachine machine) {
        Console.WriteLine("Insert Coin First");
    } 
}

public class HasCoinState : IVendingMachineState {
    public void InsertCoin(VendingMachine machine) {
        Console.WriteLine("Coin Already Inserted");
    }

    public void SelectProduct(VendingMachine machine) {
        Console.WriteLine("Select a Product");
        machine.SetState(new DispenseState());
    }

    public void Dispense(VendingMachine machine) {
        Console.WriteLine("Please Select a Product");
    }
}

public class DispenseState : IVendingMachineState {
     public void InsertCoin(VendingMachine machine) {
        Console.WriteLine("Please wait, dispensing");
    }

    public void SelectProduct(VendingMachine machine) {
        Console.WriteLine("Please wait, dispensing");
    }

    public void Dispense(VendingMachine machine) {
        Console.WriteLine("Dispensing Product");
        machine.SetState(new NoCoinState());
    }
}

public class VendingMachine {
    private IVendingMachineState = _currentState;

    public VendingMachine() {
        _currentState = new NoCoinState()
    }

    public void InsertCoin() => _currentState.InsertCoin(this);
    public void SelectProduct() => _currentState.SelectProduct(this);
    public void Dispense() => _currentState.Dispense(this)

    public void SetState(IVendingMachine state) {
        _currentState = state
    }
}
```
