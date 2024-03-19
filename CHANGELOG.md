# Change Log

All notable changes to this project will be documented in this file.

## [1.10] - 2024-03-20

### Changed 

- Refactored the RootWindow functionality, originally implemented as a set of functions, into a RootWindow class.

## [1.01] - 2023-07-03
   
### Changed

- Changed the method of reading the config.json file from using `json.dump` to using `with` statement.

### Fixed

- Fixed a bug that allowed multiple connections.
- Fixed an issue where the contents in the **Local Port** field were overwritten.

## [1.00] - 2023-07-03
 
### Added

- Implemented SSH tunnel functionality with a graphical user interface.