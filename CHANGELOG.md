# Changelog

File tracks updates to the emastercard installer. Updates come as new emastercard builds or changes
to the actual package itself.

Versions are tagged following this format: <e-Mastercard version>-<BHT-EMR-API or eMastercard2Nart updated count>. For example the version 4.0.8-0 means we are on the version 4.0.8 of e-Mastercard and on the
latest version of eMastercard2Nart and BHT-EMR-API as the time of the e-Mastercard release. When either
BHT-EMR-API or eMastercard2Nart gets updated then the tag will get bumped up to 4.0.8-1.

## Unreleased

## [v4.1.0-3]

### Changed

- Bumped up BHT-EMR-API to v4.11.3

## [v4.1.0-2]

### Changed

- Bumped up BHT-EMR-API to v4.11.1 (Fixes crash on local patient merge)

## [v4.1.0-1]

### Changed

- Rebuilt application on updated e-Mastercard tag v4.1.0

## [v4.1.0-0]

### Changed

- Bumped up BHT-EMR-API to v4.11.0
- Bumped up e-Mastercard to v4.1.0

## [v4.1.0-alpha-0]

### Changed

- Bumped up BHT-EMR-API to v4.10.40
- Bumped up eMastercard to v4.1.0-alpha
- Updated offline installation steps

## [v4.0.18-0] 2021-04-06

### Changed

- Bumped up BHT-EMR-API to v4.10.35
- Bumped up eMastercard to v4.0.18

## [v4.0.17-1] 2021-04-23

### Changed

- Bumped up BHT-EMR-API to v4.10.34
- Added autoloading of metadata after loading backup

## [v4.0.17-0] 2021-04-14

### Changed

- Bumped up e-Mastercard to v4.0.17
- Bumped up BHT-EMR-API to v4.10.33

## [v4.0.16-4] 2021-04-13

### Changed

- Bumped up BHT-EMR-API to v4.10.32


## [v4.0.16-3] 2021-04-12

### Fixed

- Fixed inability to load MySQL backups when using docker-compose version < 1.20.0

## [v4.0.16-2] 2021-04-10

### Changed

- Bumped up BHT-EMR-API to v4.10.31

## [v4.0.16-1] 2021-04-08

### Changed

- Bumped up BHT-EMR-API to v4.10.27
    * See the [Changelog](https://github.com/HISMalawi/BHT-EMR-API/blob/development/CHANGELOG.md#41028---2021-04-07)
- Added progress bar to restore_database.sh script.

## [v4.0.14-0] 2021-03-27

### Changed

- Bumped up e-Mastercard to v4.0.14
- Bumped up BHT-EMR-API to v4.10.25

## [v4.0.13-1] 2021-02-22

### Changed

- Bumped up BHT-EMR-API to v4.10.24

## [v4.0.13-0] 2021-01-11

### Changed

- Bumped up e-Mastercard to v4.0.13

## [v4.0.12-0] 2020-12-23

### Changed

- Bumped up e-Mastercard to v4.0.12
- Bumped up BHT-EMR-API to v4.10.18

## [v4.0.11-0] 2020-11-24

### Changed

- Bumped up e-Mastercard to v4.0.11
- Bumped up BHT-EMR-API to v4.10.16

## [v4.0.10-0] 2020-10-26

### Changed

- Bumped up e-Mastercard to v4.0.10

## [v4.0.9-0] 2020-10-21

### Changed

- Bumped BHT-EMR-API to v4.10.15
- Bumped eMastercard to v4.0.9
