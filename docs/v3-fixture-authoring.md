# v3 fixture authoring

V3 fixtures exercise a boundary that crosses two modules. A fixture should
contain a workspace, visible tests, hidden tests, and the expected test command
in its task metadata. Keep the cause module explicit so a regression can be
assigned to the smallest responsible component without weakening the hidden
test.
