import ezdxf
import math


def measure_layer(path, layer):
    """Return the total length of all LINE and LWPOLYLINE entities on a layer."""
    # Open the DXF file and get the modelspace (where the actual drawing lives)
    doc = ezdxf.readfile(path)
    msp = doc.modelspace()

    total = 0
    for entity in msp:
        # A LINE has two points: its length is the distance between them
        if entity.dxf.layer == layer and entity.dxftype() == "LINE":
            total += (entity.dxf.end - entity.dxf.start).magnitude
        # A LWPOLYLINE is a chain of points: add up each segment
        elif entity.dxf.layer == layer and entity.dxftype() == "LWPOLYLINE":
            points = list(entity.vertices())
            for i in range(len(points) - 1):
                total += math.dist(points[i], points[i + 1])
            # A closed polyline also has a segment from the last point back to the first
            if entity.closed:
                total += math.dist(points[-1], points[0])

    return total


# Quick manual tests: expected 44.0 and 1.0
print(measure_layer("sample_plan.dxf", "DUVAR"))
print(measure_layer("sample_plan.dxf", "KAPI"))
