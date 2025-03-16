```markdown
# Ansys Electromagnetics Course: Vectors

## Slide 1: Vectors

This slide introduces the topic of the presentation: **Vectors**.  It features the Ansys logo, indicating that this is part of an Ansys training module. This module will cover the fundamentals of vectors, crucial for understanding electromagnetics.

## Slide 2: Sources

This slide lists the sources used for the material presented in the module.  This provides credibility and allows learners to refer to the original texts for further study. The sources are:

*   **"Elements of Electromagnetics," by Matthew N.O. Sadiku, 5th ed. (2010)**: A widely used and respected textbook covering the fundamentals of electromagnetics.
*   **"Engineering Electromagnetics," by Nathan Ida, 3rd ed. (2015)**: Another comprehensive textbook that offers a different perspective on electromagnetics.
*   **"Microwave Engineering," by David Pozar, 4th ed. (2012)**: A classic text focusing on the higher-frequency aspects of electromagnetics, particularly relevant to microwave circuits and systems.

The slide also indicates that the material is confidential and copyrighted by ANSYS, Inc. in 2020.

## Slide 3: What is a vector?

This slide defines what a vector is and contrasts it with a scalar quantity.

**Definition:** A **vector** is any quantity that has both *magnitude* and *direction*.

**Examples (Vectors):**

*   **The coffee shop is five miles *north* of here.**  (Magnitude: 5 miles, Direction: North)
*   **Light and heat radiate *outward* from the sun at a rate of 3 × 10<sup>8</sup> m/s.** (Magnitude: 3 × 10<sup>8</sup> m/s, Direction: Outward)
*   **The cars raced around the track *counterclockwise*, reaching speeds of over 300 mph.** (Magnitude: over 300 mph, Direction: Counterclockwise)

**Definition:** A **scalar** quantity describes only *magnitude*.

**Examples (Scalars - corresponding to the vector examples above):**

*   **To get to the coffee shop, you have to drive *five miles*.** (Magnitude only: 5 miles)
*   **Light in a vacuum travels at a rate of *3 × 10<sup>8</sup> m/s*.** (Magnitude only: 3 × 10<sup>8</sup> m/s)
*   **The racing cars reached speeds of *over 300 mph*.** (Magnitude only: over 300 mph)

**Key takeaway:** The crucial difference between a vector and a scalar is the inclusion of *direction* in the vector's description.  Without direction, a quantity is a scalar.

## Slide 4: Vector Nomenclature

This slide outlines the notation conventions used throughout the module when dealing with vectors.

*   **General Vector Representation:** A general vector is represented by a letter with an overbar.  For example,  `A` represents a vector.

    ```html
    <p>A&#772;</p>
    ```

*   **Magnitude of a Vector:** The magnitude of a vector `A` can be represented in two equivalent ways:

    *   Using absolute value bars:  |`A`|
        ```html
        <p>|A&#772;|</p>
        ```

    *   Using the letter without the overbar: `A`

*   **Scalar Nature of Magnitude:** The magnitude of a vector (`A` or |`A`|) is a *scalar* quantity. It represents the "length" or "size" of the vector, without any directional information.

*   **Unit Vectors:**
    *   A unit vector is denoted by a "hat" symbol (^) over the letter, along with a subscript indicating its direction.
    *   For a vector `A`, the unit vector in the direction of `A` is represented as: `â<sub>A</sub>`
    ```html
      &acirc;<sub>A</sub>
    ```

**Key Takeaway:** Consistent notation is essential for clarity.  The overbar indicates a vector, the absolute value bars or the plain letter indicates magnitude (a scalar), and the hat indicates a unit vector.

## Slide 5: Unit Vectors

This slide defines unit vectors and explains their importance.

*   **Definition:** A *unit vector* is any vector with a magnitude equal to *one*.

*   **Unit Vector in the Direction of A:** The unit vector in the direction of a vector `A` is calculated by dividing the vector `A` by its magnitude:

    ```html
      &acirc;<sub>A</sub> = A&#772; / A
    ```
    Or, equivalently:
	```html
      &acirc;<sub>A</sub> = A&#772; / |A&#772;|
    ```

*  **Purpose of Unit Vectors**: Unit vectors are primarily used to specify a *direction*. They are particularly useful in defining coordinate systems.

*   **Coordinate Systems and Basis Vectors:**
    *   In three-dimensional space, vectors are typically described as the sum of three *linearly independent* (mutually orthogonal) components.  This means the three components point in directions that are perpendicular to each other.
    *   A *coordinate system* provides a framework for describing space.
    *   The three unit vectors used to define a coordinate system are called *basis vectors*.

**Key Takeaways:**

*   A unit vector has a magnitude of 1 and points in a specific direction.
*   Unit vectors are essential for defining directions and forming the basis of coordinate systems.
*   Basis vectors are a set of mutually orthogonal unit vectors that span a coordinate system.

## Slide 6: The Cartesian Coordinate System

This slide introduces the Cartesian coordinate system, a fundamental system for representing vectors.

*   **Basis Vectors:** The Cartesian coordinate system uses three basis vectors:
    *   `â<sub>x</sub>`:  The unit vector along the x-axis.
    *   `â<sub>y</sub>`:  The unit vector along the y-axis.
    *   `â<sub>z</sub>`:  The unit vector along the z-axis.

*   **Coordinate Variables:**  The corresponding coordinate variables are:
    *   `x`: Represents the position along the x-axis.
    *   `y`: Represents the position along the y-axis.
    *   `z`: Represents the position along the z-axis.

* **Diagram**: The diagram illustrates the Cartesian coordinate system:
  * Three mutually perpendicular axes (x, y, z) intersecting at the origin.
  * A point P in space.
  * Dashed lines projecting point P onto each axis, demonstrating how the x, y, and z coordinates define the point's location.

**Key Takeaway**: The Cartesian coordinate system provides a simple and intuitive way to represent points and vectors in three-dimensional space using three orthogonal axes and corresponding coordinates.

## Slide 7: The Cartesian Coordinate System (Continued)

This slide continues the discussion of the Cartesian coordinate system, explaining how to represent a general vector and defining the range of coordinate variables.

*   **General Vector Representation:** Any vector within the Cartesian coordinate system can be expressed as a scaled sum of the three basis vectors:

    ```
    A = Axâx + Ayây + Azâz
    ```

    Where:
    *   `A`: The vector being represented.
    *   `Ax`: The scalar magnitude of the x-component of `A`.
    *   `Ay`: The scalar magnitude of the y-component of `A`.
    *   `Az`: The scalar magnitude of the z-component of `A`.
    *   `âx`, `ây`, `âz`: The basis vectors (unit vectors) along the x, y, and z axes, respectively.

*   **Ranges of Coordinate Variables:**  The Cartesian coordinate variables (x, y, z) can take on any real value, extending from negative infinity to positive infinity:

    ```
    -∞ ≤ x ≤ +∞
    -∞ ≤ y ≤ +∞
    -∞ ≤ z ≤ +∞
    ```
    This indicates that the Cartesian coordinate system extends infinitely in all three directions.

**Key Takeaways:**

*   A vector in Cartesian coordinates is represented by the sum of its components along each axis, each component being a scalar multiple of the corresponding unit vector.
* The coordinate variables can have any real value.

## Slide 8: Vector Addition: Numerical

This slide explains how to perform vector addition numerically in the Cartesian coordinate system.

* **Basic Principle**: Vector addition involves adding corresponding components. The x-components are added together, the y-components are added together, and the z-components are added together.

* **Numerical Vector Addition:**
  Given two vectors:
  ```
    A = Axâx + Ayây + Azâz
    B = Bxâx + Byây + Bzâz
  ```
  Their sum is calculated as:
   ```
    A + B = (Ax + Bx)âx + (Ay + By)ây + (Az + Bz)âz
  ```

* **Important Note (Limitation):** This simple component-wise addition *only* works directly for vectors expressed in *Cartesian coordinates*.  For other coordinate systems (e.g., cylindrical or spherical), a direct component-wise addition is generally *not* valid, and a more complex procedure involving coordinate transformations is required.

**Key Takeaway:** Vector addition in Cartesian coordinates is straightforward: add the corresponding components. This simplicity is a major advantage of the Cartesian system.

## Slide 9: Ansys Logo

This is a closing slide simply displaying the Ansys logo. It reinforces the association of the material with Ansys software and training.
```

Okay, here's a meticulously detailed and exhaustive set of notes derived from the provided Ansys electromagnetics course PPT content, covering all key concepts, principles, equations, and examples, with comprehensive elaborations and detailed explanations.

# Electrostatic Material Interaction

This document provides detailed notes on the Ansys course "Electrostatic Material Interaction," developed by Kathryn L. Smith, PhD.

## Sources (Slide 2)

The material presented in this course is primarily based on the following textbooks:

*   **Elements of Electromagnetics**, by Matthew N.O. Sadiku, 5th ed. (2010)
*   **Engineering Electromagnetics**, by Nathan Ida, 3rd ed. (2015)
*   **Microwave Engineering**, by David Pozar, 4th ed. (2012)

These are standard, well-regarded texts in the field of electromagnetics, providing a solid theoretical foundation for the course material.

## Agenda (Slide 3)

The course focuses on understanding how electrostatic fields interact with materials.  It contrasts the behavior of electric fields in free space with their behavior within dielectric and conductive materials. The core topics covered are:

1.  **The Constitutive Relation and Boundary Conditions:** This section introduces how materials affect the relationship between the electric field (**E**) and the electric flux density (**D**). It also explores how **E** and **D** behave at the interface between different materials.
2.  **Updating the Free-Space Equations:** This section explains how the fundamental equations of electrostatics, derived for free space, are modified to account for the presence of materials.  This primarily involves scaling by the relative permittivity.
3.  **Capacitance:** This section defines capacitance, explains how to calculate it for various geometries, and relates it to the energy stored in an electric field.

**Key Concept: Free Space vs. Materials**

In free space, the relationship between the electric flux density (**D**) and the electric field (**E**) is simple:

```
D = ε₀E
```

where ε₀ is the permittivity of free space (approximately 8.854 x 10⁻¹² F/m). This equation implies a direct proportionality between **D** and **E**.  However, most practical engineering applications involve materials, not free space.  Materials polarize in the presence of an electric field, altering this relationship.

## Boundary Conditions for the Electric Field (Slides 4-9)

These slides explain the behavior of the electric field (**E**) and electric flux density (**D**) at the boundary between two different dielectric materials. Understanding these boundary conditions is crucial for solving electrostatic problems involving multiple materials.

**Scenario:** Consider a boundary between two regions:

*   **Region 1:**  Permittivity ε₁ (and relative permittivity εᵣ₁)
*   **Region 2:**  Permittivity ε₂ (and relative permittivity εᵣ₂)

It is assumed that εᵣ₁ ≠ εᵣ₂ (the materials are different).

**Decomposition of the Electric Field:**

The electric field in each region (**E₁** in Region 1 and **E₂** in Region 2) is decomposed into two components:

*   **Tangential Component (Eₜ):**  Parallel to the boundary surface.
*   **Normal Component (Eₙ):** Perpendicular to the boundary surface.

**Derivation of Boundary Conditions:**

Two fundamental laws of electromagnetism are used to derive the boundary conditions:

1.  **Faraday's Law (for tangential components):**

    *   A rectangular loop (abcd) is considered, straddling the boundary (half in Region 1, half in Region 2).  The loop's orientation is such that its normal vector points into the page (as indicated by the ⊗ symbol).
    *   Faraday's Law in integral form is applied:

        ```html
        ∮<sub>abcd</sub> <b>E</b> ⋅ d<b>l</b> = -d/dt ∫<sub>S</sub> <b>B</b> ⋅ d<b>s</b>
        ```

        Where:
          *  ∮<sub>abcd</sub> represents the closed line integral around the loop abcd.
          *  **E** is the electric field.
          *  d**l** is an infinitesimal displacement vector along the loop.
          *  d/dt is the time derivative.
          *  ∫<sub>S</sub> represents the surface integral over the area enclosed by the loop.
          *  **B** is the magnetic flux density.
          *  d**s** is an infinitesimal area vector, normal to the surface.

    *   As the height of the loop approaches zero (the sides *ad* and *bc* shrink to zero), the following happens:
        *   The surface integral of **B** goes to zero because the area enclosed by the loop goes to zero.
        *   Only the tangential components of **E** contribute to the line integral (the normal components become negligible).

    *   This leads to:

        ```
        E₁ₜd - E₂ₜd = 0
        ```
      Where 'd' is the length of sides ab and cd.

    *   Therefore, the boundary condition for the tangential component of the electric field is:

        ```
        E₁ₜ = E₂ₜ
        ```
        **The tangential component of the electric field is continuous across the boundary.**

2.  **Gauss's Law (for normal components):**

    *   A cylindrical Gaussian surface is considered, positioned with its top half in Region 1 and its bottom half in Region 2.
    *   Gauss's Law in integral form is applied:

        ```html
        ∮<sub>S</sub> <b>D</b> ⋅ d<b>s</b> = ∫<sub>V</sub> ρ<sub>v</sub> dv
        ```

        Where:
          * ∮<sub>S</sub> is the closed surface integral over the Gaussian surface.
          * **D** is the electric flux density.
          * d**s** is an infinitesimal area vector, normal to the surface.
          * ∫<sub>V</sub> is the volume integral.
          * ρ<sub>v</sub> is the volume charge density.

    * As the height of the cylinder approaches zero:
      * The contribution from the side walls go to zero.
      * Only the contributions from the top and bottom surfaces that goes to zero are non-zero.
      * The volume charge density, ρ<sub>v</sub>, inside the cylinder goes to zero.

    * If there is a surface charge density, ρ<sub>s</sub>, on the boundary, Gauss's law simplifies to:

        ```
        D₁ₙΔS - D₂ₙΔS = ρ<sub>s</sub>ΔS
        ```

    *  Dividing by ΔS, we obtain:

        ```
        D₁ₙ - D₂ₙ = ρ<sub>s</sub>
        ```

    * Using the constitutive relation (**D** = ε**E**), this can be rewritten as:

        ```
        ε₁E₁ₙ - ε₂E₂ₙ = ρ<sub>s</sub>
        ```

    *   **The normal component of the electric flux density (D) is discontinuous across the boundary by an amount equal to the surface charge density (ρ<sub>s</sub>).  If there is no surface charge (ρ<sub>s</sub> = 0), then the normal component of D is continuous.**

**Summary of Boundary Conditions (Slide 9):**

*   **Tangential Electric Field:** E₁ₜ = E₂ₜ
*   **Normal Electric Flux Density:** ε₁E₁ₙ - ε₂E₂ₙ = ρ<sub>s</sub>

These two equations are fundamental for solving electrostatic problems involving dielectric interfaces.

## Updating Free-Space Equations (Slide 10)

This section explains how to adapt the equations derived for electrostatics in free space to situations involving materials.  The key principle is to replace the permittivity of free space (ε₀) with the permittivity of the material (ε = ε₀εᵣ), where εᵣ is the relative permittivity (also known as the dielectric constant).

**Examples:**

1.  **Force between Two Charges:**

    *   **Free Space:**

        ```html
        <b>F</b>₁ = -<b>F</b>₂ = (Q₁Q₂ / (4πε₀R²)) <b>a</b><sub>R12</sub>
        ```

    *   **Material with permittivity ε = ε₀εᵣ:**

        ```html
        <b>F</b>₁ = -<b>F</b>₂ = (Q₁Q₂ / (4πε₀ε<sub>r</sub>R²)) <b>a</b><sub>R12</sub>
        ```

    The force is reduced by a factor of εᵣ compared to the force in free space.

2.  **Voltage due to a Point Charge:**

    *   **Free Space:**

        ```
        V = Q₁ / (4πε₀r₁)
        ```

    *   **Material with permittivity ε = ε₀εᵣ:**

        ```
        V = Q₁ / (4πε₀εᵣr₁)
        ```

    The voltage is also reduced by a factor of εᵣ.

3.  **Electrostatic Energy Density:**

    *   **Free Space:**

        ```
        w<sub>E</sub> = (1/2)ε₀E²
        ```

    *   **Material with permittivity ε = ε₀εᵣ:**

        ```
        w<sub>E</sub> = (1/2)ε₀εᵣE² = (1/2)εE² = (1/2)<b>D</b> ⋅ <b>E</b>
        ```
       The energy density *increases* by a factor of εᵣ. This is because the material stores energy in the polarization of its molecules.

**General Rule:**

Whenever ε₀ appears in a free-space electrostatic equation, replace it with ε = ε₀εᵣ to obtain the corresponding equation for a material with relative permittivity εᵣ.

## Capacitance (Slides 11-16)

These slides define capacitance, explain methods for calculating it, and connect it to electrostatic energy storage.

**Definition of Capacitance:**

Capacitance (C) is defined as the ratio of the magnitude of the charge (Q) on either conductor of a two-conductor system to the magnitude of the potential difference (V) between the conductors:

```
C = Q / V
```

The unit of capacitance is the Farad (F), where 1 Farad = 1 Coulomb/Volt.

**Parallel Plate Capacitor Example (Slides 11, 14, 15):**

*   **Geometry:** Two parallel conductive plates, each with area A = wl (width * length), separated by a distance d. The space between the plates is filled with a dielectric material of permittivity ε = ε₀εᵣ.

*   **Calculating Capacitance (Method 1: Charge Approach - Slide 14):**

    1.  **Assume Charges:** Place a charge +Q on one plate and -Q on the other.
    2.  **Apply Gauss's Law:**  Assume negligible fringing fields (i.e., the electric field is uniform and perpendicular to the plates). Apply Gauss's Law to a Gaussian surface enclosing one of the plates:

        ```
        Q<sub>encl</sub> = +Q = ∫∫ ε<b>E</b> ⋅ d<b>s</b> = ∫₀<sup>w</sup> ∫₀<sup>l</sup> εE(-<b>a</b><sub>z</sub>) ⋅ dxdy(<b>a</b><sub>z</sub>) = -εEwl
        ```
        Here it's assumed that the plates are on x-y plane and +z axis is pointing from -Q plate to +Q plate.

    3.  **Solve for Electric Field:**

        ```
        <b>E</b> = -(Q / (ε₀εᵣwl)) <b>a</b><sub>z</sub>
        ```

    4.  **Calculate Voltage:** Integrate the electric field along a path from the negatively charged plate to the positively charged plate:

        ```
        V = -∫ <b>E</b> ⋅ d<b>l</b> = -∫₀<sup>d</sup> -(Q / (ε₀εᵣwl)) <b>a</b><sub>z</sub> ⋅ dz <b>a</b><sub>z</sub> = Qd / (ε₀εᵣwl)
        ```

    5.  **Calculate Capacitance:**

        ```
        C = Q / V = ε₀εᵣwl / d = εA / d
        ```

*   **Calculating Capacitance (Method 2: Voltage Approach - Slide 15):**

    1.  **Assume Voltage:** Apply a test voltage V across the plates.
    2.  **Calculate Electric Field (assuming no fringing):**

        ```
        <b>E</b> = -∇V = -(V/d) <b>a</b><sub>z</sub>
        ```
        Since the voltage varies linearly from 0 to V across the distance d.

    3.  **Apply Gauss's Law:** Use Gauss's law to find the charge on one of the plates (knowing the electric field):

        ```
        Q<sub>encl</sub> = +Q = ∫∫ ε<b>E</b> ⋅ d<b>s</b> = ∫₀<sup>w</sup> ∫₀<sup>l</sup> ε(-V/d)<b>a</b><sub>z</sub> ⋅ dxdy(<b>a</b><sub>z</sub>) = εwlV/d
        ```

    4.  **Calculate Capacitance:**

        ```
        C = Q / V = ε₀εᵣwl / d = εA / d
        ```

**General Procedure for Calculating Capacitance (Slide 12):**

1.  **Charge Approach:**
    *   Place a test charge +Q on one conductor and -Q on the other (if there are two conductors). If there's only one conductor, assume the other conductor is at infinity.
    *   Calculate the electric field **E** resulting from the test charge distribution.
    *   Integrate the electric field from one conductor to the other (or from infinity to the conductor) to find the voltage V in terms of Q.
    *   Calculate C = Q/V.

2.  **Voltage Approach:**
    *   Assume a test voltage V between the conductors (or between the conductor and ground).
    *   Calculate the electric field **E** resulting from the applied voltage (often using **E** = -∇V).
    *   Calculate the charge Q on one of the conductors using Gauss's Law or other appropriate methods.
    *   Calculate C = Q/V.

**Capacitance and Energy Storage (Slide 16):**

The energy (W) stored in a capacitor is related to the capacitance (C) and the voltage (V) or charge (Q):

```
W = (1/2)CV² = (1/2)QV = (1/2)(Q²/C)
```

This is derived from the general expression for the electrostatic energy stored in a system of charges:

```
W<sub>E</sub> = (1/2) ∑<sub>k=1</sub><sup>N</sup> Q<sub>k</sub>V<sub>k</sub>
```

For a capacitor, this simplifies to the above equations because there are only two "charges" (+Q and -Q) at potentials V and 0 (or V/2 and -V/2, depending on the reference). The capacitor stores energy in the electric field between its plates. The presence of a dielectric material (εᵣ > 1) increases the capacitance and therefore increases the amount of energy that can be stored for a given voltage.

Okay, here are the detailed notes from the provided Ansys "Magnetostatics in Free Space" course slides, meticulously crafted with comprehensive explanations, elaborations, and accurate representations of all concepts, equations, and examples. Markdown is the primary formatting language, with HTML used as needed for enhanced presentation.

# Magnetostatics in Free Space - Ansys Innovation Course

## Sources (Slide 2)

The course material is derived from the following electromagnetics textbooks:

*   **"Elements of Electromagnetics"** by Matthew N.O. Sadiku, 5th edition (2010)
*   **"Engineering Electromagnetics"** by Nathan Ida, 3rd edition (2015)
*   **"Microwave Engineering"** by David Pozar, 4th edition (2012)

These are standard, well-respected texts in the field of electromagnetics, indicating that the course material is likely to be rigorous and accurate.

## Introduction to Magnetic Fields (Slides 3-6)

### Fundamental Concepts and Definitions

Before delving into the mechanics of magnetic fields, the course introduces essential definitions and electromagnetic constants:

*   **Electromagnetic Constant (μ₀):** This is the magnetic permeability of free space.  It represents the ability of a vacuum to support the formation of a magnetic field.  It's a fundamental constant, analogous to the permittivity of free space (ε₀) in electrostatics.
    *   Value: μ₀ = 4π × 10⁻⁷ Henrys per meter (H/m)
    *   Significance:  μ₀ appears in almost every equation related to magnetostatics in free space, connecting current and charge to magnetic fields.

*   **Fundamental Magnetic Fields:**
    *   **Magnetic Field Strength (H):**  Measured in amperes per meter (A/m).  It represents the *effort* to establish a magnetic field.  It's directly related to the current creating the field.  Think of it as the *cause* of the magnetic field.
    *   **Magnetic Flux Density (B):** Measured in Tesla (T).  This is the *effect* of the magnetic field. It describes the *density* of magnetic field lines (flux) passing through a given area. It's directly related to the force experienced by moving charges in the field.  It is also often referred to as the magnetic field, though magnetic field intensity is the technically correct term for H.

*   **Relationship in Vacuum:**  In a vacuum (and to a very good approximation, in air), the magnetic flux density (B) and magnetic field strength (H) are directly proportional, connected by the permeability of free space (μ₀):

    ```html
    <p><b>B</b> = μ<sub>0</sub><b>H</b></p>
    ```

    Where:
    *   **B** is a vector quantity representing the magnetic flux density.
    *   μ₀ is the permeability of free space.
    *   **H** is a vector quantity representing the magnetic field strength.

    This simple relationship is crucial for calculations in free space.  It shows that a stronger magnetic field strength (H) directly results in a stronger magnetic flux density (B).

*   **Fundamental Field Sources:**
    *   **Electric Charge (Q):**  Measured in Coulombs (C).  *Stationary* charges are the source of *electric* fields.
    *   **Electric Current Density (J):**  Measured in Amperes per meter squared (A/m²).  This represents the flow of electric charge per unit area.  *Moving* charges (i.e., current) are the source of *magnetic* fields.  The vector nature of **J** indicates both the magnitude and direction of the current flow.

### Magnetic Flux

* **Definition:** Magnetic flux (Ψ) through a surface (S) quantifies the "amount" of magnetic field passing through that surface. It's a scalar quantity.

* **Equation:**

  ```html
  <p>Ψ = ∫<sub>S</sub> <b>B</b> ⋅ <i>d</i><b>s</b></p>
  ```

  Where:

  *   Ψ is the magnetic flux.
  *   **B** is the magnetic flux density vector.
  *   *d* **s** is a differential area vector, perpendicular to the surface S at each point.  The dot product (**B** ⋅ *d* **s**) takes the component of **B** that is perpendicular to the surface.
  *   ∫<sub>S</sub> denotes a surface integral over the surface S.

* **Interpretation:** The magnetic flux is essentially a measure of how many magnetic field lines are "captured" by the surface. If the magnetic field is uniform and perpendicular to the surface, the flux is simply B * A (where A is the area of the surface). If the field is at an angle, the dot product accounts for the component of the field perpendicular to the surface.

### Magnetic Fields and Moving Charges (Slide 4)

*   **Fundamental Principle:** Magnetic fields are produced by *moving* electric charges. This is a key difference from electric fields, which are produced by *both* stationary and moving charges.

*   **Examples:**
    *   **Electric Current:** A current flowing through a wire creates a magnetic field around the wire. The field lines form concentric circles around the wire (as shown in the slide's diagram).
    *   **Electrons Orbiting Atoms:**  Electrons orbiting the nucleus of an atom constitute a tiny current loop, and therefore generate a small magnetic field.  This is the basis of magnetism in materials.

*   **Note about Changing Electric Fields:**  The slide mentions that changing electric fields *can* also create magnetic fields. This is a crucial concept in *electrodynamics* (time-varying fields), but it's not relevant in *magnetostatics* (steady-state, time-invariant fields).  This foreshadows Faraday's Law of Induction, which is beyond the scope of this introductory magnetostatics course.

## Monopoles and Dipoles (Slides 7-9)

### Magnetic Monopoles

*   **Definition:** A magnetic monopole is a hypothetical isolated magnetic "charge" – either a "north" pole or a "south" pole existing independently.

*   **Contrast with Electrostatics:** In electrostatics, electric monopoles (positive and negative charges) exist freely. You can have an isolated positive charge or an isolated negative charge.

*   **Experimental Status:**  *No magnetic monopoles have ever been observed experimentally.*  All known magnetic sources are *dipoles*.

* **Solenoidal Law (Absence of Magnetic Monopoles):** This fundamental law of magnetism states that there are no magnetic monopoles.  It's expressed in two equivalent forms:

    *   **Point Form (Differential Form):**

        ```html
        <p>∇ ⋅ <b>B</b> = 0</p>
        ```
        This states that the divergence of the magnetic flux density (**B**) is always zero.  Divergence measures the "outflow" of a vector field from a point.  Zero divergence means there are no "sources" or "sinks" of magnetic field lines – they always form closed loops.

    *   **Integral Form:**

        ```html
        <p>∮<sub>S</sub> <b>B</b> ⋅ <i>d</i><b>s</b> = 0</p>
        ```
        This states that the magnetic flux through *any closed surface* is always zero.  This is a direct consequence of the absence of magnetic monopoles.  Any magnetic field lines that enter a closed surface must also exit it, resulting in a net flux of zero.  This is analogous to Gauss's Law for magnetism.

### Magnetic Dipoles

*   **Definition:** A magnetic dipole consists of a north and a south magnetic pole, *always* existing together.  You cannot separate the north and south poles of a magnet.

*   **Field Lines:** Magnetic field lines always form closed loops.  They emerge from the north pole, curve around, and enter the south pole.  *Inside* the magnet, the field lines continue from the south pole back to the north pole, completing the loop.

*   **Lowest-Order Polarity:**  A dipole is the lowest-order magnetic field configuration possible.  You cannot have a magnetic monopole; the simplest magnetic source is a dipole.

*   **Analogy with Electric Dipoles:** The *external* field pattern of a magnetic dipole is very similar to that of an electric dipole (formed by a positive and a negative charge). However, the internal structure is fundamentally different. Electric field lines originate on positive charges and terminate on negative charges, while magnetic field lines always form closed loops.

*   **Illustrations (Slides 8 & 9):**  The slides clearly show the difference between electric and magnetic dipole field lines, emphasizing the closed-loop nature of magnetic fields. The close-up view of the internal field lines within a magnet (Slide 9) is crucial for understanding this concept.

## Ampere's Law in a Vacuum (Slides 11-13)

### Ampere's Circuital Law

*   **Statement:** Ampere's Law relates the circulation of the magnetic field (**B**) around a closed loop to the total current passing through that loop.  It's a fundamental law of magnetostatics, analogous to Gauss's Law in electrostatics.

*   **Point Form (Differential Form):**

    ```html
    <p>∇ × <b>B</b> = μ<sub>0</sub><b>J</b></p>
    ```

    Where:

    *   ∇ × **B** is the curl of the magnetic flux density.  Curl measures the "rotation" or "circulation" of a vector field at a point.
    *   μ₀ is the permeability of free space.
    *   **J** is the current density vector.

    This equation states that a non-zero current density (**J**) creates a circulating magnetic field (**B**).  The direction of the circulation is determined by the right-hand rule.

*   **Integral Form:**

    ```html
    <p>∮<sub>C</sub> <b>B</b> ⋅ <i>d</i><b>l</b> = μ<sub>0</sub>I<sub>tot</sub></p>
    ```
    Where:

    *   ∮<sub>C</sub> denotes a line integral around a closed loop C.
    *   **B** is the magnetic flux density vector.
    *   *d* **l** is a differential length vector along the loop C.  The dot product (**B** ⋅ *d* **l**) takes the component of **B** that is tangential to the loop at each point.
    *   μ₀ is the permeability of free space.
    *   I<sub>tot</sub> is the *total* current passing through the surface bounded by the loop C.

    This is the most commonly used form of Ampere's Law.  It states that the line integral of the magnetic field around a closed loop is proportional to the total current enclosed by that loop.

*   **Interpretation (Slide 12):** The illustration on Slide 12 is essential for understanding Ampere's Law.
    *   The closed loop (C) is shown in blue.
    *   The integration surface is any surface bounded by the loop C.
    *   The current (I<sub>tot</sub>) is represented by an arrow.
    *   The symbols  ⊙ (dot in a circle) and ⊗ (cross in a circle) represent vectors pointing *out of* and *into* the page, respectively.  These indicate the direction of the magnetic field lines.

*   **Simplified Case (Slide 13):** If the loop C is chosen such that the magnitude of **B** is constant along the loop and **B** is always parallel to *d* **l**, then the integral simplifies:

    ```html
    <p>B ∮<sub>C</sub> <i>dl</i> = μ<sub>0</sub>I<sub>tot</sub></p>
    <p>B = (μ<sub>0</sub>I<sub>tot</sub>) / (∮<sub>C</sub> <i>dl</i>)</p>
    ```
    If the loop is a circle of radius *r*, then ∮<sub>C</sub> *dl* = 2π*r*. This is often used to calculate the magnetic field around a long, straight wire.

## Magnetic Vector Potential (Slides 14-16)

### Definition and Motivation

*   **Mathematical Construct:** The magnetic vector potential (**A**) is a mathematical tool used to simplify the calculation of magnetic fields. It's not a directly measurable physical quantity like **B** or **H**, but it's a very useful concept.

*   **Origin:** The definition of **A** stems from the solenoidal law (∇ ⋅ **B** = 0).  A fundamental vector calculus identity states that the divergence of the curl of *any* vector field is always zero:

    ```html
    <p>∇ ⋅ (∇ × <b>A</b>) = 0</p>
    ```

*   **Definition:**  Since ∇ ⋅ **B** = 0 and ∇ ⋅ (∇ × **A**) = 0, we *define* the magnetic vector potential **A** such that:

    ```html
    <p><b>B</b> = ∇ × <b>A</b></p>
    ```

    This guarantees that the solenoidal law is automatically satisfied.

### Derivation of the Equation for A

*   **Starting Point:**  Ampere's Law in differential form: ∇ × **B** = μ₀**J**

*   **Substitution:** Substitute **B** = ∇ × **A**:

    ```html
    <p>∇ × (∇ × <b>A</b>) = μ<sub>0</sub><b>J</b></p>
    ```

*   **Vector Identity:** Apply the vector identity: ∇ × (∇ × **A**) = ∇(∇ ⋅ **A**) - ∇²**A**

    ```html
    <p>∇(∇ ⋅ <b>A</b>) - ∇²<b>A</b> = μ<sub>0</sub><b>J</b></p>
    ```

*   **Gauge Freedom (Helmholtz's Theorem):** Helmholtz's theorem states that a vector field is uniquely defined by its curl and its divergence.  We've already specified the curl of **A** (since **B** = ∇ × **A**).  We have the freedom to choose the divergence of **A** (this is called "gauge freedom").

*   **Coulomb Gauge:**  For simplicity, we choose ∇ ⋅ **A** = 0 (this is called the Coulomb gauge).  This simplifies the equation:

    ```html
    <p>∇²<b>A</b> = -μ<sub>0</sub><b>J</b></p>
    ```

    This is a vector Poisson equation, similar in form to the Poisson equation for the electric potential in electrostatics.

*   **Solution:** The solution to this equation (in free space) is given by:

    ```html
    <p><b>A</b>(<b>r</b>) = (μ<sub>0</sub> / 4π) ∫<sub>v'</sub> (<b>J</b>(<b>r'</b>) / |<b>r</b> - <b>r'</b>|) <i>dv'</i></p>
    ```

    Where:

    *   **A**( **r**) is the magnetic vector potential at the observation point **r**.
    *   **J**( **r'**) is the current density at the source point **r'**.
    *   | **r** - **r'**| is the distance between the observation point and the source point.
    *   ∫<sub>v'</sub> denotes a volume integral over the region v' where the current density is non-zero.
    *  The primed coordinates indicate the source, while the unprimed coordinates indicate the location where the field is being calculated.

*   **Calculating B from A:** Once **A** is known, the magnetic flux density **B** can be calculated by taking the curl:

    ```html
    <p><b>B</b> = ∇ × <b>A</b> = ∇ × [(μ<sub>0</sub> / 4π) ∫<sub>v'</sub> (<b>J</b>(<b>r'</b>) / |<b>r</b> - <b>r'</b>|) <i>dv'</i>]</p>
    ```
    While the equation looks complicated, the key is that often it is easier to calculate **A** first from the integral, and then calculate **B** from the curl of **A**, rather than directly calculating **B** using the Biot-Savart law (discussed later).

## Magnetic Force Law (Slides 17-19)

### Force on a Moving Charge

*   **Equation:** The magnetic force (**F**<sub>m</sub>) on a charge (q) moving with velocity (**u**) in a magnetic field (**B**) is given by:

    ```html
    <p><b>F</b><sub>m</sub> = q<b>u</b> × <b>B</b></p>
    ```

    Where:

    *   **F**<sub>m</sub> is the magnetic force vector.
    *   q is the electric charge.
    *   **u** is the velocity vector of the charge.
    *   **B** is the magnetic flux density vector.
    *   × denotes the cross product.

*   **Direction:** The force is perpendicular to *both* the velocity of the charge and the magnetic field. The direction is determined by the right-hand rule for cross products.

*   **Magnitude:** The magnitude of the force is given by:  F<sub>m</sub> = q u B sin(θ), where θ is the angle between **u** and **B**.  The force is maximum when the velocity is perpendicular to the magnetic field (θ = 90°) and zero when the velocity is parallel to the magnetic field (θ = 0° or 180°).

*   **Lorentz Force Law:**  When both electric and magnetic fields are present, the total force (**F**) on a charge is the sum of the electric force (q**E**) and the magnetic force (q**u** × **B**):

    ```html
    <p><b>F</b> = q(<b>E</b> + <b>u</b> × <b>B</b>)</p>
    ```

    This is the complete Lorentz force law, describing the total electromagnetic force on a moving charge.

### Force on a Current-Carrying Wire

*   **Derivation:** Consider a small segment of wire of length *d* **l** carrying a current I.  The moving charges within the wire experience a magnetic force.  We can relate the charge and velocity to the current and length:

    *   q**u** can be rewritten as I *d* **l**, where I is the current and *dl* is a vector representing a differential length element of the wire in the direction of the current.
*   **Equation:** The differential magnetic force (d**F**<sub>m</sub>) on a current element I *d* **l** in a magnetic field **B** is:

    ```html
    <p><i>d</i><b>F</b><sub>m</sub> = I <i>d</i><b>l</b> × <b>B</b></p>
    ```

*   **Interpretation:** This equation is crucial for calculating the force on current-carrying wires in magnetic fields.  The direction of the force is determined by the right-hand rule (applied to *d* **l** × **B**). The total force on a wire is found by integrating this expression over the entire length of the wire.

## Biot-Savart Law (Slides 20-25)

### Introduction

*   **Purpose:** The Biot-Savart Law provides a way to calculate the magnetic field (**B**) produced by a steady current distribution. It's an alternative to Ampere's Law, and it's particularly useful for calculating fields from complex current configurations where Ampere's Law is difficult to apply.

*   **Derivation (Conceptual):** The Biot-Savart Law can be derived by considering the interaction between two current loops.  Loop 1 creates a magnetic field (according to Ampere's Law). Loop 2 experiences a force due to this magnetic field (according to the magnetic force law). By analyzing this interaction and comparing the equations, the Biot-Savart Law emerges.

### Equation (for a Current Element)

*   **Differential Form:** The magnetic field (d**B**) produced by a differential current element I *d* **l'** at a point **r** is given by:
    ```html
    <p><i>d</i><b>B</b> = (μ<sub>0</sub>I / 4π) (<i>d</i><b>l'</b> × <span style="text-decoration: overline">a</span><sub>r</sub>) / R²</p>
    ```
    Where:
    *   d**B** represents the differential contribution to the magnetic field intensity at point **r**.
    *   μ<sub>0</sub> is the permeability of free space.
    * I is the current.
    * <i>d</i><b>l'</b> is a vector element of length pointing in the direction of the current I (at the source point).
    * <span style="text-decoration: overline">a</span><sub>r</sub> is a unit vector pointing from the source point (where the current element is located) to the field point (where we are calculating the magnetic field).
    * R is the magnitude of the distance vector, pointing from the current element to the point at which the field is being determined.

* **Alternative form:**
    ```html
     <p><i>d</i><b>B</b> = (μ<sub>0</sub>I / 4π) (<i>d</i><b>l'</b> × (<b>r</b> - <b>r'</b>)) / |<b>r</b> - <b>r'</b>|³</p>
    ```
    Where:
    * **r** is position vector of the observation point.
    * **r'** is position vector of the current element.
    * |<b>r</b> - <b>r'</b>| is the distance between the observation point and the current element.

### Equation (for a Volume Current)

*   **General Form:** For a volume current density **J**, the Biot-Savart Law becomes:

    ```html
    <p><b>B</b>(<b>r</b>) = (μ<sub>0</sub> / 4π) ∫<sub>v'</sub> (<b>J</b>(<b>r'</b>) × (<b>r</b> - <b>r'</b>)) / |<b>r</b> - <b>r'</b>|³ <i>dv'</i></p>
    ```

    Where:

    *   **B**( **r**) is the magnetic flux density at the observation point **r**.
    *   **J**( **r'**) is the current density at the source point **r'**.
    *   | **r** - **r'**| is the distance between the observation point and the source point.
    *   ∫<sub>v'</sub> denotes a volume integral over the region v' where the current density is non-zero.

*   **Key Points:**
    *   The Biot-Savart Law is a vector equation. The direction of **B** is determined by the cross product.
    *   The integral can be challenging to evaluate for complex current distributions.
    *   The law applies only to *time-invariant* (steady) currents.

## Magnetic Scalar Potential (Slide 26)

*   **Analogy to Electric Potential:** Just as the electric field (**E**) can be expressed as the negative gradient of an electric scalar potential (V) in regions where there are no time-varying magnetic fields (i.e., ∇ × **E** = 0), we can define a magnetic scalar potential (V<sub>m</sub>) *in regions where there is no current* (i.e., **J** = 0). This approach simplifies calculations in current-free regions.

* **Definition (in regions with no current):**
	```html
	<p><b>B</b>=-μ<sub>0</sub>∇V<sub>m</sub></p>
	```

	Note that this is not a general definition, as it requires that **J** = 0, which makes Ampere's Law become:
	```html
    <p>∇ × <b>B</b> = 0</p>
    ```
    In cases where  ∇ × **B** = 0, we can use the Magnetic Scalar Potential. Where ∇ × **B** ≠ 0, we must use the Magnetic Vector Potential.
* **Limitations:** The magnetic scalar potential is *not* as universally applicable as the magnetic vector potential. It can only be used in regions where the current density (**J**) is zero. The magnetic vector potential (**A**) can be used in *all* situations, including those with non-zero current.

This concludes the detailed notes from the Ansys Magnetostatics course slides. The notes cover all concepts presented, providing in-depth explanations, equations, and connections between different topics. The use of both Markdown and HTML allows for clear and accurate presentation of the material. This level of detail is intended to be comprehensive and serve as a complete record of the course content.

```markdown
# Magnetostatic Material Interaction - Ansys Course Notes

Developed by Kathryn L. Smith, PhD

These notes provide a comprehensive overview of the Ansys course on Magnetostatic Material Interaction.

## Page 1: Title Page

*   **Title:** Magnetostatic Material Interaction
*   **Developer:** Kathryn L. Smith, PhD
*   **Company:** Ansys

## Page 2: Sources

This section lists the primary sources used for the course material:

*   **Elements of Electromagnetics,** by Matthew N.O Sadiku, 5th ed. (2010)
*   **Engineering Electromagnetics,** by Nathan Ida, 3rd ed. (2015)
*   **Microwave Engineering,** by David Pozar, 4th ed. (2012)

These textbooks are well-regarded and standard references in the field of electromagnetics.

## Page 3: Agenda

This page outlines the topics that will be covered in the course. The core concept is understanding how magnetic fields interact with materials, going beyond the simplified case of free space.

*   **Introduction:**  In free space, the relationship between magnetic field intensity (<span style="text-decoration: overline">H</span>) and magnetic flux density (<span style="text-decoration: overline">B</span>) is straightforward: <span style="text-decoration: overline">B</span> = μ<sub>0</sub><span style="text-decoration: overline">H</span>, where μ<sub>0</sub> is the permeability of free space.  However, real-world applications involve materials, not just free space.  This course will explore the interaction of magnetic fields with materials.

*   **Topics Covered:**
    1.  **The Constitutive Relation:** This defines how a material responds to an applied magnetic field.
    2.  **Boundary Conditions for the Magnetic Field:**  Describes how the magnetic field behaves at the interface between different materials.
    3.  **Inductance:**  A measure of a circuit's ability to store energy in a magnetic field.
    4.  **Energy, Forces, and Torques:**  Calculations related to the energy stored in a magnetic field and the forces/torques it exerts.
    5.  **Faraday's Law and Lenz's Law:**  Fundamental laws governing electromagnetic induction.
    6.  **Motional and Transformer EMF:**  Types of electromotive force (voltage) induced by magnetic fields.

## Page 4: The Constitutive Relation (Part 1)

This page introduces the concept of atomic magnetization.

*   **Atomic Magnetization (m):**  Within a material, the movement of electrons around the nucleus of an atom creates tiny magnetic dipoles, represented by the atomic magnetization vector, <span style="text-decoration: overline">m</span>.  This is analogous to a tiny current loop.  Each electron's orbital motion and intrinsic spin contribute to this magnetic moment.

* **Diagram Explanation**: The bar magnet shows an idealized scenario of atomic magnetization.  The dotted circle represents the electron's orbital movement. The vector J represents current.

## Page 5: The Constitutive Relation (Part 2)

This page explains the behavior of atomic moments in an unbiased material.

*   **Random Orientation:** In a neutral, unbiased material (no external magnetic field applied), these atomic magnetic moments (<span style="text-decoration: overline">m</span>) are randomly oriented.

*   **Zero Net Magnetic Field:** Because of the random orientation, the vector sum of all the atomic magnetic moments is zero. This results in no net macroscopic magnetic field.

* **Diagram Explanation:** The diagram shows multiple bar magnets (representing atoms) with their north (N) and south (S) poles randomly oriented, illustrating the cancellation of magnetic moments.

## Page 6: The Constitutive Relation (Part 3)

This section describes the alignment of atomic moments in the presence of an applied magnetic field.

*   **Applied Field (H<sub>a</sub>):** When an external magnetic field (<span style="text-decoration: overline">H</span><sub>a</sub>) is applied to the material, the atomic magnetic moments tend to align with the applied field.

*   **Response Field (H<sub>r</sub>):**  This alignment creates a net magnetic field within the material, known as the response field (<span style="text-decoration: overline">H</span><sub>r</sub>). The response field is due to the collective alignment of the atomic magnetic moments.

* **Diagram Explanation:** The applied magnetic field is shown pointing upwards.  The atomic magnets (N and S poles) align with this field, creating a net magnetic field (response field) in the same direction.

## Page 7: The Constitutive Relation (Part 4)

This page formalizes the constitutive relation and introduces the concept of relative permeability.

*   **Relative Permeability (μ<sub>r</sub>):** The material's response to the applied magnetic field is quantified by its relative permeability (μ<sub>r</sub>). This is a dimensionless quantity that indicates how much more (or less) permeable the material is compared to free space.

*   **Constitutive Relation:** The relationship between <span style="text-decoration: overline">B</span> and <span style="text-decoration: overline">H</span> in a material is given by:

    <span style="text-decoration: overline">B</span> = μ<sub>0</sub>μ<sub>r</sub> * <span style="text-decoration: overline">H</span> = μ * <span style="text-decoration: overline">H</span>

    where:
    *   μ = μ<sub>0</sub>μ<sub>r</sub> is the permeability of the material.
    *   `*` denotes convolution.

*   **Homogeneity:** The constitutive relation assumes the material is *homogeneous* (uniform properties throughout) or appears homogeneous at the wavelength scale. This means that the material's properties are consistent regardless of the location within the material. If the size of the atoms is much smaller than the wavelength, the material is considered homogeneous.

*   **Frequency Dependence:**  In reality, μ<sub>r</sub> can be a function of frequency.  The convolution operation (`*`) accounts for this frequency dependence.  However, for simplification, the course assumes μ<sub>r</sub> is constant with respect to frequency.

*   **Simplified Constitutive Relation:**  With the constant μ<sub>r</sub> assumption, the constitutive relation becomes:

    <span style="text-decoration: overline">B</span> = μ<span style="text-decoration: overline">H</span>

## Page 8: Boundary Conditions for the Magnetic Field (Part 1)

This page introduces the scenario of a magnetic field crossing a boundary between two different materials.

*   **Dissimilar Media:**  When a magnetic field encounters a boundary between two materials with different relative permeabilities (μ<sub>r1</sub> ≠ μ<sub>r2</sub>), the field will change direction and magnitude.

*   **Surface Current (J<sub>s</sub>):** A surface current (<span style="text-decoration: overline">J</span><sub>s</sub>) may be generated on the boundary between the two media. This current is a result of the discontinuity in the magnetic field.

* **Diagram Explanation**: The diagram shows a magnetic field (<span style="text-decoration: overline">H</span><sub>1</sub>) in Region 1 (with permeability μ<sub>1</sub>) impinging on the boundary. A surface current (<span style="text-decoration: overline">J</span><sub>s</sub>) is generated at the boundary, flowing into the page (indicated by the circles with x's). The magnetic field in Region 2 (with permeability μ<sub>2</sub>) is <span style="text-decoration: overline">H</span><sub>2</sub>.

## Page 9: Boundary Conditions for the Magnetic Field (Part 2)

This section decomposes the magnetic field into normal and tangential components and applies Ampere's Law.

*   **Normal and Tangential Components:**  To analyze the behavior at the boundary, the magnetic field is decomposed into components normal (perpendicular) and tangential (parallel) to the boundary.
    *   <span style="text-decoration: overline">H</span><sub>1n</sub>: Normal component of <span style="text-decoration: overline">H</span><sub>1</sub>
    *   <span style="text-decoration: overline">H</span><sub>1t</sub>: Tangential component of <span style="text-decoration: overline">H</span><sub>1</sub>
    *   <span style="text-decoration: overline">H</span><sub>2n</sub>: Normal component of <span style="text-decoration: overline">H</span><sub>2</sub>
    *   <span style="text-decoration: overline">H</span><sub>2t</sub>: Tangential component of <span style="text-decoration: overline">H</span><sub>2</sub>

*   **Ampere's Law:** Ampere's Law is applied to a rectangular contour (abcd) that lies across the boundary, with half of the contour in each region. The contour is oriented such that its normal is tangential to the boundary.

* **Diagram Explanation:** The rectangle abcd is drawn across the boundary. The sides 'ad' and 'bc' are very small.

## Page 10: Boundary Conditions for the Magnetic Field (Part 3)

This page derives the boundary condition for the tangential component of the magnetic field.

*   **Ampere's Law Applied:** Ampere's Law states that the line integral of the magnetic field intensity around a closed loop is equal to the enclosed current:

    ∮<sub>abcd</sub> <span style="text-decoration: overline">H</span> ⋅ d<span style="text-decoration: overline">l</span> = I<sub>enclosed</sub>

*   **Height Approaching Zero:** As the height of the rectangular contour (sides *ad* and *bc*) approaches zero, the contribution of the normal components of the magnetic field to the line integral becomes negligible.

*   **Tangential Components Remain:** Only the tangential components of the magnetic field contribute to the line integral:

     ∫<sub>ab</sub> <span style="text-decoration: overline">H</span><sub>1t</sub> ⋅ d<span style="text-decoration: overline">l</span><sub>1</sub> - ∫<sub>cd</sub> <span style="text-decoration: overline">H</span><sub>2t</sub> ⋅ d<span style="text-decoration: overline">l</span><sub>2</sub> = ∫<sub>ab</sub> J<sub>s</sub> dl

*   **Simplified Boundary Condition:**  Assuming the length of sides *ab* and *cd* is the same and very small, we can simplify to:

     H<sub>1t</sub> - H<sub>2t</sub> = J<sub>s</sub>

    This equation states that the difference in the tangential components of the magnetic field intensity across the boundary is equal to the surface current density.

## Page 11: Boundary Conditions for the Magnetic Field (Part 4)

This page introduces the Solenoidal Law and applies it to a cylindrical volume at the boundary.

*   **Cylindrical Volume:** A cylindrical volume is defined, positioned with half of its volume in Region 1 and half in Region 2. The flat surfaces are parallel to the material boundary.

*   **Solenoidal Law:** The Solenoidal Law (Gauss's Law for Magnetism) is applied to the surfaces of this cylinder.  This law states that the net magnetic flux through any closed surface is zero.  This implies that magnetic field lines are always continuous and closed loops (no magnetic monopoles).

* **Diagram Explanation:** A cylinder is placed across the boundary. d<span style="text-decoration: overline">s</span><sub>1</sub> and d<span style="text-decoration: overline">s</span><sub>2</sub> are area vectors for the top and bottom surfaces of the cylinder.

## Page 12: Boundary Conditions for the Magnetic Field (Part 5)

This section derives the boundary condition for the normal component of the magnetic field.

*   **Solenoidal Law Applied:** The Solenoidal Law for the cylindrical surface is:

     ∮<sub>S</sub> <span style="text-decoration: overline">B</span> ⋅ d<span style="text-decoration: overline">s</span> = 0

*   **Height Approaching Zero:**  As the height of the cylinder approaches zero, the contribution of the tangential components of the magnetic flux density to the surface integral becomes zero.

*   **Normal Components Remain:** Only the normal components contribute:

    ∫<sub>s1</sub> B<sub>1n</sub>dS<sub>1</sub> - ∫<sub>s2</sub> B<sub>2n</sub>dS<sub>2</sub> = 0

* **Simplified Boundary Condition:** If we assume the surface area are same and small.

     B<sub>1n</sub> = B<sub>2n</sub>

    This states that the normal component of the magnetic flux density is continuous across the boundary.

*   **Using the Constitutive Relation:**  Substituting <span style="text-decoration: overline">B</span> = μ<span style="text-decoration: overline">H</span>, we get:

     μ<sub>1</sub>H<sub>1n</sub> = μ<sub>2</sub>H<sub>2n</sub>

    This shows the relationship between the normal components of the magnetic field intensity in the two regions.

## Page 13: Boundary Conditions for the Magnetic Field (Summary)

This page summarizes the two boundary conditions derived:

1.  **Tangential Component:**  H<sub>1t</sub> - H<sub>2t</sub> = J<sub>s</sub>
2.  **Normal Component:**  μ<sub>1</sub>H<sub>1n</sub> = μ<sub>2</sub>H<sub>2n</sub>

These two equations are crucial for analyzing and solving magnetostatic problems involving different materials.

## Page 14: Inductance (Part 1)

This page introduces the concept of inductance and defines magnetic flux.

*   **Current Loop (C<sub>1</sub>):** Consider a loop of wire (C<sub>1</sub>) carrying a current I<sub>1</sub>.

*   **Magnetic Flux Density (B<sub>1</sub>):** This current I<sub>1</sub> creates a magnetic flux density (<span style="text-decoration: overline">B</span><sub>1</sub>) around the loop.

*   **Magnetic Flux (Φ<sub>11</sub>):** The total magnetic flux (Φ<sub>11</sub>) passing through the surface (S<sub>1</sub>) enclosed by the loop C<sub>1</sub> due to its own current I<sub>1</sub> is calculated by integrating the magnetic flux density over the surface:

    Φ<sub>11</sub> = ∫<sub>S1</sub> <span style="text-decoration: overline">B</span><sub>1</sub> ⋅ d<span style="text-decoration: overline">s</span><sub>1</sub>

    This flux is referred to as *self-flux* since it's generated by the loop's own current.

## Page 15: Inductance (Part 2)

This page extends the concept to mutual flux.

*   **Second Loop (C<sub>2</sub>):**  A second loop (C<sub>2</sub>) is brought near the first loop (C<sub>1</sub>).

*   **Mutual Flux (Φ<sub>12</sub>):** The magnetic flux density (<span style="text-decoration: overline">B</span><sub>1</sub>) created by I<sub>1</sub> in loop C<sub>1</sub> also passes through the surface enclosed by the second loop C<sub>2</sub>. This flux is called *mutual flux* (Φ<sub>12</sub>) because it links the two loops.

*   **Calculating Mutual Flux:**  The mutual flux is calculated as:

    Φ<sub>12</sub> = ∫<sub>S2</sub> <span style="text-decoration: overline">B</span><sub>1</sub> ⋅ d<span style="text-decoration: overline">s</span><sub>2</sub>

    Where S<sub>2</sub> is the surface enclosed by loop C<sub>2</sub>.

## Page 16: Inductance (Part 3)

This section relates magnetic flux and current using the Biot-Savart Law.

*   **Biot-Savart Law:** The Biot-Savart Law states that the magnetic flux density (<span style="text-decoration: overline">B</span><sub>1</sub>) produced by a current element is directly proportional to the current (I<sub>1</sub>).

*   **Proportionality:**  <span style="text-decoration: overline">B</span><sub>1</sub> = (some constant) * I<sub>1</sub>. The "some constant" depends on the geometry of the current loop.

*   **Flux and Magnetic Field:**  The total magnetic flux (Φ) through a loop is directly proportional to the magnetic flux density (<span style="text-decoration: overline">B</span><sub>1</sub>) because flux is the integral of B over the surface.

*   **Equations:**
    *   Φ<sub>11</sub> = ∫<sub>S1</sub> <span style="text-decoration: overline">B</span><sub>1</sub> ⋅ d<span style="text-decoration: overline">s</span><sub>1</sub>
    *   Φ<sub>12</sub> = ∫<sub>S2</sub> <span style="text-decoration: overline">B</span><sub>1</sub> ⋅ d<span style="text-decoration: overline">s</span><sub>2</sub>

## Page 17: Inductance (Part 4)

This section defines self-inductance and mutual inductance.

*   **Self-Inductance (L<sub>11</sub>):** The self-inductance of loop C<sub>1</sub> is defined as the ratio of the self-flux (Φ<sub>11</sub>) to the current (I<sub>1</sub>) producing it:

    L<sub>11</sub> = Φ<sub>11</sub> / I<sub>1</sub>

*   **Mutual Inductance (L<sub>12</sub>):** The mutual inductance between loops C<sub>1</sub> and C<sub>2</sub> is defined as the ratio of the mutual flux (Φ<sub>12</sub>) linking loop C<sub>2</sub> (due to current in C<sub>1</sub>) to the current (I<sub>1</sub>) in loop C<sub>1</sub>:

    L<sub>12</sub> = Φ<sub>12</sub> / I<sub>1</sub>

*   **Generalization for Multiple Loops:** If loop C<sub>1</sub> has N<sub>1</sub> turns and loop C<sub>2</sub> has N<sub>2</sub> turns, the equations become:

    L<sub>11</sub> = (N<sub>1</sub>Φ<sub>11</sub>) / I<sub>1</sub>
    L<sub>12</sub> = (N<sub>2</sub>Φ<sub>12</sub>) / I<sub>1</sub>

    The flux linkage is multiplied by the number of turns.

## Page 18: Inductance (Part 5)

This page discusses the symmetry of mutual inductance and defines self-inductance for the second loop.

*   **Self-Inductance of Loop C<sub>2</sub> (L<sub>22</sub>):**  Similarly, the self-inductance of loop C<sub>2</sub> is:

    L<sub>22</sub> = (N<sub>2</sub>Φ<sub>22</sub>) / I<sub>2</sub>

    Where Φ<sub>22</sub> is the self-flux through loop C<sub>2</sub> due to its own current I<sub>2</sub>.

*   **Reciprocity of Mutual Inductance:**  The mutual inductance is the same regardless of which loop is considered the "source" and which is the "receiver":

    L<sub>12</sub> = L<sub>21</sub> = (N<sub>2</sub>Φ<sub>12</sub>) / I<sub>1</sub> = (N<sub>1</sub>Φ<sub>21</sub>) / I<sub>2</sub>

    This is a fundamental property of mutual inductance.  Φ<sub>21</sub> represents the flux through loop 1 due to current in loop 2.

## Page 19: Energy, Forces, and Torques (Part 1)

This page derives the energy stored in an inductor.

*   **RL Circuit:**  Consider a simple RL circuit with a voltage source (V), a resistor (R), and an inductor (L).

*   **Inductor Voltage:** The voltage across the inductor (V<sub>L</sub>) is given by:

    V<sub>L</sub> = L(dI/dt)

*   **Instantaneous Power:**  The instantaneous power (P<sub>L</sub>) delivered to the inductor is:

    P<sub>L</sub> = V<sub>L</sub>I = LI(dI/dt)

*   **Stored Energy:**  The energy (W<sub>m</sub>) stored in the inductor is the time integral of the power:

    W<sub>m</sub> = ∫ P<sub>L</sub> dt = ∫ LI(dI/dt) dt = ∫ LI dI = (1/2)LI<sup>2</sup>

    This is a fundamental equation for the energy stored in an inductor.

## Page 20: Energy, Forces, and Torques (Part 2)

This page extends the energy calculation to multiple inductive elements and expresses energy in terms of fields.

*   **Multiple Inductors:** For a system with *n* inductive elements, the total stored energy (W<sub>m</sub>) considering both self and mutual inductances is:

    W<sub>m</sub> = (1/2) Σ<sub>i=1</sub><sup>n</sup> Σ<sub>j=1</sub><sup>n</sup> L<sub>ij</sub>I<sub>i</sub>I<sub>j</sub>

    Where L<sub>ij</sub> is the mutual inductance between elements *i* and *j* (and L<sub>ii</sub> is the self-inductance of element *i*).

*   **Energy in Terms of Fields:** The stored energy can also be expressed in terms of the magnetic field intensity (<span style="text-decoration: overline">H</span>) and magnetic flux density (<span style="text-decoration: overline">B</span>):

    W<sub>m</sub> = (1/2) ∫<sub>v</sub> <span style="text-decoration: overline">B</span> ⋅ <span style="text-decoration: overline">H</span> dv

    Where *v* is the volume over which the magnetic field is distributed.  This equation is a more general expression for the energy stored in a magnetic field.

## Page 21: Energy, Forces, and Torques (Part 3)

This page introduces the Lorentz force law and the force on a moving charge in a magnetic field.

*   **Lorentz Force Law:**  A charge (q) moving with velocity (<span style="text-decoration: overline">v</span>) in the presence of both electric (<span style="text-decoration: overline">E</span>) and magnetic (<span style="text-decoration: overline">B</span>) fields experiences a force (<span style="text-decoration: overline">F</span><sub>total</sub>) given by:

    <span style="text-decoration: overline">F</span><sub>total</sub> = <span style="text-decoration: overline">F</span><sub>e</sub> + <span style="text-decoration: overline">F</span><sub>m</sub> = q<span style="text-decoration: overline">E</span> + q<span style="text-decoration: overline">v</span> × <span style="text-decoration: overline">B</span>

    Where:
    *   <span style="text-decoration: overline">F</span><sub>e</sub> is the electric force.
    *   <span style="text-decoration: overline">F</span><sub>m</sub> is the magnetic force.

*   **Magnetic Force Only:**  If the electric field is zero (<span style="text-decoration: overline">E</span> = 0), the force is due solely to the magnetic field:

    <span style="text-decoration: overline">F</span><sub>m</sub> = q<span style="text-decoration: overline">v</span> × <span style="text-decoration: overline">B</span>

*   **Force in Terms of Current:**  The magnetic force can be rewritten in terms of current (<span style="text-decoration: overline">I</span>):

     <span style="text-decoration: overline">F</span><sub>m</sub> = <span style="text-decoration: overline">I</span> × <span style="text-decoration: overline">B</span>

    This is because current is essentially moving charges. The cross product indicates that the force is perpendicular to both the current direction and the magnetic field.

## Page 22: Energy, Forces, and Torques (Part 4)

This page calculates the torque on a current loop in a uniform magnetic field.

*   **Current Loop in Magnetic Field:** Consider a rectangular loop of wire carrying current *I* placed in a uniform magnetic field (<span style="text-decoration: overline">B</span>) directed along the x-axis.  The loop is oriented in the z-x plane.

*   **Force on Each Side:** The force on each side of the loop is calculated using  <span style="text-decoration: overline">F</span><sub>m</sub> = <span style="text-decoration: overline">I</span> × <span style="text-decoration: overline">B</span>.
    *   **Side a-b:** Force is out of the page (+y direction): (Iâ<sub>z</sub> × Bâ<sub>x</sub> = Fâ<sub>y</sub>)
    *   **Side b-c:** Force is zero: (Iâ<sub>x</sub> × Bâ<sub>x</sub> = 0)
    *   **Side c-d:** Force is into the page (-y direction): (-Iâ<sub>z</sub> × Bâ<sub>x</sub> = -Fâ<sub>y</sub>)
    *   **Side d-a:** Force is zero: (-Iâ<sub>x</sub> × Bâ<sub>x</sub> = 0)

    Where â<sub>x</sub>, â<sub>y</sub> and â<sub>z</sub> are unit vectors.

*   **Torque (T):**  The forces on sides a-b and c-d create a *torque* that tends to rotate the loop.  The magnitude of the torque is:

    T = 2Fd/2 = Fd

    Where:
    *   F is the magnitude of the force on each side (a-b and c-d).
    *   d is the length of sides b-c and d-a (the distance between the forces).

## Page 23: Energy, Forces, and Torques (Part 5)

This section generalizes the torque equation and introduces the magnetic dipole moment.

*   **Rotating Loop:** If the loop is allowed to rotate around a central axis, the torque will change as the angle (φ) between the loop's normal and the magnetic field (<span style="text-decoration: overline">B</span>) changes.

*   **General Torque Equation:** The torque is given by:

    T = *l*IBd cos φ

    Where *l* is the length of sides a-b and c-d.

*   **Torque Vector:**  Using the right-hand rule, the torque vector can be expressed as:

    <span style="text-decoration: overline">T</span> = <span style="text-decoration: overline">m</span> × <span style="text-decoration: overline">B</span>

    Where <span style="text-decoration: overline">m</span> is the *magnetic dipole moment* of the loop.

*   **Magnetic Dipole Moment (m):**  The magnetic dipole moment is defined as:

    <span style="text-decoration: overline">m</span> = *l*dI<span style="text-decoration: overline">n</span>

    Where:
    *    *l*d is area of the loop
    *   <span style="text-decoration: overline">n</span> is the unit vector normal to the plane of the loop, determined by the right-hand rule (curl fingers in direction of current, thumb points in direction of <span style="text-decoration: overline">n</span>). In this case <span style="text-decoration: overline">n</span> =  â<sub>y</sub>.

## Page 24: Faraday's Law and Lenz's Law (Part 1)

This page introduces Faraday's Law of electromagnetic induction.

*   **Time-Varying Magnetic Flux:** When the total magnetic flux (Φ) through a conductive loop changes with time, a voltage (V<sub>ind</sub>) is induced around the loop.

*   **Faraday's Law:**  Faraday's Law quantifies this induced voltage:

    V<sub>ind</sub> = -(d/dt) ∫<sub>S</sub> <span style="text-decoration: overline">B</span> ⋅ d<span style="text-decoration: overline">s</span> = -(dΦ/dt)

    The negative sign indicates the direction of the induced voltage (Lenz's Law).

* **Diagram Explanation:** B shows a time varying magnetic flux.

* **Induced Voltage:** The changing magnetic flux induces a voltage V<sub>ind</sub> across the gap in the conductive loop. Because the loop is conductive, the voltage appears entirely across the gap.

## Page 25: Faraday's Law and Lenz's Law (Part 2)

This section expresses Faraday's Law in terms of the electric field and explains Lenz's Law.

*   **Voltage and Electric Field:**  Voltage can also be expressed as the line integral of the electric field:  V = ∫ <span style="text-decoration: overline">E</span> ⋅ d<span style="text-decoration: overline">l</span>

*   **Lenz's Law (from Faraday's Law):**  Combining Faraday's Law with the electric field representation of voltage, we get:

     ∮<sub>C</sub> <span style="text-decoration: overline">E</span> ⋅ d<span style="text-decoration: overline">l</span> = -(d/dt) ∫<sub>S</sub> <span style="text-decoration: overline">B</span> ⋅ d<span style="text-decoration: overline">s</span> = -(dΦ/dt)

*   **Lenz's Law (Explanation):** The negative sign in Faraday's and Lenz's Laws signifies that the induced voltage (and the resulting induced current) creates a magnetic flux that *opposes* the change in the original magnetic flux. This is a fundamental principle of energy conservation. The induced magnetic field tries to counteract the change that caused it.

## Page 26: Motional and Transformer EMF (Part 1)

This section introduces the concept of transformer EMF.

*   **Causes of Changing Flux:**  There are two ways the magnetic flux (Φ) through a surface can change:
    1.  **Changing Magnetic Field:**  The applied magnetic field (<span style="text-decoration: overline">B</span>(t)) itself can change with time.
    2.  **Motion of the Loop:** The conductive loop can move within a static (but possibly non-uniform) magnetic field.

* **Transformer EMF:**
    emf = - (d/dt)∫<sub>s</sub> B . ds
*   **Transformer EMF (Induced EMF):** When the change in flux is due to a time-varying magnetic field, the induced voltage is called "transformer EMF" or "induced EMF."

## Page 27: Motional and Transformer EMF (Part 2)

This section introduces the concept of motional EMF.

*   **Motional EMF:**  When the change in flux is due to the movement of a conductive loop (or a conductor) within a static magnetic field, the induced voltage is called "motional EMF."  This is because the charges within the conductor are moving through the magnetic field, experiencing a magnetic force (q<span style="text-decoration: overline">v</span> × <span style="text-decoration: overline">B</span>).

*   **Motional EMF Equation:** The motional EMF can be calculated as:

    emf<sub>motional</sub> = ∮<sub>C</sub> (<span style="text-decoration: overline">v</span> × <span style="text-decoration: overline">B</span>) ⋅ d<span style="text-decoration: overline">l</span>

    Where <span style="text-decoration: overline">v</span> is the velocity of the conductor.

* **Diagram Explanation:** The loop is moving with velocity v.

*   **Total EMF:** The total EMF experienced by a loop is the sum of the motional and transformer EMFs:

    emf<sub>total</sub> = -∫<sub>S</sub> (d<span style="text-decoration: overline">B</span>/dt) ⋅ d<span style="text-decoration: overline">s</span> + ∮<sub>C</sub> (<span style="text-decoration: overline">v</span> × <span style="text-decoration: overline">B</span>) ⋅ d<span style="text-decoration: overline">l</span>

## Page 28: Ansys Logo

This is the concluding slide with the Ansys logo.
```

Okay, here's a meticulously detailed and exhaustive set of notes from the provided Ansys Electromagnetics course PPT content, formatted primarily in Markdown with HTML used for enhanced equation presentation and organization where needed.

# Electrostatics in Free Space - Ansys Innovation Course

## Sources (Slide 2)

The material presented in this course is derived from the following textbooks:

*   **"Elements of Electromagnetics"** by Matthew N.O. Sadiku, 5th edition (2010)
*   **"Engineering Electromagnetics"** by Nathan Ida, 3rd edition (2015)
*   **"Microwave Engineering"** by David Pozar, 4th edition (2012)

## Introduction to Electric Fields (Slide 3)

Before diving into the mechanics of electric fields, several fundamental terms and concepts must be defined.

### Electromagnetic Constants:

*   **∈₀ (Electric Permittivity of Free Space):**  Represents the capability of a vacuum to permit electric fields. Its value is approximately 8.854 x 10⁻¹² Farads per meter (F/m). This constant describes how strong the electric field generated is for a given amount of charge.
*   **c (Speed of Light in Vacuum):** The speed at which all electromagnetic radiation travels in a vacuum. Its value is approximately 3 x 10⁸ meters per second (m/s).
*   **e (Elementary Charge):** The magnitude of the electric charge carried by a single electron. Its value is approximately -1.6019 x 10⁻¹⁹ Coulombs (C).  The negative sign indicates that the electron has a negative charge.

### Fundamental Electric Fields:

*   **E (Electric Field):** A vector field that describes the force experienced by a unit positive charge at a given point in space. It is measured in volts per meter (V/m).  The electric field points in the direction that a positive test charge would move.
*   **D (Electric Flux Density):**  A vector field related to the electric field, taking into account the effects of the medium. It is measured in Coulombs per meter squared (C/m²). It represents the density of electric field lines passing through a surface.
*   **Relationship between D and E:** In a vacuum (and for the purposes of this course), the electric flux density is directly proportional to the electric field, and the constant of proportionality is the permittivity of free space:

    ```html
    <p><b>D</b> = &epsilon;<sub>0</sub><b>E</b></p>
    ```

### Fundamental Field Sources:

*   **Q (Electric Charge):**  A fundamental property of matter that can be either positive or negative.  It is measured in Coulombs (C).
*   **J (Electric Current Density):** Represents the amount of electric charge flowing per unit time per unit area.  It is measured in Amperes per meter squared (A/m²).

## Introduction to Electric Fields (cont.) (Slide 4)

*   **Electric Field as a Force Field:** An electric field, **E**, is a vector field. This means it has both magnitude and direction at every point in space.  The key property of an electric field is that it exerts a force on any electric charge present within the field.

*   **Visual Representation:** The slide depicts a positive charge surrounded by outward-pointing electric field lines (red arrows). An electron, placed in this field, experiences an attractive force (F, black arrow) towards the positive charge.

*   **Explanation:** The electron experiences an attractive force because it has a negative charge, and negative charges are attracted to positive charges. The electric field created by the positive charge mediates this force.  The direction of the electric field lines indicates the direction a *positive* test charge would move. Since the electron is negative, it moves in the opposite direction.

## Introduction to Electric Fields (cont.) (Slide 5)

*   **Analogy to Gravitational Fields:**  The concept of an electric field is analogous to a gravitational field. Just as a gravitational field exerts a force on objects with mass, an electric field exerts a force on objects with charge.

*   **Visual Representation:** The slide shows the Earth surrounded by inward-pointing gravitational field lines. A rocket experiences a downward force (F) due to this gravitational field.

*   **Explanation:** The rocket experiences a downward force because of its mass and the Earth's gravitational field. The gravitational field lines point towards the center of the Earth, indicating the direction of the force on a massive object. This analogy helps to visualize the concept of a field mediating a force.

## Charge (Slide 6)

*   **Charge as a Field Source:**  Charge is a fundamental property of matter that is the *source* of electric fields.

*   **Direction of Electric Fields:**
    *   **Positive Charges:**  Create electric fields that point *outward* from the charge.
    *   **Negative Charges:** Create electric fields that point *inward* towards the charge.

*   **Visual Representation:** The slide shows two diagrams:
    *   **(a) Electric field around a positive charge +Q:**  Arrows point radially outward from the central positive charge.
    *   **(b) Electric field around a negative charge -Q:** Arrows point radially inward towards the central negative charge.

* **Important:** The color variations in the images are visual aids to show changes in field strength, not different types of fields. The field is stronger (higher magnitude) closer to the charges.

## Coulomb's Law: Force (Slide 7)

*   **Coulomb's Law:** Describes the electrostatic force between two *point charges*. A point charge is an idealized model of a charge that occupies a single point in space.

*   **Equation:**

    ```html
    <p><b>F</b><sub>1</sub> = -<b>F</b><sub>2</sub> = - (Q<sub>1</sub>Q<sub>2</sub> / (4&pi;&epsilon;<sub>0</sub>R<sup>2</sup>)) <b>&acirc;</b><sub>R12</sub></p>
    ```
     Where:

    *   **F₁:** The force experienced by charge 1 due to charge 2 (in Newtons, N).
    *   **F₂:** The force experienced by charge 2 due to charge 1 (in Newtons, N).
    *   **Q₁:** The magnitude of the first point charge (in Coulombs, C).
    *   **Q₂:** The magnitude of the second point charge (in Coulombs, C).
    *   **ε₀:** The permittivity of free space (8.854 x 10⁻¹² F/m).
    *   **R:** The distance between the two charges (in meters, m).
    *   **â<sub>R12</sub>:** A *unit vector* pointing from charge 1 to charge 2.  A unit vector has a magnitude of 1 and indicates direction.

*   **Key Concepts:**

    *   **Action-Reaction Pair:** The forces **F₁** and **F₂** are equal in magnitude and opposite in direction (Newton's Third Law).
    *   **Inverse Square Law:** The force is inversely proportional to the *square* of the distance between the charges (1/R²).  This means that if you double the distance, the force decreases by a factor of four.
    *   **Proportional to Charge:** The force is directly proportional to the product of the magnitudes of the charges (Q₁Q₂).  If you double either charge, the force doubles.

## Coulomb's Law: Force (cont.) (Slide 8)

*   **Vector Representation:** This slide provides a visual and vector-based representation of Coulomb's Law.

*   **Diagram:**
    *   Two point charges, Q₁ and Q₂, are shown in a 3D coordinate system (x, y, z).
    *   **r₁:** Position vector pointing from the origin to Q₁.
    *   **r₂:** Position vector pointing from the origin to Q₂.
    *   **R:** The distance between Q₁ and Q₂.
    *   **â<sub>R12</sub>:** Unit vector pointing from Q₁ to Q₂.
    *   **â<sub>R21</sub>:** Unit vector pointing from Q₂ to Q₁.
    *   **F₁:** Force on Q₁ (due to Q₂), pointing in the direction of **â<sub>R21</sub>** (away from Q₂ if the charges have the same sign).
    *   **F₂:** Force on Q₂ (due to Q₁), pointing in the direction of **â<sub>R12</sub>** (away from Q₁ if the charges have the same sign).

*   **Vector Equations:**

    *   **R (Distance):**  The magnitude of the difference between the position vectors:

        ```html
        <p>R = |<b>r</b><sub>2</sub> - <b>r</b><sub>1</sub>|</p>
        ```

    *   **â<sub>R12</sub> (Unit Vector):** The difference vector divided by its magnitude:

        ```html
        <p><b>&acirc;</b><sub>R12</sub> = (<b>r</b><sub>2</sub> - <b>r</b><sub>1</sub>) / |<b>r</b><sub>2</sub> - <b>r</b><sub>1</sub>| = (<b>r</b><sub>2</sub> - <b>r</b><sub>1</sub>) / R</p>
        ```

*   **Explanation:** This slide shows how to calculate the distance and unit vector between the charges using their position vectors. This is necessary for applying Coulomb's Law in a coordinate system.

## Coulomb's Law: Force (cont.) (Slide 9)

*   **Force Direction:** This slide emphasizes the direction of the forces based on the signs of the charges.

*   **Notes:**
    *   **Equal and Opposite:** The forces are always equal in magnitude and opposite in direction.
    *   **Attractive vs. Repulsive:**
        *   **Opposite Signs (e.g., + and -):** The forces are *attractive*, pulling the charges towards each other.
        *   **Same Signs (e.g., + and +, or - and -):** The forces are *repulsive*, pushing the charges away from each other.

*   **Diagram:** Simple arrows illustrate the attractive and repulsive forces between two charges.

## Coulomb's Law: Electric Field (Slide 10)

*   **Electric Field from Coulomb's Law:**  Coulomb's Law can be used to derive the expression for the electric field created by a point charge.

*   **Definition of Electric Field:** The electric field (**E**) at a point is defined as the force (**F**) per unit charge (**Q**) experienced by a test charge placed at that point:

    ```html
    <p><b>E</b> = <b>F</b> / Q</p>
    ```

*   **Derivation:**
    1.  Consider a point charge Q₁ at the origin and a test charge Q₂ at a point P.
    2.  The force on Q₂ due to Q₁ is given by Coulomb's Law:

        ```html
        <p><b>F</b><sub>2</sub> = (Q<sub>1</sub>Q<sub>2</sub> / (4&pi;&epsilon;<sub>0</sub>R<sup>2</sup>)) <b>&acirc;</b><sub>R</sub></p>
        ```
    3.  Divide both sides by Q₂ to get the electric field at point P due to Q₁:

        ```html
        <p><b>E</b> = <b>F</b><sub>2</sub> / Q<sub>2</sub> = (Q<sub>1</sub> / (4&pi;&epsilon;<sub>0</sub>R<sup>2</sup>)) <b>&acirc;</b><sub>R</sub></p>
        ```
        Where:

        *   **R:**  The distance from Q₁ (the source charge) to the observation point P.
        *   **â<sub>R</sub>:** A unit vector pointing from Q₁ to point P.

* **Diagram:**  A point charge Q₁ at the origin, with radial electric field lines (red) emanating from it. Point P is at a distance R from Q₁.

*   **Key Idea:** The electric field exists even if there is no test charge (Q₂) present.  It represents the potential to exert a force on a charge if one were placed there.

## Coulomb's Law: Electric Field (cont.) (Slide 11)

*   **Generalized Electric Field Equation:** This slide generalizes the electric field equation for a point charge located *not* at the origin.

*   **Diagram:**  A point charge Q₁ is located at a position defined by the vector **r'**.  The observation point P is located at a position defined by the vector **r**.

*   **Equation:**

    ```html
    <p><b>E</b> = (1 / (4&pi;&epsilon;<sub>0</sub>)) * (Q(<b>r</b> - <b>r'</b>) / |<b>r</b> - <b>r'</b>|<sup>3</sup>)</p>
    ```
    Where:

    *   **r:** Position vector of the observation point P.
    *   **r':** Position vector of the point charge Q.
    *    **|r - r'|:** The distance between the point charge and the observation point.
    * **(r - r') / |r - r'|³:** The vector pointing from source charge to field point P, divided by the cube of the distance. This effectively combines the 1/R² dependence with the unit vector.

*   **Explanation:** This equation is a more general form of the electric field equation.  It allows you to calculate the electric field at any point in space due to a point charge located anywhere in space. The vector (**r** - **r'**) points from the source charge (Q) to the point where the field is being evaluated (P).

## Superposition (Slide 12)

*   **Principle of Superposition:**  The total electric field at a point due to multiple charges is the *vector sum* of the electric fields due to each individual charge.

*   **Equation:**

    ```html
    <p><b>E</b><sub>total</sub> = <b>E</b><sub>Q1</sub> + <b>E</b><sub>Q2</sub> + <b>E</b><sub>Q3</sub> + ...</p>
    ```

*   **Diagram:**  Three charges (Q₁, Q₂, Q₃) are shown. The electric field vectors from each charge at a specific point are shown in different colors.

*   **Explanation:**  To find the total electric field at a point, you calculate the electric field due to each charge *individually* (as if the other charges weren't there), and then you add those electric field vectors together. This is a fundamental principle that applies to all linear systems, including electromagnetics.  It significantly simplifies calculations in complex charge distributions.

## Charge Density (Slide 13)

*   **Continuous Charge Distributions:**  Instead of dealing with discrete point charges, it's often more convenient to describe charge distributions using *charge densities*.

*   **Types of Charge Density:**

    *   **Line Charge Density (ρₗ):**  Charge distributed along a line.  Units: Coulombs per meter (C/m).
        *   ```html
            <p>Q<sub>tot</sub> = &int;<sub>l'</sub> &rho;<sub>l</sub> dl'</p>
            ```
            This equation calculates the *total* charge by integrating the linear charge density along the line l'.

    *   **Surface Charge Density (ρₛ):** Charge distributed over a surface. Units: Coulombs per square meter (C/m²).
        *   ```html
            <p>Q<sub>tot</sub> = &int;<sub>s'</sub> &rho;<sub>s</sub> ds'</p>
            ```
            This equation calculates the *total* charge by integrating the surface charge density over the surface s'.

    *   **Volume Charge Density (ρᵥ):** Charge distributed throughout a volume.  Units: Coulombs per cubic meter (C/m³).
        *    ```html
            <p>Q<sub>tot</sub> = &int;<sub>v'</sub> &rho;<sub>v</sub> dv'</p>
            ```
            This equation calculates the *total* charge by integrating the volume charge density over the volume v'.

*   **Diagrams:** Illustrate line, surface, and volume charge distributions.

*   **Key Idea:** Charge densities allow us to treat charge as a continuous quantity, which is often a good approximation for macroscopic systems.

## Coulomb's Law: Charge Density (Slide 14)

*   **Electric Field from Charge Densities:**  This slide combines Coulomb's Law with the concept of charge density to provide formulas for calculating the electric field due to continuous charge distributions.

*   **Equations:**

    *   **For a collection of N point charge sources Qₙ:**

        ```html
        <p><b>E</b> = (1 / (4&pi;&epsilon;<sub>0</sub>)) &sum;<sub>n=1</sub><sup>N</sup> (Q<sub>n</sub>(<b>r</b> - <b>r'</b><sub>n</sub>) / |<b>r</b> - <b>r'</b><sub>n</sub>|<sup>3</sup>)</p>
        ```

    *   **For a line charge source ρₗ distributed over l':**

        ```html
        <p><b>E</b> = (1 / (4&pi;&epsilon;<sub>0</sub>)) &int;<sub>l'</sub> (&rho;<sub>l</sub>(<b>r</b> - <b>r'</b>) / |<b>r</b> - <b>r'</b>|<sup>3</sup>) dl'</p>
        ```

    *   **For a surface charge source ρₛ distributed over s':**

        ```html
        <p><b>E</b> = (1 / (4&pi;&epsilon;<sub>0</sub>)) &int;<sub>s'</sub> (&rho;<sub>s</sub>(<b>r</b> - <b>r'</b>) / |<b>r</b> - <b>r'</b>|<sup>3</sup>) ds'</p>
        ```

    *   **For a volume charge source ρᵥ distributed over v':**

        ```html
        <p><b>E</b> = (1 / (4&pi;&epsilon;<sub>0</sub>)) &int;<sub>v'</sub> (&rho;<sub>v</sub>(<b>r</b> - <b>r'</b>) / |<b>r</b> - <b>r'</b>|<sup>3</sup>) dv'</p>
        ```
        Where:

        *  **r:** Position vector to the observation point.
        *   **r':**  Position vector to the source element (dl', ds', or dv').
        * Integral represents summing up (integrating) the contributions from infinitely small parts of the charge distribution.

*   **Important Note:** In all cases, **r'** points to the *source* of the electric field (the charge element), and **r** points to the *observation point* where the electric field is being calculated.

## Electric Flux Density (Slide 15)

* **D Field Definition:** The electric flux density (**D**) is a vector field that is related to the electric field (**E**) and how the electric field interacts with a *material medium*. It's a measure of the "flow" of electric field lines.

* **Technical Relationship:**  In general, the relationship between **D** and **E** is complex and involves a *convolution* in the time domain. This is because materials do not respond instantaneously to changes in the electric field.  There's a time lag and a history dependence.

* **Simplified Relationship (for this course):**  For this introductory course, a simplified relationship is used, assuming a linear, isotropic, and homogeneous medium (and specifically, a *vacuum*):

    ```html
    <p><b>D</b> = &epsilon;<sub>0</sub><b>E</b></p>
    ```
    This means that **D** and **E** are parallel vectors, and the magnitude of **D** is simply the magnitude of **E** multiplied by the permittivity of free space.  This is only strictly true in a vacuum. In other materials, ε₀ would be replaced by ε, the permittivity of the material.

## Gauss' Law (Slide 16)

* **Gauss's Law Statement:**  Gauss's Law provides a powerful way to relate the electric flux through a *closed surface* to the total charge *enclosed* by that surface.

* **Equation:**

    ```html
    <p>Q<sub>encl</sub> = &#8750;<sub>S</sub> <b>D</b> &middot; d<b>S</b></p>
    ```
    Where:

    *   **Q<sub>encl</sub>:** The total electric charge enclosed by the surface S.
    *   **&#8750;<sub>S</sub>:**  A closed surface integral. This means you are integrating over the entire surface.
    *   **D:** The electric flux density.
    *   **dS:**  A differential area vector.  It is a vector whose magnitude is equal to the area of an infinitesimally small piece of the surface, and whose direction is perpendicular (normal) to that piece of the surface, pointing *outward*.
    * **·** represents the dot product between vectors.

* **Diagram:** Shows a positive charge, the resulting electric field, and a closed spherical surface (Gaussian surface) enclosing the charge.  The electric field lines pass through the Gaussian surface.

* **Key Idea:** Gauss's Law states that the net outward electric flux through any closed surface is proportional to the total charge enclosed within that surface. The shape of the surface does not matter, only the amount of enclosed charge.

## Gauss' Law (cont.) (Slide 17)

* **Applying Gauss's Law with Charge Densities:** This slide shows how Gauss's Law can be expressed in terms of different charge densities.

*   **Equation (General):**

    ```html
    <p>Q<sub>encl</sub> = &#8750;<sub>S</sub> <b>D</b> &middot; d<b>S</b></p>
    ```

*   **Specific Cases:**

    *   **Line Charge Distribution:**

        ```html
        <p>Q<sub>encl</sub> = &#8750;<sub>S</sub> <b>D</b> &middot; d<b>S</b> = &int;<sub>l'</sub> &rho;<sub>l</sub> dl'</p>
        ```

    *   **Surface Charge Distribution:**

        ```html
        <p>Q<sub>encl</sub> = &#8750;<sub>S</sub> <b>D</b> &middot; d<b>S</b> = &int;<sub>s'</sub> &rho;<sub>s</sub> ds'</p>
        ```

    *   **Volume Charge Distribution:**

        ```html
        <p>Q<sub>encl</sub> = &#8750;<sub>S</sub> <b>D</b> &middot; d<b>S</b> = &int;<sub>v'</sub> &rho;<sub>v</sub> dv'</p>
        ```

* **Explanation:** These equations show the equivalence between the surface integral of the electric flux density and the volume, surface, or line integral of the corresponding charge density. This is simply restating Gauss's Law using the definitions of charge density.

## Gauss' Law (cont.) (Slide 18)

*   **Differential Form of Gauss's Law:**  This slide derives the *differential* form of Gauss's Law from the integral form, using the divergence theorem.

*   **Volume Charge Distribution (Starting Point):**

    ```html
    <p>Q<sub>encl</sub> = &#8750;<sub>S</sub> <b>D</b> &middot; d<b>S</b> = &int;<sub>v'</sub> &rho;<sub>v</sub> dv'</p>
    ```

*   **Divergence Theorem:** A fundamental theorem in vector calculus that relates a surface integral to a volume integral:

    ```html
    <p>&#8750;<sub>S</sub> <b>A</b> &middot; d<b>S</b> = &int;<sub>v</sub> &nabla; &middot; <b>A</b> dv</p>
    ```
    Where **A** is any vector field.

*   **Application of Divergence Theorem:** Applying the divergence theorem to the electric flux density **D**:

    ```html
     <p>Q<sub>encl</sub> = &#8750;<sub>S</sub> <b>D</b> &middot; d<b>S</b> = &int;<sub>v'</sub> &rho;<sub>v</sub> dv' = &int;<sub>v</sub> &nabla; &middot; <b>D</b> dv</p>
    ```
*   **Differential Form of Gauss's Law:** Since the volume integrals are equal for *any* arbitrary volume, the integrands must be equal:

    ```html
    <p>&rho;<sub>v</sub> = &nabla; &middot; <b>D</b></p>
    ```
    This is the differential form of Gauss's law.  It states that the divergence of the electric flux density at a point is equal to the volume charge density at that point.

*   **Significance of Differential Form:** The differential form is often more useful for solving problems where the charge density is a known function of position. It relates the *local* value of the charge density to the *local* behavior of the electric flux density.

## Electric Work (Slide 19)

*   **Work Done by Electric Field:**  Moving a charged particle within an electric field requires work to be done, either by the field or by an external force.

*   **Work Definition:** Work is defined as force multiplied by displacement:

    ```html
    <p>Work = Force &times; Displacement</p>
    ```

* **Work Equation:**
    The work done in moving a charge from point A to point B is the negative of the line integral of the force along the path:
    ```html
    <p>W = - &int;<sub>A</sub><sup>B</sup> <b>F</b> &middot; d<b>l</b></p>
    ```
   Where:

    * W: work done
    * **F**: The force acting on the charge.
    *   d**l**: An infinitesimal displacement vector along the path.

*   **Diagram:** Shows a charge Q moving from point A to point B along a path, with an infinitesimal displacement vector d**l** and the force **F** acting on the charge.

* **Important:**

    * **Negative Sign:** The negative sign is a convention. Positive work is done *by* an external force (against the field), and negative work is done *by* the electric field.
    * **Direction Matters (Dot Product):** The dot product (**F** · d**l**) means that only the component of the force *parallel* to the displacement contributes to the work.

## Electric Potential (Slide 20)

*   **Electric Potential (Voltage):**  Electric potential, often called *voltage*, is the potential energy per unit charge. It represents the amount of work needed to move a unit positive charge from a reference point to a specific point in an electric field.

*   **Potential Energy Equation:**
    ```html
     <p>Potential Energy = Work / Charge = (Force x Displacement) / Charge</p>
    ```
    ```html
     <p>V<sub>AB</sub> = W/Q = -(1/Q)&int;<sub>A</sub><sup>B</sup> <b>F</b> &middot; d<b>l</b></p>
    ```
    Where V<sub>AB</sub> is the potential difference between points B and A.

* **Electric Potential and Electric Field:** Recall that **F** = Q**E**. Substituting this into the equation for V<sub>AB</sub>:

   ```html
    <p>V<sub>AB</sub> = - &int;<sub>A</sub><sup>B</sup> <b>E</b> &middot; d<b>l</b></p>
    ```

*   **Diagram:** Shows points A and B, with the potential difference V<sub>AB</sub> between them. The infinitesimal displacement vector d**l** is also shown.

*   **Key Concepts:**

    *   **Potential Difference:** Voltage is always measured *between two points*. It's the difference in electric potential between those points.
    *   **Reference Point:**  A reference point is needed to define the absolute potential at a given location. Often, this reference point is taken to be infinitely far away (where the electric field is assumed to be zero).

## Electric Potential (cont.) (Slide 21)

*   **Path Independence:**  A crucial property of the electrostatic field is that the electric potential difference between two points is *independent of the path* taken between those points.

*   **Diagram:** Shows three points (A, B, C) and two different paths between A and B: a direct path (A→B) and an indirect path (A→C→B).

*   **Equation:**

    ```html
    <p>V<sub>AB</sub> = V<sub>AC</sub> + V<sub>CB</sub></p>
    ```

*   **Explanation:** This equation shows that the potential difference between A and B is the same whether you go directly from A to B or take a detour through point C. This is a consequence of the fact that the electrostatic field is *conservative*. This property comes from the fact that the curl of the electrostatic E field is always zero.

## Electric Potential (cont.) (Slide 22)

*   **Reference Point at Infinity:**  It's common practice to choose the reference point for electric potential to be at infinity. This means that the electric potential is defined as the work required to bring a unit positive charge from infinity to a specific point in the electric field.

*   **Derivation:**  Consider a point charge Q₁ at the origin.  The electric field due to Q₁ is:

    ```html
    <p><b>E</b> = (Q<sub>1</sub> / (4&pi;&epsilon;<sub>0</sub>r<sup>2</sup>)) <b>&acirc;</b><sub>R</sub></p>
    ```

    The potential difference between a point B (at a distance r₁ from Q₁) and infinity is:

    ```html
    <p>V<sub>AB</sub> = - &int;<sub>&infin;</sub><sup>B</sup> <b>E</b> &middot; d<b>l</b> = - &int;<sub>&infin;</sub><sup>r<sub>1</sub></sup> (Q<sub>1</sub> / (4&pi;&epsilon;<sub>0</sub>r<sup>2</sup>)) <b>&acirc;</b><sub>R</sub> &middot; d<b>r</b></p>
    ```
Since d**l** = d**r** = dr **â**<sub>R</sub> (in spherical coordinates)

    ```html
    <p> V<sub>AB</sub>= - &int;<sub>&infin;</sub><sup>r<sub>1</sub></sup> (Q<sub>1</sub> / (4&pi;&epsilon;<sub>0</sub>r<sup>2</sup>)) dr </p>
    <p> V<sub>AB</sub> = (Q<sub>1</sub> / (4&pi;&epsilon;<sub>0</sub>)) * [-1/r]<sub>&infin;</sub><sup>r<sub>1</sub></sup></p>
    <p>V<sub>AB</sub> = (Q<sub>1</sub> / (4&pi;&epsilon;<sub>0</sub>r<sub>1</sub>)) = V<sub>B</sub></p>
    ```
* **Result:** The electric potential due to a point charge Q₁ at a distance r₁ is:
    ```html
    <p>V<sub>B</sub> = V = (Q<sub>1</sub> / (4&pi;&epsilon;<sub>0</sub>r<sub>1</sub>)) </p>
    ```

* **Diagram:** A point charge Q₁ at the origin with radial field lines. Point B is at a distance r₁ from Q₁. The reference point A is at infinity.

*   **Key Idea:** This equation gives the absolute potential at a point due to a point charge, using infinity as the reference.

## Electric Potential: Charge Density (Slide 23)

* **Potential from Charge Densities:**  This slide extends the concept of electric potential to continuous charge distributions, using the principle of superposition.

*   **Equations:**

    *   **For a point charge source Q:**

        ```html
        <p>V = (1 / (4&pi;&epsilon;<sub>0</sub>)) * (Q / |<b>r</b> - <b>r'</b>|)</p>
        ```

    *   **For a line charge source ρₗ distributed over l':**

        ```html
        <p>V = (1 / (4&pi;&epsilon;<sub>0</sub>)) &int;<sub>l'</sub> (&rho;<sub>l</sub> / |<b>r</b> - <b>r'</b>|) dl'</p>
        ```

    *   **For a surface charge source ρₛ distributed over s':**

        ```html
        <p>V = (1 / (4&pi;&epsilon;<sub>0</sub>)) &int;<sub>s'</sub> (&rho;<sub>s</sub> / |<b>r</b> - <b>r'</b>|) ds'</p>
        ```

    *   **For a volume charge source ρᵥ distributed over v':**

        ```html
        <p>V = (1 / (4&pi;&epsilon;<sub>0</sub>)) &int;<sub>v'</sub> (&rho;<sub>v</sub> / |<b>r</b> - <b>r'</b>|) dv'</p>
        ```
        Where:

        *   **r:**  Position vector to the observation point (where the potential is being calculated).
        *   **r':** Position vector to the source element (dl', ds', or dv').

*   **Explanation:** These equations are analogous to the electric field equations for charge densities.  To find the potential due to a continuous charge distribution, you integrate the contributions from infinitesimally small charge elements. The key difference is that potential is a *scalar* quantity, making the calculations often simpler than those for the electric field (which is a vector).

## Electric Potential and Electric Field (Slide 24)

*   **Relationship between V and E:** This slide shows the fundamental relationship between electric potential (V) and electric field (**E**).  They are *not* independent; one can be derived from the other.

*   **From V to E (Gradient):**
    We know:

    ```html
    <p>V = - &int;<sub>A</sub><sup>B</sup> <b>E</b> &middot; d<b>l</b> = +&int;<sub>B</sub><sup>A</sup> <b>E</b> &middot; d<b>l</b></p>
    ```
    And because the electrostatic field produces a voltage that is independant of path:

    ```html
    <p>&#8752;<b>E</b> &middot; d<b>l</b> = 0 </p>
    ```
    Using Stoke's theorem on the above expression we can state:

    ```html
    <p>&#8752;<b>E</b> &middot; d<b>l</b> =  &#8747;<sub>S</sub> &nabla; &times; <b>E</b> = 0</p>
    ```
    And recalling that for any scalar field V:
    ```html
    <p>&nabla; &times; &nabla;V = 0</p>
    ```
     Then that implies:

    ```html
    <p><b>E</b> = -&nabla;V</p>
    ```

    The electric field is the *negative gradient* of the electric potential. The gradient operator (∇) points in the direction of the *greatest increase* of a scalar field. The negative sign indicates that the electric field points in the direction of *decreasing* potential.

*   **Key Concepts:**

    *   **Equipotential Surfaces:** Surfaces where the electric potential is constant.  The electric field is always perpendicular to equipotential surfaces.
    *   **Relationship Strength:** The magnitude of the electric field is related to how rapidly the potential changes in space.  A strong electric field corresponds to a large potential gradient.

## Electrostatic Energy (Slide 25)

*   **Energy Stored in a System of Charges:**  Bringing charges together (or separating them) requires work, and this work is stored as *electrostatic potential energy* in the system of charges.
* First Charge (Q1) has no other charges to work against, so W1 = 0

*   **Bringing in the First Charge (Q₁):**  If you start with an empty region of space and bring in the first charge (Q₁) from infinity, *no work* is required (W₁ = 0).  This is because there is no existing electric field to work against.
*   **Bringing in the Second Charge (Q₂):** When you bring in the second charge (Q₂) from infinity, work *is* required because of the electric field created by Q₁.
* W2 = Q2 * V21, Where V21 represents the potential at charge 2 due to charge 1.

## Electrostatic Energy (cont.) (Slide 26)

*   **Bringing in the Third Charge (Q₃):**  When you bring in the third charge (Q₃), work

