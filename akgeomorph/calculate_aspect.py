# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Calculate aspect
# Author: Timm Nawrocki
# Last Updated: 2024-05-04
# Usage: Execute in ArcGIS Pro Python 3.9+.
# Description: "Calculate aspect" is a function that calculates float and integer aspect.
# ---------------------------------------------------------------------------

# Define function to calculate aspect
def calculate_aspect(area_input, elevation_input, z_unit, aspect_float, aspect_output):
    """
    Description: calculates 32-bit float raw aspect and 16-bit signed aspect
    Inputs: 'area_input' -- a raster of the study area to set snap raster and extract area
            'elevation_input' -- an input 32-bit float elevation raster
            'aspect_float' -- a file path for an output 32-bit float aspect raster in degrees
            'aspect_output' -- [optional] a file path for an output 16-bit integer aspect raster in degrees
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

    # Calculate raw aspect in degrees
    print('\tCalculating raw aspect...')
    aspect_raster = SurfaceParameters(elevation_input,
                                      'ASPECT',
                                      'QUADRATIC',
                                      cell_size,
                                      'FIXED_NEIGHBORHOOD',
                                      z_unit,
                                      '',
                                      'GEODESIC_AZIMUTHS',
                                      'NORTH_POLE_ASPECT')

    # Export rasters
    print('\tExporting aspect as 32-bit float raster...')
    arcpy.management.CopyRaster(aspect_raster,
                                aspect_float,
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
    arcpy.management.BuildPyramids(aspect_float,
                                   '-1',
                                   'NONE',
                                   'BILINEAR',
                                   'L77',
                                   '',
                                   'OVERWRITE')
    arcpy.management.CalculateStatistics(aspect_float)

    # Create integer aspect if file is specified
    if aspect_output != None:
        # Convert to integer
        print('\tConverting to integer...')
        integer_raster = Int(aspect_raster + 0.5)

        # Extract to area raster
        print('\tExtracting raster to area...')
        extract_integer = ExtractByMask(integer_raster, area_raster)

        print('\tExporting aspect as 16-bit integer raster...')
        arcpy.management.CopyRaster(extract_integer,
                                    aspect_output,
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
        arcpy.management.BuildPyramids(aspect_output,
                                       '-1',
                                       'NONE',
                                       'BILINEAR',
                                       'L77',
                                       '',
                                       'OVERWRITE')
        arcpy.management.CalculateStatistics(aspect_output)
