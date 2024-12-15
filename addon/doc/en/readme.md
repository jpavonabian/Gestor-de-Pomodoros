# Pomodoro Manager for NVDA

## Description

**Pomodoro Manager** is an add-on for the NVDA screen reader that implements the Pomodoro technique, helping users manage their work and break times effectively. The Pomodoro technique involves dividing work time into intervals (traditionally 25 minutes), separated by short breaks. This add-on is ideal for users looking to improve productivity and better manage their time while using NVDA.

## How It Works

Once activated, the add-on allows users to start, pause, resume, or stop the Pomodoro timer using specific keyboard shortcuts. Additionally, it provides auditory and verbal feedback at the beginning and end of each work or break session. The add-on automatically manages the cycles of work and rest, including long breaks after every four completed work cycles.

### Keyboard Shortcuts
Keyboard shortcuts must be assigned from the Input Gestures option in NVDA's Preferences menu. The options can be found under the Pomodoro Manager category.

## Changelog
### 1.11
Updated to the latest NVDA testing version.
### 1.10
- Fixed a bug where time continued to advance even when a Pomodoro was paused.

### 1.9
- Changed the add-on's internal name to avoid issues with the official store.

### 1.8
- Fixed a Braille and messaging error.
- Fixed an issue with time management.
- Refactored much of the internal code.

### 1.7
- Fixed a distribution channel error.
- Fixed a bug when trying to stop a Pomodoro that had not been started before.

### 1.6
- Changed the tone duration and frequency.
- Messages from the add-on now have high priority to ensure they are not missed during other activities.
- Tones are no longer played on the right channel only; this was an error.

### 1.5
- Keyboard shortcuts have been removed. They must now be assigned by the user.

### 1.4
- Updated keyboard shortcuts for better intuitiveness.
- Tweaked the internal code slightly.
- Shortcuts now appear correctly in the gesture categories.

### 1.3
- Input gestures can now be reassigned under the "Pomodoro Manager" category. [PR #1](https://github.com/jpavonabian/Gestor-de-Pomodoros/pull/1)

### 1.2
- Fixed the add-on's internal handling by NVDA.

### 1.1
- The add-on does not run in secure screens.
- Automated release process using GitHub Actions.

### 1.0

- Initial release of the add-on.
- Basic Pomodoro functionality implemented, including starting, pausing, resuming, and stopping the timer.
- Auditory and verbal announcements for the start and end of work and break sessions.

## Special Thanks
- To Sukil Etxenike <sukiletxe@yahoo.es> for setting me on the right path when I lacked experience in developing add-ons and didn't know where to start.
- To Ángel Alcántar <rayoalcantar@gmail.com> for reviewing the code.
- To Noelia Ruiz Martínez <nrm1977@gmail.com> for the feedback on the code and for putting up with so many rookie questions.
