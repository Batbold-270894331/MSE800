"""
Admin Menu
==========
CLI menu for Admin role.
"""

from tabulate import tabulate
from services.car_service import CarService
from services.booking_service import BookingService
from services.admin_service import AdminService
from utils.helpers import (
    clear_screen, print_header, print_success, print_error, print_info,
    print_section, prompt, prompt_choice, format_currency, pause,
)


def admin_menu(user):
    """Admin main menu loop."""
    car_svc = CarService()
    booking_svc = BookingService()
    admin_svc = AdminService()

    while True:
        clear_screen()
        print(user.view_dashboard())
        print()
        print("  1. Verify pending users")
        print("  2. Approve / Reject car listings")
        print("  3. View all bookings")
        print("  4. Handle insurance claims")
        print("  5. View platform reports")
        print("  6. Suspend a user")
        print("  7. Logout")
        print()

        choice = prompt_choice("Select option", ['1','2','3','4','5','6','7'])

        if choice == '1':
            _verify_users(admin_svc)
        elif choice == '2':
            _handle_cars(car_svc)
        elif choice == '3':
            _view_all_bookings(booking_svc)
        elif choice == '4':
            _handle_claims(admin_svc)
        elif choice == '5':
            _view_reports(admin_svc)
        elif choice == '6':
            _suspend_user(admin_svc)
        elif choice == '7':
            print_info("Logging out...")
            break


def _verify_users(svc):
    clear_screen()
    print_header("VERIFY PENDING USERS")
    users = svc.get_pending_users()
    if not users:
        print_info("No pending users.")
        pause()
        return

    rows = []
    for u in users:
        rows.append([u['id'], u['name'], u['email'], u['role'].capitalize(),
                     u['license_number'] or '—'])
    print(tabulate(rows,
                   headers=['ID','Name','Email','Role','License'],
                   tablefmt='grid'))

    uid = prompt("\nEnter user ID to verify (or 'cancel')")
    if uid.lower() == 'cancel':
        return
    try:
        ok, msg = svc.verify_user(int(uid))
        print_success(msg) if ok else print_error(msg)
    except ValueError:
        print_error("Invalid ID")
    pause()


def _handle_cars(svc):
    clear_screen()
    print_header("PENDING CAR LISTINGS")
    cars = svc.get_pending_cars()
    if not cars:
        print_info("No cars awaiting approval.")
        pause()
        return

    rows = []
    for c in cars:
        rows.append([c.id, c.owner_id,
                     f"{c.year} {c.make} {c.model}",
                     c.location, format_currency(c.daily_rate)])
    print(tabulate(rows,
                   headers=['ID','OwnerID','Vehicle','Location','Rate'],
                   tablefmt='grid'))

    cid = prompt("\nEnter car ID (or 'cancel')")
    if cid.lower() == 'cancel':
        return
    action = prompt_choice("Action: (a)pprove or (r)eject", ['a','r'])

    try:
        cid = int(cid)
        if action == 'a':
            ok, msg = svc.approve_car(cid)
        else:
            ok, msg = svc.reject_car(cid)
        print_success(msg) if ok else print_error(msg)
    except ValueError:
        print_error("Invalid ID")
    pause()


def _view_all_bookings(svc):
    clear_screen()
    print_header("ALL PLATFORM BOOKINGS")
    bookings = svc.get_all_bookings()
    if not bookings:
        print_info("No bookings yet.")
        pause()
        return

    rows = []
    for b in bookings:
        rows.append([
            b['id'],
            f"{b['year']} {b['make']} {b['model']}",
            b['renter_name'], b['owner_name'],
            f"{b['start_date']} → {b['end_date']}",
            format_currency(b['total_amount']),
            b['status'].upper(),
        ])
    print(tabulate(rows,
                   headers=['ID','Car','Renter','Owner','Period','Total','Status'],
                   tablefmt='grid'))
    pause()


def _handle_claims(svc):
    clear_screen()
    print_header("INSURANCE CLAIMS")
    claims = svc.get_pending_claims()
    if not claims:
        print_info("No pending claims.")
        pause()
        return

    for c in claims:
        print(f"\n  Claim #{c['id']} — Booking #{c['booking_id']}")
        print(f"  Car: {c['make']} {c['model']}")
        print(f"  Description: {c['description']}")
        print(f"  Amount: {format_currency(c['claim_amount'])}")

    cid = prompt("\nEnter claim ID (or 'cancel')")
    if cid.lower() == 'cancel':
        return
    action = prompt_choice("Action: (a)pprove or (r)eject", ['a','r'])

    try:
        cid = int(cid)
        if action == 'a':
            ok, msg = svc.approve_claim(cid)
        else:
            ok, msg = svc.reject_claim(cid)
        print_success(msg) if ok else print_error(msg)
    except ValueError:
        print_error("Invalid ID")
    pause()


def _view_reports(svc):
    clear_screen()
    print_header("PLATFORM REPORTS")
    stats = svc.get_platform_stats()
    print()
    for k, v in stats.items():
        print(f"  {k:25s}: {v}")
    pause()


def _suspend_user(svc):
    clear_screen()
    print_header("SUSPEND USER")
    uid = prompt("User ID to suspend (or 'cancel')")
    if uid.lower() == 'cancel':
        return
    try:
        ok, msg = svc.suspend_user(int(uid))
        print_success(msg) if ok else print_error(msg)
    except ValueError:
        print_error("Invalid ID")
    pause()
