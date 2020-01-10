# pymensor

This package is a GPIB (IEEE 488.2) driver for 
[Mensor Modular Pressure Controllers](https://www.mensor.com/products_pressure_controllers_en_co.WIKA).

<p align="center">
  <img src="https://www.mensor.com/upload/WIKA_Thumbnails/Product-Detail-Large/PIC_PR_CPC6050_de_de_68774.jpg.png" height="400" />
</p>

This package is written for and tested on the model CPC6000, but is intended to work for all WIKA pressure controllers made by Mensor.

Please feel free to raise any issues or contact the maintainers to contribute.

# Installation

```
pip install pymensor
```

# Dependencies

This package depends on `pyvisa`.

# Usage

### Python

For more complex projects, use python to automate your workflow.

```python
from pymensor import PressureController
```
