# Change Log

All notable changes to this project will be documented in this file.

## [2.00] - 2024-03-20

### Added

- Implemented an **advanced settings** window where users can exert more control over tunnel behaviors.
- Enabled the option to disable connectivity checks before setting up the tunnel within the **advanced settings**.

### Changed

- Split the configuration file into two separate files: `config.json` and `config_advanced.json`, providing more flexibility in managing configurations.

### Fixed

- Fixed an issue where the connectivity check could fail under certain conditions that do not affect the tunnel. Now, users have the option to disable the connectivity check.

## [1.10] - 2024-03-20

### Changed 

- Refactored the functionality of the RootWindow from a set of functions into a RootWindow class.

## [1.01] - 2023-07-03
   
### Changed

- Modified the method of reading the `config.json` file from using `json.dump` to using a `with` statement.

### Fixed

- Resolved a bug that allowed multiple connections.
- Corrected an issue where the contents in the **Local Port** field were overwritten.

## [1.00] - 2023-07-03
 
### Added

- Implemented SSH tunnel functionality with a graphical user interface.