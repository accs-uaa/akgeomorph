# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Calculate surface area ratio
# Author: Timm Nawrocki
# Last Updated: 2024-05-04
# Usage: Must be executed in an ArcGIS Pro Python 3.7 installation.
# Description: "Calculate surface area ratio" is a function that calculates surface area ratio. This function is adapted from Geomorphometry and Gradient Metrics Toolbox 2.0 by Jeff Evans and Jim Oakleaf (2014) available at https://github.com/jeffreyevans/GradientMetrics.
# ---------------------------------------------------------------------------

# Define function to calculate surface area ratio
def calculate_surface_area(area_input, slope_input, conversion_factor, surfacearea_output):
    """
    Description: calculates 16-bit signed surface area ratio
    Inputs: 'area_input' -- a raster of the study area to set snap raster and extract area
            'slope_input' -- an input 32-bit float slope raster in degrees
            'conversion_factor' -- an integer to be multiplied with the output for conversion to integer raster
            'surfacearea_output' -- an output 16-bit integer surface area ratio raster
    Returned Value: Returns a raster dataset on disk
    Preconditions: requires an input float slope raster
    """

    # Import packages
    from numpy import pi
    import arcpy
    from arcpy.sa import Cos
    from arcpy.sa import ExtractByMask
    from arcpy.sa import Float
    from arcpy.sa import Int
    from arcpy.sa import Raster

    # Set overwrite option
    arcpy.env.overwriteOutput = True

    # Specify core usage
    arcpy.env.parallelProcessingFactor = "75%"

    # Set snap raster and extent
    area_raster = Raster(area_input)
    arcpy.env.snapRaster = area_raster
    arcpy.env.extent = area_raster.extent

    # Set cell size environment
    cell_size = arcpy.management.GetRasterProperties(area_raster, 'CELLSIZEX', '').getOutput(0)
    arcpy.env.cellSize = int(cell_size)

    # Calculate cell area
    cell_area = float(cell_size) ** 2

    # Convert degrees to radians
    print('\tConverting degrees to radians...')
    slope_radian = Raster(slope_input) * (pi/180)

    # Calculate surface area ratio
    print('\tCalculating surface area ratio...')
    surfacearea_raster = Float(cell_area) / Cos(slope_radian)

    # Convert to integer
    print('\tConverting to integer...')
    integer_raster = Int((surfacearea_raster * conversion_factor) + 0.5)

    # Extract to area raster
    print('\tExtracting raster to area...')
    extract_integer = ExtractByMask(integer_raster, area_raster)

    # Export raster
    print('\tExporting area raster as 16-bit signed...')
    arcpy.management.CopyRaster(extract_integer,
                                surfacearea_output,
                                '',
                                '32767',
                                '-32768',
                                'NONE',
                                'NONE',
                                '16_BIT_SIGNED',
                                'NONE',
                                'NONE',
                                'TIFF',
                                'NONE')
    arcpy.management.BuildPyramids(surfacearea_output,
                                   '-1',
                                   'NONE',
                                   'BILINEAR',
                                   'L77',
                                   '',
                                   'OVERWRITE')
    arcpy.management.CalculateStatistics(surfacearea_output)
