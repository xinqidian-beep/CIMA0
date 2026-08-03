# 假设已有 planet, clip, display_io
compute = ComputeSystem(capacity=4.0, decay=0.08)
dynamics = InternalDynamics(planet, clip)
observer = InternalDynamicsObserver()
display = DisplayIO()

last_diff_sum = 0.5          # 初始信号

for t in range(300):
    # 1. 资源恢复 + 分配
    compute.step()
    signal = min(1.0, last_diff_sum * 1.5)
    budget = compute.allocate(signal)["compute_budget"]
    observer.update_resource(int(budget) + 1)   # 至少给 1，避免长期黑

    # 2. 动力学前进
    dynamics.step()

    # 3. 自己举手采样
    snap = observer.observe(dynamics)

    # 4. 渲染
    frame = display.encode(snap)

    # 5. 记录本拍差别，供下一拍信号使用
    if hasattr(dynamics, "_last_diff"):
        last_diff_sum = sum(dynamics._last_diff.values()) or 0.1

    # 6. 显示（用你现有的窗口代码）
    # cv2.imshow("internal", frame)
    # 或 pygame / 其他