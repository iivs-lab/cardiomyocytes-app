# Open each application window at most once per process

- Status: accepted
- Date: 2026-10-16

## Context and problem statement

Decision 0004 allows one window per sub-app in a process. The shared
menu bar now puts the same items in the launcher and in every sub-app
window, so the settings window and the About window, which also shows
the licenses, can be asked for from any of them. Without a rule, each
request could open another copy: two settings windows could edit the
same values, and the user would not know which one holds the result.

## Considered options

- One window of each kind per process, shared by every window that
  asks for it.
- One window per requesting window, such as a settings window for the
  launcher and another for each sub-app.
- No limit: every request opens a new window.

## Decision outcome

One window of each kind per process. The launcher, the settings
window, the About window, and each sub-app's window exist at most once
in a process. Asking for one that is already open, from a menu item or
a launcher button, brings it to the front, restoring it first if it is
minimized.

The GUI front end opens and tracks these windows, since it alone knows
them all; a sub-app reaches them only through the front end
(decision 0001).

## Consequences

- The front end keeps the open windows by kind and closes them all
  when the application quits.
- The settings window holds settings for the whole application and for
  every sub-app, so opening it from a sub-app shows that sub-app's
  section rather than a window of its own.
- Short-lived dialogs that belong to one window's task, such as a file
  picker or a confirmation, are not covered: each window opens its own.
- A second process still has windows of its own (decision 0004), so two
  settings windows can exist on one machine. Settings must therefore be
  written atomically (`TODO.md`).
