# Open each sub-app in its own window from a launcher

- Status: accepted
- Date: 2026-10-16

## Context and problem statement

The GUI hosts several sub-apps, and they must work together. For
example, with profile analysis and the comparison of quantified
results both open, a result quantified in profile analysis goes
straight into the comparison. The handoff left open how the main
window offers the sub-apps (a menu, tabs, or a sidebar) and proposed
that values pass between sub-apps through the frame, so that sub-apps
never import each other.

## Considered options

For the windows:

- One main window that shows the sub-apps in tabs or a sidebar.
- A launcher window with a button per sub-app, each sub-app opening in
  a window of its own.

For values passed between sub-apps:

- Through the front end: a sub-app declares the value types it
  accepts, and a sender asks the front end for targets.
- A global event bus that any sub-app publishes to and listens on.
- Sub-apps holding references to each other.

## Decision outcome

- The application opens a launcher with one button per registered
  sub-app. A button opens that sub-app in its own top-level window,
  importing the sub-app the first time.
- One process holds at most one window per sub-app; pressing the
  button again brings that window to the front. To open the same
  sub-app twice, the user starts the application again. Each process
  is isolated, and nothing passes between processes.
- Closing the launcher quits the application: the open sub-app windows
  close too, asking first about unsaved changes.
- Values pass through the GUI front end. A receiving sub-app declares
  the value types it accepts; the types live in `common/core/`, and
  the interface sub-apps use to reach the front end lives in
  `common/gui/`. A sender asks the front end which targets accept a
  value and hands it over. An action such as "add to comparison" shows
  whenever a sub-app that accepts the value is registered.
- When the target sub-app is not open, the front end asks the user
  whether to open it, and opens it and delivers the value only if the
  user agrees.

An event bus is simpler to start but hides who listens to what;
references between sub-apps break the rule that they never import
each other.

## Consequences

- A sub-app can be tested alone with a fake front end in place of the
  real one.
- Two processes can open the same result file or write the settings at
  the same time. Saving a result has to notice that the file changed
  since it was read, and settings have to be written atomically.
- Not implemented yet: the launcher has no buttons, and there are no
  sub-apps.
