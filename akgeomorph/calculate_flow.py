# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Calculate flow accumulation
# Author: Timm Nawrocki
# Last Updated: 2024-05-04
# Usage: Execute in ArcGIS Pro Python 3.9+.
# Description: "Calculate flow accumulation" is a function that calculates flow accumulation from a float elevation raster.
# ---------------------------------------------------------------------------

# Define function to calculate flow accumulation
def calculate_flow(elevation_input, accumulation_output, direction_output):
    """
    Description: calculates 32-bit float flow accumulation and direction rasters
    Inputs: 'elevation_input' -- an input 32-bit float elevation raster
            'accumulation_output' -- a file path for an output 32-bit float flow accumulation raster
            'direction_output' -- a file path for an output 32-bit float flow direction raster
    Returned Value: Returns raster datasets on disk
    Preconditions: requires float input elevation raster
    """

    # Import packages
    import arcpy
    from arcpy.sa import DeriveContinuousFlow
    from arcpy.sa import Raster

    # Set overwrite option
    arcpy.env.overwriteOutput = True

    # Specify core usage
    arcpy.env.parallelProcessingFactor = "75%"

    # Set snap raster and extent
    area_raster = Raster(elevation_input)
    arcpy.env.snapRaster = area_raster
    arcpy.env.extent = area_raster.extent

    # Set cell size environment
    cell_size = arcpy.management.GetRasterProperties(area_raster, 'CELLSIZEX', '').getOutput(0)
    arcpy.env.cellSize = int(cell_size)

    # Calculate flow accumulation
    print('\tCalculating flow accumulation...')
    accumulation_raster = DeriveContinuousFlow(elevation_input,
                                               '',
                                               '',
                                               direction_output,
                                               'MFD',
                                               'NORMAL')

    # Export raster
    print('\tExporting flow accumulation raster as 32-bit float...')
    arcpy.management.CopyRaster(accumulation_raster,
                                accumulation_output,
                                '',
                                '',
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
    arcpy.management.BuildPyramids(accumulation_output,
                                   '-1',
                                   'NONE',
                                   'BILINEAR',
                                   'LZ77',
                                   '',
                                   'OVERWRITE')
    arcpy.management.CalculateStatistics(accumulation_output)
