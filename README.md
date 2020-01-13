# pymensor

<table>
<tr>
    <td>Latest Release</td>
    <td>
        <a href="https://pypi.org/project/pymensor/">
        <img src="https://img.shields.io/pypi/v/pymensor" alt="latest release" />
        </a>
    </td>
</tr>
</table>

This package is a GPIB (IEEE 488.2) driver for 
[Mensor Modular Pressure Controllers](https://www.mensor.com/products_pressure_controllers_en_co.WIKA).

<p align="center">
  <img src="https://www.mensor.com/upload/WIKA_Thumbnails/Product-Detail-Large/PIC_PR_CPC6050_de_de_68774.jpg.png" height="400" />
</p>

This package is written for and tested on the now obsolete model [CPC6000](https://www.mensor.com/upload/OI_CPC6000_archived_en_um_30501.pdf), 
but is intended to work for all WIKA pressure controllers made by Mensor.

Please feel free to raise any issues or contact the maintainers to contribute.

# Installation

```
pip install pymensor
```

# Dependencies

This package depends on `pyvisa`.

This package, along with PyVisa, depends on a VISA installation being present on the system.
By default, PyVisa uses the IVI library as the backend, which can be installed with NI-VISA.
Alternatively, you can install `pyvisa-py` as the backend instead of the IVI library. 
In any case, the bitness of the VISA library **must match** the bitness of the Python installation.

See the PyVisa documentation on [Configuring the Backend](https://pyvisa.readthedocs.io/en/latest/introduction/configuring.html).

# Usage

### Python

```python
from pymensor import PressureController
```
