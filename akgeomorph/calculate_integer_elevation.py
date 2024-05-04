# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Calculate integer elevation
# Author: Timm Nawrocki
# Last Updated: 2024-05-04
# Usage: Execute in ArcGIS Pro Python 3.9+.
# Description: "Calculate integer elevation" is a function that calculates integer elevation from float elevation.
# ---------------------------------------------------------------------------

# Define function to calculate integer elevation
def calculate_integer_elevation(area_input, elevation_input, elevation_output):
    """
    Description: calculates 16-bit signed elevation
    Inputs: 'area_input' -- a raster of the study area to set snap raster and extract area
            'elevation_input' -- an input 32-bit float elevation raster
            'elevation_output' -- a file path for an output 16-bit integer elevation raster
    Returned Value: Returns a raster dataset on disk
    Preconditions: requires float input elevation raster
    """

    # Import packages
    import arcpy
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

    # Round to integer
    print(f'\t\tConverting values to integers...')
    integer_raster = Int(Raster(elevation_input) + 0.5)

    # Extract to area raster
    print('\t\tExtracting raster to area...')
    extract_integer = ExtractByMask(integer_raster, area_raster)

    # Copy extracted raster to output
    print(f'\t\tExporting integer elevation as 16-bit signed raster...')
    arcpy.management.CopyRaster(extract_integer,
                                elevation_output,
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
