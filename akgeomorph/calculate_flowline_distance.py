# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Calculate distance to flowline
# Author: Timm Nawrocki
# Last Updated: 2024-05-04
# Usage: Execute in ArcGIS Pro Python 3.9+.
# Description: "Calculate distance to flowline" is a function that calculates the distance accumulation to the nearest flowline raster cell.
# ---------------------------------------------------------------------------

# Define function to calculate distance to flowline
def calculate_flowline_distance(area_input, flowline_input, flowline_output):
    """
    Description: calculates 16-bit signed distance to flowline
    Inputs: 'area_input' -- a raster of the study area to set snap raster and extract area
            'flowline_input' -- an input flowline network raster (flowline = 1, other = nodata)
            'flowline_output' -- a file path for an output 16-bit integer distance to flowline raster
    Returned Value: Returns a raster dataset on disk
    Preconditions: requires input flowline network raster
    """

    # Import packages
    import arcpy
    from arcpy.sa import DistanceAccumulation
    from arcpy.sa import ExtractByMask
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

    # Calculate distance to stream
    print('\tCalculating distance to stream...')
    stream_distance = DistanceAccumulation(flowline_input)

    # Convert to integer
    print('\tConverting to integer...')
    integer_raster = Int((stream_distance) + 0.5)

    # Extract to area raster
    print('\tExtracting raster to area...')
    extract_integer = ExtractByMask(integer_raster, area_raster)

    # Export raster
    print('\tExporting stream distance raster as 16-bit signed...')
    arcpy.management.CopyRaster(extract_integer,
                                flowline_output,
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
    arcpy.management.BuildPyramids(flowline_output,
                                   '-1',
                                   'NONE',
                                   'BILINEAR',
                                   'LZ77',
                                   '',
                                   'OVERWRITE')
    arcpy.management.CalculateStatistics(flowline_output)
