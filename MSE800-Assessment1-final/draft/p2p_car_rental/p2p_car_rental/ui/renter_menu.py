"""
Renter Menu
===========
CLI menu for Renter role.

Handles the full 'Make booking' flow with include/extend use cases.
"""

from tabulate import tabulate
from services.car_service import CarService
from services.booking_service import BookingService
from services.review_service import ReviewService
from patterns.insurance_strategy import list_all_insurance, get_insurance
from utils.helpers import (
    clear_screen, print_header, print_success, print_error, print_info,
    print_section, prompt, prompt_choice, prompt_yes_no,
    format_currency, pause,
)
from utils.validators import is_valid_date, is_positive_number
# Pull demo discount codes from config so business team can change them
# in ONE place instead of hunting through code
from config import DISCOUNT_CODES


def renter_menu(user):
    """Renter main menu loop."""
    car_svc = CarService()
    booking_svc = BookingService()
    review_svc = ReviewService()

    while True:
        clear_screen()
        print(user.view_dashboard())
        print()
        print("  1. Search & filter cars")
        print("  2. View car details + Make booking")
        print("  3. My bookings")
        print("  4. Cancel a booking")
        print("  5. Submit review")
        print("  6. View profile")
        print("  7. Logout")
        print()

        choice = prompt_choice("Select option", ['1','2','3','4','5','6','7'])

        if choice == '1':
            _search_cars(car_svc)
        elif choice == '2':
            _make_booking_flow(car_svc, booking_svc, user)
        elif choice == '3':
            _view_my_bookings(booking_svc, user)
        elif choice == '4':
            _cancel_booking(booking_svc, user)
        elif choice == '5':
            _submit_review(review_svc, booking_svc, user)
        elif choice == '6':
            _view_profile(user)
        elif choice == '7':
            print_info("Logging out...")
            break


def _search_cars(svc):
    clear_screen()
    print_header("SEARCH CARS")
    location = prompt("Filter by location (or leave empty)", allow_empty=True)
    max_price = prompt("Max price per day (or leave empty)", allow_empty=True)

    max_price_val = None
    if max_price:
        try:
            max_price_val = float(max_price)
        except ValueError:
            print_error("Invalid price")
            pause()
            return

    cars = svc.search_cars(location=location or None, max_price=max_price_val)
    _display_cars(cars)
    pause()


def _display_cars(cars):
    if not cars:
        print_info("No cars match your criteria.")
        return
    rows = []
    for c in cars:
        rows.append([
            c.id, f"{c.year} {c.make} {c.model}",
            c.location, format_currency(c.daily_rate),
            f"{c.min_rent_period}-{c.max_rent_period} days",
        ])
    print(tabulate(rows,
                   headers=['ID','Vehicle','Location','Rate/day','Period'],
                   tablefmt='grid'))


def _make_booking_flow(car_svc, booking_svc, user):
    """
    Full make-booking use case:
      Include: Check availability
      Include: Calculate fee
      Extend:  Select insurance (optional)
      Extend:  Apply discount (optional)
    """
    clear_screen()
    print_header("MAKE A BOOKING")

    # Step 1: pick a car
    car_id = prompt("Enter car ID (search cars first if needed)")
    try:
        car_id = int(car_id)
    except ValueError:
        print_error("Invalid ID")
        pause()
        return

    car = car_svc.get_car_by_id(car_id)
    if not car or not car.is_approved or not car.is_available:
        print_error("Car not found or not available")
        pause()
        return

    # Step 2: show details (Use Case: View car details)
    print_section("CAR DETAILS")
    for k, v in car.get_details().items():
        print(f"  {k:18s}: {v}")
    print()

    if not prompt_yes_no("Continue with booking this car?"):
        print_info("Cancelled")
        pause()
        return

    # Step 3: dates
    while True:
        start = prompt("Start date (YYYY-MM-DD)")
        if is_valid_date(start):
            break
        print_error("Invalid date format")

    while True:
        end = prompt("End date (YYYY-MM-DD)")
        if is_valid_date(end) and end >= start:
            break
        print_error("Invalid date or end before start")

    # Step 4: «include» Check availability + Calculate fee (with no insurance first)
    available, msg = booking_svc.check_availability(car_id, start, end)
    if not available:
        print_error(msg)
        pause()
        return
    print_success("Car is available for these dates")

    # Step 5: «extend» Select insurance
    print_section("SELECT INSURANCE (optional)")
    print("  0. No insurance")
    for i, ins in enumerate(list_all_insurance(), start=1):
        print(f"  {i}. {ins}")

    while True:
        ic = prompt("Choose insurance (0-3)")
        if ic in ('0','1','2','3'):
            break
        print_error("Choose 0, 1, 2, or 3")

    insurance_map = {'0':'none', '1':'basic', '2':'standard', '3':'premium'}
    insurance_name = insurance_map[ic]

    # Step 6: «extend» Apply discount code
    print_section("DISCOUNT CODE (optional)")
    discount_percent = 0
    code = prompt("Enter discount code (or leave empty)", allow_empty=True)
    if code:
        code_upper = code.upper()
        if code_upper in DISCOUNT_CODES:
            discount_percent = DISCOUNT_CODES[code_upper]
            print_success(f"Discount {discount_percent}% applied!")
        else:
            print_error("Invalid discount code (ignored)")

    # Step 7: Show price breakdown
    insurance = get_insurance(insurance_name)
    pricing = booking_svc.calculate_total(car, start, end,
                                            insurance, discount_percent)

    print_section("PRICE BREAKDOWN")
    print(f"  Days:               {pricing['days']}")
    print(f"  Base price:         {format_currency(pricing['base_price'])}")
    if pricing['discount'] > 0:
        print(f"  Discount:          -{format_currency(pricing['discount'])}")
    print(f"  Owner amount:       {format_currency(pricing['owner_amount'])}")
    print(f"  Platform fee (15%): {format_currency(pricing['platform_fee'])}")
    print(f"  Insurance ({insurance_name}): {format_currency(pricing['insurance_fee'])}")
    print(f"  {'─' * 40}")
    print(f"  TOTAL:              {format_currency(pricing['total_amount'])}")
    print()

    if not prompt_yes_no("Confirm booking?"):
        print_info("Booking cancelled")
        pause()
        return

    # Step 8: create booking
    ok, msg, _ = booking_svc.make_booking(
        car, user.id, start, end, insurance_name, discount_percent
    )
    if ok:
        print_success(msg)
    else:
        print_error(msg)
    pause()


def _view_my_bookings(svc, user):
    clear_screen()
    print_header("MY BOOKINGS")
    bookings = svc.get_renter_bookings(user.id)
    if not bookings:
        print_info("No bookings yet.")
    else:
        rows = []
        for b in bookings:
            rows.append([
                b['id'],
                f"{b['year']} {b['make']} {b['model']}",
                f"{b['start_date']} → {b['end_date']}",
                b['insurance_type'].capitalize(),
                format_currency(b['total_amount']),
                b['status'].upper(),
            ])
        print(tabulate(rows,
                       headers=['ID','Car','Period','Insurance','Total','Status'],
                       tablefmt='grid'))
    pause()


def _cancel_booking(svc, user):
    clear_screen()
    print_header("CANCEL BOOKING")
    bookings = svc.get_renter_bookings(user.id)
    cancelable = [b for b in bookings if b['status'] in ('pending','approved')]
    if not cancelable:
        print_info("No cancellable bookings.")
        pause()
        return

    for b in cancelable:
        print(f"  [{b['id']}] {b['make']} {b['model']} — "
              f"{b['start_date']} → {b['end_date']} — {b['status'].upper()}")

    bid = prompt("\nEnter booking ID (or 'cancel')")
    if bid.lower() == 'cancel':
        return
    try:
        bid = int(bid)
        if prompt_yes_no(f"Are you sure you want to cancel #{bid}?"):
            ok, msg = svc.cancel_booking(bid, user.id)
            print_success(msg) if ok else print_error(msg)
    except ValueError:
        print_error("Invalid ID")
    pause()


def _submit_review(review_svc, booking_svc, user):
    clear_screen()
    print_header("SUBMIT REVIEW")
    bookings = booking_svc.get_renter_bookings(user.id)
    reviewable = [b for b in bookings if b['status'] in ('approved','completed')]
    if not reviewable:
        print_info("You have no bookings to review yet.")
        pause()
        return

    for b in reviewable:
        print(f"  [{b['id']}] {b['make']} {b['model']} — {b['start_date']}")

    bid = prompt("\nBooking ID to review (or 'cancel')")
    if bid.lower() == 'cancel':
        return
    try:
        bid = int(bid)
    except ValueError:
        print_error("Invalid ID")
        pause()
        return

    booking = next((b for b in reviewable if b['id'] == bid), None)
    if not booking:
        print_error("Invalid booking ID")
        pause()
        return

    while True:
        rating_str = prompt("Rating (1-5)")
        try:
            rating = int(rating_str)
            if 1 <= rating <= 5:
                break
        except ValueError:
            pass
        print_error("Rating must be an integer 1-5")

    comment = prompt("Comment (optional)", allow_empty=True)

    ok, msg = review_svc.submit_review(
        booking_id=bid,
        reviewer_id=user.id,
        reviewee_id=booking['owner_id'],
        rating=rating,
        comment=comment,
    )
    print_success(msg) if ok else print_error(msg)
    pause()


def _view_profile(user):
    clear_screen()
    print_header("MY PROFILE")
    for k, v in user.view_profile().items():
        print(f"  {k:15s}: {v}")
    pause()
