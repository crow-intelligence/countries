import os

import folium

m = folium.Map(world_copy_jump=False, no_wrap=False)

folium.Marker(
    location=[0, 0], popup="I will disapear when moved outside the wrapped map domain."
).add_to(m)

m.save(os.path.join("maps", "ContinuousWorld_0.html"))

m
