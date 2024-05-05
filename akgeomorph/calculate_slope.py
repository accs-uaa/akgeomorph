# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Calculate slope
# Author: Timm Nawrocki
# Last Updated: 2024-05-04
# Usage: Execute in ArcGIS Pro Python 3.9+.
# Description: "Calculate slope" is a function that calculates float and integer slope in degrees.
# ---------------------------------------------------------------------------

# Define function to calculate slope
def calculate_slope(area_input, elevation_input, z_unit, slope_float, slope_output):
    """
    Description: calculates 32-bit float slope and 16-bit signed slope
    Inputs: 'area_input' -- a raster of the study area to set snap raster and extract area
            'elevation_input' -- an input 32-bit float elevation raster
            'z-unit' -- a string of the elevation unit
            'slope_float' -- a file path for an output 32-bit float slope raster in degrees
            'slope_output' -- a file path for an output 16-bit integer slope raster in degrees
    Returned Value: Returns a raster dataset on disk
    Preconditions: requires float input elevation raster
    """

    # Import packages
    import arcpy
    from arcpy.sa import ExtractByMask
    from arcpy.sa import Int
    from arcpy.sa import Raster
    from arcpy.sa import SurfaceParameters

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

    # Calculate raw slope
    print('\tCalculating raw slope...')
    slope_raster = SurfaceParameters(elevation_input,
                                     'SLOPE',
                                     'QUADRATIC',
                                     cell_size,
                                     'FIXED_NEIGHBORHOOD',
                                     z_unit,
                                     'DEGREE',
                                     'GEODESIC_AZIMUTHS',
                                     '')

    # Convert to integer
    print('\tConverting to integer...')
    integer_raster = Int(slope_raster + 0.5)

    # Extract to area raster
    print('\tExtracting raster to area...')
    extract_integer = ExtractByMask(integer_raster, area_raster)

    # Export 32-bit raster
    print('\tExporting slope as 32-bit float raster...')
    arcpy.management.CopyRaster(slope_raster,
                                slope_float,
                                '',
                                '0',
                                '-2147483648',
                                'NONE',
                                'NONE',
                                '32_BIT_FLOAT',
                                'NONE',
                                'NONE',
                                'TIFF',
                                'NONE',
                                'CURRENT_SLICE',
                                'NO_TRANSPOSE')
    arcpy.management.BuildPyramids(slope_float,
                                   '-1',
                                   'NONE',
                                   'BILINEAR',
                                   'LZ77',
                                   '',
                                   'OVERWRITE')
    arcpy.management.CalculateStatistics(slope_float)

    # Export 16-bit raster
    print('\tExporting slope as 16-bit integer raster...')
    arcpy.management.CopyRaster(extract_integer,
                                slope_output,
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
    arcpy.management.BuildPyramids(slope_output,
                                   '-1',
                                   'NONE',
                                   'BILINEAR',
                                   'LZ77',
                                   '',
                                   'OVERWRITE')
    arcpy.management.CalculateStatistics(slope_output)
