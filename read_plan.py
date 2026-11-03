import ezdxf

# Open the DXF file and get the modelspace (where the actual drawing lives)
doc = ezdxf.readfile("sample_plan.dxf")
msp = doc.modelspace()

# Print the type and layer of every entity on the DUVAR layer
for entity in msp:
    if entity.dxf.layer == "DUVAR":
        print(entity.dxftype(), entity.dxf.layer)
