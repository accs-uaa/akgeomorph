# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Calculate distance to flowline
# Author: Timm Nawrocki
# Last Updated: 2024-05-06
# Usage: Execute in ArcGIS Pro Python 3.9+.
# Description: "Calculate distance to flowline" is a function that calculates the distance accumulation to the nearest flowline raster cell.
# ---------------------------------------------------------------------------

# Define function to calculate distance to flowline
def calculate_flowline_distance(accumulation_input, threshold, flowline_output, distance_output):
    """
    Description: calculates 16-bit signed distance to flowline
    Inputs: 'accumulation_input' -- an input 32-bit float flow accumulation raster
            'threshold' - an integer threshold value (recommend 10,000 for streams, 1,000,000 for rivers)
            'flowline_output' -- a file path for an output 1-bit integer flowline raster
            'distance_output' -- a file path for an output 16-bit integer distance to flowline raster
    Returned Value: Returns a raster dataset on disk
    Preconditions: requires input flow accumulation raster
    """

    # Import packages
    import os
    import arcpy
    from arcpy.sa import Con
    from arcpy.sa import DistanceAccumulation
    from arcpy.sa import ExtractByMask
    from arcpy.sa import Int
    from arcpy.sa import IsNull
    from arcpy.sa import Raster
    from arcpy.sa import SetNull

    # Set overwrite option
    arcpy.env.overwriteOutput = True

    # Specify core usage
    arcpy.env.parallelProcessingFactor = "75%"

    # Set snap raster and extent
    area_raster = Raster(accumulation_input)
    arcpy.env.snapRaster = area_raster
    arcpy.env.extent = area_raster.extent

    # Set cell size environment
    cell_size = arcpy.management.GetRasterProperties(area_raster, 'CELLSIZEX', '').getOutput(0)
    arcpy.env.cellSize = int(cell_size)

    # Calculate flowlines
    if os.path.exists(flowline_output) == 0:
        print('\tCalculating flowlines...')
        flowline_raster = SetNull(Raster(accumulation_input) < threshold, 1)
        # Export flowlines
        print('\tExporting flowlines raster as 1-bit...')
        arcpy.management.CopyRaster(flowline_raster,
                                    flowline_output,
                                    '',
                                    '',
                                    '0',
                                    'NONE',
                                    'NONE',
                                    '1_BIT',
                                    'NONE',
                                    'NONE',
                                    'TIFF',
                                    'NONE')
        arcpy.management.BuildPyramids(flowline_output,
                                       '-1',
                                       'NONE',
                                       'BILINEAR',
                                       'LZ77',
                                       '',
                                       'OVERWRITE')
        arcpy.management.CalculateStatistics(flowline_output)

    # Determine if flowline raster is all nodata
    raster_status = arcpy.management.GetRasterProperties(flowline_output, 'ALLNODATA')

    # Calculate distance to flowline if the flowline raster contains valid data
    if int(raster_status[0]) == 0:
        print('\tCalculating distance to flowline...')
        flowline_distance = DistanceAccumulation(flowline_output)

        # Convert to integer
        print('\tConverting to integer...')
        integer_raster = Int((flowline_distance) + 0.5)
        corrected_raster = Con(integer_raster > 32767, 32767, integer_raster)

        # Extract to area raster
        print('\tExtracting raster to area...')
        extract_integer = ExtractByMask(corrected_raster, area_raster)

        # Export raster
        print('\tExporting stream distance raster as 16-bit signed...')
        arcpy.management.CopyRaster(extract_integer,
                                    distance_output,
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
        arcpy.management.BuildPyramids(distance_output,
                                       '-1',
                                       'NONE',
                                       'BILINEAR',
                                       'LZ77',
                                       '',
                                       'OVERWRITE')
        arcpy.management.CalculateStatistics(distance_output)

    # Calculate flowline distance as maximum possible if flowline raster is all nodata
    else:
        print('\tInferring maximum distance to flowline...')
        flowline_distance = Con(IsNull(Raster(accumulation_input)), Raster(accumulation_input), 32767)

        # Export raster
        print('\tExporting stream distance raster as 16-bit signed...')
        arcpy.management.CopyRaster(flowline_distance,
                                    distance_output,
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
        arcpy.management.BuildPyramids(distance_output,
                                       '-1',
                                       'NONE',
                                       'BILINEAR',
                                       'LZ77',
                                       '',
                                       'OVERWRITE')
        arcpy.management.CalculateStatistics(distance_output)
