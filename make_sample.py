import ezdxf

# Create a new DXF document and get its modelspace
doc = ezdxf.new()
msp = doc.modelspace()

# Define the layers: walls (DUVAR) and doors (KAPI)
doc.layers.add("DUVAR")
doc.layers.add("KAPI")

# Outer walls as a closed rectangle (10 x 8)
msp.add_lwpolyline(
    [(0, 0), (10, 0), (10, 8), (0, 8)],
    close=True,
    dxfattribs={"layer": "DUVAR"},
)

# Interior wall splitting the plan
msp.add_line((6, 0), (6, 8), dxfattribs={"layer": "DUVAR"})

# Door opening on the bottom wall
msp.add_line((2, 0), (3, 0), dxfattribs={"layer": "KAPI"})

doc.saveas("sample_plan.dxf")
print("Saved sample_plan.dxf")
