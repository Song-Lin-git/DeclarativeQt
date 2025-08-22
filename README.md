## What is Declarative-Qt？

*Declarative-Qt* is a lightweight **declarative UI framework** for **Windows software** development using **Python**.
Built on the traditional imperative PyQt5, it enhances and adapts native Qt components following declarative design
principles.
Leveraging Qt's powerful signal & slot mechanism, it implements a state-driven mechanism.
Combined with an improved Python lambda syntax, it allows embedding small logic blocks and derived states directly in
the UI code, further strengthening decoupling and modularity.

#### 1. ***State-Driven UI Mechanism***

Native Qt provides a highly regarded **signal & slot** mechanism,
valued for its strong decoupling, thread safety, and powerful communication capabilities.
*Declarative-Qt* builds a state-driven mechanism on top of it.

The approach works as follows: a state class called `Remember`
<span style="color:darkcyan">(named in homage to Jetpack Compose)</span>
inherits from `QObject`, incorporates a `PyQtSignal`, and maintains a state value.
It exposes an interface to update this value, and whenever the value changes, the signal is emitted.
Components bound to this state listen to the signal and respond through their slot functions.

For example, when a `Button` is bound to a string state for its text,
its slot function reacts to the state change by calling Qt’s native `QPushButton.setText` method.
This updates only the button’s text, achieving automatic updates with minimal re-rendering.

#### 2. ***Tree-Like Indented Code Style***

Like other mainstream declarative UI frameworks,
*Declarative-Qt* allows developers to visually understand the structure of the UI component tree directly from the UI
code,
including the hierarchical relationships and relative positioning of components.
Also, developers can conveniently adjust the UI layout by changing the positions of components in the code,
without worrying about their exact coordinates.

#### 3. ***Chainable Style-Modifier***

Native Qt uses QSS
<span style="color:grey">(Qt Style Sheets, a `CSS-like` system with similar syntax and behavior)</span>
as its primary and most powerful styling mechanism.
To improve the efficiency and accuracy of writing QSS strings,
*Declarative-Qt* encapsulates QSS syntax and rules into the chainable style-modifier module called `DqtStyle`.
Combined with the state-driven mechanism,
this approach provides greater flexibility for dynamic style parameters,
enabling them to adapt dynamically to more complex and interactive UI requirements.

#### 4. ***Component Tree Building and Rendering Logic***

In *Declarative-Qt*, UI components exist as class objects.
Inner components are passed as parameters to their parent components, which store them as member variables and complete
their own initialization.

- When program runs, Python first constructs the innermost components.
  This process essentially computes the parameters required for constructing the parent component.
  As a result, the building order of components follows an inside-out, **post-order** traversal of the component tree.

- When the UI is initially displayed, Qt runs a top-down render pass
  <span style="color:grey">(`paintEvent`/...)</span> starting at the root component
  <span style="color:grey">(`QMainWindow`/`QDialog`/...)</span>.
  In effect, the component tree is **rendered in pre-order**.

- *Declarative-Qt*’s **auto-layout mechanism** is handled within the `resizeEvent`.
  Whenever the window is resized or any component's size is updated,
  the sizes and positions of its children will be recalculated and updated.
  This update, in turn, triggers the `resizeEvent` of the child components.
  Consequently, a top-down, **pre-order** partial re-layout and re-render is performed,
  starting from the outermost component that initiated the change and propagating inward.

## How to Use Declarative-Qt?

- ***Dependencies***

```text
python          3.12+
pyqt5           5.15.11
matplotlib      3.9.2
pillow          10.4.0
sqlite          3.45.3
beautifulsoup4  4.12.3
```

- ***Start with Declarative-Qt***

Use `git clone` to obtain this repository, and you can start your development tasks directly within the *Declarative-Qt*
project.

```commandline
git clone https://github.com/Song-Lin-git/DeclarativeQt.git
```

In the near future, a fully usable package will be prepared and uploaded to `PyPI`.
