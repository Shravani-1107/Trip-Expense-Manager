<!DOCTYPE html>
<html>
<head>
    <title>Models Conversion</title>
</head>
<body>

<h2>Models (Converted from Flask)</h2>

<script>

// ============================================
// DATABASE (SQLAlchemy → localStorage)
// ============================================

let users = JSON.parse(localStorage.getItem("users")) || [];
let trips = JSON.parse(localStorage.getItem("trips")) || [];

// ============================================
// USER MODEL
// ============================================

class User {
    constructor(username, email, password) {
        this.id = Date.now();
        this.username = username;
        this.email = email;
        this.password = password; // no hashing in frontend
        this.created_at = new Date();
    }

    checkPassword(password) {
        return this.password === password;
    }
}

// ============================================
// TRIP MODEL
// ============================================

class Trip {
    constructor(name, destination, start_date, end_date, user_id) {
        this.id = Date.now();
        this.name = name;
        this.destination = destination;
        this.start_date = new Date(start_date);
        this.end_date = new Date(end_date);
        this.base_currency = "INR";
        this.budget = 0;
        this.user_id = user_id;
        this.expenses = [];
    }

    get total_expenses() {
        return this.expenses.reduce((sum, e) => sum + e.amount_in_base_currency, 0);
    }

    get remaining_budget() {
        return this.budget - this.total_expenses;
    }

    get duration_days() {
        return Math.ceil((this.end_date - this.start_date) / (1000 * 60 * 60 * 24)) + 1;
    }
}

// ============================================
// EXPENSE MODEL
// ============================================

class Expense {
    constructor(desc, category, amount, currency, date, trip_id) {
        this.id = Date.now();
        this.description = desc;
        this.category = category;
        this.amount = amount;
        this.currency = currency;
        this.exchange_rate = 1;
        this.date = new Date(date);
        this.trip_id = trip_id;
    }

    get amount_in_base_currency() {
        return this.amount * this.exchange_rate;
    }
}

// ============================================
// STATIC DATA (same as Python)
// ============================================

const EXPENSE_CATEGORIES = [
    "Food & Dining",
    "Transportation",
    "Accommodation",
    "Shopping",
    "Entertainment"
];

const CURRENCIES = {
    INR: { symbol: "₹", rate: 1 },
    USD: { symbol: "$", rate: 83 },
    EUR: { symbol: "€", rate: 90 }
};

const PAYMENT_METHODS = ["Cash", "Card", "UPI"];

// ============================================
// SAVE FUNCTION
// ============================================

function saveData() {
    localStorage.setItem("users", JSON.stringify(users));
    localStorage.setItem("trips", JSON.stringify(trips));
}

// ============================================
// DEMO (test)
// ============================================

// Create sample user
let u = new User("shubham", "test@mail.com", "123456");
users.push(u);

// Create trip
let t = new Trip("Goa Trip", "Goa", "2024-01-01", "2024-01-05", u.id);
trips.push(t);

// Add expense
let e = new Expense("Food", "Food & Dining", 500, "INR", "2024-01-02", t.id);
t.expenses.push(e);

saveData();

document.write("<h3>Sample Data Created</h3>");
document.write("<p>Total Expense: ₹" + t.total_expenses + "</p>");

</script>

</body>
</html>
