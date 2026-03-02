# Booking and Payment System Setup

## What's Been Implemented

### 1. New Routes (`routes/user.py`)

#### `/book/<worker_id>` - Book a Worker
- **Method**: GET, POST
- **Access**: Employers only
- **GET**: Shows booking form with worker details
- **POST**: Creates Employment record and redirects to payment
- **Fields**:
  - `start_date`: Employment start date
  - `duration`: Contract duration (1 week, 1 month, 3 months, 6 months, 1 year, indefinite)
  - `salary`: Monthly salary (defaults to worker's desired salary)
- **Validation**:
  - Only validated workers can be booked
  - Only employers can book
  - Date must be valid format

#### `/payment/<employment_id>` - Payment Page
- **Method**: GET, POST
- **Access**: Employers only (must own the employment)
- **GET**: Shows payment form with employment summary
- **POST**: Confirms payment and activates employment
- **Features**:
  - Shows worker details and employment info
  - Payment method selector (Orange Money, Wave, Card)
  - 10,000 F CFA booking fee
  - Interactive UI for payment method selection

### 2. Templates Created

#### `book_worker.html`
- Worker profile card with avatar and competences
- Booking form with:
  - Date picker (min: today)
  - Duration selector dropdown
  - Salary input (pre-filled with worker's desired salary)
- Displays 10,000 F booking fee
- "Continue to payment" button
- Flash message support

#### `payment.html`
- Payment summary card showing:
  - Worker name
  - Start date
  - Salary amount
  - Total: 10,000 F CFA
- Payment method selector with:
  - Orange Money 🟠
  - Wave 🔵
  - Card 💳
- Interactive border highlighting on selection
- Phone number/card input field
- "Confirm payment" button
- JavaScript for payment method switching
- Security badge "🔒 Paiement 100% sécurisé"

### 3. Updated Templates

#### `search.html`
- Changed from `current_user.is_authenticated` to `session.get('user_id')`
- Updated booking link: `url_for('user.book_worker', worker_id=worker.id)`
- Shows "Réserver" button for logged-in employers
- Shows "Connexion pour réserver" for non-logged-in users

### 4. Updated Routes

#### `routes/main.py`
- Fixed `User.status == "valide"` to use `UserStatus.VALIDATED` enum
- Added UserStatus import

## Workflow

### Employer Books a Worker

1. **Search Page** (`/search`)
   - Employer searches for workers
   - Clicks "Réserver" on a worker

2. **Booking Page** (`/book/<worker_id>`)
   - Form shows worker info
   - Employer fills: start date, duration, salary
   - Submits form
   - Employment created with PENDING status

3. **Payment Page** (`/payment/<employment_id>`)
   - Shows employment summary
   - Employer selects payment method
   - Enters phone/card number
   - Submits payment
   - Employment status changes to ACTIVE
   - Redirects to dashboard with success message

### Worker Sees Employment

1. Worker logs in
2. Dashboard shows new employment in table
3. Status shows "✓ Actif" (green badge)
4. Can see employer info and salary

## Database Flow

```
Employment Record:
├── Status: PENDING (created on booking)
│   └── Changes to ACTIVE (after payment)
├── employer_id: Current user's employer profile
├── worker_id: Selected worker
├── salary: Amount from form
├── start_date: Date from form
└── created_at: Auto timestamp
```

## Payment Methods

Currently just for UI demonstration. In production you would:
- Integrate with Orange Money API
- Integrate with Wave API
- Integrate with payment gateway for cards
- Store payment transaction details
- Handle payment success/failure callbacks

## Security Features

- `@login_required` decorator on all routes
- Validates employer owns the employment before payment
- Only VALIDATED workers can be booked
- Prevents booking if no employer profile exists
- Session-based authentication

## Styling

All templates use existing CSS from `style.css`:
- `.card`, `.card-header`, `.card-avatar`
- `.form-group`, `.form-container`
- `.btn`, `.btn-primary`, `.btn-full`
- `.tag`, `.tags`
- Custom inline styles for payment method grid
- Responsive design maintained

## Profile Verification

Before workers appear in search, they must be verified.

### Quick Verification (SQLite)

```bash
sqlite3 instance/msm.db
```

```sql
-- Verify specific user
UPDATE users SET status = 'validated', is_verified = 1 WHERE email_address = 'worker@example.com';

-- Verify all pending users
UPDATE users SET status = 'validated', is_verified = 1 WHERE status = 'pending';
```

### Python Script Method

Create `verify_user.py`:
```python
from app import create_app
from models import db, User, UserStatus
import sys

app = create_app()
email = sys.argv[1]

with app.app_context():
    user = User.query.filter_by(email_address=email).first()
    if user:
        user.status = UserStatus.VALIDATED
        user.is_verified = True
        db.session.commit()
        print(f"✅ Verified {user.first_name}!")
```

Run: `python3 verify_user.py worker@example.com`

## Testing the Flow

1. **Reset database**:
   ```bash
   python3 reset_db.py
   ```

2. **Create accounts**:
   - Register as employer
   - Register as worker
   - Complete both profiles

3. **Verify worker** (SQLite):
   ```sql
   UPDATE users SET status = 'validated' WHERE email_address = 'worker@example.com';
   ```

4. **Book as employer**:
   - Login as employer
   - Go to `/search`
   - Click "Réserver" on the worker
   - Fill booking form
   - Click "Continue to payment"
   - Fill payment info
   - Click "Confirm payment"

5. **Check dashboards**:
   - Employer dashboard shows the employment
   - Worker dashboard shows the employment
   - Both see ACTIVE status

## Flash Messages

- Success: "Paiement confirmé avec succès!" (green)
- Errors: Various validation messages (red)
- Categories: `success` or default (error)

## Future Enhancements

- Add payment status tracking (paid/unpaid)
- Store payment method and transaction ID
- Add payment history page
- Implement real payment gateway integration
- Add refund functionality
- Add contract PDF generation
- Email notifications on booking/payment
- SMS notifications for mobile money
- Add booking cancellation with refund logic
- Track booking fee separately from salary payments

## Notes

- Booking fee is fixed at 10,000 F CFA
- This is a one-time fee per employment
- Actual salary payments would be handled separately
- Employment start_date is stored but not actively enforced
- No end_date is set during booking (can be added later)
- Duration is stored as string, not used for calculations yet