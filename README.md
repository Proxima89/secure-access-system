## Project Title: Secure Access System "SAS"

## Overview
The Secure Access System or SAS is a solution for integrating a web-based application with hardware components to manage access control to data centers, server rooms, sport facilities etc. using the RFID technology. It features an interface that enables administrators to monitor access points and perform full CRUD operations on members data.

## Features
- User authentication and authorization.
- Sofware and Hardware controlled access.
- Dashboard for real-time monitoring.
- CRUD Actions allowed for admins.
- Reporting and analytics.

## Usage

Note: This repo is focused mainly on the software part of the system.

1. Before a user is granted access to a secured building, an RFID tag will be linked with their credentials (names), after running the `save_user.py` file inside python environment. The file `save_user.py` can also rewrite if already user exist on it.

2. Main file is `access_controll_app.py`. Tap your card to the RFID reader, if your RFID is recorded in the database, you will be granted an access, where the system will send a signal to the DC relay and this will unlock the electronic switch, and same for when you exiting the facility.

## Configuration
- Setup your Raspbery PI.
- Connect and configure all the hardware components that are necessary. (Find the list below)
- You will need a database, preferably MySQL, with the necessary tables.
- Setup your secrets in a `.env` file.
- Setup desktop application Tkinter
- You need your own web server (Nginex) to monitor the access from your browser. (Optional)

List of the hardware components:

- Gather the RaspberyPI4 PCB and rest of the electronic components:
1. Raspberry PI 4.
2. Micro SD card 16GB+
3. Power Cable for the Raspbery.
4. RC522 RFID Reader, and RFID card or keyring.
5. LCD Display type I2C.
6. Relay for DC operations.
7. 12V Power Cable for the Relay and the Door lock.
8. Resistor ~10kΩ.
9. NPN Transistor.
10. Diode for extra protection
11. Buzzer.
12. Electronic Door Lock 12V.
13. Breadboard.
14. Breadboard cables, type male to female, and male to male.

## Troubleshooting
If you encounter any issues with the Secure Access System, try the following troubleshooting steps:
- Check the server logs for error messages.
- Make sure your Raspbery PI is configured correctly.
- Verify that all software dependencies are installed correctly. Here `requirements.txt` I am listing all of the dependancies that i used on my end, but you mind not need all of them.
- Verify that all the libraries for your electronic components are installed correctly.
- Ensure that database and database connections are configured properly.
- Make sure your electronic components are connected properly.

## Contributing
Contributions to the SAS are welcome! Follow these guidelines to contribute:

1. **Fork the repository**: Click the "Fork" button at the top right of this repository to create a copy of the repository on your GitHub account.
2. **Create a new branch**: Create a new branch for your feature or bug fix. Use a descriptive name for your branch (e.g., `feature/add-login`, `bugfix/fix-authentication`).
   `git checkout -b feature/your-feature-name`
## License
The SAS is an open to the public. licensed under the [MIT License](https://opensource.org/licenses/MIT).

3. Set up the development environment: Follow the instructions in this file to set up your development environment. Ensure that all dependencies are installed. If you install the dependancies from the requirement.txt file you have to make sure you hardware components are all setup and connected as well.

`python -m venv venv
source venv/bin/activate  # For Windows you might use venv\Scripts\activate
pip install -r requirements.txt`

4. Make your changes: Implement your feature or bug fix. Ensure that your code follows the project's coding standards and includes appropriate documentation and tests.
5. Run tests: Run the existing tests (Still under process) and add new tests as needed to ensure your changes work correctly.
pytest
6. Commit your changes: Write a clear and concise commit message describing your changes.
`git add .
git commit -m "Add detailed description of your changes"`
7. Push your changes: Push your changes to your forked repository.
`git push origin feature/your-feature-name`
8. Submit a pull request: Go to the original repository and submit a pull request. Provide a detailed description of your changes and any additional context that might be helpful for the reviewers.

We appreciate your contributions and will review your pull request as soon as possible. Thank you for helping improve the Secure Access System!

## License
The Secure Access System is open source and available to the public under the [MIT License](https://opensource.org/licenses/MIT).

The MIT License is a permissive license that allows you to freely use, modify, and distribute the software, provided that you include the original copyright notice and a copy of the license in any distribution. This means you can use the Secure Access System in your own projects, whether they are open source or proprietary.

By contributing to this project, you agree that your contributions will be licensed under the MIT License.
