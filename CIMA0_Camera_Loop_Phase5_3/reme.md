目前架构变化后的职责应该是：

core/

terminal/
    camera/
        camera_io.py
        camera_planet.py
        camera_observer.py


compute_system/
        compute_system.py
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
****************************

三者关系：

main.py
    |
    | 调度
    |
    v

InternalDynamics
    |
    | 转发
    |
    v

Planet
    |
    | 演化
    |
    v

State
***************************
最终闭环应该是：
Planet
  |
  | state
  v

snapshot


  |
  v

ComputeSystem

  |
  | activity
  | sampling
  | 
  v


Observer

  |
  | read selected state
  v


IO