# cyber-security-project-1

A TODO web app

## Setup

As prerequisities python 3 and django should be installed. The course's [installation instructions](https://cybersecuritybase.mooc.fi/installation-guide) should be enough to get everything needed installed.

### Installing and running the project


1. Clone the repository with `git clone https://github.com/joelkur/cyber-security-project-1.git`


2. In the project root folder, run migrations with `python3 manage.py migrate`
3. Create test data with `python3 manage.py initdb`
4. Run the server with `python3 manage.py runserver`
5. The project should be running at http://localhost:8000

### Test users
The `initdb` command creates the following users:

- admin:admin
- alex:fisheye
- piter:greenlake

## Flaws

### Flaw 1: [Cryptographic Failure]
Links to the flaw sources:
- [/todoapp/models.py#L9](/todoapp/models.py#L9)
- [/todoapp/models.py#L13](/todoapp/models.py#L13)

Cryptographic failure refers to situations where a cryptographic system or algorithm fails to provide the intended level of security. Cryptography is the science of secure communication and involves the use of mathematical algorithms to encode and protect sensitive information.

A simple fix for this could be using Django's built-in password management for hashing and other password related logic. Since the `User` model class is extended from `AbstractUser`, which already has password hashing functionality, the `enter_password` and `validate_password` methods could simply be removed in `User` model to enable Django's original password management functionality.

Below are links to Django's built-in way of handling passwords, found in the Django source code:
https://github.com/django/django/blob/main/django/contrib/auth/hashers.py#L38
https://github.com/django/django/blob/main/django/contrib/auth/hashers.py#L72

### Flaw 2: [Broken Access Control]
Links to the flaw sources:
- [/todoapp/views.py#L8](/todoapp/views.py#L8)
- [/todoapp/views.py#L19](/todoapp/views.py#L19)
- [/todoapp/views.py#L31](/todoapp/views.py#L31)

Broken Access Control refers to a security vulnerability that occurs when there is inadequate or improper enforcement of access restrictions in a web application or system. Access control mechanisms are designed to ensure that users can only access the resources and perform actions they are authorized to do. However, if these access controls are not correctly implemented, attackers can exploit the weaknesses to gain unauthorized access to sensitive information or perform unauthorized actions. To reproduce this, with the initial test data log in with e.g. user `piter` and go to link http://localhost:8000/todos/10/. This should open a view that displays todo belonging to user `alex` - with the ability to mark the todo as done or delete it.

This can be fixed by implementing a check that the requesting user matches the owner of the target resource, and if a mismatch occurs the access should be prevented. Each of the views containing the flaw has commented out code for a possible fix.

Links to the fixes:
- [/todoapp/views.py#L11](/todoapp/views.py#L11)
- [/todoapp/views.py#L22](/todoapp/views.py#L22)
- [/todoapp/views.py#L34](/todoapp/views.py#L34)

### Flaw 3: [SQL injection]
Links to the flaw sources:
- [/todoapp/views.py#L55](/todoapp/views.py#L55)

SQL injection is a security vulnerability that occurs when an attacker is able to manipulate SQL queries executed by a web application's database. It happens when the application fails to properly validate or sanitize user input that is used to construct SQL queries, allowing an attacker to insert malicious SQL code.
Here's an example of a simple SQL injection attack:
`SELECT * FROM users WHERE username = '<username>' AND password = '<password>';`

Suppose there is a login form on a website that accepts a username and password. The application constructs an SQL query to validate the credentials:

To reproduce the SQL injection in the application, you can type e.g. `%' UNION SELECT username, password FROM auth_user WHERE username LIKE '%%` to the search input and then press search. This should display all todos, and additionally plaintext passwords of each user in the list. Although not visible in the rendered view in browser, also usernames of each user is included in the response, which can be seen if inspecting the raw HTML response.

One fix for this flaw is to use Django's built-in object relational mapper for building, executing and reading the database query. This suggested fix is commented out in the code after the flawed line. Another way of fixing the issue via raw SQL would be by using prepared statements. Prepared statements builds the query beforehand without executing it, leaving placeholders for parameters. Later the compiled query can be executed with different input as parameters, without the worry of the input affecting the original query.

Links to the fixes:
- [/todoapp/views.py#L58](/todoapp/views.py#L58)

### Flaw 4: [Cross-site scripting (XSS)]
Links to the flaw sources:
- [/project/settings.py#73](/project/settings.py#L73)

Cross-site scripting (XSS) is a type of web security vulnerability that allows attackers to inject malicious scripts or code into web pages viewed by other users. It occurs when a web application does not properly validate or sanitize user input before displaying it on a website.

The process typically involves an attacker finding a vulnerable website and exploiting it by injecting malicious code, usually in the form of JavaScript, into the website's content. This can happen through input fields, such as search boxes, comment sections, or form inputs, where the user-supplied data is not properly sanitized or validated by the application.

One way of reproducing this scenario can be achieved with the following steps:
1. Log in with `alex`
2. To one of the input fields in "Add new todo" form, write `<script>alert(document.cookie)</script>`, and submit the form
3. Copy the link of the new todo to clipboard, log out and login with `piter`
4. Go to the link in clipboard
5. Now an alert should appear containing the contents of pite's cookie

In this particular case, the root of the issue comes from the project settings, where templates are configured to not automatically escape user input. Removing this line enables the automatic input escaping functionality and thus fixing XSS issues.

Links to the fixes:
- [/project/settings.py#73](/project/settings.py#L73)

### Flaw 5: [Identification and Authentication Failures]
Links to the flaw sources:
- [/project/session.py#L5](/project/session.py#L5)
- [/project/settings.py#L34](/project/settings.py#L34)

Identification and authentication failures refer to security vulnerabilities or weaknesses in the processes of verifying and validating the identities of users or entities accessing a system or network. These failures can occur in various contexts, such as computer systems, networks, online services, or physical access control systems.

Identification is the process of claiming an identity, typically through the use of a username, email address, or other unique identifier. Authentication, on the other hand, is the process of verifying the claimed identity by providing proof of identity, such as a password, PIN, biometric data, or digital certificate.

The session key should be fixed to be unpredictable, as an example a securely generated random bytes. The session should also be expired and invalidated when the user logs out of the system. Django has this functionality already built-in, so again a simple fix in this application would be to remove the custom `SessionStore` and use Django's built-in one.

To fix the session cookie being accessible with javascript, the session cookie should be set as HTTP only.

Links to the fixes:
- [/project/settings.py#L30](/project/settings.py#L30)
- [/project/settings.py#L33](/project/settings.py#L33)
