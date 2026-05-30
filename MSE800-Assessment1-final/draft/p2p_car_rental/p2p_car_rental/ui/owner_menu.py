"""
Owner Menu
==========
CLI menu for Owner role.
"""

from tabulate import tabulate
from services.car_service import CarService
from services.booking_service import BookingService
from services.review_service import ReviewService
from utils.helpers import (
    clear_screen, print_header, print_success, print_error, print_info,
    prompt, prompt_choice, prompt_yes_no, format_currency, pause,
)
from utils.validators import (
    is_non_empty, is_valid_year, is_positive_number,
)


def owner_menu(user):
    """Owner main menu loop."""
    car_svc = CarService()
    booking_svc = BookingService()
    review_svc = ReviewService()

    while True:
        clear_screen()
        print(user.view_dashboard())
        rating = review_svc.get_user_avg_rating(user.id)
        print(f"  Average rating: {rating if rating else 'No reviews yet'}")
        print()
        print("  1. View my cars")
        print("  2. Add new car listing")
        print("  3. Remove car listing")
        print("  4. View pending bookings")
        print("  5. Approve / Reject booking")
        print("  6. View earnings")
        print("  7. View profile")
        print("  8. Logout")
        print()

        choice = prompt_choice("Select option", ['1','2','3','4','5','6','7','8'])

        if choice == '1':
            _view_my_cars(car_svc, user)
        elif choice == '2':
            _add_car(car_svc, user)
        elif choice == '3':
            _remove_car(car_svc, user)
        elif choice == '4':
            _view_pending_bookings(booking_svc, user)
        elif choice == '5':
            _handle_booking(booking_svc, user)
        elif choice == '6':
            _view_earnings(booking_svc, user)
        elif choice == '7':
            _view_profile(user)
        elif choice == '8':
            print_info("Logging out...")
            break


def _view_my_cars(svc, user):
    clear_screen()
    print_header("MY CARS")
    cars = svc.get_owner_cars(user.id)
    if not cars:
        print_info("You haven't listed any cars yet.")
    else:
        rows = []
        for c in cars:
            status = "Approved" if c.is_approved else "Pending"
            avail = "Available" if c.is_available else "Unavailable"
            rows.append([c.id, f"{c.year} {c.make} {c.model}",
                          c.location, format_currency(c.daily_rate),
                          status, avail])
        print(tabulate(rows,
                       headers=['ID','Vehicle','Location','Rate/day','Approval','Status'],
                       tablefmt='grid'))
    pause()


def _add_car(svc, user):
    clear_screen()
    print_header("ADD NEW CAR LISTING")
    print("Fill in your car details (all required):\n")

    make = prompt("Make (e.g. Toyota)")
    model = prompt("Model (e.g. Corolla)")

    while True:
        year = prompt("Year (e.g. 2020)")
        if is_valid_year(year):
            year = int(year)
            break
        print_error("Invalid year. Use a year from 1990 to next year.")

    while True:
        mileage = prompt("Mileage in km (e.g. 50000)")
        try:
            mileage = int(mileage)
            if mileage >= 0:
                break
        except ValueError:
            pass
        print_error("Invalid mileage")

    location = prompt("Location (e.g. Auckland)")

    while True:
        rate = prompt("Daily rate in USD (e.g. 50)")
        if is_positive_number(rate):
            rate = float(rate)
            break
        print_error("Invalid rate")

    while True:
        min_p = prompt("Minimum rent period in days (e.g. 1)")
        try:
            min_p = int(min_p)
            if min_p >= 1:
                break
        except ValueError:
            pass
        print_error("Invalid value")

    while True:
        max_p = prompt("Maximum rent period in days (e.g. 30)")
        try:
            max_p = int(max_p)
            if max_p >= min_p:
                break
        except ValueError:
            pass
        print_error("Max must be >= min")

    ok, msg, _ = svc.add_car(user.id, make, model, year, mileage,
                              location, rate, min_p, max_p)
    if ok:
        print_success(msg)
    else:
        print_error(msg)
    pause()


def _remove_car(svc, user):
    clear_screen()
    print_header("REMOVE CAR LISTING")
    cars = svc.get_owner_cars(user.id)
    if not cars:
        print_info("You have no cars to remove.")
        pause()
        return

    for c in cars:
        print(f"  [{c.id}] {c.year} {c.make} {c.model} — {c.location}")

    car_id = prompt("\nEnter car ID to remove (or 'cancel')")
    if car_id.lower() == 'cancel':
        return

    if not prompt_yes_no(f"Confirm remove car #{car_id}?"):
        print_info("Cancelled")
        pause()
        return

    try:
        ok, msg = svc.remove_car(user.id, int(car_id))
        print_success(msg) if ok else print_error(msg)
    except ValueError:
        print_error("Invalid ID")
    pause()


def _view_pending_bookings(svc, user):
    clear_screen()
    print_header("PENDING BOOKING REQUESTS")
    bookings = svc.get_owner_bookings(user.id, status='pending')
    if not bookings:
        print_info("No pending booking requests.")
    else:
        rows = []
        for b in bookings:
            rows.append([
                b['id'], b['renter_name'],
                f"{b['year']} {b['make']} {b['model']}",
                f"{b['start_date']} → {b['end_date']}",
                format_currency(b['owner_amount']),
            ])
        print(tabulate(rows,
                       headers=['ID','Renter','Car','Period','You earn'],
                       tablefmt='grid'))
    pause()


def _handle_booking(svc, user):
    clear_screen()
    print_header("APPROVE / REJECT BOOKING")
    bookings = svc.get_owner_bookings(user.id, status='pending')
    if not bookings:
        print_info("No pending bookings.")
        pause()
        return

    for b in bookings:
        print(f"  [{b['id']}] {b['renter_name']} — "
              f"{b['year']} {b['make']} {b['model']} — "
              f"{b['start_date']} → {b['end_date']} — "
              f"{format_currency(b['owner_amount'])}")

    bid = prompt("\nEnter booking ID (or 'cancel')")
    if bid.lower() == 'cancel':
        return

    action = prompt_choice("Action: (a)pprove or (r)eject", ['a', 'r'])

    try:
        bid = int(bid)
        if action == 'a':
            ok, msg = svc.approve_booking(bid, user.id)
        else:
            ok, msg = svc.reject_booking(bid, user.id)
        print_success(msg) if ok else print_error(msg)
    except ValueError:
        print_error("Invalid ID")
    pause()


def _view_earnings(svc, user):
    clear_screen()
    print_header("MY EARNINGS")
    total = svc.get_owner_earnings(user.id)
    bookings = svc.get_owner_bookings(user.id)

    print(f"\n  Total earnings: {format_currency(total)}\n")

    approved = [b for b in bookings if b['status'] in ('approved','completed')]
    print(f"  Total completed bookings: {len(approved)}")
    print(f"  Pending: {len([b for b in bookings if b['status']=='pending'])}")
    print(f"  Rejected: {len([b for b in bookings if b['status']=='rejected'])}")
    pause()


def _view_profile(user):
    clear_screen()
    print_header("MY PROFILE")
    profile = user.view_profile()
    for k, v in profile.items():
        print(f"  {k:15s}: {v}")
    pause()
