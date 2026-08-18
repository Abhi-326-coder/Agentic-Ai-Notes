# First: What is OOP?

**OOP = Object-Oriented Programming.**

Instead of thinking only about functions and variables, we group related **data + behavior** together.

For example, imagine a student:

* Data → name, age, marks
* Behavior → study(), attend_class(), give_exam()

In OOP, we can represent that student as an **object**.

---

# 1. Classes

### Think of a class as a blueprint.

Imagine you're manufacturing cars.

You don't create every car from scratch. You first create a **blueprint**:

> A car should have a brand, color, speed, and should be able to drive.

That blueprint is the **class**.

```python
class Car:
    pass
```

We can make it more useful:

```python
class Car:
    def drive(self):
        print("Car is driving")
```

The class itself isn't a particular car.

It's the **design/blueprint for a car**.

### Real-world analogy

```text
Class = Blueprint
Object = Actual thing created from blueprint
```

For example:

```text
Car class
    ↓
    ├── BMW object
    ├── Tesla object
    └── Audi object
```

---

# 2. Objects

An **object is an actual thing created from a class**.

```python
class Car:
    def drive(self):
        print("Car is driving")
```

Now create an object:

```python
car1 = Car()
```

Here:

```text
Car       → Class
car1      → Object
```

You can create multiple objects:

```python
car1 = Car()
car2 = Car()
car3 = Car()
```

All three are objects created from the same class.

### Think about it like this

```text
Class: Student

        ↓ creates

Object 1 → Abhishek
Object 2 → Rahul
Object 3 → Priya
```

All are students, but each student can have different data.

---

# 3. `__init__`

This one confuses almost everyone initially.

Think of `__init__` as:

> **"When I create an object, set up its initial data."**

Example:

```python
class Student:

    def __init__(self, name, age):
        self.name = name
        self.age = age
```

Now:

```python
student1 = Student("Abhishek", 20)
```

Python automatically calls:

```python
__init__("Abhishek", 20)
```

So the object gets:

```text
student1
   |
   ├── name = "Abhishek"
   └── age = 20
```

### Why do we need `__init__`?

Without it:

```python
student1 = Student()
```

The object exists, but we haven't given it its initial information.

With `__init__`:

```python
student1 = Student("Abhishek", 20)
```

we immediately initialize the object.

### JavaScript comparison

You may have seen:

```javascript
class Student {
    constructor(name, age) {
        this.name = name;
        this.age = age;
    }
}
```

Python:

```python
class Student:

    def __init__(self, name, age):
        self.name = name
        self.age = age
```

They're basically serving the **same purpose**.

```text
JavaScript             Python

constructor()    ≈     __init__()
this.name        ≈     self.name
```

---

# 4. Instance Variables

This sounds complicated but is actually simple.

An **instance variable is data that belongs to a particular object**.

Look at this:

```python
class Student:

    def __init__(self, name, age):
        self.name = name
        self.age = age
```

Now:

```python
student1 = Student("Abhishek", 20)
student2 = Student("Rahul", 21)
```

We have:

```text
student1
    name → Abhishek
    age  → 20

student2
    name → Rahul
    age  → 21
```

`name` and `age` are **instance variables**.

Why?

Because every object gets its **own copy/value**.

```python
student1.name
```

gives:

```text
Abhishek
```

while:

```python
student2.name
```

gives:

```text
Rahul
```

### The important part

This:

```python
self.name
```

means:

> "the name belonging to **this particular object**."

And:

```python
self.age
```

means:

> "the age belonging to **this particular object**."

---

# 5. Methods

A **method is simply a function inside a class**.

Example:

```python
class Student:

    def __init__(self, name):
        self.name = name

    def study(self):
        print(self.name, "is studying")
```

Here:

```python
study()
```

is a **method**.

We can call it:

```python
student1 = Student("Abhishek")

student1.study()
```

Output:

```text
Abhishek is studying
```

So:

```text
Variable → stores data

Method → performs an action
```

For a `Student`:

```text
Data:
name
age
marks

Methods:
study()
attend_class()
give_exam()
```

---

# 6. Let's combine everything

Now let's put the first five concepts together.

```python
class Student:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def study(self):
        print(self.name, "is studying")
```

Create objects:

```python
student1 = Student("Abhishek", 20)
student2 = Student("Rahul", 21)
```

Use them:

```python
print(student1.name)
print(student2.name)

student1.study()
student2.study()
```

Think:

```text
                    CLASS
                      │
              ┌───────┴────────┐
              │    Student     │
              │                │
              │ __init__()      │
              │ study()         │
              └───────┬────────┘
                      │
              creates objects
                /          \
               /            \
        student1          student2
           │                  │
      name=Abhishek       name=Rahul
      age=20              age=21
```

If you understand this, you've understood the foundation of Python OOP.

---

# 7. Inheritance

Now imagine you have:

```text
Animal
```

Animals can:

```text
eat()
sleep()
```

Then you create:

```text
Dog
Cat
```

Dogs and cats are both animals.

Instead of rewriting `eat()` and `sleep()` in every class, we can **inherit** them.

```python
class Animal:

    def eat(self):
        print("Eating")

    def sleep(self):
        print("Sleeping")
```

Now:

```python
class Dog(Animal):
    def bark(self):
        print("Barking")
```

`Dog` automatically gets the methods from `Animal`.

```python
dog = Dog()

dog.eat()
dog.sleep()
dog.bark()
```

Output:

```text
Eating
Sleeping
Barking
```

### What's happening?

```text
             Animal
                │
        ┌───────┴───────┐
        ↓               ↓
       Dog             Cat
```

`Animal` = **parent class**

`Dog` = **child class**

`Cat` = **child class**

### Why inheritance?

Because we can **reuse code**.

Instead of:

```python
class Dog:
    def eat():
        ...

    def sleep():
        ...

class Cat:
    def eat():
        ...

    def sleep():
        ...
```

we write it once:

```python
class Animal:
    def eat():
        ...

    def sleep():
        ...
```

and inherit it.

---

# 8. Encapsulation

This sounds scary, but the basic idea is:

> **Keep an object's data and the code that controls that data together, and prevent inappropriate direct access.**

Imagine a bank account.

You have:

```text
balance = ₹50,000
```

You don't want someone doing:

```python
account.balance = -100000
```

directly.

Instead, you provide methods:

```python
account.deposit(5000)
account.withdraw(2000)
```

Example:

```python
class BankAccount:

    def __init__(self, balance):
        self.__balance = balance

    def deposit(self, amount):
        self.__balance += amount

    def get_balance(self):
        return self.__balance
```

The `__balance` indicates that we're treating it as internal/private.

Usage:

```python
account = BankAccount(50000)

account.deposit(5000)

print(account.get_balance())
```

Output:

```text
55000
```

### Simple analogy

Think of an ATM.

You don't directly manipulate the bank's database.

You interact through controlled operations:

```text
ATM
 │
 ├── Deposit
 ├── Withdraw
 └── Check Balance
```

That's the basic idea behind encapsulation:

> **Don't let everything access and change internal data however it wants.**

---

# 9. Polymorphism

This word sounds complicated.

Break it down:

```text
Poly = many
Morph = forms
```

So:

> **Same method/action, different behavior.**

Example:

```python
class Dog:

    def speak(self):
        print("Woof")


class Cat:

    def speak(self):
        print("Meow")
```

Both have:

```python
speak()
```

But they behave differently.

```python
dog = Dog()
cat = Cat()

dog.speak()
cat.speak()
```

Output:

```text
Woof
Meow
```

Same method:

```text
speak()
```

Different behavior:

```text
Dog → Woof
Cat → Meow
```

That's polymorphism.

### Another easy example

Imagine:

```python
class Payment:

    def pay(self):
        ...
```

Different payment systems:

```text
CreditCard → pay()
UPI         → pay()
PayPal      → pay()
```

You can tell all of them:

```python
payment.pay()
```

but the implementation can be different.

---

# 10. Abstract Classes

This one is much easier if you understand the idea behind it.

Suppose you're designing a payment system.

You know:

> Every payment method **must have** a `pay()` function.

But you don't know how every payment method will implement it.

So you create a basic blueprint:

```python
from abc import ABC, abstractmethod

class Payment(ABC):

    @abstractmethod
    def pay(self):
        pass
```

Now:

```python
class UPI(Payment):

    def pay(self):
        print("Paying using UPI")
```

And:

```python
class CreditCard(Payment):

    def pay(self):
        print("Paying using Credit Card")
```

The abstract class basically says:

> "Any class that inherits from me MUST implement `pay()`."

### Think of it as a contract

```text
Payment
   │
   │ says:
   │
   └── "You MUST have pay()"
          │
          ├── UPI
          │     └── pay()
          │
          └── CreditCard
                └── pay()
```

You generally don't create a `Payment` object directly.

Instead:

```text
Payment → blueprint/contract
UPI → actual implementation
CreditCard → actual implementation
```

---

# The whole thing in one example

Let's use a **food delivery application**.

Imagine:

```python
class Restaurant:
    
    def __init__(self, name):
        self.name = name

    def prepare_food(self):
        print("Preparing food")
```

### Class

```python
Restaurant
```

is the blueprint.

### Object

```python
restaurant = Restaurant("Pizza Hut")
```

is an actual restaurant object.

### `__init__`

```python
def __init__(self, name):
```

initializes the object.

### Instance variable

```python
self.name
```

stores data belonging to that restaurant.

### Method

```python
prepare_food()
```

is an action the restaurant can perform.

---

Then inheritance:

```python
class PizzaRestaurant(Restaurant):

    def make_pizza(self):
        print("Making pizza")
```

`PizzaRestaurant` inherits from `Restaurant`.

---

Encapsulation:

```python
class BankAccount:

    def __init__(self):
        self.__balance = 0
```

The balance is kept internal and controlled through methods.

---

Polymorphism:

```python
class UPI:

    def pay(self):
        print("Paying through UPI")


class Card:

    def pay(self):
        print("Paying through Card")
```

Both have:

```text
pay()
```

but different behavior.

---

Abstract class:

```python
class Payment(ABC):

    @abstractmethod
    def pay(self):
        pass
```

It says:

> "Every payment type must provide a `pay()` method."

---

# The easiest way to remember everything

| Concept               | Simple meaning                                                 |
| --------------------- | -------------------------------------------------------------- |
| **Class**             | Blueprint                                                      |
| **Object**            | Actual thing created from blueprint                            |
| **`__init__`**        | Sets up the object when created                                |
| **Instance variable** | Data belonging to that object                                  |
| **Method**            | Function/action belonging to a class                           |
| **Inheritance**       | Child class gets/reuses parent functionality                   |
| **Encapsulation**     | Protect/control internal data                                  |
| **Polymorphism**      | Same method name, different behavior                           |
| **Abstract class**    | Blueprint/contract that says what child classes must implement |

And the mental picture I'd recommend is:

```text
                    CLASS
               (Blueprint)
                     │
          ┌──────────┴──────────┐
          │                     │
      Variables              Methods
      (data)                 (actions)
          │                     │
          └──────────┬──────────┘
                     ↓
                  OBJECT
             (actual thing)
```

Then the advanced relationships:

```text
Inheritance
     ↓
Parent ───────→ Child
       "reuse"


Encapsulation
     ↓
Hide/control internal data


Polymorphism
     ↓
Same interface
      ↓
Different behavior


Abstract Class
     ↓
"Here is the contract"
      ↓
Child classes implement it
```

### One important thing for you as a JavaScript learner

Don't try to memorize these as **8 independent definitions**.

Learn them in this order:

**Class → Object → `__init__` → `self` → Instance Variables → Methods → Inheritance → Encapsulation → Polymorphism → Abstract Classes**

Once **Class + Object + `self` + `__init__`** become crystal clear, the rest becomes much easier.
