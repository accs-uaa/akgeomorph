# AKgeomorph

AKgeomorph is a Python package that contains functions for calculation of geomorphology metrics for Alaska.

*Author*: Timm Nawrocki, Alaska Center for Conservation Science, University of Alaska Anchorage

*Created On*: 2023-10-10

*Last Updated*: 2024-05-04

*Description*: Functions for calculating topographic and hydrographic metrics for modeling or descriptive purposes.

## Getting Started
These instructions will enable you to import functions from the AKgeomorph package into scripts. This package depends on an installation of ArcGIS Pro 3.1+ and therefore must be installed into the bundled Python installation. A Spatial Analyst (sa) license is required to run the functions.

### Prerequisites

1. Python 3.9+
2. pip
3. arcpy
4. datetime
8. time

### Installing

To install the AKgeomorph package, use the pip install command below from the Python console of the ArcGIS Pro Python 3 installation.

```bash
pip install git+https://github.com/accs-uaa/akgeomorph
```

## Usage
This section describes the purpose of each function and provides details of parameters and outputs.

### Functions

#### calculate_aspect

The *calculate_aspect* function is used to calculate the aspect in degrees from North Pole perspective using geodesic azimuths and a quadratic estimator. 

##### **Parameters that must be modified:**

* *area_input*: a raster of the study area to set snap raster and extract area
* *elevation_input*: an input 32-bit float elevation raster
* *aspect_float*: a file path for an output 32-bit float aspect raster in degrees
* *aspect_output*: [optional] a file path for an output 16-bit integer aspect raster in degrees (set to None if no output is desired)

##### Example

```
calculate_aspect(area_input, elevation_input, z_unit, aspect_float, None)
```

## Credits

### Authors

* **Timm Nawrocki** - *Alaska Center for Conservation Science, University of Alaska Anchorage*

### Usage Requirements

Usage of the scripts, packages, tools, or routines included in this repository should be cited as follows:

Nawrocki, T.W. 2024. AKgeomorph. Git Repository. Available: https://github.com/accs-uaa/akgeomorph

The functions in the AKgeomorph package derive from previous work by Evans et al. (2014). Therefore, please also cite:

Evans, J.S., J. Oakleaf, S.A. Cushman, and D. Theobald. 2014. An ArcGIS Toolbox for Surface Gradient and Geomorphometric Modeling, version 2.0-0. Available: http://evansmurphy.wix.com/evansspatial.

#### Roughness

If using the roughness, please cite:

1. Riley, S.J., S.D. DeGloria, and R. Elliot. 1999. A terrain ruggedness index that quantifies topographic heterogeneity. Intermountain Journal of Sciences. 5. 1-4.

#### Surface Area Ratio

If using the surface area ratio function, please cite:

1. Pike, R.J., and S.E. Wilson. 1971. Elevation relief ratio, hypsometric integral, and geomorphic area altitude analysis. Bulletin of the Geological Society of America. 82. 1079-1084.

#### Topographic Wetness Index (Compound Topographic Index)

If using the topographic wetness index function, please cite:

1. Gessler, P.E., I.D. Moore, N.J. McKenzie, and P.J. Ryan. 1995. Soil-landscape modeling and spatial prediction of soil attributes. International Journal of GIS. 9. 421-432.
2. Moore, I.D., P.E. Gessler, G.A. Nielsen, and G.A. Petersen. 1993. Terrain attributes: estimation methods and scale effects. In: Jakeman, A.J., and M. McAleer (eds.). Modeling Change in Environmental Systems. Wiley. London, United Kingdom. 189-214.

#### Heat Load Index

If using the heat load index function, please cite:

1. McCune, B., and D. Keon. 2002. Equations for potential annual direct incident radiation and heat load index. Journal of Vegetation Science. 13. 603-606.

## License
[MIT](https://choosealicense.com/licenses/mit/)
