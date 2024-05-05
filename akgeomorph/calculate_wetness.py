# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Calculate topographic wetness
# Author: Timm Nawrocki
# Last Updated: 2024-05-04
# Usage: Execute in ArcGIS Pro Python 3.9+.
# Description: "Calculate topographic wetness" is a function that calculates an index of topographic wetness. This function is adapted from Geomorphometry and Gradient Metrics Toolbox 2.0 by Jeff Evans and Jim Oakleaf (2014) available at https://github.com/jeffreyevans/GradientMetrics. This version is updated to weight the resulting wetness index by the inverse of slope.
# ---------------------------------------------------------------------------

# Define function to calculate compound topographic index
def calculate_wetness(area_input, slope_input, accumulation_input, conversion_factor, neighborhood, wetness_output):
    """
    Description: calculates 16-bit signed topographic wetness
    Inputs: 'area_input' -- a raster of the study area to set snap raster and extract area
            'slope_input' -- an input 32-bit float slope raster
            'accumulation_input' -- an input 32-bit float flow accumulation raster
            'conversion_factor' -- an integer to be multiplied with the output for conversion to integer raster
            'neighborhood' -- an integer representing the cell neighborhood for smoothing
            'wetness_output' -- a file path for an output 16-bit integer topographic wetness raster
    Returned Value: Returns a raster dataset on disk
    Preconditions: requires input elevation, flow accumulation, and raw slope raster
    """

    # Import packages
    from numpy import pi
    import arcpy
    from arcpy.sa import Con
    from arcpy.sa import Cos
    from arcpy.sa import ExtractByMask
    from arcpy.sa import Int
    from arcpy.sa import IsNull
    from arcpy.sa import Ln
    from arcpy.sa import Nibble
    from arcpy.sa import Raster
    from arcpy.sa import SetNull
    from arcpy.sa import Tan
    from arcpy.sa import FocalStatistics
    from arcpy.sa import NbrRectangle

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

    # Smooth slope
    print('\tSmoothing slope...')
    neighborhood = NbrRectangle(neighborhood, neighborhood, 'CELL')
    slope_degree = FocalStatistics(Raster(slope_input), neighborhood, 'MEAN', 'DATA')

    # Convert degrees to radians
    print('\tConverting slope degrees to radians...')
    slope_radian = slope_degree * (pi/180)

    # Calculate slope tangent
    print('\tCalculating slope tangent...')
    slope_tangent = Con(slope_radian > 0, Tan(slope_radian), 0.001)

    # Correct flow accumulation
    print('\tModifying flow accumulation...')
    accumulation_corrected = (Raster(accumulation_input) + 1) * float(cell_size)

    # Calculate wetness index as natural log of corrected flow accumulation divided by slope tangent
    print('\tCalculating wetness index...')
    wetness_index = Ln(accumulation_corrected / slope_tangent)

    # Weight wetness by cosine
    print('\tWeighting by cosine slope...')
    wetness_weighted = Con(slope_radian >= (pi/6), 0, wetness_index * Cos(slope_radian * 3))

    # Nibble wetness raster
    print('\tFilling missing values...')
    null_raster = SetNull(IsNull(wetness_weighted), 1, '')
    filled_raster = Nibble(wetness_weighted, null_raster, 'DATA_ONLY', 'PROCESS_NODATA', '')

    # Convert to integer
    print('\tConverting to integer...')
    integer_raster = Int((filled_raster * conversion_factor) + 0.5)

    # Extract to area raster
    print('\tExtracting raster to area...')
    extract_integer = ExtractByMask(integer_raster, area_raster)

    # Export raster
    print('\tExporting wetness raster as 16-bit signed...')
    arcpy.management.CopyRaster(extract_integer,
                                wetness_output,
                                '',
                                '',
                                '-32768',
                                'NONE',
                                'NONE',
                                '16_BIT_SIGNED',
                                'NONE',
                                'NONE',
                                'TIFF',
                                'NONE')
    arcpy.management.BuildPyramids(wetness_output,
                                   '-1',
                                   'NONE',
                                   'BILINEAR',
                                   'LZ77',
                                   '',
                                   'OVERWRITE')
    arcpy.management.CalculateStatistics(wetness_output)
