core/

├── io/
│
│   ├── transport/
│   │
│   │   ├── envelope.py
│   │   ├── packet.py
│   │   ├── router.py
│   │   └── view.py
│   │
│   └── display_io.py


├── compute_system/compute_system.py
│
│   └── sampling/
│       │
│       └── sampler.py


└── terminal/
    │
    └── camera/
        │
        ├── camera_compute.py
        ├── camera_io.py
        ├── camera_observer.py
        └── camera_planet.py
core/internal_dynamics/

    internal_dynamics.py
	
	cloud_collision.py

    attention/attention_field.py

    cache/observation_cache.py

    cloud/Planetfield.py
	     cell.py                
         cloud_field.py 
         cloud_state.py
    organs/clip_field.py		
		
core/observer/internal_dynamics_observer.py  



******************************************
                 +-------------+
                 | PlanetField |
                 +-------------+
                       |
                       |
                 CloudState
                       |
                       |
+-------------+        |
| CLIPField   |------+
+-------------+
                       |
                       v

                CloudCollision

                       |
                       v

              collision event
			  
			  