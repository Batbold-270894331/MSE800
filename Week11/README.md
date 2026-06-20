# Smart AI-Powered Library Management and Recommendation System

## Overview

This project is a smart web-based library management system designed to support book management, borrowing and returning, AI-powered book discovery, recommendations, chatbot support, and administrative reporting.

The system supports three main roles: **Reader/User**, **Librarian**, and **Administrator**. A Reader/User is the main library user who searches books, borrows and returns books, writes reviews, and uses AI features such as chatbot support, smart search, summaries, and recommendations.

## Group T

- Sangam Poudel
- Batbold Chuluunbaatar

## Main Objectives

- Provide a simple web-based library system for Readers/Users, Librarians, and Administrators.
- Manage books, users, borrowing records, reviews, ratings, and availability.
- Support AI-powered features such as chatbot assistance, smart search, recommendations, and book summaries.
- Provide role-based access control and admin insights.
- Prepare the system for final demonstration and cloud or Docker-based deployment.

## User Roles

| Role | Description |
| --- | --- |
| Reader | Main library user who searches, borrows, returns, reviews books, and uses AI chatbot and recommendations. |
| Librarian | Library staff member who manages books, borrowing records, and library operations. |
| Administrator | System-level user who manages users, roles, dashboard insights, and administrative settings. |

## Core Features

- User registration and login with role-based access control.
- Reader/User dashboard for book search, recommendations, borrowed books, reviews, and chatbot access.
- Librarian/Admin dashboard for book management, borrowing records, user records, and insights.
- Book management: add, view, edit, delete, search, and details view.
- Borrowing and returning workflow with automatic available-copy updates.
- Borrowing history, late return tracking, reviews, and ratings.
- AI chatbot, natural-language smart search, personalized recommendations, and AI-generated book summaries.
- Deployment-ready web application using Docker or cloud hosting.

## Functional Requirements

| ID | Requirement | Description | Related screen | Implemented | Sprint |
| --- | --- | --- | --- | --- | --- |
| FR-01 | User Registration | Reader, Librarians, and Administrators can create an account by entering required details such as name, email, password, and role where applicable. | Register Screen | Authentication module; User table | Sprint 1 |
| FR-02 | User Login | Registered users can log in using a valid email and password. | Login Screen | Authentication module | Sprint 1 |
| FR-03 | Role-Based Access Control | The system provides different access permissions for Reader, Librarian, and Administrator roles. | Login Screen; Dashboard; Admin Pages | User role logic; protected routes/pages | Sprint 1 |
| FR-04 | Reader Dashboard | Reader can view book search options, recommendations, borrowed books, reviews, and chatbot access from one main area. | Reader Dashboard | Frontend dashboard layout; user navigation | Sprint 1 / Sprint 2 |
| FR-05 | Librarian/Admin Dashboard | Librarians and Administrators can access book management, borrowing records, user records, and library insights. | Librarian Dashboard; Admin Dashboard | Dashboard module; reporting pages | Sprint 2 |
| FR-06 | Add Book | Librarians or Administrators can add a new book by entering title, author, ISBN, category, description, total copies, and available copies. | Add Book Screen | Book management module; Book table | Sprint 1 |
| FR-07 | View Book List | Users can view all books in a clear list or card format with important book details and availability status. | Book List Screen | Book listing page; Book table | Sprint 1 |
| FR-08 | Edit Book | Librarians or Administrators can update book information such as title, author, category, description, and copy count. | Edit Book Screen | Book management module | Sprint 1 |
| FR-09 | Delete Book | Librarians or Administrators can remove incorrect or outdated book records when required. | Book List Screen; Book Details Screen | Book management module | Sprint 1 |
| FR-10 | Basic Book Search | Users can search for books by title, author, ISBN, category, or keyword. | Book Search Screen; Book List Screen | Book search function | Sprint 1 |
| FR-11 | Book Details View | Users can open a book record and view full information including availability, category, description, rating, AI summary, and borrow option. | Book Details Screen | Book details page; Book table; Review table | Sprint 1 / Sprint 2 |
| FR-12 | Borrow Book | Readers can borrow an available book. The system creates a loan record with issue date and due date. | Book Details Screen; Borrow Screen | Borrow/return module; Loan table | Sprint 2 |
| FR-13 | Return Book | Readers or Librarians can return borrowed books. The system records the return date. | My Loans Screen; Return Book Screen | Borrow/return module; Loan table | Sprint 2 |
| FR-14 | Update Available Copies | The system automatically updates available book copies when a book is borrowed or returned. | Borrow Screen; Return Screen; Book List Screen | Database update logic; Book table | Sprint 2 |
| FR-15 | Borrowing History | Readers can view their own borrowing history. Librarians and Administrators can view overall borrowing records. | My Loans Screen; Borrowing Records Screen | Loan history module; Loan table | Sprint 2 |
| FR-16 | Review and Rating | Readers can submit ratings and reviews for books they have read or borrowed. | Book Details Screen; Review Screen | Review/rating module; Review table | Sprint 2 |
| FR-17 | AI Chatbot Assistant | Users can ask questions about book availability, borrowing rules, system usage, and book discovery using a chatbot. | Chatbot Screen; Chatbot Widget | LLM API integration; chatbot module | Sprint 2 |
| FR-18 | Smart Natural-Language Search | Users can search using natural language rather than exact keywords, for example: 'books similar to Harry Potter but for adults'. | Smart Search Screen; Book Search Screen | AI search logic; LLM API integration | Sprint 2 |
| FR-19 | Personalized Recommendations | The system recommends books using borrowing history, preferred category, ratings, popular trends, or simple rule-based logic. | Reader Dashboard; Recommendation Screen; Book Details Screen | Recommendation engine | Sprint 2 |
| FR-20 | AI-Generated Book Summaries | The system generates short original summaries, key themes, difficulty level, and suggested audience information for books. | Book Details Screen; AI Summary Section | LLM summarization feature | Sprint 2 |
| FR-21 | Admin Insights Dashboard | Administrators and Librarians can view active users, popular books, borrowing trends, trending categories, and late return patterns. | Admin Insights Dashboard | Reporting/dashboard module | Sprint 2 |
| FR-22 | Late Return Tracking | The system identifies overdue or late-returned books using due dates and return dates. | Admin Dashboard; Borrowing Records Screen | Loan due-date logic; reporting module | Sprint 2 |
| FR-23 | User Management | Administrators can view users and manage roles or account access where required. | User Management Screen | User/admin module; User table | Sprint 1 / Sprint 2 |
| FR-24 | Reservation Support | The database design should support future book reservations for unavailable books, even if implemented as a simple or future-ready feature. | Book Details Screen; Reservation Screen | Reservation table/design | Sprint 1 / Future Enhancement |
| FR-25 | Final Deployment | The completed application must be deployed using Docker or cloud hosting for demonstration and final presentation. | Kick-off web application | Docker/cloud deployment | Sprint 2 |

## Non-Functional Requirements

| ID | Requirement | Description | Related screen | Implemented | Sprint |
| --- | --- | --- | --- | --- | --- |
| NFR-01 | Usability | The system must be simple and easy to use for Readers, Librarians, and Administrators with clear navigation, forms, buttons, and messages. | All Screens | Bootstrap UI; wireframes; manual usability testing | Sprint 1 / Sprint 2 |
| NFR-02 | Responsive Design | The web interface must work properly on desktop and mobile web browsers. | Login; Dashboard; Book List; Book Details; Chatbot | HTML, CSS, Bootstrap responsive layout | Sprint 1 |
| NFR-03 | Security | Passwords must not be stored as plain text. The system should use secure password hashing. | Register Screen; Login Screen | Authentication module; password_hash field | Sprint 1 |
| NFR-04 | Access Control | Users must only access pages and actions allowed for their role. Readers must not access protected admin pages. | Dashboard; Admin Pages; Book Form Screens | Role-based route/page protection | Sprint 1 |
| NFR-05 | Data Accuracy | Borrowing and returning books must correctly update loan records and available copy counts. | Borrow Screen; Return Screen; Book List Screen | Borrow/return logic; integration testing | Sprint 2 |
| NFR-06 | Performance | Book search, book listing, and dashboard data should load within a reasonable time for a small-to-medium library database. | Book Search Screen; Book List Screen; Dashboard | Database queries; searchable fields; testing | Sprint 1 / Sprint 2 |
| NFR-07 | Reliability | Main workflows such as login, book management, borrowing, returning, AI search, and dashboard viewing should work without system crashes. | All Main Screens | Unit testing; integration testing; bug fixing | Sprint 2 |
| NFR-08 | Maintainability | The project should use a clear modular structure and object-oriented classes such as User, Book, Loan, and Review. | Not screen-specific; affects all screens | Backend folder structure; model classes | Sprint 1 |
| NFR-09 | Scalability | The system design should allow future features such as QR issuing, email reminders, voice search, multilingual chatbot, and PWA support. | Book Details; Borrow Screen; Chatbot; Dashboard | Modular architecture; database design | Sprint 1 / Future Enhancement |
| NFR-10 | AI Output Safety | AI summaries must be original overviews and must not reproduce copyrighted book text. | AI Summary Section; Chatbot Screen | LLM prompt design; AI output validation | Sprint 2 |
| NFR-11 | AI Grounding | The chatbot should answer using real library data where possible, such as available books, categories, and borrowing rules. | Chatbot Widget; Book Search Screen | AI chatbot integration with database/API | Sprint 2 |
| NFR-12 | Error Handling | The system must display clear error messages for invalid login, missing form data, unavailable books, and failed AI responses. | Login; Register; Book Form; Borrow Screen; Chatbot | Form validation; backend validation; UI messages | Sprint 1 / Sprint 2 |
| NFR-13 | Testability | The system must support unit, integration, UI, and AI output testing. | All Screens | pytest; manual testing; integration testing; AI validation | Sprint 2 |
| NFR-14 | Deployment Readiness | The system must be containerized or prepared for cloud deployment. | Live Application | Docker; cloud hosting; final deployment setup | Sprint 2 |
| NFR-15 | Browser Compatibility | The application should work in common modern web browsers. | All Web Screens | Browser-based HTML/CSS/JavaScript frontend | Sprint 1 / Sprint 2 |
| NFR-16 | Data Persistence | User, book, loan, review, rating, and reservation data must be stored permanently in the database. | Register; Book Management; Borrow/Return; Review Screens | SQLite database design | Sprint 1 |
| NFR-17 | Consistent UI Design | Buttons, forms, tables, cards, and navigation should follow a consistent visual style across the system. | All Screens | Shared layout; Bootstrap components | Sprint 1 |
| NFR-18 | Documentation | The project must include final documentation, sprint records, test results, deployment notes, and presentation materials. | Not screen-specific | Final report; presentation; sprint documentation | Sprint 2 |

## Screen-Based Requirement Mapping

| Screen | Related requirements | Sprint | Sprint |
| --- | --- | --- | --- |
| Login Screen | FR-02, FR-03, NFR-03, NFR-04, NFR-12 | FR-02, FR-03, NFR-03, NFR-04, NFR-12 | Sprint 1 |
| Register Screen | FR-01, NFR-03, NFR-12, NFR-16 | FR-01, NFR-03, NFR-12, NFR-16 | Sprint 1 |
| Reader/User Dashboard | FR-04, FR-17, FR-19, NFR-01, NFR-02 | FR-04, FR-17, FR-19, NFR-01, NFR-02 | Sprint 1 / Sprint 2 |
| Librarian/Admin Dashboard | FR-05, FR-21, FR-22, NFR-01, NFR-06 | FR-05, FR-21, FR-22, NFR-01, NFR-06 | Sprint 2 |
| Book List Screen | FR-07, FR-10, FR-14, NFR-06, NFR-17 | FR-07, FR-10, FR-14, NFR-06, NFR-17 | Sprint 1 / Sprint 2 |
| Add/Edit Book Screen | FR-06, FR-08, FR-09, NFR-12, NFR-16 | FR-06, FR-08, FR-09, NFR-12, NFR-16 | Sprint 1 |
| Book Details Screen | FR-11, FR-12, FR-16, FR-19, FR-20 | FR-11, FR-12, FR-16, FR-19, FR-20 | Sprint 1 / Sprint 2 |
| Borrow/Return Screen | FR-12, FR-13, FR-14, FR-15, NFR-05 | FR-12, FR-13, FR-14, FR-15, NFR-05 | Sprint 2 |
| My Loans Screen | FR-13, FR-15, FR-22, NFR-05 | FR-13, FR-15, FR-22, NFR-05 | Sprint 2 |
| Review/Rating Screen | FR-16, NFR-16 | FR-16, NFR-16 | Sprint 2 |
| Chatbot Screen / Widget | FR-17, FR-18, NFR-10, NFR-11, NFR-12 | FR-17, FR-18, NFR-10, NFR-11, NFR-12 | Sprint 2 |
| Smart Search Screen | FR-18, FR-19, NFR-06, NFR-11 | FR-18, FR-19, NFR-06, NFR-11 | Sprint 2 |
| AI Summary Section | FR-20, NFR-10 | FR-20, NFR-10 | Sprint 2 |
| User Management Screen | FR-03, FR-23, NFR-04 | FR-03, FR-23, NFR-04 | Sprint 1 / Sprint 2 |
| Live Application / Deployment | FR-25, NFR-14, NFR-18 | FR-25, NFR-14, NFR-18 | Sprint 2 |

## Project Summary

Sprint 1 builds the system foundation, including authentication, role-based access, database design, UI layout, and basic book management. Sprint 2 completes borrowing and returning workflows, AI chatbot, recommendations, AI summaries, smart search, admin dashboard, testing, deployment, and final documentation.
