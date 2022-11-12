# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2022-11-12
### Added
- Using user settings file for remembering input and output folders
### Fixed
- Error after closing window without calculation action
### Internal
- Add logging via loguru

## [1.0.0] - 2022-10-20
### Added
- Calculation of budget proposal for new year from Office Open XML format and IS VERA XML exports of statements 001, 002 and 051
- Calculation of closed municipal budgets for last years from IS VERA XML exports
- Support of IS VERA XML files used to send public finance information into Monitor (Complete overview of public finance)
- Support of Office Open XML format in specific format for City of Česká Kamenice Board and Council.
- Support for parsing 001 - Balance Sheet Statement of IS VERA export
- Support for parsing 002 - Profit and Loss Statement Statement of IS VERA export
- Support for parsing 051 - FIN 2-12 M - Budget Fulfillment of LGU Statement of IS VERA export
- Support for parsing 100 - 100 - Indicators of accounting entity Statement of Monitor (StatniPokladna) in limited scope
- Export result into HTML page based by html template with svg charts
- Export of Polozka and Radek items used in calculation into CSV file
- Export calculated indicators into CSV file
- Export all files in GUID named folder in output folder parameter
- Option to open Finder(MacOS)/Explorer(Windows) in GUID name output folder for quicker access to result
- Window for entering input parameters and for selecting needed calculation
- Window with progress bar during calculation
- Window with result information
- HTML template with final results
- Documentation in CTIME.txt for Czech non-developer users and in README.md

### Internal
- Apache 2.0 license
- PyInstaller for making *.exe and *.app release bundles
- Basic windows for common users thanks to PySimpleGUI
- Makefile with support of MacOs and Windows 10 with make tool
- Windows exe bundle minimal version targets Windows 10 build 17074
- MacOS app bundle tested on MacOS 12.6