<!--suppress ALL -->
<div align="center">
  <a href="https://github.com/TheTrustyPwo/Bmt-Macro/graphs/contributors" target="_blank">
    <img src="https://img.shields.io/github/contributors/TheTrustyPwo/Bmt-Macro.svg?style=for-the-badge" alt="Contributors">
  </a>
  <a href="https://github.com/TheTrustyPwo/Bmt-Macro/network/members" target="_blank">
    <img src="https://img.shields.io/github/forks/TheTrustyPwo/Bmt-Macro.svg?style=for-the-badge" alt="Forks">
  </a>
  <a href="https://github.com/TheTrustyPwo/Bmt-Macro/stargazers" target="_blank">
    <img src="https://img.shields.io/github/stars/TheTrustyPwo/Bmt-Macro.svg?style=for-the-badge" alt="Contributors">
  </a>
  <a href="https://github.com/TheTrustyPwo/Bmt-Macro/issues" target="_blank">
    <img src="https://img.shields.io/github/issues/TheTrustyPwo/Bmt-Macro.svg?style=for-the-badge" alt="Forks">
  </a>
  <a href="https://github.com/TheTrustyPwo/Bmt-Macro/blob/master/LICENSE.txt" target="_blank">
    <img src="https://img.shields.io/github/license/TheTrustyPwo/Bmt-Macro.svg?style=for-the-badge" alt="Contributors">
  </a>
</div>


<!-- PROJECT TITLE -->
<!--suppress HtmlDeprecatedAttribute, HtmlUnknownAnchorTarget -->

<div align="center">
<h3 align="center">Badminton Booking Macro</h3>
  <p align="center">
    Automatically books badminton courts with custom configuration on
    <a href="https://www.mesrc.net/">mesrc.net</a>
    <br/>
    <a href="https://github.com/TheTrustyPwo/Bmt-Macro/issues">Report Bug</a>
    ·
    <a href="https://github.com/TheTrustyPwo/Bmt-Macro/issues">Request Feature</a>
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#configuration">Configuration</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

This is a rather simple Python script which makes use of Selenium's ability
to interact with the web browser to automatically book badminton courts on
<a href="https://www.mesrc.net/">mesrc.net</a> which are free of charge.

Some awesome features:
* Lightweight
* Runs in the background
* Automatic execution at any time you want
* Instant setup and configurable

### Disclaimer
Use this program at your own risk. This is probably against the terms and conditions of the website.
This program is merely demonstrating the capabilities of the Selenium webdriver, and you are liable
for all consequences of your actions.

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- INSTALLATION -->
## Installation

Prerequisites: Cookie Editor browser extension, of if you know how to view browser cookies

### Quick Download

1. Head to <a href="https://github.com/TheTrustyPwo/Bmt-Macro/releases/">Release</a> and download the release zip file
2. Once complete, extract the zip file
3. In the extracted folder, you should see 3 files, namely `main.exe`, `config.json` and `cookies.json`
4. Go to <a href="https://www.mesrc.net/">mesrc.net</a> and sign in
5. Using the <a href="https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm?hl=en">Cookie Editor</a> extension, export your cookies which should copy them to your clipboard
6. Open `cookies.json` and clear all the text in the file and paste your cookies in
7. Note that you need to do this every time your cookies change (Which depends on your activity)
8. Modify `config.json` to your liking. Refer to the section below.
9. Finally, run main.exe which should open a terminal

### Running From Source

Alternatively, you can clone the repository can run the script from source, which
could give you more flexibility and also allowing the modification of source code.

On top of cookie editor, python and pip also must be installed on your system.

1. Clone this repository
    ```shell
   git clone https://github.com/TheTrustyPwo/Bmt-Macro.git
   cd Bmt-Macro
   ```
2. Install the required packages
    ```shell
   pip install -r requirements.txt
    ```
3. Rename `config.json.example` and `cookies.json.example` to `config.json` and `cookies.json` respectively
4. Go to <a href="https://www.mesrc.net/">mesrc.net</a> and sign in
5. Using the <a href="https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm?hl=en">Cookie Editor</a> extension, export your cookies which should copy them to your clipboard
6. Open `cookies.json` and clear all the text in the file and paste your cookies in
7. Note that you need to do this every time your cookies change (Which depends on your activity)
8. Modify `config.json` to your liking. Refer to the section below.
9. Run the script
    ```shell
   python main.py
    ```

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONFIGURATION -->
## Configuration

This is a list of configurable options in the `config.json` file and what they mean.

| Configurable | Description                                                                                                                                                                                        | Default      | Datatype |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|----------|
| `headless`   | If set to true, the browser will be invisible which will possibly increases performance and reduce unnecessary lag.                                                                                | false        | bool     |
| `debug`      | If set to true, debug messages will be printed. Screenshots will also be taken of the full webpage, but this requires headless to be enabled to work properly                                      | false        | bool     |
| `execute`    | The specific date and time to execute the script, i.e. start booking. Usually, you would want to set this to midnight and run the script overnight. It MUST be in the format `DD/MM/YYYY hh:mm:ss` | -            | str      |
| `date`       | Date which you want to book. It MUST be in the format `DD/MM/YYYY`.                                                                                                                                | -            | str      |
| `time_start` | The time you want to start playing. It MUST be an integer representing the hour in 24-hour format. (i.e. 7am is 7, 6pm is 18, etc.)                                                                | 10           | int      |
| `time_end`   | The time you want to stop playing. It MUST be an integer representing the hour in 24-hour format. (i.e. 7am is 7, 6pm is 18, etc.) Keep in mind that the maximum duration is 2 hours.              | 12           | int      |
| `purpose`    | This option should not really matter, but it is required in the booking form, and it represents your purpose. (i.e. Recreational, Competitive, etc.)                                               | Recreational | str      |
| `pax`        | This option should not really matter, but it is required in the booking form, and it represents the number of expected people that will be present.                                                | 4            | int      |

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the GNU GPLv3 License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

TheTrustyPwo - Pwo#0001 - thetrustypwo@gmail.com

Project Link: [https://github.com/TheTrustyPwo/Bmt-Macro](https://github.com/TheTrustyPwo/Bmt-Macro)

<p align="right">(<a href="#top">back to top</a>)</p>