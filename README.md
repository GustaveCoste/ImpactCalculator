# Impact calculator POC

Library to calculate impact and impact uncertainty of a product system.

## Concepts:

- **Base product:** Product that simply has an impact value and an uncertainty of this value.
- **Compound product:** Product made up from usage of other products (compound or base), with an uncertainty associated
  to the quantity of product used.

## Limitations

- Cannot handle circular product systems (LCA tools needed for this).
- Does not handle unit conversion

## TODO

- Implement different pedigree matrix coefficients (sector specific)
- Adapt basic uncertainty for geometric standard deviation calculation from pedigree matrix
- Add characterisation of the uncertainty related to the choice of the process (additional pedigree matrix for product
  usage)
- Implement Monte-Carlo loop
- Display contribution of each product to the total impact
- Add a way to make Monte-Carlo deterministic with seed
- Allow for variable correlation
- Add other types of uncertainty through new `Amount` classes