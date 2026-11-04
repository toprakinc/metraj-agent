import ezdxf
import math

# Open the DXF file and get the modelspace (where the actual drawing lives)
doc = ezdxf.readfile("sample_plan.dxf")
msp = doc.modelspace()

total = 0
for entity in msp:
    # A LINE has two points: its length is the distance between them
    if entity.dxf.layer == "DUVAR" and entity.dxftype() == "LINE":
        total += (entity.dxf.end - entity.dxf.start).magnitude
    # A LWPOLYLINE is a chain of points: add up each segment
    elif entity.dxf.layer == "DUVAR" and entity.dxftype() == "LWPOLYLINE":
        points = list(entity.vertices())
        for i in range(len(points) - 1):
            total += math.dist(points[i], points[i + 1])
        # A closed polyline also has a segment from the last point back to the first
        if entity.closed:
            total += math.dist(points[-1], points[0])

print(total)
