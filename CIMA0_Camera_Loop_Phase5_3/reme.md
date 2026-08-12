目前架构变化后的职责应该是：

core/

terminal/
    camera/
        camera_io.py
        camera_planet.py
        camera_observer.py


compute_system/
        compute_system.py
        allocation.py
        sampling/
            sampler.py


internal_dynamics/
        internal_dynamics.py
        cloud/


display_io.py
其中：

CameraObserver：决定哪些位置更新

Sampler：决定选择规则

ComputeSystem：提供预算

DisplayIO：只显示